---
title: 流式输出的前端设计
description: 用 SSE 事件和可恢复状态设计更可靠的流式交互
date: 2026-02-25
tags:
  - SSE
  - Vue
  - 项目实践
---

# 流式输出的前端设计

流式响应把一次请求变成一串事件。界面需要同时处理增量文本、连接状态、结束信号和错误，因此应先建立明确的状态模型。

## 状态模型

可以将状态拆成 `idle`、`connecting`、`streaming`、`done` 和 `error`。只有 `streaming` 状态允许追加片段，`done` 之后的迟到事件应被忽略。

```ts
type StreamState = 'idle' | 'connecting' | 'streaming' | 'done' | 'error'

function appendChunk(state: StreamState, text: string, output: string) {
  if (state !== 'streaming') return output
  return output + text
}
```

## 体验与可靠性

- 首个字节到达前显示连接状态，避免用户误以为页面失去响应。
- 使用 `AbortController` 让用户可以主动停止生成。
- 将服务端事件 id 保存到内存或本地状态，必要时支持断线重连。
- 结束时统一释放 reader、计时器和按钮状态。

流式 UI 的重点是让每个中间状态都可解释、可恢复，而不是单纯追求更快地显示文字。
