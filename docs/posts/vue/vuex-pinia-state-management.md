---
title: Vuex 原理与 Vue 3 Pinia 状态管理对比
category: vue
description: 从 Vuex 的 State、Getters、Mutations、Actions 出发，对比 Vue 3 Pinia 的 Store、响应式状态和模块组织方式。
date: "2026-10-28"
publishedAt: "2026-10-28T09:54:38+08:00"
tags:
  - Vuex
  - Pinia
  - Vue 3
  - 状态管理
  - 前端八股
---

# Vuex 原理与 Vue 3 Pinia 状态管理对比

## 一、什么是 Vuex？

Vuex 是 Vue.js 的集中式状态管理库，主要用于管理多个组件需要共享的状态。

在普通 Vue 组件中，可以使用 `data` 或 `ref` 保存组件自己的状态。但是，当多个组件需要共享同一份数据时，如果仅通过 props 和自定义事件逐层传递，组件之间的通信就可能变得复杂。

例如，一个后台管理系统可能需要在以下组件中共享用户信息：

- `Header`：显示当前登录用户。
- `Sidebar`：根据用户角色显示菜单。
- `UserInfo`：展示用户详细信息。
- `PermissionButton`：根据权限决定是否显示操作按钮。

如果每个组件都独立维护用户信息，就容易出现数据不一致的问题。

Vuex 通过 Store 集中管理这些共享状态，让不同组件能够读取同一份数据，并通过约定的方式修改状态。

### 1. Vuex 的核心组成

| 模块 | 作用 |
|---|---|
| State | 保存共享状态 |
| Getters | 根据 State 派生数据 |
| Mutations | 同步修改 State |
| Actions | 处理业务逻辑、异步操作，并通过提交 Mutation 修改状态 |
| Store | 组织和管理上述状态及相关方法 |

其中，State 是核心数据源，其他模块围绕 State 的读取、修改和业务操作展开。

### 2. Vuex 的核心工作流程

Vuex 的典型数据流可以表示为：

```text
Vue Component
     │
     │ dispatch(action)
     ▼
   Actions
     │
     │ commit(mutation)
     ▼
  Mutations
     │
     │ 修改 State
     ▼
   State
     │
     │ 响应式更新
     ▼
Vue Component 重新渲染
```

例如，用户点击一个按钮，希望将计数器增加 1：

1. 组件分发 `increment` Action。
2. Action 执行业务逻辑。
3. Action 提交 `increment` Mutation。
4. Mutation 同步修改 State。
5. Vue 的响应式系统检测到相关状态变化。
6. 使用该状态的组件更新视图。

需要注意，**不是所有 Vuex 状态修改都必须经过 Action**。组件可以直接提交 Mutation。Action 主要用于组织业务逻辑和异步操作。

## 二、Vuex 的核心模块

### 1. State：集中存储状态

State 用于保存需要共享的数据。

```js
import { createStore } from 'vuex';

const store = createStore({
  state() {
    return {
      count: 0,
      user: {
        name: '张三',
        role: 'admin',
      },
    };
  },
});

export default store;
```

在 Vue 3 中，Vuex 4 可以与 Vue 3 配合使用。

组件中可以通过 `useStore()` 获取 Store：

```vue
<script setup>
import { computed } from 'vue';
import { useStore } from 'vuex';

const store = useStore();

const count = computed(() => store.state.count);
</script>

<template>
  <p>{{ count }}</p>
</template>
```

这里使用 `computed` 是为了建立响应式读取关系。当 `store.state.count` 发生变化时，`count` 会随之更新。

### 2. Getters：获取派生状态

Getters 类似于基于 State 计算出来的派生数据。

例如，State 中保存了商品列表，可以通过 Getter 获取商品总数：

```js
const store = createStore({
  state() {
    return {
      products: [
        { id: 1, price: 100 },
        { id: 2, price: 200 },
      ],
    };
  },

  getters: {
    totalPrice(state) {
      return state.products.reduce(
        (total, product) => total + product.price,
        0,
      );
    },
  },
});
```

