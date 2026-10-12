---
title: Node.js 事件循环与 I/O
description: 从任务队列理解 Node.js 如何调度异步 I/O
date: 2026-01-28
tags:
  - Node.js
  - Event Loop
  - 异步
---

# Node.js 事件循环与 I/O

Node.js 用 JavaScript 主线程执行回调，同时把文件、网络等 I/O 交给系统或 libuv。回调完成后进入队列，事件循环再选择合适的时机执行它们。

## 一个可观察的顺序

```js
console.log('sync')
setTimeout(() => console.log('timer'), 0)
queueMicrotask(() => console.log('microtask'))
console.log('end')
```

同步代码先执行；当前调用栈清空后处理微任务；计时器回调要等到对应阶段才有机会执行。不要依赖不同运行时下过于细微的顺序，业务代码更应避免在回调之间共享隐式状态。

## 服务端实践

- 不要在请求处理器里执行大规模同步计算。
- 统一设置超时和取消，避免连接长期占用。
- 把 I/O、领域逻辑和响应格式拆成清晰的模块。

NestJS 的依赖注入可以帮助隔离这些模块，但不能替代对事件循环和资源生命周期的理解。
