import { createContentLoader } from 'vitepress'

interface Article {
  title: string
  url: string
  date: string
  category: string
}

interface Project {
  name: string
  url: string
  description: string
}

export declare const data: { articles: Article[]; projects: Project[] }

// VitePress watches these Markdown sources in dev and embeds the data at build time.
export default createContentLoader(['posts/**/*.md', 'projects.md'], {
  includeSrc: true,
  transform(pages) {
    const articles: Article[] = pages
      .filter((page) => page.url.startsWith('/posts/') && !page.url.includes('_template'))
      .map((page) => {
        const meta = page.frontmatter
        // Explicit update dates avoid unrelated Git commits changing editorial order.
        const rawDate = meta.updated ?? meta.date
        const date = rawDate instanceof Date
          ? rawDate.toISOString().slice(0, 10)
          : String(rawDate ?? '')
        if (!meta.title || !/^\d{4}-\d{2}-\d{2}$/.test(date) || Number.isNaN(Date.parse(date))) {
          throw new Error(`文章缺少有效的 title 或 date/updated：${page.url}`)
        }
        return {
          title: String(meta.title),
          url: page.url,
          date,
          category: Array.isArray(meta.tags) ? String(meta.tags[0] ?? '') : '',
        }
      })
      .sort((a, b) => b.date.localeCompare(a.date) || a.url.localeCompare(b.url))

    const source = pages.find((page) => page.url === '/projects')?.src
    if (!source) throw new Error('找不到项目实践页面')
    // Only the existing named project sections with real source links are featured.
    const projects: Project[] = source
      .split(/^## /m)
      .slice(1)
      .flatMap((section) => {
        const heading = section.split('\n')[0]
        const anchor = heading.match(/\{#([\w-]+)\}/)?.[1]
        const background = section.match(/\*\*项目背景：\*\*\s*([^\n]+)/)?.[1]
        const hasSource = /\*\*项目源码：\*\*\s*\[[^\]]+\]\(https:\/\/[^)]+\)/.test(section)
        if (!anchor || !background || !hasSource) return []
        return [{
          name: heading.replace(/\s*\{#[\w-]+\}/, '').split(' · ')[0],
          url: `/projects#${anchor}`,
          description: background.split(/[，。]/)[0] + '。',
        }]
      })
      .slice(0, 3)

    return { articles: articles.slice(0, 8), projects }
  },
})
