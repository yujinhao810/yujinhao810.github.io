---
title: 从 Tool Calling 到 MCP：让 Agent 使用工具
description: 理解模型、工具服务和上下文之间的协议边界
date: 2026-03-08
tags:
  - AI Agent
  - Tool Calling
  - MCP
  - RAG
---

# 从 Tool Calling 到 MCP：让 Agent 使用工具

模型本身只能生成文本。Agent 的“行动能力”来自一个闭环：模型提出结构化的工具调用，运行时执行工具，再把结果作为上下文交回模型。

## Tool Calling 的最小闭环

1. 应用向模型提供工具名称、参数 schema 和用途描述。
2. 模型返回一个结构化调用请求，应用校验参数并执行函数。
3. 应用把工具结果放回对话上下文，请模型生成最终回复或继续调用。

```ts
type ToolCall = { name: string; arguments: Record<string, unknown> }

async function runAgent(call: ToolCall) {
  const tool = registry[call.name]
  if (!tool) throw new Error(`Unknown tool: ${call.name}`)
  const input = tool.schema.parse(call.arguments)
  return tool.execute(input)
}
```

工具边界必须包含参数校验、权限检查、超时和可观测日志。模型输出只是“不可信的请求”，不能直接当作函数调用参数。

## MCP 解决什么问题

当每个应用都为每个数据源编写一套私有适配器时，工具会难以复用。MCP 将工具、资源和提示词抽象成可发现的协议，让 Agent 客户端可以连接不同的 MCP Server。

这并不意味着所有工具都应该暴露为 MCP。稳定的领域边界、清晰的权限模型和可管理的部署方式，比协议本身更重要。

## RAG 与工具调用的关系

RAG 负责把相关知识检索进上下文；工具调用负责执行有副作用或需要实时数据的动作。一个 Agent 可以先检索文档，再调用工单系统，最后把结果整理给用户。

> 先定义“模型可以请求什么”，再定义“系统允许执行什么”。协议只是边界的表达方式。
