<script setup lang="ts">
import { computed } from 'vue'
import { useData } from 'vitepress'
const { page, frontmatter } = useData()
const isArticle = computed(() => page.value.relativePath.startsWith('posts/'))
const date = computed(() => {
  const raw = frontmatter.value.publishedAt || frontmatter.value.date
  return typeof raw === 'string' ? raw : raw instanceof Date ? raw.toISOString() : ''
})
const label = computed(() => {
  if (!date.value.includes('T')) return date.value
  return date.value.slice(0, 19).replace('T', ' ') + (date.value.endsWith('+08:00') ? '（UTC+08:00）' : '')
})
</script>

<template>
  <p v-if="isArticle && date" class="article-publication">
    发布于 <time :datetime="date">{{ label }}</time>
  </p>
</template>

<style scoped>
.article-publication { margin: 0 0 20px; color: var(--vp-c-text-2); font-size: 12px; line-height: 1.8; }
</style>
