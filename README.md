# JynxHao

这是一个基于 VitePress 的简体中文技术博客，面向 GitHub Pages 用户站点部署。站点源码位于 `docs/`，构建产物位于 `docs/.vitepress/dist`。

## 本地开发

```bash
npm install
npm run docs:dev
```

打开终端输出的本地地址即可预览。正式构建：

```bash
npm run docs:build
npm run docs:preview
```

## 新增文章

复制 `docs/posts/_template.md` 到对应分类目录，填写 Frontmatter 和正文；文章总索引、分类列表、首页近期文章和侧边栏都会自动生成。新增文件后重启开发服务器刷新侧边栏。完整说明见[新增文章指南](docs/writing.md)。原博客迁移清单和验证结果见 [migration/README.md](migration/README.md)。

## GitHub Pages 首次部署

1. 你的 GitHub 主页是 `https://github.com/yujinhao810`。GitHub Pages 用户站点仓库名必须与 GitHub 账号完全一致：如果账号是 `yujinhao`，仓库应为 `yujinhao.github.io`；如果账号实际是 `yujinhao810`，仓库应为 `yujinhao810.github.io`。
2. 页面中的个人主页链接已更新为 `https://github.com/yujinhao810`。用户站点根路径不需要设置 `base`。
3. 初始化并推送 `main` 分支：

   ```bash
   git init
   git add .
   git commit -m "feat: initialize personal tech blog"
   git branch -M main
   # 如果实际 GitHub 账号是 yujinhao：
   git remote add origin https://github.com/yujinhao/yujinhao.github.io.git
   # 如果实际 GitHub 账号是 yujinhao810：
   # git remote add origin https://github.com/yujinhao810/yujinhao810.github.io.git
   git push -u origin main
   ```

4. 在仓库 Settings → Pages → Build and deployment 中选择 **GitHub Actions**。
5. 推送到 `main` 或在 Actions 页面手动运行 `Deploy VitePress site to GitHub Pages`，工作流会构建并发布 `docs/.vitepress/dist`。

工作流使用 GitHub Pages 官方 artifact 流程，权限仅包含读取内容、写入 Pages 和 OIDC 部署所需权限。不要提交 `.env`、令牌或 `node_modules`。

## 目录结构

```text
docs/
├─ .vitepress/      # VitePress 配置、主题和构建输出
├─ categories/      # 分类索引
├─ posts/           # 独立 Markdown 文章
├─ public/          # 静态资源
├─ about.md         # 关于我
├─ articles.md      # 文章总索引
└─ projects.md      # 项目实践模板
```
