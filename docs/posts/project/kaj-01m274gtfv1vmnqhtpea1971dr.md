---
title: "低代码中JSON Schema 与 TypeScript作用"
description: "该项目中 JSON Schema 与 TypeScript 的核心知识点可以总结为以下几条。"
date: "2026-09-11"
publishedAt: "2026-09-11T10:25:09.816223+08:00"
source: "https://kajspace.cn/articles/01M274GTFV1VMNQHTPEA1971DR/"
tags: ["前端"]
---

# 低代码中JSON Schema 与 TypeScript作用

该项目中 JSON Schema 与 TypeScript 的核心知识点可以总结为以下几条。

1. 两者描述的是同一个业务对象

`ComponentData` 和 JSON Schema 中的 `$defs.component`，都描述单个组件：

```text
组件 = id + type + name + style + props + events + children
```

区别不在于描述对象不同，而在于使用阶段不同。

2. TypeScript 负责编译期类型约束

代码中的：

```ts
interface ComponentData {
  id: string
  type: ComponentType
  style: ComponentStyle
  props: ComponentProps
  children?: ComponentData[]
}
```

主要用于：

- 开发阶段类型检查
- 编辑器自动补全
- 函数参数约束
- 防止代码中访问不存在的字段
- 区分 TextProps、ImageProps、FormProps 等不同属性类型

它主要约束源码中的变量和函数，编译后通常不会保留。

3. JSON Schema 负责运行时数据校验

`src/schema/page.schema.ts` 描述页面 JSON 的合法结构：

```text
PageData
├── id
├── meta
├── components
└── style
```

组件结构由：

```text
$defs.component
```

描述，并通过：

```text
children.items.$ref = '#/$defs/component'
```

实现递归组件树。

JSON Schema 主要用于校验：

- 导入的 JSON 文件
- localStorage 恢复的数据
- 外部接口返回的数据
- 发布或运行时加载的数据

4. 当前项目的数据不是 JSON Schema，而是 JSON Schema 的实例

要区分：

```text
pageSchema = 规则、说明书
currentPage = 当前实际页面数据
```

例如：

```text
currentPage.value.components
```

是实际业务数据；它应该符合 `pageSchema` 的约束。

拖拽、移动、缩放、修改属性时，修改的是：

```text
Pinia 中的 currentPage 数据
```

不是：

```text
pageSchema
```

5. 页面数据处理流程

导入或恢复页面时：

```text
JSON.parse
    ↓
AJV 校验 JSON Schema
    ↓
递归检查 children
    ↓
normalizePageData
    ↓
写入 Pinia currentPage
    ↓
Vue 响应式更新 DOM
```

导出时则相反：

```text
Pinia currentPage
    ↓
JSON.stringify
    ↓
导出页面 JSON
```

6. 递归 children 是 JSON Schema 的重要特征

当前结构是：

```text
Page
└── components[]
    └── ComponentData
        └── children[]
            └── ComponentData
                └── children[]
```

因此可以表达：

```text
Page
└── Container
    ├── Text
    └── Button
```

TypeScript 通过：

```text
children?: ComponentData[]
```

表达递归类型。

JSON Schema 通过：

```text
children: {
  type: 'array',
  items: {
    $ref: '#/$defs/component'
  }
}
```

表达递归数据结构。

7. 两者目前并不是完全等价

当前 TypeScript 对字段描述更详细，例如：

```ts
interface ComponentStyle {
  top: number
  left: number
  width: number
  height: number
  opacity: number
}
```

但当前 JSON Schema 里的 `style` 主要只校验：

```text
style: {
  type: 'object'
}
```

同样，TypeScript 能区分不同组件的 props 类型，但当前 JSON Schema 对 `props` 的校验还比较宽松。

因此目前关系是：

```text
TypeScript：较详细、偏开发期
JSON Schema：较通用、偏运行期
```

8. 项目中还有一种“组件属性 schema”

`registry.ts` 中的：

```text
ComponentProtocol.schema
```

不是标准 JSON Schema，而是属性面板配置，例如：

```text
{
  key: 'content',
  label: '文本内容',
  type: 'string'
}
```

它用于告诉 `PropertyPanel.vue`：

```text
content 显示文本输入框
chartType 显示下拉框
color 显示颜色选择器
```

所以项目里有两种 schema：

| 类型 | 作用 |
| --- | --- |
| `page.schema.ts` 中的 JSON Schema | 校验页面 JSON 数据 |
| `ComponentProtocol.schema` | 生成属性编辑面板 |

9. 最核心的分工

```text
TypeScript
负责“代码如何正确使用组件数据”

JSON Schema
负责“外部传入的组件数据是否合法”

Pinia
保存当前页面 JSON 数据

Vue
把页面 JSON 数据渲染成虚拟 DOM 和真实 DOM

AJV
执行 JSON Schema 运行时校验
```

一句话总结：

```text
TypeScript 是开发阶段的类型契约，
JSON Schema 是运行阶段的数据契约，
二者共同保证低代码页面数据结构稳定、可校验、可导入、可保存和可运行。
```
