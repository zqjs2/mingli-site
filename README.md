# 子清见山 · 易学与命理笔记

知识库 + 个人博客站点，MkDocs + MaterialX，托管在 Cloudflare Pages。

- 在线地址：https://zqjs.ziqing.ccwu.cc
- 好记域名：https://zqjs.ziqing.ccwu.cc（CNAME 指向 Pages 项目）
- 代码仓库：https://github.com/zqjs2/mingli-site
- 本地目录：G:\mingli-site

---

## 一、目录结构（内容框架）

```
docs\
  index.md                  首页（板块导航）
  yijing\                   易经（总览 / 基础概念 / 六十四卦）
  fengshui\                 风水（总览 + 五个二级板块）
    tianxing\               天星风水
    bagua\                  八卦风水
    yizhaiduan\             一宅断
    sanyuan\                三元风水
    xuankong\               玄空大卦
  bazi\                     四柱八字（总览 / 干支基础）
  qimen\                    奇门遁甲
  mianxiang\                面相学
  cases\                    命例库
  notes\                    学习笔记
  blog\posts\               博客文章（按日期命名）
  about\                    关于本站
  tags.md                   标签汇总页
```

目录名和网址一律用英文短路径（例如 /fengshui/xuankong/），中文只出现在标题和正文里。

---

## 二、三种写作方式（挑一种即可）

### 方式 A：本地写（推荐，能实时预览）

```powershell
cd G:\mingli-site
python -m mkdocs serve      # 本地预览 http://127.0.0.1:8000 ，存盘自动刷新
```

写完按 Ctrl+C 停止。

### 方式 B：在 GitHub 网页上写（不用开本地环境）

1. 打开 https://github.com/zqjs2/mingli-site
2. 进 `docs` 目录，点右上角 `Add file` → `Create new file`
3. 文件名写成路径，例如 `docs/fengshui/xuankong/rumen.md`
4. 写内容，点 `Commit changes`

### 方式 C：博客随笔

在 `docs/blog/posts/` 下新建，文件名用日期打头，例如 `2026-12-01-shishen.md`：

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

分类页、归档页、标签页、RSS 都由插件自动生成，不用手写。

---

## 三、加一个新的板块（内容框架随时可调）

三步，改完就生效：

1. 建目录和文件：`docs\<新板块>\index.md`
2. 在 `mkdocs.yml` 的 `nav:` 里加一行，例如
   `- 六爻占卜: liuyao/index.md`
3. 首页 `docs\index.md` 的导航表格里补一行链接（可选，但建议）

风水再拆二级板块同理：建 `docs/fengshui\<name>\index.md`，在 `nav:` 里缩进挂在「风水」下面。

---

## 四、发布上线（每次改完必做）

```powershell
cd G:\mingli-site
python -m mkdocs build --clean
$env:HTTP_PROXY="http://127.0.0.1:10808"; $env:HTTPS_PROXY="http://127.0.0.1:10808"
git add -A
git commit -m "更新：xxx"
git push
```

推送后要上线，再执行一次部署：

```powershell
$env:CLOUDFLARE_API_TOKEN="（令牌，见本地 G:\mingli-site\.cf-token）"
$env:CLOUDFLARE_ACCOUNT_ID="f53b5c67bac22f5d18ae9b4bccdce0bd"
$env:HTTPS_PROXY="http://127.0.0.1:10808"
& G:\cf\wrangler.cmd pages deploy site --project-name zqjs --branch main
```

> 现在是「推送 + 手动部署」。若想改成 `git push` 后自动上线：在 Cloudflare 面板把 Pages 项目
> `zqjs` 连接到 GitHub 仓库 `zqjs2/mingli-site`，构建命令 `mkdocs build`、输出目录 `site`。

---

## 五、常用信息

| 项目 | 值 |
| --- | --- |
| 站点配置 | `G:\mingli-site\mkdocs.yml` |
| 主题 | `materialx`（mkdocs-materialx 10.2.3） |
| 依赖 | `G:\mingli-site\requirements.txt` |
| 构建产物 | `G:\mingli-site\site` |
| Cloudflare 账户 ID | `f53b5c67bac22f5d18ae9b4bccdce0bd` |
| Cloudflare 项目 | `zqjs` |
| Cloudflare 域名区 | `ziqing.ccwu.cc`（zqjs.ziqing.ccwu.cc 走 CNAME） |

## 六、写作约定（建议）

- 一节一个 `##` 标题，方便右侧目录自动生成
- 术语第一次出现给一句白话解释，方便以后回看
- 涉及命例，隐去真实姓名/生日，只留必要命理要素
- 每个板块首页保持「核心思路 + 学习清单 + 笔记入口」三块结构
