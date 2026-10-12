import { defineConfig } from 'vitepress'

const sidebar = [
  {
    text: 'JavaScript / TypeScript',
    collapsed: false,
    items: [{ text: 'Promise 与 async/await', link: '/posts/javascript/promise-async' }],
  },
  {
    text: 'Vue / 前端工程化',
    collapsed: false,
    items: [{ text: 'Vue 3 Composition API 实践', link: '/posts/vue/composition-api' }],
  },
  {
    text: '算法与数据结构',
    collapsed: false,
    items: [{ text: '滑动窗口：无重复字符的最长子串', link: '/posts/algorithm/longest-substring' }],
  },
  {
    text: 'Node.js / NestJS',
    collapsed: false,
    items: [{ text: 'Node.js 事件循环与 I/O', link: '/posts/node/event-loop' }],
  },
  {
    text: 'AI Agent / RAG / MCP',
    collapsed: false,
    items: [{ text: '从 Tool Calling 到 MCP', link: '/posts/ai-agent/tool-calling-mcp' }],
  },
  {
    text: '项目实践',
    collapsed: false,
    items: [{ text: '流式输出的前端设计', link: '/posts/project/streaming-ui' }],
  },
]

export default defineConfig({
  lang: 'zh-CN',
  title: '个人技术博客',
  description: '记录前端、工程化与 AI Agent 的学习与实践。',
  cleanUrls: true,
  srcExclude: ['**/_template.md'],
  lastUpdated: true,
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: '首页', link: '/' },
      { text: '技术文章', link: '/articles' },
      { text: '算法题解', link: '/categories/algorithm' },
      { text: 'AI Agent', link: '/categories/ai-agent' },
      { text: '项目实践', link: '/projects' },
      { text: '关于我', link: '/about' },
    ],
    sidebar,
    search: { provider: 'local' },
    outline: { level: [2, 3], label: '本页目录' },
    docFooter: { prev: '上一篇', next: '下一篇' },
    lastUpdatedText: '最近更新',
    footer: { message: '保持好奇，持续交付。', copyright: 'Copyright © 2026 · Personal Tech Blog' },
    editLink: {
      pattern: 'https://github.com/yujinhao810/yujinhao.github.io/edit/main/docs/:path',
      text: '在 GitHub 上编辑此页',
    },
  },
})
