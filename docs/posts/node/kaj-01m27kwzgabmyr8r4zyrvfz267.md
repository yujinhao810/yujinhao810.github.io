---
title: "HealthFlow中的后端接口"
description: "以普通接口为例："
date: "2026-09-11"
publishedAt: "2026-09-11T14:54:04.488810+08:00"
source: "https://kajspace.cn/articles/01M27KWZGABMYR8R4ZYRVFZ267/"
tags: ["后端"]
---

# HealthFlow中的后端接口

## 一、请求的整体处理链路 {#kaj-h-30e79dcd-a7bd-47a7-9e91-32b61d39fc80}

以普通接口为例：

```text
React fetch()
   ↓
NestJS / Express
   ↓
路由匹配 Controller
   ↓
AuthGuard 身份认证
   ↓
ValidationPipe / DTO 校验
   ↓
Controller 提取参数
   ↓
Service 执行业务逻辑
   ↓
Prisma / Redis / LLM / LangGraph
   ↓
返回 JSON
```

例如前端调用：

```html
api<HealthRecord[]>('/health/records')
```

后端对应：

```js
@Controller('health/records')
@UseGuards(AuthGuard)
export class HealthRecordsController {
  @Get()
  list(@CurrentUser() user: AuthUser) {
    return this.records.list(user);
  }

  @Post()
  create(@CurrentUser() user: AuthUser, @Body() body: CreateHealthRecordDto) {
    return this.records.create(user, body);
  }
}
```

对应源码：

- `health-records.controller.ts (line 9)`
- `client.ts (line 24)`

Controller 只负责：

- 匹配 URL 和 HTTP 方法
- 读取请求参数
- 身份认证
- 参数校验
- 调用 Service

具体业务逻辑放在 Service 中，而不是全部写在 Controller 里。

---

## 二、项目中的接口类型 {#kaj-h-37f7eb65-13ca-4433-8181-8bad3cb5f1ea}

## 1. REST 风格 JSON 接口 ⭐⭐⭐⭐⭐ {#kaj-h-16c0e6a9-baf7-42a8-a9c0-99d0c351120e}

这是项目中数量最多的一类接口。

典型资源包括：

```text
/auth
/conversations
/health/records
/health/snapshots
/health/insights
/integrative-diagnosis
/agent-runs
/uploads
/llm
```

### 常见 HTTP 方法 {#kaj-h-1adc79b7-184b-4036-ab1a-0ce2b1c90d0a}

| 方法 | 典型用途 | 项目示例 |
| --- | --- | --- |
| `GET` | 查询资源 | `GET /conversations` |
| `POST` | 创建资源或触发动作 | `POST /health/records` |
| `PATCH` | 局部更新 | `PATCH /auth/profile` |
| `DELETE` | 删除资源 | `DELETE /health/records/:id` |

例如会话接口：

```text
POST   /conversations
GET    /conversations
GET    /conversations/:id
DELETE /conversations/:id
POST   /conversations/:id/messages
```

对应 `chat.controller.ts (line 11)`。

健康记录接口：

```text
GET    /health/records
POST   /health/records
DELETE /health/records/:id
```

辅助分诊接口：

```text
POST   /integrative-diagnosis
POST   /integrative-diagnosis/follow-up
POST   /integrative-diagnosis/:id/supplement
POST   /integrative-diagnosis/:id/retry
GET    /integrative-diagnosis
GET    /integrative-diagnosis/:id
DELETE /integrative-diagnosis/:id
```

对应 `integrative-diagnosis.controller.ts (line 8)`。

严格来说，项目并不是完全纯粹的 REST，因为还存在一些“动作型接口”：

```text
POST /health/snapshots/generate
POST /health/insights/refresh
POST /health/insights/:id/read
POST /integrative-diagnosis/:id/retry
POST /llm/validate
```

这些接口更像：

> REST 资源接口 + Command 风格动作接口

面试时可以说：

> 项目整体采用 REST 风格的 HTTP API，资源查询和增删改使用 GET、POST、PATCH、DELETE；对于生成快照、刷新洞察、重试诊断等业务动作，则使用 POST 动作接口。

---

## 2. JSON 请求和响应 ⭐⭐⭐⭐⭐ {#kaj-h-5098dba1-047a-4157-adb3-b74cf1f206ff}

普通接口一般使用：

```text
Content-Type: application/json
```

前端公共请求方法会自动设置：

```text
headers.set('Content-Type', 'application/json');
```

例如创建健康记录：

```html
api<HealthRecord>('/health/records', {
  method: 'POST',
  body: JSON.stringify(input),
});
```

后端通过：

```text
@Body() body: CreateHealthRecordDto
```

接收请求体。

项目启动时配置了全局参数管道：

```text
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,
    transform: true,
  }),
);
```

对应 `main.ts (line 23)`。

这意味着：

- `whitelist: true`：过滤 DTO 中没有声明的字段
- `transform: true`：尝试进行类型转换
- DTO 可以配合 `class-validator` 做参数校验

