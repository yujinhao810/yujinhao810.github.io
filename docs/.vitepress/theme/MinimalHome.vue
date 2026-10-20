<script setup lang="ts">
import { withBase } from 'vitepress'
import { data } from './home.data'

const categories = [
  { label: '前端八股', url: '/categories/javascript' },
  { label: '计算机网络', url: '/categories/network' },
  { label: '算法', url: '/categories/algorithm' },
  { label: 'Agent', url: '/categories/ai-agent' },
]
</script>

<template>
  <div class="minimal-home">
    <header class="profile-header" aria-labelledby="profile-heading">
      <img class="profile-avatar" :src="withBase('/avatar.png')" alt="Jinhao Yu 的考拉头像" width="64" height="64" />
      <div class="profile-copy">
        <h1 id="profile-heading">Jinhao Yu <span lang="zh-CN">俞金浩</span></h1>
        <p class="profile-motto">记录代码，也记录思考</p>
        <p class="profile-intro" lang="en">Exploring frontend fundamentals, algorithms, and AI agents.</p>
        <div class="profile-education" lang="en" aria-label="Education">
          <p>Master’s student · Hangzhou Normal University</p>
          <p>Bachelor’s · Ningbo University of Technology</p>
        </div>
      </div>
    </header>

    <section aria-labelledby="recent-heading" class="home-section">
      <div class="section-heading">
        <h2 id="recent-heading">近期文章</h2>
        <nav class="topic-nav" aria-label="文章专题">
          <a v-for="category in categories" :key="category.url" :href="withBase(category.url)">{{ category.label }}</a>
        </nav>
      </div>
      <ul v-if="data.articles.length" class="article-list">
        <li v-for="article in data.articles" :key="article.url">
          <a :href="withBase(article.url)" class="article-link">{{ article.title }}</a>
          <div class="article-meta">
            <time :datetime="article.date">{{ article.date }}</time>
            <span v-if="article.tags.length">{{ article.tags[0] }}</span>
          </div>
        </li>
      </ul>
      <p v-else class="home-empty">文章整理中。</p>
      <a class="all-articles" :href="withBase('/articles')">查看全部文章 <span aria-hidden="true">→</span></a>
    </section>

    <section v-if="data.projects.length" aria-labelledby="projects-heading" class="home-section">
      <h2 id="projects-heading">代表项目</h2>
      <ul class="project-list">
        <li v-for="project in data.projects" :key="project.url">
          <a :href="withBase(project.url)">{{ project.name }}</a>
          <p>{{ project.description }}</p>
        </li>
      </ul>
    </section>
  </div>
</template>

<style scoped>
.minimal-home {
  width: calc(100% - 48px);
  max-width: 760px;
  margin: 0 auto;
  padding: 32px 0 64px;
  color: var(--vp-c-text-1);
}
.profile-header {
  display: flex;
  align-items: flex-start;
  gap: 20px;
  padding-bottom: 28px;
  margin-bottom: 28px;
  border-bottom: 1px solid var(--vp-c-divider);
}
.profile-avatar { flex-shrink: 0; width: 64px; height: 64px; object-fit: cover; border-radius: 50%; border: 1px solid var(--vp-c-divider); background: #fff; }
.profile-copy { min-width: 0; }
.profile-copy h1 { margin: 0; font-size: 23px; font-weight: 600; line-height: 1.5; letter-spacing: -.02em; }
.profile-copy h1 span { margin-left: 8px; font-size: 17px; font-weight: 400; color: var(--vp-c-text-2); }
.profile-motto { margin: 4px 0 12px; font-size: 13px; color: var(--vp-c-text-2); }
.profile-intro { margin: 0 0 8px; font-size: 13px; line-height: 1.8; color: var(--vp-c-text-2); }
.profile-education { font-size: 12px; line-height: 1.8; color: var(--vp-c-text-2); }
.profile-education p { margin: 0; }
.section-heading { display: flex; align-items: baseline; justify-content: space-between; flex-wrap: wrap; gap: 12px 24px; margin-bottom: 8px; }
.home-section h2 { margin: 0 0 16px; font-size: 16px; font-weight: 600; line-height: 1.5; }
.section-heading h2 { margin: 0; }
.topic-nav { display: flex; flex-wrap: wrap; gap: 18px; font-size: 12px; line-height: 1.8; }
.topic-nav a { color: var(--vp-c-text-2); }
.home-section + .home-section { margin-top: 36px; }
ul { margin: 0; padding: 0; list-style: none; }
.article-list li {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  align-items: baseline;
  column-gap: 24px;
  padding: 16px 0;
  border-bottom: 1px solid var(--vp-c-divider);
}
a { color: var(--vp-c-text-1); text-decoration: none; text-underline-offset: 4px; overflow-wrap: anywhere; }
a:hover { color: var(--vp-c-brand-1); text-decoration: underline; }
a:focus-visible { outline: 2px solid var(--vp-c-brand-1); outline-offset: 5px; border-radius: 2px; }
.article-link { font-size: 15px; font-weight: 500; line-height: 1.75; }
.article-meta { display: flex; gap: 12px; color: var(--vp-c-text-2); font-size: 12px; line-height: 1.75; white-space: nowrap; font-variant-numeric: tabular-nums; }
.all-articles { display: inline-block; margin-top: 18px; font-size: 13px; color: var(--vp-c-text-2); line-height: 1.8; }
.project-list { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 24px; }
.project-list a { font-size: 14px; font-weight: 500; line-height: 1.75; }
.project-list p { margin: 6px 0 0; color: var(--vp-c-text-2); font-size: 13px; line-height: 1.85; }
.home-empty { color: var(--vp-c-text-2); font-size: 14px; }
@media (max-width: 639px) {
  .minimal-home { padding: 24px 0 40px; }
  .profile-header { gap: 14px; padding-bottom: 24px; margin-bottom: 24px; }
  .profile-avatar { width: 48px; height: 48px; }
  .profile-copy h1 { font-size: 20px; }
  .profile-copy h1 span { display: block; margin-left: 0; font-size: 14px; }
  .project-list { grid-template-columns: 1fr; gap: 16px; }
  .article-list li { grid-template-columns: 1fr; row-gap: 4px; padding: 14px 0; }
  .home-section + .home-section { margin-top: 28px; }
}
@media (min-width: 640px) {
  .minimal-home { width: calc(100% - 96px); }
}
</style>
