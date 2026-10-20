---
title: 新增文章指南
description: 复制模板并发布一篇新的技术文章
---

# 新增文章指南

## 1. 复制模板

复制 `docs/posts/_template.md` 到对应分类目录，例如 `docs/posts/javascript/my-topic.md`。文件名只使用小写英文和短横线，确保链接稳定。

## 2. 填写 Frontmatter

```yaml
---
title: 文章标题
description: 一句话说明文章解决的问题
date: "2026-03-10"
publishedAt: "2026-03-10T10:00:00+08:00"
tags:
  - JavaScript
  - 学习笔记
---
```

`date` 使用 `YYYY-MM-DD`，表示首次发布日期。新文章填写 `publishedAt`，保存实际发布时间与时区，例如 `publishedAt: "2026-10-14T16:40:58+08:00"`，确保同一天的文章也能按发布先后排序。复制模板后替换示例日期和时间。迁移文章保留原站完整时间，不要将迁移当天作为发布日期。修改旧文时可添加 `updated`，不覆盖 `date` 和 `publishedAt`。

文章索引、分类页、首页和侧边栏都从 Markdown 元数据生成，无需手动添加链接。默认由目录决定分类，也可以在 Frontmatter 中填写 `category: network`，将文章归入“计算机网络”等栏目而不改变原有网址。分类标识与名称集中在 `docs/.vitepress/catalog.ts`；计算机网络新文章可放在 `docs/posts/network/`，其他学习记录可放在 `docs/posts/notes/`。新增栏目时，在该配置中添加分类，并创建对应的 `docs/categories/<分类标识>.md` 索引页。新增文件后重启开发服务器刷新侧边栏，正式构建会重新生成全部导航。页面底部的文章导航使用完整标题，与正文标题保持一致。

力扣题解的 `title` 和正文一级标题统一使用 `题号. 题目名称`，例如 `384. 打乱数组`。LCR 系列保留题号前缀，例如 `LCR 126. 斐波那契数`；一篇文章讨论多道题时，各题用 ` + ` 连接。

首页无需添加文章链接：它会自动读取 `docs/posts/` 下的 Markdown 元数据，按 `publishedAt` 倒序排列，在“近期文章”中展示最新发布的 8 篇文章。文章列表、分类页和侧边栏使用相同规则。缺少完整时间的旧文章回退到 `date`；发布时间完全相同时，按网址稳定排序。`updated` 仅记录修改日期，不影响发布顺序。模板不会出现在首页。

首页代表项目直接读取 `docs/projects.md`：保留项目二级标题中的 `{#项目锚点}`、`**项目背景：**` 和 `**项目源码：**` 字段即可。首页显示背景的第一个短句，链接到原项目详情，不需要另写首页项目数据。

## 3. 本地检查

```bash
npm run docs:dev
npm run docs:build
```

提交前检查链接、代码示例和暗色模式下的对比度。文章不需要手动添加目录，VitePress 会根据标题自动生成。

## 4. 原博客迁移

原站文章对应关系和完整发布时间保存在 `migration/kajspace-manifest.json`，迁移过程见 `migration/README.md`。`source` 字段仅保留迁移来源记录，页面顶部显示发布时间。导入文章文件名采用原站永久 ID，避免同名文章相互覆盖；已有文章网址保持不变。
