import { createContentLoader } from 'vitepress'
import { toArticles, type Article } from '../catalog'

export declare const data: Article[]
export default createContentLoader('posts/**/*.md', { transform: toArticles })
