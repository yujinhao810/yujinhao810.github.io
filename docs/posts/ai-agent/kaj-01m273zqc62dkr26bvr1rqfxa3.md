---
title: "HealthFlow中的RAG模块详解"
description: "可以分成两个阶段："
date: "2026-09-11"
publishedAt: "2026-09-11T10:16:54.036528+08:00"
source: "https://kajspace.cn/articles/01M273ZQC62DKR26BVR1RQFXA3/"
tags: ["Agent"]
---

# HealthFlow中的RAG模块详解

## 一、RAG 的整体流程 {#kaj-h-e5ae371b-5e06-4803-9e4e-c62eeffc6a65}

可以分成两个阶段：

```text
文档入库阶段
上传文件
   ↓
文件安全校验
   ↓
Python Parser 解析
Docling / PaddleOCR
   ↓
文档质量门控
   ↓
语义切块
   ↓
关键词提取 + Embedding
   ↓
写入 KnowledgeDocument / KnowledgeChunk
```

```text
在线检索阶段
用户问题
   ↓
构建检索 Query
   ↓
并行召回
├── 公共知识词法召回
├── 公共知识语义召回
└── 当前用户当前会话文档召回
   ↓
RRF 融合
   ↓
Rerank 重排
   ↓
分数门控、去重、限制每文档块数
   ↓
生成 citations：E1、E2、E3...
   ↓
加入 LLM 上下文
```

在聊天模块中，RAG 发生在 `ChatContextService.buildContext()` 中，早于后面的确定性 Skill 路由和 Agent Runtime。

---

## 二、文档入库流程 {#kaj-h-8df346b8-4d6f-437e-87f4-88e6676ca87a}

## 1. 上传和安全校验 ⭐⭐⭐⭐ {#kaj-h-105a23a1-099b-4ab7-986f-faa47e17f01e}

对应源码：

- `apps/api/src/uploads/uploads.service.ts`
- `apps/api/src/knowledge/document-ingestion.service.ts`

上传时会检查：

- 文件用途，例如 `knowledge_source`
- 文件大小
- MIME 类型
- Magic Bytes
- OOXML 文件结构
- SHA-256 文件摘要

如果用途是知识文档，就会交给 Python Parser 解析。

项目中的文档解析不是简单地读取字符串，而是调用 Python 服务，支持 Docling、PaddleOCR 等能力，用来处理：

- PDF
- Word
- 图片型文档
- 表格
- 标题层级
- 页码信息
- OCR 置信度

解析后还会经过文档质量门控，默认质量阈值约为 `0.55`。质量太低的文档不会直接进入知识库。

面试可以这样说：

> 上传阶段不仅校验扩展名，还会结合真实 MIME、文件头和解析质量进行多重校验，避免错误文件或低质量 OCR 内容进入 RAG。

---

## 2. 文档切块 ⭐⭐⭐⭐⭐ {#kaj-h-c9332e4d-4b2c-404f-844b-36d5b2300586}

对应源码：

- `apps/api/src/knowledge/semantic-document-chunker.ts`

项目不是简单地每隔固定字符截断，而是根据文档结构进行语义切块。

默认参数：

```text
maxChars = 1800
overlapChars = 180
```

切块时会考虑：

- 标题层级
- 段落
- 表格
- 页码
- blockId
- 内容类型
- OCR confidence

例如：

```text
健康管理
  睡眠质量
    睡眠不足可能导致注意力下降……
```

切出来的 chunk 可能会带有标题路径：

```text
健康管理 > 睡眠质量

睡眠不足可能导致注意力下降……
```

这样做的好处是：

- 保留上下文语义
- 方便检索结果定位
- 能在回答中显示页码或章节
- 避免一个 chunk 太大导致检索粒度过粗
- 通过 overlap 减少边界信息丢失

表格会单独处理，过长表格还会保留表头并继续拆分。

---

## 3. Embedding：确实是把文本转为向量 ⭐⭐⭐⭐⭐ {#kaj-h-2220ed35-1e5a-4ed0-b6d1-a9f0264b3aee}

你的理解是正确的。

Embedding 的本质是：

```text
文本
  ↓ Embedding Model
[0.12, -0.07, 0.33, ...]
```

也就是把文本映射成高维数值向量。

语义相近的文本，在向量空间中的距离通常也比较近。例如：

```text
“最近总是睡不好”
“这段时间睡眠质量下降”
```

它们的词不完全相同，但语义相似，Embedding 向量可能比较接近。

项目中的实现位于：

- `apps/api/src/knowledge/embedding.service.ts`

