---
title: Vue 3 Composition API 的可复用边界
description: 用搜索列表拆分状态、请求和视图，让组合式函数保持可测试
date: 2026-02-18
tags:
  - Vue 3
  - Composition API
  - 组件设计
---

# Vue 3 Composition API 的可复用边界

组合式 API 的价值不在于把所有代码放进 `setup`，而在于让一组有明确职责的状态和副作用可以被命名、测试和复用。

## 先区分三类状态

页面通常同时包含查询条件、请求状态和展示数据。查询条件属于用户输入，请求状态属于流程，展示数据属于服务端结果。把它们混在一个巨大响应式对象里，会让重置和测试都变得困难。

## 一个小型 composable

```ts
import { ref, watch } from 'vue'

export function useSearch(fetcher: (keyword: string) => Promise<string[]>) {
  const keyword = ref('')
  const items = ref<string[]>([])
  const loading = ref(false)

  async function search() {
    loading.value = true
    try {
      items.value = await fetcher(keyword.value)
    } finally {
      loading.value = false
    }
  }

  watch(keyword, search)
  return { keyword, items, loading, search }
}
```

真实项目中还应补充防抖、竞态保护和错误状态。组合式函数接收 `fetcher`，可以在单元测试中注入一个纯函数。

## 组件边界

容器组件负责获取数据和组织流程，展示组件接收 props 并发出事件。这样可以把“列表为空”的视觉决策留在展示组件，同时让请求逻辑在页面之间复用。