组件读取：

```js
const totalPrice = computed(
  () => store.getters.totalPrice,
);
```

这里的 `totalPrice` 不是独立保存的状态，而是根据 `products` 计算出来的结果。

### 3. Mutations：同步修改 State

Mutation 是 Vuex 中约定的同步状态修改入口。

```js
const store = createStore({
  state() {
    return {
      count: 0,
    };
  },

  mutations: {
    increment(state) {
      state.count++;
    },

    add(state, payload) {
      state.count += payload;
    },
  },
});
```

调用方式：

```js
store.commit('increment');
store.commit('add', 5);
```

Mutation 的第一个参数是 `state`，第二个参数可以是传入的 `payload`。

例如：

```js
store.commit('add', 5);
```

相当于向 `add` Mutation 传入数值 `5`。

Vuex 要求 Mutation 保持同步，是为了让每次状态变化都能被明确追踪。如果在 Mutation 中执行异步操作，状态究竟在什么时候改变就会变得难以判断。

需要注意：Vuex 的严格模式会检查是否存在 Mutation 之外的状态修改，并在开发环境中对违规修改报错。但生产环境下，严格模式通常不建议开启，因为它会带来额外的检查开销。

### 4. Actions：处理业务逻辑和异步操作

Action 与 Mutation 的主要区别在于，Action 可以执行异步操作，并通过 `commit()` 提交 Mutation。

```js
const store = createStore({
  state() {
    return {
      count: 0,
    };
  },

  mutations: {
    setCount(state, value) {
      state.count = value;
    },
  },

  actions: {
    async fetchCount({ commit }) {
      const response = await fetch('/api/count');
      const data = await response.json();

      commit('setCount', data.count);
    },
  },
});
```

组件中调用：

```js
await store.dispatch('fetchCount');
```

这个过程可以拆成三个阶段：

1. `dispatch('fetchCount')` 分发 Action。
2. Action 请求后端接口，获得数据。
3. Action 调用 `commit('setCount', data.count)`，通过 Mutation 更新 State。

Action 接收的参数是 `context`，其中包含 `state`、`getters`、`commit`、`dispatch` 等属性和方法。

例如：

```js
actions: {
  async fetchCount(context) {
    const response = await fetch('/api/count');
    const data = await response.json();

    context.commit('setCount', data.count);
  },
}
```

也可以通过解构只取需要的属性：

```js
actions: {
  async fetchCount({ commit, state }) {
    console.log(state.count);

    commit('setCount', 10);
  },
}
```

Action 并不是只能处理异步操作，同步业务逻辑也可以放在 Action 中。关键区别是：Mutation 负责同步修改状态，而 Action 负责组织业务操作，并在需要时提交 Mutation。

## 三、Vuex 中 Action 和 Mutation 的区别

| 对比项 | Mutation | Action |
|---|---|---|
| 主要职责 | 同步修改 State | 组织业务逻辑和异步操作 |
| 是否允许异步操作 | 不应该进行异步操作 | 可以 |
| 如何调用 | `commit()` | `dispatch()` |
| 第一个参数 | `state` | `context` |
| 是否能直接修改 State | 是 | 不应直接修改 Vuex State，应通过 Mutation |
| 典型场景 | `count++`、更新用户信息 | 请求接口、处理业务流程 |

可以用一句话记忆：

**Mutation 负责同步修改状态，Action 负责组织业务操作；异步 Action 通常在获取数据后提交 Mutation。**

还需要纠正一个常见误解：Mutation 不一定只能被一个地方调用，同类型 Mutation 也不要求名称在整个应用中绝对唯一。为了避免意外行为，实际项目中应合理规划 Mutation 类型名称。

## 四、Vue 3 为什么更推荐 Pinia？

Pinia 是 Vue 官方推荐的状态管理方案，适用于 Vue 3 应用。它保留了集中管理共享状态的核心思想，同时简化了 Vuex 中的一些概念。

Vuex 4 仍然可以用于 Vue 3 项目，并不是 Vue 3 一定不能使用 Vuex。对于新项目，通常优先考虑 Pinia。