例如聊天请求 DTO：

```text
export class SendMessageDto {
  @IsString()
  @MaxLength(8000)
  content!: string;

  @IsOptional()
  @IsArray()
  @ArrayMaxSize(6)
  @IsUUID('4', { each: true })
  attachmentIds?: string[];

  @IsOptional()
  @IsBoolean()
  ragEnabled?: boolean;
}
```

对应 `send-message.dto.ts (line 3)`。

不过项目不是所有模块都使用 DTO：

- 普通聊天、健康记录等使用 `class-validator DTO`
- 辅助分诊使用 `Zod schema`
- LLM 配置也使用 `Zod schema`

例如辅助分诊 Controller 接收：

```js
create(
  @CurrentUser() user: AuthUser,
  @Body() body: CreateDiagnosisDto,
) {
  return this.diagnosis.create(user, body);
}
```

但 Service 内部还会使用共享的 Zod schema 做更严格的结构校验。

所以面试可以这样说：

> 项目有两层校验：Controller 层主要使用 DTO 和 `ValidationPipe`，复杂的 Agent 输入在 Service 内部再通过 Zod schema 做结构化校验。

---

## 3. SSE 流式接口 ⭐⭐⭐⭐⭐ {#kaj-h-ff5f5a6a-814f-4c39-a05d-d6896aba83f5}

最重要的流式接口是：

```text
POST /conversations/:id/stream
```

它用于聊天回复的流式输出。

对应 `chat.controller.ts (line 44)`。

后端设置：

```text
res.setHeader('Content-Type', 'text/event-stream');
res.setHeader('Cache-Control', 'no-cache, no-transform');
res.setHeader('Connection', 'keep-alive');
```

然后不断写入 SSE 事件：

```text
res.write(`event: ${event}\n`);
res.write(`data: ${JSON.stringify(data)}\n\n`);
```

事件结构大致是：

```text
event: assistant_delta
data: {"type":"assistant_delta","text":"..."}

event: tool_call
data: {"type":"tool_call", ...}

event: tool_result
data: {"type":"tool_result", ...}

event: assistant_done
data: {"type":"assistant_done","fullText":"..."}
```

当前聊天流中可能出现：

```text
retrieval_started
retrieval_done
tool_call
tool_result
agent_step
plan_generated
assistant_delta
assistant_done
error
```

前端不是使用原生 `EventSource`，而是使用：

```text
fetch()
response.body.getReader()
```

逐块读取响应，然后自己按 `\n\n` 拆分 SSE 事件。

对应 `chat.ts (line 79)`。

这是因为当前接口是：

```text
POST + JSON body + Bearer Token
```

而原生 `EventSource` 更适合简单的 GET SSE 请求，不方便直接发送 POST 请求体。

面试时可以这样回答：

> 项目的聊天接口使用基于 HTTP 的 SSE，而不是 WebSocket。后端通过 `text/event-stream` 持续写入事件，前端通过 `fetch` 的 `ReadableStream` 读取。之所以没有使用 EventSource，是因为聊天请求需要 POST 请求体、附件 ID 和 RAG 开关等参数。

---

## 4. 文件上传接口：`multipart/form-data` ⭐⭐⭐⭐ {#kaj-h-0113b4fd-98f3-4beb-bd34-2df884cd1206}

上传接口：

```text
POST /uploads
POST /auth/avatar
```

使用 NestJS 的：

```text
FileInterceptor('file')
```

例如：

```js
@Post()
@UseInterceptors(FileInterceptor('file'))
create(
  @CurrentUser() user: AuthUser,
  @UploadedFile() file: Express.Multer.File | undefined,
  @Body('purpose') purpose: 'chat_attachment' | 'knowledge_source',
) {
  return this.uploads.create(user, file, purpose);
}
```

对应 `uploads.controller.ts (line 22)`。

前端使用：

```js
const form = new FormData();
form.append('file', file);
form.append('purpose', purpose);
```

此时请求类型是：

```text
Content-Type: multipart/form-data
```

文件上传之后，后端会根据 `purpose` 进入不同流程：

```text
chat_attachment
  → 保存为聊天附件

knowledge_source
  → 解析文档
  → 文档质量检查
  → 切块
  → Embedding
  → 写入 RAG 知识库
```

---

## 5. 二进制文件下载接口 ⭐⭐⭐ {#kaj-h-49205ed3-f211-4116-909a-de8d11230d7a}

文件内容接口：

```text
GET /uploads/:id/content
GET /auth/avatar/:filename
```

这类接口不返回 JSON，而是直接返回文件流：

```text
res.setHeader('Content-Type', file.mimeType);
res.setHeader(
  'Content-Disposition',
  `inline; filename*=UTF-8''${encodeURIComponent(file.originalName)}`,
);

createReadStream(file.storagePath).pipe(res);
```

对应 `uploads.controller.ts (line 50)`。

因此项目后端同时支持：

```text
JSON 响应
SSE 文本事件流
文件二进制流
```

---

