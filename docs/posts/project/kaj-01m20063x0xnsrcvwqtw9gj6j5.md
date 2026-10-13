---
title: "低代码核心知识点"
description: "本文档对应当前仓库 vue-lowcode-builder 的实际实现，说明页面数据如何描述、用户操作如何改变数据，以及 Vue 如何把数据渲染成 DOM。关键源码入口：src/types/index.ts、src/stores/edito"
date: "2026-09-08"
publishedAt: "2026-09-08T15:54:45.121146+08:00"
source: "https://kajspace.cn/articles/01M20063X0XNSRCVWQTW9GJ6J5/"
tags: ["前端"]
---

# 低代码核心知识点

## Vue 低代码编辑器核心知识点

本文档对应当前仓库 `vue-lowcode-builder` 的实际实现，说明页面数据如何描述、用户操作如何改变数据，以及 Vue 如何把数据渲染成 DOM。关键源码入口：`src/types/index.ts`、`src/stores/editor.ts`、`src/stores/history.ts`、`src/components/EditorCanvas.vue`。

## 1. 总体心智模型 {#article-section-1}

```text
用户事件
  → ComponentPanel / EditorCanvas / PropertyPanel
  → Pinia editorStore 修改 PageData
  → Vue 响应式系统发现变化
  → 生成新 Virtual DOM
  → 新旧 Virtual DOM diff
  → patch 真实 DOM
  → 用户看到新页面并继续操作
```

核心原则：**PageData 是页面事实来源；DOM 是渲染结果和事件入口，不是页面数据源。**

## 2. 模块职责 {#article-section-2}

| 模块 | 文件 | 职责 |
| --- | --- | --- |
| 应用入口 | `src/main.ts` | 创建 Vue App，注册 Pinia、Router、Element Plus |
| 路由壳 | `src/App.vue`、`src/router/index.ts` | 通过 RouterView 加载编辑器 |
| 编辑器外壳 | `src/components/Editor.vue` | 顶部工具栏、三栏布局、预览、导入导出 |
| 组件资产库 | `ComponentPanel.vue` | 展示资产，发起 dragstart，展示图层列表 |
| 画布 | `EditorCanvas.vue` | drop、选中、移动、缩放、坐标换算、网格、辅助线 |
| 属性面板 | `PropertyPanel.vue` | 页面信息、组件样式、props、events、图层、删除 |
| 组件协议 | `components/registry.ts` | 默认值、元数据、属性字段、渲染器映射 |
| 组件渲染器 | `components/*.vue` | 根据 ComponentData 渲染 Text/Image/Button/Input/Form |
| 页面状态 | `stores/editor.ts` | currentPage、currentComponent、创建/修改/删除/持久化 |
| 历史状态 | `stores/history.ts` | Command、undoStack、redoStack |
| 类型契约 | `types/index.ts` | PageData、ComponentData、ComponentProtocol、Command |

## 3. Schema 与数据模型 {#article-section-3}

### 3.1 页面 Schema（页面 DSL）

```ts
interface PageData {
  id: string
  meta: PageMeta
  components: ComponentData[]
  style: PageStyle
}

interface ComponentData {
  id: string
  type: ComponentType
  name: string
  style: ComponentStyle
  props: ComponentProps
  events: ComponentEvent[]
  schemaVersion: string
}
```

字段含义：

- `id`：实例身份，用于选中、修改、删除、历史和 Vue `:key`。
- `type`：`Text`、`Image`、`Button`、`Input`、`Form`。
- `style`：位置、尺寸、层级、旋转、透明度以及视觉样式。
- `props`：组件内容和业务属性。
- `events`：点击动作等交互配置。
- `schemaVersion`：当前数据版本为 `2026.03`。

### 3.2 当前不是递归组件树

`PageData.components` 是扁平数组：

```text
Page
└── components[]
    ├── Text
    ├── Image
    ├── Button
    ├── Input
    └── Form
```

当前没有通用 `children`，所以不支持容器内嵌套组件、树路径插入或跨容器移动。所有页面级组件都是画布根节点的直接子项，使用绝对定位。 `Form.props.fields` 是表单自己的业务数组，不是通用组件子树。

### 3.3 组件协议不是标准 JSON Schema

`componentProtocols` 描述“如何创建一个组件”：

