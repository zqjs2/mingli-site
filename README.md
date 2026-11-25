# 明理斋 · 易学与命理笔记

知识库 + 博客站点，MkDocs + MaterialX。

## 日常只用三条命令

```powershell
cd G:\mingli-site
python -m mkdocs serve      # 本地预览 http://127.0.0.1:8000 ，改文件自动刷新
python -m mkdocs build      # 生成静态站点到 site\
```

## 写一篇普通文章

1. 在对应目录新建 `.md`，例如 `docs\bazi\十神详解.md`
2. 文件第一行到第三行可以加标题（`# 标题`）
3. 在 `mkdocs.yml` 的 `nav:` 里加一行 `- 十神详解: bazi/十神详解.md`（不加也能访问，只是侧边栏看不到）

## 写一篇博客（带日期、分类、标签）

在 `docs\blog\posts\` 新建文件，例如 `2026-12-01-十神初探.md`：

```markdown
---
date: 2026-12-01
categories:
  - 八字
tags:
  - 十神
  - 学习笔记
---

# 十神初探

正文……
```

博客列表、分类页、归档页、RSS 都不用手写，插件自动生成。

## 目录约定

```
docs\
  index.md              首页
  yijing\               易经
  fengshui\             风水
  bazi\                 四柱八字
  cases\                命例库
  notes\                学习笔记
  blog\posts\           博客文章（按日期命名）
  about\                关于本站
  tags.md               标签汇总页
```

## 发布到 Cloudflare Pages

1. 把整个 `G:\mingli-site` 推到 GitHub 仓库
2. Cloudflare Pages → 连接该仓库
3. 构建命令 `mkdocs build`，输出目录 `site`
4. 之后每次 `git push`，一分钟左右自动上线

> 也可以直接用 `.github\workflows\deploy.yml` 发布到 GitHub Pages（Settings → Pages 选 GitHub Actions）。