Pinia 的主要特点包括：

- 不需要单独定义 Mutations。
- 使用 `state`、`getters` 和 `actions` 组织状态。
- 支持 Composition API 风格的 Store 定义。
- 对 TypeScript 有更好的原生支持。
- 支持将 Store 按业务模块拆分。
- 支持通过插件扩展能力。

### 1. Pinia 的基本结构

先创建一个 Store：

```ts
// stores/counter.ts
import { defineStore } from 'pinia';

export const useCounterStore = defineStore('counter', {
  state: () => ({
    count: 0,
  }),

  getters: {
    doubleCount: (state) => state.count * 2,
  },

  actions: {
    increment() {
      this.count++;
    },

    async fetchCount() {
      const response = await fetch('/api/count');
      const data = await response.json();

      this.count = data.count;
    },
  },
});
```

这里：

- `defineStore()` 用于定义一个 Store。
- `'counter'` 是 Store 的唯一标识 ID。
- `state` 保存状态。
- `getters` 定义派生数据。
- `actions` 定义业务方法，可以包含同步或异步逻辑。

与 Vuex 不同，Pinia 不要求把同步状态修改单独写在 Mutation 中。Action 可以直接修改 Store 的状态。

### 2. 在 Vue 组件中使用 Pinia

```vue
<script setup lang="ts">
import { useCounterStore } from '@/stores/counter';

const counterStore = useCounterStore();
</script>

<template>
  <p>当前计数：{{ counterStore.count }}</p>
  <p>两倍计数：{{ counterStore.doubleCount }}</p>

  <button @click="counterStore.increment()">
    增加
  </button>

  <button @click="counterStore.fetchCount()">
    从接口获取计数
  </button>
</template>
```

可以看到，组件不需要调用 `commit()` 或 `dispatch()`，而是直接调用 Store 的方法：

```js
counterStore.increment();
counterStore.fetchCount();
```

Pinia 仍然使用 Vue 的响应式系统，因此当状态变化时，读取这些状态的组件会相应更新。

使用 Pinia 前，需要在 Vue 应用入口注册：

```ts
import { createApp } from 'vue';
import { createPinia } from 'pinia';
import App from './App.vue';

const app = createApp(App);

app.use(createPinia());
app.mount('#app');
```

## 五、Vuex 与 Pinia 的核心区别

| 对比项 | Vuex | Pinia |
|---|---|---|
| 推荐场景 | 维护已有 Vuex 项目 | Vue 3 新项目 |
| 状态定义 | `state` | `state` |
| 派生状态 | `getters` | `getters` |
| 状态修改 | 通常通过 Mutation | 可以直接修改，也可以在 Action 中修改 |
| 业务方法 | `actions` | `actions` |
| 异步操作 | 通常在 Action 中执行 | 可以在 Action 中执行 |
| 调用方式 | `commit()`、`dispatch()` | 直接调用 Store 方法 |
| TypeScript | 支持，但部分场景需要更多类型声明 | 类型推导更自然 |
| 模块组织 | 常见做法是使用 modules | 通常定义多个独立 Store |
| Composition API | 可以使用 | 支持自然，适合 Vue 3 开发模式 |

### 1. 最重要的区别：Mutation 是否必需

Vuex：

```js
mutations: {
  increment(state) {
    state.count++;
  },
},

actions: {
  increment({ commit }) {
    commit('increment');
  },
},
```

调用时：

```js
store.dispatch('increment');
```

Pinia：

```ts
actions: {
  increment() {
    this.count++;
  },
},
```

调用时：

```ts
counterStore.increment();
```

Pinia 将状态修改和业务方法整合到更直观的 Store API 中，减少了额外的概念和样板代码。

### 2. Pinia 也不是只能通过 Action 修改状态

Pinia 允许直接修改状态：

```ts
counterStore.count++;
```

也可以使用 `$patch()` 一次更新多个字段：

```ts
counterStore.$patch({
  count: 10,
});
```

如果涉及复杂业务逻辑，通常仍然建议将修改封装在 Action 中，以保持代码结构清晰。