```ts
interface ComponentProtocol {
  type: ComponentType
  label: string
  category: '基础' | '营销'
  description: string
  defaultStyle: ComponentStyle
  defaultProps: ComponentProps
  schema: ComponentSchemaField[]
}
```

当前 `schema` 只有 `{ key, label, type, options? }`，不是含 `$schema`、`properties`、`required` 的标准 JSON Schema；属性面板也仍然按组件类型写死，没有根据 `protocol.schema` 动态生成。

## 4. 页面组件为什么是绝对定位 {#article-section-4}

画布是定位参照物：

```text
.canvas-background { position: relative; }
.component-wrapper { position: absolute; }
```

wrapper 的位置来自 `ComponentData.style`：

```text
{
  top: `${component.style.top}px`,
  left: `${component.style.left}px`,
  width: `${component.style.width}px`,
  height: `${component.style.height}px`,
  zIndex: component.style.zIndex,
  transform: `rotate(${component.style.rotate}deg)`
}
```

页面层是 `absolute + left/top/width/height` 的自由画布；组件内部仍可使用 flex 或普通流。编辑器三栏外壳的布局与页面组件布局是两回事。预览也使用相同绝对坐标。

## 5. 两种拖拽机制 {#article-section-5}

### 5.1 从组件库拖入：HTML5 Drag and Drop

```text
dragstart → DataTransfer → dragover → drop
```

作用是创建新组件。

### 5.2 画布内移动：Mouse Events

```text
mousedown → document mousemove → document mouseup
```

作用是修改已有组件的 `left/top`，不使用 `DataTransfer`，也不创建新实例。

## 6. DataTransfer {#article-section-6}

`DataTransfer` 是浏览器原生拖放 API 的临时数据容器。组件面板在 `dragstart` 时只写入类型：

```text
event.dataTransfer.setData('componentType', componentType)
event.dataTransfer.effectAllowed = 'copy'
```

例如拖动按钮时载荷是 `{ componentType: 'Button' }`。此时还没有 `ComponentData`、实例 ID 或 Pinia 数据变更。drop 后用 `getData('componentType')` 读取。它不属于 Pinia，也不会进入页面 JSON。

## 7. getBoundingClientRect 与坐标转换 {#article-section-7}

```js
const rect = backgroundRef.value.getBoundingClientRect()
```

该 API 返回 DOM 元素相对于浏览器视口的位置和视觉尺寸，例如 `left/top/width/height`。

鼠标事件的 `clientX/clientY` 是视口坐标，而 Schema 的 `style.left/style.top` 是画布内部逻辑坐标。drop 时需要：

```text
left = (event.clientX - rect.left) / canvasScale
top = (event.clientY - rect.top) / canvasScale
```

含义：

1. 减去 `rect.left/top`，去掉画布在浏览器中的外部偏移。
2. 除以 `canvasScale`，把缩放后的视觉距离还原为未缩放的逻辑距离。
3. `align()` 在开启时按 `GRID_SIZE = 10` 吸附。
4. `normalizeComponentLayout()` 限制组件不能越过画布边界。

示例：画布左边缘为 300，鼠标 `clientX=700`，缩放为 0.5，则逻辑 `left=(700-300)/0.5=800`。Schema 保存 800，而不是视觉距离 400。

## 8. 从资产拖入画布的完整链路 {#article-section-8}

```text
ComponentPanel 生成资产列表
  → dragstart 写入 componentType
  → EditorCanvas dragover.prevent 允许 drop
  → drop 读取 type、clientX/Y、rect、canvasScale、snapToGrid、currentPage
  → 坐标转换并网格吸附
  → editorStore.addComponent(type, { style: { left, top } })
  → getComponentProtocol(type)
  → createProtocolComponent 创建实例
  → normalizeComponentLayout 修正边界
  → 新增 Command.execute
  → push 到 currentPage.components
  → 设置 currentComponent
  → Vue 更新画布、图层列表、属性面板、预览
```

`createProtocolComponent()` 会：生成唯一 `id`；深拷贝 `defaultStyle/defaultProps`；用 drop 坐标和新 `zIndex` 覆盖默认位置；创建默认 click 事件；写入 `name/schemaVersion`。

新增命令的正向操作是：

```text
currentPage.components.push(normalized)
currentComponent = normalized
touchPageMeta()
```

