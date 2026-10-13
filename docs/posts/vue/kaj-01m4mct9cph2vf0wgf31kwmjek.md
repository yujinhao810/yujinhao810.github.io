---
title: "Vue 2 与 Vue 3 的区别详解"
description: "Vue 2 和 Vue 3 都是渐进式 JavaScript 框架，核心目标是通过响应式数据和组件化开发构建用户界面。"
date: "2026-10-11"
publishedAt: "2026-10-11T10:31:39.577139+08:00"
source: "https://kajspace.cn/articles/01M4MCT9CPH2VF0WGF31KWMJEK/"
tags: ["前端"]
---

# Vue 2 与 Vue 3 的区别详解

<span id="kaj-h-51b76382-7062-497e-9c29-f1f6142b30b1"></span>

## 一、概述 {#kaj-h-a2122615-598e-4110-80a1-a2261384d8c3}

Vue 2 和 Vue 3 都是渐进式 JavaScript 框架，核心目标是通过响应式数据和组件化开发构建用户界面。

Vue 3 在 Vue 2 的基础上，对响应式系统、组件逻辑组织、虚拟 DOM、TypeScript 支持和应用配置等方面进行了改进。

两者的主要区别可以归纳为以下几个方面：

1. 响应式原理：`Object.defineProperty` 与 `Proxy`。
2. API 设计：Options API 与 Composition API。
3. 生命周期：部分生命周期名称发生变化。
4. 虚拟 DOM：增加静态提升、Patch Flags 等优化。
5. 模板能力：Vue 3 支持多根节点。
6. 全局 API：从全局 Vue 构造器转向应用实例。
7. 状态管理：Vue 3 项目中常使用 Pinia。

## 二、响应式原理 {#kaj-h-0f006754-82c7-45a5-8d02-b3ff30180ecd}

响应式系统是 Vue 的核心功能之一。当响应式数据发生变化时，Vue 会通知依赖该数据的相关更新任务，使页面自动更新。

### 2.1 Vue 2：Object.defineProperty {#kaj-h-5d2aea8b-4459-493a-b006-9750fde4b8de}

Vue 2 主要通过 `Object.defineProperty()` 劫持对象已有属性的 getter 和 setter，实现依赖收集与更新通知。

```js
const data = {
  name: 'Tom'
}

Object.defineProperty(data, 'name', {
  get() {
    console.log('读取 name')
    return 'Tom'
  },
  set(value) {
    console.log('修改 name:', value)
  }
})

data.name
data.name = 'Jerry'
```

读取 `data.name` 时触发 `get`，修改时触发 `set`。Vue 会在这些操作中进行依赖收集和变更通知。

Vue 2 的主要限制：

- 新增对象属性不能自动通过原有的属性劫持机制被检测，需要使用 `Vue.set()` 等方式。
- 直接通过数组索引修改元素、直接修改 `length` 等操作存在检测限制。
- 初始化响应式对象时，需要遍历并处理已有属性。

### 2.2 Vue 3：Proxy {#kaj-h-fd120756-68b1-45b8-bf64-314f11069648}

Vue 3 主要通过 `Proxy` 代理对象，并结合 `Reflect` 实现属性访问和修改等操作的拦截。

```js
const data = new Proxy(
  { name: 'Tom' },
  {
    get(target, key, receiver) {
      console.log('读取属性:', key)
      return Reflect.get(target, key, receiver)
    },

    set(target, key, value, receiver) {
      console.log('修改属性:', key)
      return Reflect.set(target, key, value, receiver)
    }
  }
)

data.name
data.age = 18
```

与 `Object.defineProperty()` 不同，`Proxy` 可以代理整个对象，因此能够拦截新增属性、删除属性以及数组索引等更多类型的操作。

### 2.3 两者的区别 {#kaj-h-48854e9a-089c-4624-b02b-24ee7f381a6d}

| 对比项 | Vue 2 | Vue 3 |
| --- | --- | --- |
| 主要实现方式 | Object.defineProperty | Proxy |
| 代理对象 | 主要劫持已有属性 | 代理整个对象 |
| 新增对象属性 | 需要特殊处理 | 通常可自动检测 |
| 数组索引修改 | 存在检测限制 | 可以拦截相关操作 |
| 响应式实现 | 需要处理对象已有属性 | 可以按需代理对象操作 |

需要注意，Vue 3 的响应式系统并非所有数据都直接使用 Proxy。例如，`ref()` 的响应式行为也涉及 getter 和 setter。

## 三、Options API 与 Composition API {#kaj-h-9ef0b432-c1f1-4419-a652-2d33bc346ac3}

### 3.1 Vue 2：Options API {#kaj-h-a3bab598-0d70-439e-aecd-e672b94c1b83}

Vue 2 主要使用 Options API，将组件逻辑按照不同选项进行组织。

```js
<script>
export default {
  data() {
    return {
      count: 0
    }
  },

  methods: {
    increment() {
      this.count++
    }
  },

  computed: {
    doubleCount() {
      return this.count * 2
    }
  }
}
</script>
```

