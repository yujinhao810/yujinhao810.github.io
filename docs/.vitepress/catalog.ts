export const categories = [
  { id: 'javascript', title: 'JavaScript / TypeScript' },
  { id: 'vue', title: 'Vue / 前端工程化' },
  { id: 'algorithm', title: '算法与数据结构' },
  { id: 'node', title: 'Node.js / NestJS' },
  { id: 'ai-agent', title: 'AI Agent / RAG / MCP' },
  { id: 'project', title: '项目实践' },
  { id: 'notes', title: '学习与随笔' },
] as const

export interface Article {
  title: string
  url: string
  date: string
  publishedAt: string
  categoryId: string
  category: string
  description: string
  tags: string[]
  sortTime: number
}

function dateString(value: unknown): string {
  return value instanceof Date ? value.toISOString() : String(value ?? '')
}

// 按完整发布时间倒序排列；旧文更新不改变发布顺序，同一时间以网址稳定排序。
export function toArticles(pages: { url: string; frontmatter: Record<string, any> }[]): Article[] {
  return pages.filter(p => p.url.startsWith('/posts/') && !p.url.includes('_template')).map(page => {
    const meta = page.frontmatter
    const date = dateString(meta.date).slice(0, 10)
    const publishedAt = dateString(meta.publishedAt || meta.date)
    const categoryId = page.url.split('/')[2]
    const category = categories.find(c => c.id === categoryId)
    const sortTime = Date.parse(publishedAt)
    if (!meta.title || !category || !/^\d{4}-\d{2}-\d{2}$/.test(date) || Number.isNaN(sortTime)) {
      throw new Error(`文章元数据无效：${page.url}`)
    }
    return {
      title: String(meta.title), url: page.url, date, publishedAt, categoryId,
      category: category.title, description: String(meta.description ?? ''),
      tags: Array.isArray(meta.tags) ? meta.tags.map(String) : [], sortTime,
    }
  }).sort((a, b) => b.sortTime - a.sortTime || a.url.localeCompare(b.url))
}
