import { createContentLoader } from 'vitepress'
import { toArticles, type Article } from '../catalog'

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
    const articles = toArticles(pages)

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
