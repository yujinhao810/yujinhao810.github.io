---
title: 项目实践
description: 俞金浩参与和负责的全栈、低代码与 AI 应用项目
---

# 项目实践

这里记录我在全栈应用、AI 工作流和可视化搭建方向的实践。每个项目都从背景、技术栈和具体贡献展开。

## HealthFlow · AI 全栈健康管理平台 {#healthflow}

**项目周期：** 2026.02 — 2026.06

**项目背景：** 基于 React + NestJS 构建的个人健康管理与 AI 辅助平台，覆盖健康档案、趋势分析、流式 AI 对话、知识库问答和辅助分诊。项目将 AI 对话、工具调用、知识检索和 Agent 工作流整合到统一应用链路中。

**技术栈：** React、TypeScript、Ant Design、React Router、TanStack Query、NestJS、Prisma、PostgreSQL、LangGraph.js、RAG、SSE

**核心功能：**

- 健康总览、健康记录、趋势图表与 AI 对话模块。
- 基于 POST SSE 的流式 AI 对话，支持增量消息、检索状态、异常状态和 AbortController 中止生成。
- 文档解析、OCR、结构化语义切分、Embedding、混合检索与 RRF 融合，返回带来源引用的上下文。
- 基于 LangGraph.js StateGraph 编排多阶段健康分析流程，支持条件路由、多节点执行和结果汇总。
- 记录 Tool Calling 事件链路与 AgentRun 执行过程，工具异常时回退到普通对话流程。

**个人贡献：**

- 使用 React + TypeScript 开发健康总览、健康记录、趋势图表和 AI 对话模块，结合 TanStack Query 管理请求与缓存，并使用 React Hook / Context 管理页面交互状态。
- 使用 `fetch + ReadableStream + TextDecoder` 解析 SSE 分片，实时更新消息和连接状态，并支持主动中止生成。
- 设计 RAG 检索链路，完成文档解析、OCR、切分、Embedding、混合检索和 RRF 融合。
- 使用 LangGraph.js StateGraph 拆分多阶段健康分析节点，通过共享 State 和条件路由控制流程分支。

**项目源码：** [github.com/yujinhao810/Health-Flow](https://github.com/yujinhao810/Health-Flow.git)

**在线演示：** [healthflowai.top](https://healthflowai.top)

## 营销页面搭建平台 · 前端开发者 {#vue-lowcode-builder}

**项目周期：** 2025.06 — 2025.08

**项目背景：** 基于 Web 的低代码可视化页面搭建平台，通过组件拖拽与配置化方式快速生成业务页面，支持复杂交互编辑、实时预览，适用于活动营销和落地页等高频页面构建场景。

**技术栈：** Vue 3、TypeScript、Element Plus、Pinia、Vue Router、Vite

**核心功能：**

- 基于 JSON Schema 定义页面结构和组件树，使用 TypeScript 接口与枚举约束属性和交互行为。
- 支持组件拖拽、缩放、旋转、自由布局，以及属性面板与画布状态的实时双向联动。
- 通过命令模式实现撤销 / 重做，覆盖组件新增、删除和属性变更等高频编辑操作。
- 可扩展通用组件覆盖文本、图片、表单、图表和营销组件，统一支持样式配置、属性定制和事件绑定。
- 实现图层管理、自动对齐、页面预览、z-index 管理、JSON 导出与持久化存储。

**个人贡献：** 负责编辑器核心架构与数据模型设计，使用 Vue 3 Composition API 完成交互、画布状态和配置系统，并完善撤销 / 重做、可扩展组件、图层管理和页面预览能力。

**项目源码：** [github.com/yujinhao810/vue-lowcode-builder](https://github.com/yujinhao810/vue-lowcode-builder.git)

**在线演示：** 尚未配置

## 实习项目：煤矿隐蔽致灾动态管理平台

**公司：** 浙江众合科技股份有限公司 · 前端开发实习生

**时间：** 2026.05 — 2026.08

使用 Vue 3、Vite、Element Plus、Axios、Pinia、ECharts 和 micro-app 参与平台前端开发，完成业务模块接口联调、列表与统计图表、预警数据接入和多页面复用。

- 封装风险评价、灾害成果图等业务组件，通过 props 适配不同业务场景。
- 使用 requestId 校验响应有效性，处理筛选竞态、Blob / Object URL 预览、MIME 识别和异常回退。
- 通过 iframe + postMessage 实现业务页面与 3D 地质模型组件的数据交互。
- 参与 micro-app 子应用接入、动态菜单、路由鉴权、树形文件管理和 FormData 上传。

## 相关技术文章

- [流式输出的前端设计](/posts/project/streaming-ui)
- [从 Tool Calling 到 MCP：让 Agent 使用工具](/posts/ai-agent/tool-calling-mcp)