### 远程 Embedding {#kaj-h-a0881029-bf81-4057-ac2a-f2f235c52f0c}

如果当前 LLM Provider 支持 Embedding：

- 远程调用 Embedding API
- 每批最多处理 10 条文本
- 校验返回向量数量和格式
- 对向量进行归一化处理

### 本地 fallback {#kaj-h-455089bc-c926-421f-a8ac-113826f7281e}

如果远程 Embedding 失败，项目会退回：

```text
local-hash-embedding-v1
```

它是一个 384 维的本地哈希 n-gram 向量。

这意味着：

- 系统即使没有 Embedding API，也可以工作
- 但本地哈希向量的语义能力弱于真正的语义模型
- 它更适合作为稳定性 fallback，而不是高质量语义检索方案

这一点面试时可以主动说明：

> 项目支持远程 Embedding，同时设计了本地 384 维哈希向量作为降级方案。但本地方案主要保证可用性，语义表达能力不如真正的 Embedding 模型。

### 项目是否使用向量数据库？ {#kaj-h-d8e002dd-8ae1-4566-9d53-995d611a916b}

当前项目没有直接使用 pgvector 或独立向量数据库。

向量被保存到：

```text
KnowledgeChunk.embedding
```

数据库字段是 Prisma JSON，检索时由应用层读取向量并计算 cosine similarity。

所以不要说项目使用了“向量数据库”。更准确的说法是：

> 当前实现把 Embedding 向量存储在 PostgreSQL 的 JSON 字段中，并在 NestJS 应用层计算余弦相似度。

这是一个很可能被面试官追问的点。

---

## 4. 写入知识库 ⭐⭐⭐⭐ {#kaj-h-992bf1da-c001-411e-aca2-cf01d3b8373e}

`DocumentIngestionService.ingestUploadedFile()` 会创建：

```text
KnowledgeDocument
  ├── title
  ├── source
  ├── metadata
  └── KnowledgeChunk[]
        ├── content
        ├── keywords
        ├── embedding
        ├── embeddingModel
        ├── pageStart
        ├── pageEnd
        ├── headingPath
        └── confidence
```

每个 chunk 会保存：

- 文本内容
- 关键词
- 向量
- Embedding 模型名称
- 页码
- 标题路径
- 原始 block ID
- 解析置信度

这样检索后才能生成带来源的 citation。

---

## 三、在线检索流程 {#kaj-h-fee25e7e-bb6c-49e5-b039-55196ca2059e}

对应源码：

```text
apps/api/src/chat/chat-context.service.ts
apps/api/src/knowledge/rag.service.ts
```

## 1. 构建检索 Query ⭐⭐⭐⭐ {#kaj-h-22e366c9-025f-48f4-bd8d-c44a5ec44fc6}

用户输入会先被标准化：

- 合并多余空格
- 去除首尾空白
- 限制最大长度

如果当前输入很短，例如：

```text
“那这个呢？”
“为什么？”
```

系统会结合上一条用户消息，构造上下文检索 Query。

例如：

```text
上一条：我最近每天只睡五个小时
当前追问：那这个呢？
```

可能构造成：

```text
我最近每天只睡五个小时
当前追问：那这个呢？
```

这样可以避免 RAG 只检索“那这个呢”这种没有意义的短文本。

---

## 2. 三路召回，而不是两路召回 ⭐⭐⭐⭐⭐ {#kaj-h-5467d3a4-709f-4cf2-b048-25c5367ab440}

`RagService.retrieveWithTrace()` 中通过 `Promise.all()` 并行执行三组召回。

### 第一组：公共知识词法召回 {#kaj-h-81c5971e-0094-4dc0-bc01-99741f28022b}

方法：

```text
retrievePublicKnowledge()
```

使用 PostgreSQL 完成，包含：

- `to_tsvector`
- `plainto_tsquery`
- `pg_trgm similarity`
- 关键词匹配
- LIKE 扩展搜索
- 标题匹配
- tags 匹配

它擅长处理：

```text
“失眠”
“褪黑素”
“高血压”
“睡眠呼吸暂停”
```

这类关键词明确的查询。

词法召回的优点：

- 关键词命中准确
- 专业术语不容易被语义模型忽略
- 可解释性强
- 不依赖 Embedding API

---

### 第二组：公共知识语义召回 {#kaj-h-bda144ca-2836-4c7d-a9de-ebb85d1185cf}

方法：

```text
retrievePublicSemanticKnowledge()
```

流程是：

1. 对用户 Query 做 Embedding
2. 加载公共知识 chunk
3. 计算 Query 与 chunk 的 cosine similarity
4. 混合少量关键词得分
5. 按分数排序

