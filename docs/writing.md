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
date: 2026-03-10
tags:
  - JavaScript
  - 学习笔记
---
```

日期使用 `YYYY-MM-DD`。文章索引目前集中维护在 `docs/articles.md`，新增后按日期降序加一行，并在需要时更新 `docs/.vitepress/config.ts` 的侧边栏。

首页无需添加文章链接：它会自动读取 `docs/posts/` 下的 Markdown 元数据，按 `updated`（没有时使用 `date`）倒序排列，在“近期文章”中展示最新的 8 篇文章。更新旧文时可添加 `updated: 2026-10-12`，日期格式同样为 `YYYY-MM-DD`。模板不会出现在首页。

首页代表项目直接读取 `docs/projects.md`：保留项目二级标题中的 `{#项目锚点}`、`**项目背景：**` 和 `**项目源码：**` 字段即可。首页显示背景的第一个短句，链接到原项目详情，不需要另写首页项目数据。

## 3. 本地检查

```bash
npm run docs:dev
npm run docs:build
```

提交前检查链接、代码示例和暗色模式下的对比度。文章不需要手动添加目录，VitePress 会根据标题自动生成。
