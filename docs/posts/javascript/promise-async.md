---
title: Promise 与 async/await：从状态机到错误边界
description: 从 Promise 状态转换理解串行、并行和错误传播
date: 2026-03-02
tags:
  - JavaScript
  - Promise
  - 异步编程
---

# Promise 与 async/await：从状态机到错误边界

异步代码难读，通常不是因为语法复杂，而是因为“什么时候完成”和“错误由谁处理”没有被明确表达。Promise 把一次异步操作建模为可观察的状态机，`async/await` 则提供了更接近同步代码的阅读方式。

## Promise 的三种状态

一个 Promise 只能从 `pending` 进入 `fulfilled` 或 `rejected`，状态一旦落定就不会再次改变。这个单向转换让调用方可以安全地注册多个回调，而不用担心重复完成。

```ts
function wait(ms: number) {
  return new Promise<void>((resolve) => {
    setTimeout(resolve, ms)
  })
}

wait(300).then(() => console.log('完成'))
```

## 串行与并行

当第二个请求依赖第一个请求的结果时使用串行；没有依赖时应尽早并行，避免把等待时间相加。

```ts
const user = await fetchUser(id)
const [profile, permissions] = await Promise.all([
  fetchProfile(user.id),
  fetchPermissions(user.id),
])
```

`Promise.all` 的特点是“一个失败，整体失败”。如果业务希望收集每个任务的结果，可以改用 `Promise.allSettled`，然后分别处理 `fulfilled` 和 `rejected`。

## 错误边界

`try/catch` 只会捕获当前 `await` 链上的拒绝。把边界放在一次用户操作的入口处，通常比在每一个底层函数里重复提示更容易维护。

```ts
async function loadDashboard() {
  try {
    return await fetchDashboard()
  } catch (error) {
    console.error('dashboard request failed', error)
    return { sections: [] }
  }
}
```

底层函数应保留足够的错误上下文并继续抛出；入口层再决定展示重试、空状态还是错误提示。

## 取消与竞态

Promise 本身没有取消协议。浏览器请求可以通过 `AbortController` 取消，搜索框等场景还需要在响应返回时校验请求序号，避免旧结果覆盖新结果。

## 复杂度与检查清单

- `Promise.all` 的时间复杂度取决于最慢的任务，空间复杂度为任务数量 `O(n)`。
- 串行 `await` 会把独立任务的等待时间相加。
- 每个异步入口都应明确加载、成功、失败和取消状态。
- 对可重试请求设置边界，避免无限重试放大故障。

> 先画出依赖关系，再决定串行还是并行；先定义错误边界，再开始补 `catch`。