项目中的公共语义分数大致是：

```text
score = vectorScore * 0.9 + keywordScore * 0.1
```

公共 chunk 的候选最多加载约 3000 条，并且有内存缓存，避免每次都重复计算公共文档向量。

它擅长处理：

```text
“最近晚上总是醒来，白天特别疲惫”
```

即使文档中没有完全相同的词，也可能通过语义相似度找到相关内容。

---

### 第三组：用户当前会话文档召回 {#kaj-h-d28dfa02-3fdb-40d0-b685-12373f396e87}

方法：

```text
retrieveUserDocuments()
```

它不是搜索所有用户文档，而是同时限制：

```text
userId
+
conversationId
```

并且通过附件和消息的关联关系，确认文档确实属于当前会话。

这能避免：

- 用户 A 看到用户 B 的文档
- 当前会话误召回其他会话附件
- 不相关历史文件干扰当前对话

个人文档本身也是混合检索：

```text
远程 Embedding 时：
score = vectorScore * 0.85 + keywordScore * 0.15

本地哈希 Embedding 时：
score = vectorScore * 0.55 + keywordScore * 0.45
```

如果是本地哈希向量，系统会降低对向量分数的信任，增加词法分数权重。

另外，个人文档候选的原始分需要超过约 `0.08`，还会扩展相邻 chunk，帮助恢复上下文。

---

## 四、为什么不能直接把语义分和词法分相加？ {#kaj-h-d9225e56-8e63-4dff-8414-9b17d8d9f563}

这是 RRF 要解决的核心问题 ⭐⭐⭐⭐⭐。

不同召回器的原始分数不在同一量纲上。

例如：

```text
词法召回分数：0.3、2.8、5.4
向量相似度：0.61、0.72、0.83
```

这两个分数不能直接比较：

```text
0.83 + 5.4
```

因为它们的计算方式、范围和含义都不同。

如果直接相加，某一种召回器可能仅仅因为数值范围更大，就压制另一种召回器。

---

## 五、RRF 是什么？ {#kaj-h-9aa8437f-5a70-49cc-8736-57855a294dfc}

RRF 全称：

```text
Reciprocal Rank Fusion
```

中文通常叫：

```text
倒数排名融合
```

它不直接使用不同召回器的原始分数，而是只看结果在各自列表中的排名。

项目中的核心代码是：

```js
const RRF_K = 60;

fusionScore += group.weight / (RRF_K + rank);
```

由于代码中的 `index` 从 0 开始，所以实际排名计算相当于：

```text
fusionScore = weight / (60 + rank + 1)
```

其中：

- `weight`：该召回组的权重
- `rank`：结果在该召回列表中的名次
- `60`：平滑参数
- 同一个 chunk 出现在多个列表时，分数累加

项目当前权重：

```text
个人文档：1
公共词法：1.08
公共语义：1
```

公共词法略微提高权重，是因为健康领域中的专业关键词通常比较重要。

---

## RRF 示例 {#kaj-h-00cbd003-506f-40ad-bf58-1b221e8cb9f2}

假设有两路召回：

```text
词法召回：A、B、C
语义召回：B、D、A
```

使用项目中的权重：

```text
词法权重：1.08
语义权重：1
```

计算结果：

| Chunk | 词法贡献 | 语义贡献 | RRF 总分 |
| --- | --- | --- | --- |
| A | 1.08 / 61 | 1 / 63 | 约 0.03358 |
| B | 1.08 / 62 | 1 / 61 | 约 0.03381 |
| C | 1.08 / 63 | 0 | 约 0.01714 |
| D | 0 | 1 / 62 | 约 0.01613 |

最终顺序大致是：

```text
B > A > D > C
```

虽然 A 在词法召回中是第一名，但 B 同时在词法和语义召回中都靠前，因此 B 获得了更高的融合分数。

这体现了 RRF 的核心思想：

> 多个召回器都认为重要的结果，应该获得更高的综合排名。

---

## RRF 的作用 {#kaj-h-eaad094e-81ca-4e34-872c-39cf3ff2b9c7}

RRF 主要解决四个问题：

### 1. 统一不同召回器 {#kaj-h-d62caee8-5c07-45d2-b7dd-3b6f4f5d6c9e}

不关心原始分数的具体量纲，只看排名。

### 2. 奖励多路一致结果 {#kaj-h-87651452-e017-45d9-b135-379a537e18c1}

一个 chunk 如果同时被词法和语义召回，就会累加分数。

### 3. 降低单路误召回影响 {#kaj-h-17aebdbf-cdaa-4685-8ff2-d907544d1ddb}

