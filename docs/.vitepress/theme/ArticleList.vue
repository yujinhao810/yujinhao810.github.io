<script setup lang="ts">
import { computed } from 'vue'
import { withBase } from 'vitepress'
import { data } from './posts.data'

const props = defineProps<{ category?: string }>()
const articles = computed(() => props.category ? data.filter(a => a.categoryId === props.category) : data)
</script>

<template>
  <p class="article-count">共 {{ articles.length }} 篇 · 按发布时间排序</p>
  <ul v-if="articles.length" class="catalog-list">
    <li v-for="article in articles" :key="article.url">
      <a :href="withBase(article.url)">{{ article.title }}</a>
      <p class="catalog-meta">
        <time :datetime="article.publishedAt">{{ article.date }}</time>
        <span v-if="!category">{{ article.category }}</span>
        <span v-if="article.tags.length">{{ article.tags.join(' · ') }}</span>
      </p>
      <p v-if="article.description" class="catalog-description">{{ article.description }}</p>
    </li>
  </ul>
  <p v-else>这个分类还没有文章。</p>
</template>

<style scoped>
.article-count { color: var(--vp-c-text-2); font-size: 13px; }
.catalog-list { list-style: none; padding: 0; }
.catalog-list li { margin: 0; padding: 18px 0; border-bottom: 1px solid var(--vp-c-divider); }
.catalog-list a { font-weight: 500; overflow-wrap: anywhere; }
.catalog-meta { display: flex; flex-wrap: wrap; gap: 4px 14px; margin: 6px 0 0; color: var(--vp-c-text-2); font-size: 12px; line-height: 1.8; }
.catalog-description { margin: 6px 0 0; color: var(--vp-c-text-2); font-size: 14px; line-height: 1.8; overflow-wrap: anywhere; }
</style>