撤销按 ID 找到实例并 `splice` 删除。

## 9. 画布内选择、移动和缩放 {#article-section-9}

### mousedown：按下鼠标

`startDrag()` 只接受左键，阻止默认行为，选中组件，保存 `dragId`、`dragInitial` 和鼠标起点，然后在 `document` 注册 `mousemove/mouseup`。监听放在 document 上，保证鼠标离开组件后仍能拖动。

### mousemove：按住鼠标移动

```text
dx = (event.clientX - dragStartX) / canvasScale
dy = (event.clientY - dragStartY) / canvasScale
left = dragInitial.left + dx
top = dragInitial.top + dy
```

之后网格吸附、边界限制，并调用 `applyComponentStyle(dragId, { left, top })`。它实时修改 Pinia 中的 `ComponentData.style`，再由 Vue 更新 DOM。辅助线属于编辑器运行时状态，不会写入页面 JSON。

### mouseup：松开鼠标

`stopDrag()` 取得操作开始时的 before 快照和结束时的 after 样式，提交历史命令，然后清理拖动变量、辅助线、cursor 和 document 监听器。

缩放手柄走 `beginResize → onResize → stopResize`，根据方向同时计算 `left/top/width/height`。

### 已修复的撤销问题

旧实现中 mousemove 已覆盖组件样式，mouseup 才读取 `prevStyle`，导致 before 和 after 相同。现在 `dragInitial/resizeInitial` 显式作为 before 传入：

```text
before = mousedown 时的 style
after  = mouseup 时的 style
undo   = 恢复 before
redo   = 再次 execute，应用 after
```

## 10. 属性面板数据流 {#article-section-10}

属性面板通过 `watch(currentComponent)` 深拷贝三份本地状态：

```text
currentComponent.style             → localStyle
currentComponent.props             → localProps
currentComponent.events[0].config  → localEventConfig
```

用户修改 Element Plus 控件并触发 `change`：

```text
input/select/slider DOM 事件
  → v-model 修改本地 ref
  → commitStyle / commitProps / commitEvents
  → editorStore 创建 Command
  → 修改 currentPage 中的 ComponentData
  → Vue 更新画布、图层和面板
```

`localStyle/localProps` 是 JavaScript 响应式数据，不是 DOM；输入框、textarea、select 才是真实 DOM。

## 11. Vue 响应式渲染 {#article-section-11}

`currentPage` 由 Vue `ref()` 管理，对象和数组通过响应式 Proxy 追踪。 `components.push()`、`splice()` 或替换 `style/props/events` 后，依赖它的 computed 和模板进入更新队列。

画布关键计算：

```text
sortedComponents：按 style.zIndex 排序
wrapperStyle：style → CSS top/left/width/height/zIndex/transform
getRenderer：type → componentRendererMap 中的 Vue 组件
```

模板使用 `v-for :key="component.id"`。真实流程是：

```text
PageData 变化
  → 重新 render
  → 新 Virtual DOM
  → 新旧 Virtual DOM diff
  → patch 真实 DOM
```

不是把 Virtual DOM 与真实 DOM 做完整直接比较。 `:key` 让 Vue 复用已有节点，新增时只创建新增节点，移动时通常只更新 style。

## 12. History Command、撤销和重做 {#article-section-12}

```ts
interface Command {
  label?: string
  execute(): void
  undo(): void
}
```

新操作：

```text
command.execute()
undoStack.push(command)
redoStack = []
```

撤销：

```js
const command = undoStack.pop()
command.undo()
redoStack.push(command)
```

`pop()` 会返回并删除栈顶命令，所以撤销不是清空整个 undoStack，而是移动一条命令到 redoStack。

重做：

```js
const command = redoStack.pop()
command.execute()
undoStack.push(command)
```

没有单独的 `redo()`，因为重做就是撤销后再次执行同一个 `execute()`。

### 为什么新操作要清空 redoStack

假设历史为 `A → B → C`，撤销 B/C 后状态回到 A：

```text
undoStack = [A]
redoStack = [C, B]
```

如果此时执行新操作 D，历史已经分叉：

```text
      → B → C   旧分支
A
      → D       当前分支
```

因此 D 执行后必须是：

```text
undoStack = [A, D]
redoStack = []
```

