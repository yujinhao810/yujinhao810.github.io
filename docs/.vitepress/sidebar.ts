import { existsSync, readFileSync, readdirSync } from 'node:fs'
import { resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createMarkdownRenderer } from 'vitepress'
import { categories, toArticles } from './catalog'

export async function loadSidebar() {
  const docs = fileURLToPath(new URL('../', import.meta.url))
  const md = await createMarkdownRenderer(docs)
  const pages = categories.flatMap(category => {
    const dir = resolve(docs, 'posts', category.id)
    if (!existsSync(dir)) return []
    const files = readdirSync(dir)
    return files.filter(file => file.endsWith('.md') && !file.startsWith('_')).map(file => {
      const source = readFileSync(resolve(dir, file), 'utf8').replace(/^\uFEFF/, '')
      const frontmatterBlock = source.match(/^---\r?\n[\s\S]*?\r?\n---/)?.[0]
      if (!frontmatterBlock) throw new Error(`文章缺少 Frontmatter：${file}`)
      const env: { frontmatter?: Record<string, any> } = {}
      // Reuse VitePress's YAML parser without rendering article code blocks.
      md.render(frontmatterBlock, env)
      return { url: `/posts/${category.id}/${file.slice(0, -3)}`, frontmatter: env.frontmatter ?? {} }
    })
  })
  const articles = toArticles(pages)
  return categories.map(category => ({
    text: category.title,
    collapsed: true,
    items: articles.filter(a => a.categoryId === category.id).map(a => ({ text: a.title, link: a.url })),
  })).filter(group => group.items.length)
}
