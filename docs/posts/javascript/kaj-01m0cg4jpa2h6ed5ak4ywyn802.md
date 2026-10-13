---
title: "关于async和await的细节"
description: "async 函数中的 throw 会使返回的 Promise 进入 rejected 状态；await 一个 rejected Promise 时，会在 await 处抛出这个 Promise 的拒绝理由。"
date: "2026-08-19"
publishedAt: "2026-08-19T15:53:19.740010+08:00"
source: "https://kajspace.cn/articles/01M0CG4JPA2H6ED5AK4YWYN802/"
tags: ["前端"]
---

# 关于async和await的细节

**async 函数中的 throw 会使返回的 Promise 进入 rejected 状态；await 一个 rejected Promise 时，会在 await 处抛出这个 Promise 的拒绝理由。**

### `async` 中的 `throw` → `reject`（向上转换） {#kaj-h-1e4d075a-2769-491c-abba-1dffa2db0235}

在 `async` 函数内部，`throw new Error()` 会被隐式捕获，并自动等价于 `return Promise.reject(new Error())`。

`async function foo() {`

`  throw new Error('出错了');`

`}`

`// 上面的代码 完全等价于 下面的普通函数：`

`function foo() {`

`  return Promise.reject(new Error('出错了'));`

`}`

`// 调用时，必须用 .catch 或 try/catch 处理`

`foo().catch(err => console.log(err.message)); // '出错了'`

**关键细节**：如果 `async` 函数里 `return new Error('xx')`（注意是 `return` 不是 `throw`），那么返回的 Promise 状态是 `fulfilled`**（成功）**，值就是那个 Error 对象，而**不会**触发 `.catch`。所以，**只有** `throw` **才会触发拒绝**。

### `await` 中的 `reject` → `throw`（向下转换） {#kaj-h-82fc424f-07da-48a8-bf17-95f99235580c}

当 `await` 等待一个 Promise 时，如果这个 Promise 最终状态是 `rejected`，`await` 会把这次“异步拒绝”**反向转换**为“同步抛出异常”。因此，你必须用 `try...catch` 来捕获它，否则程序会报错。

`async function bar() {`

`  const rejectedPromise = Promise.reject(new Error('网络错误'));`

`  `

`  // 等价于：在这一行直接 throw new Error('网络错误')`

`  await rejectedPromise; `

`}`

`// 必须用 try/catch 包裹`

`async function run() {`

`  try {`

`    await bar();`

`  } catch (err) {`

`    console.log(err.message); // '网络错误' `

`  }`

`}`

**关键细节**：`await` 只负责“抛出”错误，它本身**不会**帮你自动捕获。如果你忘了写 `try...catch`，这个错误会冒泡到外层，变成**未捕获的 Promise 错误**（Unhandled Promise Rejection）。

**async 函数中的 throw 会使返回的 Promise 进入 rejected 状态；await 一个 rejected Promise 时，会在 await 处抛出这个 Promise 的拒绝理由。**
