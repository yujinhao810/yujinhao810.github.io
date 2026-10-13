import DefaultTheme from 'vitepress/theme'
import { h } from 'vue'
import ArticleMeta from './ArticleMeta.vue'
import './custom.css'

export default {
  extends: DefaultTheme,
  Layout: () => h(DefaultTheme.Layout, null, { 'doc-before': () => h(ArticleMeta) }),
}