常见选项包括：

- `data`：定义组件数据。
- `methods`：定义组件方法。
- `computed`：定义计算属性。
- `watch`：监听数据变化。
- `mounted`：处理组件挂载后的逻辑。

这种组织方式简单直观，适合中小型组件。

但当组件业务复杂时，同一个业务功能的状态、方法和监听逻辑可能分散在多个选项中，不利于统一维护。

### 3.2 Vue 3：Composition API {#kaj-h-aa79e64c-0fe6-4ceb-b072-58af63905bb7}

Vue 3 在继续支持 Options API 的基础上，引入了 Composition API。

```js
<script setup>
import { ref, computed } from 'vue'

const count = ref(0)

const doubleCount = computed(() => count.value * 2)

function increment() {
  count.value++
}
</script>

<template>
  <button @click="increment">
    {{ count }} / {{ doubleCount }}
  </button>
</template>
```

Composition API 允许将同一业务功能相关的状态、计算属性和方法组织在一起。

它的主要优势包括：

1. 逻辑组织更加灵活。
2. 便于通过 Composable 函数复用业务逻辑。
3. 对 TypeScript 的支持更加自然。
4. 更适合复杂组件和大型项目。

例如，可以将计数逻辑抽取为独立函数：

```js
// useCounter.js
import { ref, computed } from 'vue'

export function useCounter() {
  const count = ref(0)

  const doubleCount = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  return {
    count,
    doubleCount,
    increment
  }
}
```

组件调用 `useCounter()` 即可复用这套逻辑。

需要注意：Vue 3 并没有废弃 Options API，开发者可以根据项目和团队情况选择合适的写法。

## 四、生命周期的区别 {#kaj-h-11f112cb-d732-4e3a-bed9-20390bc5e6db}

Vue 3 对部分生命周期钩子进行了重命名，特别是组件销毁相关的钩子。

| Vue 2 | Vue 3 组合式 API | 说明 |
| --- | --- | --- |
| beforeCreate | setup 执行前期对应的初始化阶段 | 初始化早期 |
| created | setup 执行期间完成相关初始化 | 初始化相关逻辑 |
| beforeMount | onBeforeMount | 挂载前 |
| mounted | onMounted | 挂载后 |
| beforeUpdate | onBeforeUpdate | 更新前 |
| updated | onUpdated | 更新后 |
| beforeDestroy | onBeforeUnmount | 卸载前 |
| destroyed | onUnmounted | 卸载后 |
| errorCaptured | onErrorCaptured | 捕获后代组件错误 |

在 Vue 3 中，可以通过组合式生命周期 API 注册回调：

```js
import { onMounted, onUnmounted } from 'vue'

onMounted(() => {
  console.log('组件挂载完成')
})

onUnmounted(() => {
  console.log('组件卸载完成')
})
```

需要注意，`setup()` 执行时组件尚未完成挂载，因此如果需要访问已经挂载的 DOM，通常应在 `onMounted()` 中进行。

此外，Vue 3 仍然支持 `beforeCreate` 和 `created` 这类 Options API 钩子，但使用 Composition API 时，通常直接在 `setup()` 中完成相应初始化工作。

## 五、虚拟 DOM 与 Diff 算法优化 {#kaj-h-52287059-b505-4584-86c2-f00eb6fb0726}

Vue 2 和 Vue 3 都使用虚拟 DOM。虚拟 DOM 是使用 JavaScript 对象描述 UI 结构的一种方式。

当响应式数据发生变化时，Vue 会重新执行相关渲染逻辑，生成新的虚拟 DOM，并通过比较和更新过程修改必要的真实 DOM。

Vue 3 在编译器和运行时之间增加了更多优化机制。

### 5.1 静态提升 {#kaj-h-fe76f30b-7143-4b26-9254-04ad58d32f07}

对于可以复用的静态节点，Vue 3 编译器可以将其提升到渲染函数外部，避免每次渲染时重复创建相同的节点描述。

### 5.2 Patch Flags {#kaj-h-f2819144-fea5-4a6f-a583-8db1d1b5206d}

编译器可以为动态节点添加标记，说明哪些属性或内容可能发生变化。

更新时，Vue 可以利用这些信息减少不必要的比较工作。

### 5.3 Block Tree {#kaj-h-dc13b87e-bfe3-47c0-9571-ce1194bff5bd}

Vue 3 可以追踪动态节点，减少更新过程中对大量静态节点的遍历。

这些优化共同提高了模板渲染与更新的效率，但实际收益仍取决于组件结构和具体业务场景。

## 六、Vue 3 支持多根节点 {#kaj-h-6e10bde8-313c-46da-b4d8-487602b275d2}

Vue 2 的普通组件模板通常要求具有一个根节点。

```html
<template>
  <div>
    <h1>标题</h1>
    <p>内容</p>
  </div>
</template>
```

Vue 3 支持多根节点：

