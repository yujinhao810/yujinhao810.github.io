---
title: "低代码平台--从组件资产拖入画布：新增组件完整链路"
description: "用户从组件资产库按下并开始拖动"
date: "2026-09-08"
publishedAt: "2026-09-08T10:18:45.630446+08:00"
source: "https://kajspace.cn/articles/01M1ZCYVJT21F3H4TD9GMHV6Q0/"
tags: ["前端"]
---

# 低代码平台--从组件资产拖入画布：新增组件完整链路

### **完整链路** {#kaj-h-8c567ef3-4acd-4416-8119-2cc874944baa}

用户从组件资产库按下并开始拖动

→ dragstart

→ DataTransfer 临时保存 componentType

→ 鼠标移动到画布

→ dragover.prevent 允许画布接收 drop

→ 用户松开鼠标

→ drop

→ 读取组件类型、鼠标位置、画布 DOM 边界和画布缩放比例

→ 将浏览器视口坐标转换成画布逻辑坐标

→ 根据 componentType 查询组件默认协议

→ 创建 ComponentData 实例

→ 创建并执行“新增组件”Command

→ 把实例加入 Pinia 的 currentPage.components

→ 设置为 currentComponent

→ Vue 响应式系统发现依赖数据变化

→ 重新执行相关组件的渲染逻辑

→ 比较新旧 Virtual DOM

→ 将差异更新到真实 DOM

→ 画布、图层列表和属性面板同步更新

### 1. 左侧拖动的不是已经创建好的组件 {#kaj-h-7712754f-ed61-478c-aaeb-c6b657775f4d}

更准确的说法不是“选中组件拖到画布”，而是：

> 从组件资产库选择一种组件类型，拖到画布以创建一个新组件。

`dragstart` 时只传递：

```text
componentType = 'Button'
```

此时还没有：

- 组件实例
- 组件 ID
- 实例样式
- 实例属性
- 页面 Schema 节点

完整组件实例是在 `drop` 后，根据组件协议创建的。

### 2. DataTransfer 只负责一次拖放过程 {#kaj-h-0804e5ea-23d4-4ddc-90d4-7c9bf83681b0}

它是浏览器提供的临时数据载体：

```text
event.dataTransfer.setData('componentType', componentType)
```

画布释放时读取：

```text
event.dataTransfer.getData('componentType')
```

它不属于 Pinia，也不会保存进页面 JSON。拖放完成以后，这份临时数据就不再承担作用。

### 3. drop 读取的不只是组件类型 {#kaj-h-ef05d180-4e61-41ba-8c92-0556ffe579eb}

画布在 `drop` 时还会使用：

```text
event.clientX / clientY
    鼠标释放点的浏览器视口坐标

backgroundRef.getBoundingClientRect()
    画布在浏览器中的实际位置

canvasScale
    当前画布缩放比例

snapToGrid / GRID_SIZE
    是否需要网格吸附

currentPage
    页面尺寸和已有组件
```

坐标转换公式是：

```text
left = (event.clientX - rect.left) / canvasScale
top  = (event.clientY - rect.top) / canvasScale
```

例如：

```text
鼠标 clientX：700
画布 rect.left：300
画布缩放：0.5

组件逻辑 left：
(700 - 300) / 0.5 = 800
```

最终保存在 Schema 中的是未缩放的逻辑坐标 `800`。

### 4. 创建实例时才读取默认协议 {#kaj-h-9a68c47b-5d54-48bf-a9ca-c746867de1d7}

`addComponent(type)` 会调用：

```text
getComponentProtocol(type)
```

取得：

```text
label
defaultStyle
defaultProps
schema
```

随后创建：

```text
{
  id,
  type,
  name,
  schemaVersion,
  style,
  props,
  events
}
```

其中：

```text
默认协议的 style
+ drop 计算出的 left/top
+ 当前图层 zIndex
= 实例最终 style
```

这个实例才会进入页面数据。

