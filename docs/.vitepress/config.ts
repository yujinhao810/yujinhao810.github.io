import { defineConfig } from 'vitepress'
import { loadSidebar } from './sidebar'

export default defineConfig(async () => ({
  lang: 'zh-CN',
  title: 'JynxHao',
  description: '前端八股、算法与 Agent 技术的学习与实践。',
  head: [['link', { rel: 'icon', type: 'image/png', href: '/avatar.png' }]],
  cleanUrls: true,
  srcExclude: ['**/_template.md'],
  lastUpdated: true,
  transformPageData(pageData) {
    // 信息页不参与文章翻页，避免共享侧边栏生成无关的“下一篇”。
    if (!pageData.relativePath.startsWith('posts/')) {
      pageData.frontmatter.prev = false
      pageData.frontmatter.next = false
    }
  },
  themeConfig: {
    logo: { src: '/avatar.png', alt: 'JynxHao 头像' },
    nav: [
      { text: '首页', link: '/' },
      { text: '技术文章', link: '/articles' },
      { text: '算法题解', link: '/categories/algorithm' },
      { text: 'AI Agent', link: '/categories/ai-agent' },
      { text: '项目实践', link: '/projects' },
      { text: '关于我', link: '/about' },
    ],
    sidebar: await loadSidebar(),
    search: { provider: 'local' },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdatedText: '最近更新',
    footer: { message: '保持好奇，持续交付。', copyright: 'Copyright © 2026 · JynxHao' },
  },
}))