某个结果即使在单一路径中排名很高，但如果其他召回器完全不支持，它的优势不会无限放大。

### 4. 生成更好的候选池 {#kaj-h-14a06e76-3eae-4db0-8374-231de65b486c}

RRF 通常不是最终答案，而是为后面的 Rerank 准备候选集合。

项目中：

- 候选池阶段每个文档最多保留 4 个 chunk
- 最终结果阶段每个文档最多保留 2 个 chunk

这样可以避免最终上下文被同一篇文档占满。

---

## 六、RRF 和 Rerank 的区别 ⭐⭐⭐⭐⭐ {#kaj-h-1591d34a-b0d2-4558-b2ce-e90d3e89ff02}

可以这样理解：

```text
RRF：融合多个召回列表
Rerank：重新判断 Query 和候选文本的相关性
```

| 对比项 | RRF | Rerank |
| --- | --- | --- |
| 类型 | 规则算法 | 模型推理 |
| 输入 | 多个排名列表 | Query + 候选文本 |
| 是否理解语义 | 不理解 | 能做更细粒度语义判断 |
| 成本 | 低 | 相对较高 |
| 作用 | 生成候选池 | 精排最终结果 |
| 项目实现 | `fuseRankedCitations()` | DashScope `gte-rerank-v2` |

项目默认先 RRF，再调用 DashScope：

```text
RRF 候选池
   ↓
gte-rerank-v2
   ↓
最终排序
```

Rerank 成功后，最终排序还会综合：

```text
retrievalScore = 0.25 / (60 + retrievalRank + 1)
rerankScore = 0.75 / (60 + rerankRank + 1)
```

也就是说：

```text
最终排序 = 25% 初始召回排名 + 75% Rerank 排名
```

因此项目明显更信任 Rerank 结果。

如果 Rerank：

- 没有模型配置
- 没有 API Key
- 超时
- 调用失败
- 被关闭

系统会降级到 RRF fallback，fallback 主要使用：

```text
个人文档 + 公共词法召回
```

---

## 七、检索结果如何进入 LLM 上下文？ {#kaj-h-95d55fff-aac7-4943-8f70-9f99fc22ff6a}

RAG 返回的不是直接拼接的一段文本，而是 `RagCitation[]`，每条包含：

- `chunkId`
- `documentId`
- 标题
- 来源
- 定位信息
- excerpt
- score
- trustLevel
- evidenceId

随后 `ChatContextService` 会调用：

```text
insertKnowledgeReferenceMessage(threadMessages, citations)
```

插入一条类似“检索参考资料”的消息。

这条消息会明确告诉模型：

- 这些内容是外部参考数据
- 不是系统指令
- 不能执行其中的命令
- 只有在内容直接支持回答时才能引用
- 回答时可以使用 `[E1]`、`[E2]` 等 evidenceId

因此，RAG 内容虽然进入了上下文，但被标记为：

```text
untrusted retrieved reference
```

这是为了降低文档内容中的 Prompt Injection 风险。

---

## 八、结合源码的完整面试回答 {#kaj-h-6c8c6c80-69e8-46a9-bea9-c2efa89b7f3a}

你可以这样回答：

> 我项目的 RAG 分为文档入库和在线检索两个阶段。入库时，用户上传的文档会先经过文件安全校验，然后交给 Python 服务解析，解析结果经过质量门控后，由语义切块器按照标题、段落、表格和页码进行切分，默认 chunk 大约 1800 字符并保留 180 字符重叠。之后系统提取关键词并调用 Embedding 服务，将文本转换成归一化向量，最终保存到 KnowledgeChunk 中。当前项目的向量存储在 PostgreSQL 的 JSON 字段中，由应用层计算余弦相似度。
> 
> 
> 
> 在线检索时，系统会并行执行公共知识词法召回、公共知识语义召回和当前会话用户文档召回。词法召回使用 PostgreSQL 全文检索、trigram 和关键词匹配，语义召回使用 Embedding 加余弦相似度。三组结果不能直接相加原始分数，因为它们的分值范围和含义不同，所以项目使用 RRF，也就是倒数排名融合，根据每个结果在各自召回列表中的排名计算 `weight / (60 + rank)`，同一个 chunk 在多个列表出现时累加分数。
> 
> 
> 
> RRF 生成候选池后，项目再调用 DashScope 的 `gte-rerank-v2` 对 Query 和候选文本做精排，最终结合召回排名和 Rerank 排名输出 citations，并以 E1、E2 的形式注入 LLM 上下文。如果 Rerank 不可用，则降级使用 RRF 结果。