## 6. 辅助分诊使用普通 JSON + 前端轮询 ⭐⭐⭐⭐ {#kaj-h-141171c9-6a39-4f73-a1ec-9c92302e3d93}

辅助分诊没有使用 SSE。

创建接口：

```text
POST /integrative-diagnosis
```

前端先获得一个诊断会话对象，状态可能是：

```text
pending
completed
failed
```

如果状态是 `pending`，React Query 会定期重新请求：

```js
refetchInterval: (query) =>
  query.state.data?.status === 'pending' ? 2000 : false
```

对应 `useDiagnosis.ts (line 39)`。

历史列表中的 pending 会每 3 秒刷新一次，详情页中的 pending 会每 2 秒刷新一次。

所以辅助分诊的前端交互是：

```text
POST 创建诊断
   ↓
返回 pending 会话
   ↓
前端定时 GET 查询
   ↓
status = completed
   ↓
展示最终结果
```

这不是 WebSocket，也不是 SSE，而是：

> 普通 JSON 接口 + React Query polling

这样设计的好处是：

- 实现简单
- 页面刷新后可以继续查询
- 诊断结果持久化在数据库中
- 不依赖长连接

---

## 三、认证方式 {#kaj-h-d30ae3b1-b032-4b9d-9ef4-ed9603317c47}

前端登录成功后保存访问令牌：

```text
localStorage
```

后续请求发送：

```html
Authorization: Bearer <token>
```

前端公共请求方法中：

```js
if (token) {
  headers.set('Authorization', `Bearer ${token}`);
}
```

后端通过：

```text
@UseGuards(AuthGuard)
```

保护接口。

`AuthGuard` 会：

1. 读取 `Authorization` 请求头
2. 解析 Bearer Token
3. 调用 `AuthService.getUserFromToken()`
4. 将用户放入 request
5. 通过 `@CurrentUser()` 注入 Controller

例如：

```js
@Get()
list(@CurrentUser() user: AuthUser) {
  return this.records.list(user);
}
```

这也是项目多租户数据隔离的基础：Service 查询数据库时会携带当前用户 ID。

---

## 四、接口的代码分层方式 {#kaj-h-eab05b9f-93a4-47b7-9206-fdfbe0e9f2c1}

项目采用比较典型的 NestJS 分层：

```text
Controller
  ↓
Service
  ↓
Domain Service / Agent / RAG / LLM
  ↓
Prisma / Redis / 外部 API
```

例如聊天请求：

```text
ChatController
  ↓
ChatStreamService
  ↓
ChatContextService
  ↓
RagService / AgentRuntime / SkillRegistry
  ↓
LLM Provider / Prisma
```

Controller 不直接：

- 查询 Prisma
- 拼接复杂 Prompt
- 调用模型
- 执行 Skill

这些都由 Service 或领域模块负责。

---

## 五、项目是否统一返回 `{ data }`？ {#kaj-h-297ab29c-60d5-4368-a540-5e502193242c}

项目里存在一个 `ResponseInterceptor`，它可以把结果包装成：

```text
{
  "data": {}
}
```

但是当前 `main.ts` 中没有看到它被注册为全局拦截器。

因此当前实际情况更接近：

```text
{
  "id": "...",
  "status": "completed"
}
```

而不是：

```text
{
  "data": {
    "id": "...",
    "status": "completed"
  }
}
```

前端的 `api()` 也直接执行：

```js
return response.json();
```

所以面试时不要笼统地说“所有接口统一返回 `{ data }` 包装”。更准确的说法是：

> 项目定义过统一响应拦截器，但当前主应用没有全局启用它，实际接口主要直接返回 Service 结果；错误则由 NestJS 异常机制转换为 JSON 错误响应。

---

## 六、可以直接用于面试的回答 {#kaj-h-ef84feea-11c8-414e-9cad-bb35f0c52cbe}

> HealthFlow 的后端接口基于 NestJS，整体采用 REST 风格的 HTTP API。普通业务接口使用 GET、POST、PATCH、DELETE，以 JSON 作为主要请求和响应格式，例如会话、健康记录、健康快照和辅助分诊。
> 
> 
> 
> Controller 主要负责路由映射、认证、参数接收和调用 Service，业务逻辑放在 Service 层。接口通过 `AuthGuard` 校验 Bearer Token，通过 `ValidationPipe`、DTO 和 Zod schema 做输入校验。
> 
> 
> 
> 项目还有几类特殊接口：文件上传使用 `multipart/form-data` 和 Multer 的 `FileInterceptor`；文件内容和头像通过 Node.js 文件流返回；聊天使用 `POST /conversations/:id/stream` 返回 `text/event-stream`，前端通过 `fetch + ReadableStream` 逐段读取，实现模型输出、RAG、Tool Calling 等事件的实时展示。
> 
> 
> 
> 辅助分诊没有使用 SSE，而是返回 JSON 诊断会话，前端通过 React Query 轮询 pending 状态。项目没有使用 GraphQL 或 WebSocket。