```html
<template>
  <h1>标题</h1>
  <p>内容</p>
</template>
```

Vue 3 可以通过 Fragment 等机制管理多个根节点，不需要为了满足单根节点要求额外添加容器。

不过，如果组件存在多个根节点，Vue 通常无法自动判断未声明的 `class`、`id` 等属性应该传递到哪个节点，因此可能需要显式绑定 `$attrs`。

## 七、全局 API 与应用实例 {#kaj-h-d3d1a679-c7ee-430f-a3f7-3b79eadcbff2}

### 7.1 Vue 2 的写法 {#kaj-h-87fb9901-023f-4dfb-b91b-7c4d930048c1}

```js
import Vue from 'vue'
import App from './App.vue'

new Vue({
  render: h => h(App)
}).$mount('#app')
```

Vue 2 的部分配置和插件能力依赖全局 Vue 构造器。

### 7.2 Vue 3 的写法 {#kaj-h-d0ea11cf-5775-427a-a974-120e100cdcd5}

```js
import { createApp } from 'vue'
import App from './App.vue'

const app = createApp(App)

app.mount('#app')
```

Vue 3 通过 `createApp()` 创建应用实例，并将插件、全局配置等能力与应用实例关联。

例如：

```js
app.config.globalProperties.$message = () => {
  console.log('message')
}
```

这种设计能够更好地隔离不同应用实例的配置，减少全局状态相互影响。

## 八、状态管理：Vuex 与 Pinia {#kaj-h-3999e00b-fa92-40cc-ba1d-ec2f0078eba4}

Vue 2 项目中经常使用 Vuex；在 Vue 3 项目中，Pinia 是常见的状态管理方案。

Pinia 支持通过组合式写法定义 Store：

```js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCounterStore = defineStore('counter', () => {
  const count = ref(0)

  const doubleCount = computed(() => count.value * 2)

  function increment() {
    count.value++
  }

  return {
    count,
    doubleCount,
    increment
  }
})
```

与传统 Vuex 写法相比，Pinia 不要求通过 `mutations` 统一修改状态，并且具有较好的 TypeScript 支持。

但不能简单认为 Vue 2 只能使用 Vuex、Vue 3 只能使用 Pinia。实际选择需要考虑框架版本、状态管理库版本及项目需求。

## 九、Vue 3 的首次渲染流程 {#kaj-h-d42c6058-c91d-4d93-b365-c8d2eb4de2eb}

理解 Vue 2 与 Vue 3 的区别时，还需要了解 Vue 3 组件的基本执行流程。

以 Vue 3 + Vite 项目为例：

```text
浏览器加载 HTML 和 JavaScript
          ↓
执行 main.js
          ↓
createApp(App)
          ↓
安装插件、配置应用
          ↓
app.mount('#app')
          ↓
初始化组件实例，执行 setup()
          ↓
执行 render 函数
          ↓
生成虚拟 DOM（VNode）
          ↓
通过 patch 过程创建真实 DOM
          ↓
浏览器样式计算、布局、绘制与合成
          ↓
页面显示
```

需要区分模板编译和模板执行：

- 模板编译：通常在构建阶段将模板转换为渲染函数。
- 执行 setup：组件初始化时执行，建立响应式状态和相关逻辑。
- 执行 render：首次渲染时生成虚拟 DOM，后续更新时也可能再次执行。
- 创建或更新真实 DOM：Vue 根据虚拟 DOM 执行挂载和更新操作。
- 浏览器渲染：浏览器将更新后的页面内容显示到屏幕上。

对于使用 `<script setup>` 的组件，其内容会被编译为组件的 `setup` 逻辑。首次挂载时，Vue 先完成组件初始化，再执行渲染逻辑。

## 十、总结 {#kaj-h-1050f898-9711-4dfa-aa5a-baf6c99305ca}

Vue 2 与 Vue 3 的主要区别可以归纳为以下几点：

1. **响应式原理**：Vue 2 主要使用 `Object.defineProperty`，Vue 3 主要使用 `Proxy`。
2. **代码组织**：Vue 2 常用 Options API，Vue 3 新增 Composition API，方便复杂业务逻辑的组织和复用。
3. **生命周期**：Vue 3 将 `beforeDestroy`、`destroyed` 分别调整为 `beforeUnmount`、`unmounted`，并提供组合式生命周期 API。
4. **渲染性能**：Vue 3 通过静态提升、Patch Flags、Block Tree 等机制减少不必要的渲染工作。
5. **模板能力**：Vue 3 支持多根节点。
6. **应用配置**：Vue 3 通过 `createApp()` 创建应用实例，使配置和插件管理更加灵活。
7. **状态管理**：Pinia 是 Vue 3 项目中常见的状态管理方案。

总体而言，Vue 3 在响应式能力、复杂业务逻辑组织、渲染优化和 TypeScript 支持等方面进行了改进。对于现代前端开发，掌握 Vue 3 的 Composition API、响应式系统、组件生命周期以及虚拟 DOM 更新机制尤为重要。