否则重做 B 会产生 `A → D → B`，旧命令携带的过期组件索引、组件集合、zIndex 或样式快照可能覆盖新操作。新建页面和导入页面整体替换 `currentPage`，所以要清空两个栈。

## 13. 持久化、导入、导出、预览 {#article-section-13}

### 启动加载

`EditorCanvas` 挂载时调用 `loadPersistedPage()`：

```text
localStorage.marketing-editor-page
  → JSON.parse
  → normalizePageData
  → currentPage
```

没有数据或解析失败则 `createNewPage()`。

### 保存和导出

点击保存时对 `currentPage` 执行 `JSON.stringify` 写入 localStorage。导出按钮也序列化 `currentPage`，生成 JSON 文件。普通拖动和属性修改只改变内存中的 Pinia 状态，不会自动保存。

### 导入和预览

导入流程为 `JSON.parse → normalizePageData → 替换 currentPage → 清空历史 → persistPage`。预览直接读取同一份 `currentPage`，没有第二份页面数据。

## 14. 数据、运行时状态和 DOM 的边界 {#article-section-14}

| 对象 | 位置 | 是否导出 JSON | 是否 DOM |
| --- | --- | --- | --- |
| `currentPage` | Pinia/Vue 内存 | 是 | 否 |
| `ComponentData` | `currentPage.components` | 是 | 否 |
| `currentComponent` | Pinia 编辑状态 | 否 | 否 |
| `localStyle/localProps` | PropertyPanel 的 ref | 否 | 否 |
| `guides`、拖动起点、cursor | 编辑器运行时 | 否 | 部分显示结果是 |
| input/textarea/select | 浏览器 DOM | 否 | 是 |
| 画布组件 wrapper | 浏览器 DOM | 否 | 是 |

DOM 负责提供事件和几何信息（例如 `clientX`、`getBoundingClientRect()`），以及呈现 Vue 根据数据生成的结果。

## 15. 常见误区 {#article-section-15}

1. **拖动时直接移动 DOM。** 实际是先修改 `ComponentData.style`，再由 Vue 更新 DOM。
2. **DataTransfer 携带完整协议。** 当前只携带 `componentType`，完整协议在 drop 后查询。
3. **属性面板数据就是 DOM。** `localStyle/localProps` 是响应式 JavaScript 数据，控件才是 DOM。
4. **redo 需要独立函数。** 当前模型用再次 `execute()` 完成 redo。
5. **撤销清空整个 undoStack。** `pop()` 只移动一条栈顶命令。
6. **两种拖拽相同。** 资产库拖入是 HTML5 DnD；画布移动是鼠标事件。
7. **修改后立即写 localStorage。** 当前需要点击保存，或走导入/新建中的持久化逻辑。

## 16. 当前实现边界与演进方向 {#article-section-16}

已经具备：组件协议注册、扁平绝对定位画布、新增/删除/样式/属性编辑、图层调整、网格吸附、辅助线、命令式撤销重做、localStorage 与 JSON 导入导出、画布与预览共用 PageData。

当前边界：

- 没有递归 `children`，不是通用容器组件树。
- `registry.schema` 不是标准 JSON Schema。
- 属性面板不是由 schema 动态生成。
- `events` 目前主要用于保存配置，渲染器没有完整执行点击动作的运行时逻辑。
- 编辑操作不会自动持久化。
- 历史命令主要基于组件 ID、数组和快照，不是树路径模型。

如果演进为真正的组件树，可引入：

```ts
interface ComponentNode {
  id: string
  type: string
  props: Record<string, unknown>
  style: ComponentStyle
  children?: ComponentNode[]
}
```

再用标准 JSON Schema 或更完整的字段协议驱动属性面板，并将历史目标从数组索引提升为节点 ID/树路径。

## 17. 最终总结 {#article-section-17}

```text
组件协议：定义“可以创建什么”
ComponentData：记录“某个组件实例是什么”
PageData：记录“整个页面是什么”
Pinia：保存当前编辑中的页面状态
Command：记录一次可撤销的数据变更
Vue Renderer：把 ComponentData 翻译成 DOM
DOM：接收用户输入并显示结果
localStorage / JSON：保存和交换 PageData
```

最重要的一句话：

> 用户操作最终要落到 PageData，PageData 的变化再通过 Vue 响应式系统反映到 DOM；DOM 不负责反向定义页面，只负责提供事件和呈现页面。