### 5. “执行命令”本质上是在修改页面数据 {#kaj-h-588969ed-a9ce-41b6-a6d5-bc82433f9d0f}

新增命令大致包含：

```text
{
  execute() {
    currentPage.components.push(component)
    currentComponent = component
  },

  undo() {
    currentPage.components.splice(index, 1)
    currentComponent = null
  }
}
```

History Store 会：

```text
调用 command.execute()
→ 把 command 放入 undoStack
→ 清空 redoStack
```

所以 Command 是对数据修改的包装，使这次操作可以撤销和重做。

### 6. Vue 不是直接比较虚拟 DOM 和真实 DOM {#kaj-h-221738be-3662-4d3b-93a9-08eb9cd04b95}

更准确的过程是：

```text
Pinia 数据变化
→ Vue 重新执行受影响组件的渲染
→ 生成新的 Virtual DOM
→ 新 Virtual DOM 与旧 Virtual DOM 对比
→ 计算差异
→ 将差异 patch 到真实 DOM
```

因此应该说：

> Vue 比较新旧虚拟 DOM，然后更新真实 DOM。

不是：

> Vue 把虚拟 DOM 和真实 DOM进行对比。

新增组件时，Vue 根据：

```text
:key="component.id"
```

识别已有组件，只创建新增组件对应的 DOM，不会重建整个画布。

### 7. 同步更新的不只是画布 {#kaj-h-0bee795b-ca19-402b-bd57-11885ddb5206}

因为新增命令同时修改了：

```text
currentPage.components
currentComponent
```

所以会影响多个视图：

```text
currentPage.components
├─ EditorCanvas：出现新组件
├─ ComponentPanel：图层列表出现新图层
└─ Editor Preview：预览出现新组件

currentComponent
├─ EditorCanvas：出现选中框和缩放手柄
└─ PropertyPanel：显示新组件的属性
```

这几个模块没有互相直接通知，而是共同读取 Pinia 状态：

```text
组件面板 ─┐
画布     ─┼─ 读取/修改 → Pinia Store
属性面板 ─┤
预览     ─┘
```

Pinia 是它们之间的状态中心。

### 8. 画布内移动不使用 DataTransfer {#kaj-h-afc0e364-cd77-4cea-ae26-edf6b7cbb5ff}

需要把两种“拖拽”分开：

```text
从资产库拖入画布：
dragstart → DataTransfer → dragover → drop
作用：创建一个新组件
```

```text
移动画布中的已有组件：
mousedown → mousemove → mouseup
作用：修改已有组件的 left/top
```

第二种流程直接根据鼠标位移修改：

```text
component.style.left
component.style.top
```

不经过 `DataTransfer`，也不创建新实例。

### 9. 数据更新不等于立即持久化 {#kaj-h-a5df9f07-e118-4e7a-836d-82200fe23107}

新增组件以后，修改的是运行内存中的：

```text
Pinia currentPage
```

并没有自动写入 `localStorage`。

当前项目需要点击“保存”才执行：

```text
localStorage.setItem(
  STORAGE_KEY,
  JSON.stringify(currentPage)
)
```

因此状态可以分成：

```text
DataTransfer
    一次拖放过程中的临时数据

Pinia currentPage
    当前编辑会话中的页面数据

localStorage / JSON 文件
    持久化后的页面数据

真实 DOM
    页面数据当前的视觉呈现
```

最终，你的理解可以整理成这一句话：

> 用户从资产库拖出组件类型，浏览器用 DataTransfer 暂存该类型；画布在 drop 时结合鼠标位置、画布边界和缩放比例计算逻辑坐标，再从组件协议创建 ComponentData，通过 Command 写入 Pinia 的 PageData；Vue 感知状态变化，生成新的虚拟 DOM并与旧虚拟 DOM比较，最后只更新真实 DOM 中发生变化的部分，同时驱动画布、图层列表和属性面板保持一致。