因此，Pinia 的灵活性更高，但也意味着团队需要自行约定状态修改规范。

### 3. Pinia 的模块组织方式更轻量

Vuex 常见的模块结构：

```text
store/
├── index.js
└── modules/
    ├── user.js
    └── cart.js
```

Pinia 通常按业务创建独立 Store：

```text
stores/
├── user.ts
├── cart.ts
└── counter.ts
```

使用时分别调用：

```ts
const userStore = useUserStore();
const cartStore = useCartStore();
```

这使得 Store 的组织和复用更直观，也便于配合 Composition API 开发。

## 六、Vuex 和 Pinia 的底层原理一样吗？

它们的实现细节不同，但核心目标相似：集中管理共享状态，并让组件在状态变化后正确更新。

在 Vue 3 中，Pinia 依托 Vue 的响应式系统，例如 `ref`、`reactive` 和相关响应式机制来管理状态。Vuex 4 也与 Vue 3 的响应式系统配合使用。

可以从三个层面理解：

1. **状态层：** Store 保存共享状态。
2. **业务层：** Getters 负责派生数据，Actions 负责业务逻辑。
3. **视图层：** 组件读取响应式状态，状态变化后 Vue 更新相关视图。

Vuex 的特点是通过 Mutation 和 Action 明确区分状态修改与业务操作；Pinia 则减少了这层强制区分，让开发者直接通过 Store 的状态和方法完成业务逻辑。

因此，Pinia 并不是简单地把 Vuex 改了个名字，而是在保持集中式状态管理思想的同时，简化了 API，并改善了 TypeScript 和 Vue 3 开发体验。

## 七、面试高频问题

### 1. Vuex 的核心原理是什么？

Vuex 将共享状态集中保存在 Store 中。组件读取 State 或 Getters，当需要修改状态时，可以提交 Mutation；涉及异步请求或复杂业务流程时，可以通过 Action 组织操作，再提交 Mutation 更新状态。Vue 的响应式系统会根据状态变化更新相关视图。

### 2. 为什么 Vuex 的 Mutation 必须同步？

Mutation 同步执行有利于明确状态变化的发生时机，便于调试、追踪和记录状态变更。如果 Mutation 中包含异步操作，状态变化的时间和顺序就会变得不明确。

### 3. Action 和 Mutation 有什么区别？

Mutation 负责同步修改 State，通过 `commit()` 调用；Action 负责业务逻辑，可以包含异步操作，通过 `dispatch()` 调用，并可提交 Mutation。

### 4. Pinia 为什么不需要 Mutation？

Pinia 采用更简化的 Store API，允许直接修改状态，也允许在 Action 中修改状态。它不再要求开发者把所有同步状态修改单独抽取成 Mutation，从而减少样板代码。

### 5. Vuex 和 Pinia 应该怎么选？

对于 Vue 3 新项目，通常优先选择 Pinia，因为它更简洁、类型推导更自然，也更贴合 Composition API。已有 Vuex 项目则可以继续维护，不必仅仅因为使用 Vuex 就立即重写。

## 八、总结

Vuex 和 Pinia 都是为了解决组件间共享状态管理问题的工具，二者都依托 Vue 的响应式系统实现视图更新。

最需要记住的知识点是：

1. Vuex 的核心模块包括 State、Getters、Mutations 和 Actions。
2. Mutation 负责同步修改状态，Action 可以处理异步操作并提交 Mutation。
3. Pinia 保留了 State、Getters 和 Actions 的组织方式，但取消了 Mutation 的强制要求。
4. Pinia 支持直接修改状态，也支持在 Action 中封装业务逻辑。
5. Vue 3 新项目通常优先选择 Pinia，已有 Vuex 项目可以根据实际需求继续维护。

从前端面试角度看，建议先熟练掌握 Vuex 的 `commit`、`dispatch`、Mutation 和 Action 的区别，再理解 Pinia 为什么能够简化状态管理流程，以及它如何与 Vue 3 的 Composition API 配合使用。
