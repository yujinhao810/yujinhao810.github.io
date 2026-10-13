---
title: 技术文章
description: 按分类浏览所有技术文章
---

<script setup>
import ArticleList from './.vitepress/theme/ArticleList.vue'
import { categories } from './.vitepress/catalog'
import { withBase } from 'vitepress'
</script>

# 技术文章

前端、算法与 Agent 技术的学习记录。新增文章请参考[文章新增指南](/writing)。

## 按分类浏览

<ul>
  <li v-for="category in categories" :key="category.id">
    <a :href="withBase('/categories/' + category.id)">{{ category.title }}</a>
  </li>
</ul>

## 全部文章

<ArticleList />
