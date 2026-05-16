# tonymistark.github.io

个人技术博客，基于 [Hexo](https://hexo.io/) 构建，使用 [NexT](https://github.com/theme-next/hexo-theme-next) 主题，托管于 GitHub Pages。

## 内容

- **Rust 学习笔记** — 官方 Rust Book 的翻译与整理笔记，涵盖变量、所有权、结构体、枚举、错误处理等章节。
- **技术随笔** — 如 Ubuntu 时钟显示秒等实用技巧。
- **关于页** — 个人履历与技能介绍。

## 技术栈

| 工具 | 用途 |
|---|---|
| [Hexo](https://hexo.io/) ^6.3 | 静态站点生成 |
| [NexT](https://github.com/theme-next/hexo-theme-next) | 主题（git submodule） |
| EJS + Stylus | 模板引擎 / CSS 预处理器 |
| GitHub Actions | CI/CD 自动构建部署 |
| GitHub Pages | 站点托管 |

## 环境准备

```bash
# 克隆项目（含主题子模块）
git clone --recurse-submodules https://github.com/TonyMistark/tonymistark.github.io.git
cd tonymistark.github.io

# 如果已克隆但未初始化子模块
git submodule update --init --recursive

# 安装 Node.js 依赖
npm install

# 全局安装 hexo-cli
npm install -g hexo-cli
```

## Hexo 使用手册

### 本地开发

```bash
# 启动本地开发服务器（默认 http://localhost:4000）
hexo server
# 或
npm run server

# 启动时预览草稿
hexo server --draft

# 构建静态文件
hexo generate
# 或
npm run build

# 清理构建缓存（db.json 和 public/）
hexo clean
# 或
npm run clean
```

### 创建文章

```bash
# 创建新文章
hexo new post "<标题>"
# 例：hexo new post "hello-world"

# 创建草稿（不会发布）
hexo new draft "<标题>"

# 将草稿发布为正式文章
hexo publish post "<标题>"
```

文章文件生成在 `source/_posts/` 下，文件名为 `<标题>.md`。Front-matter 中可设置 `tags`、`categories`、`date` 等字段。

### 创建页面

```bash
# 创建新页面（如关于页、友链页）
hexo new page "<页面名>"
# 例：hexo new page "about"
```

页面文件生成在 `source/<页面名>/index.md`。

### 草稿工作流

```bash
# 新建草稿
hexo new draft "draft-title"

# 本地预览草稿
hexo server --draft

# 满意后发布为正式文章
hexo publish post "draft-title"
```

### 常用命令速查

| 命令 | 简写 | 说明 |
|---|---|---|
| `hexo init` | — | 初始化 Hexo 项目 |
| `hexo new post <t>` | `hexo n <t>` | 新建文章 |
| `hexo new draft <t>` | — | 新建草稿 |
| `hexo publish post <t>` | `hexo p <t>` | 发布草稿 |
| `hexo server` | `hexo s` | 启动本地服务器 |
| `hexo generate` | `hexo g` | 生成静态文件 |
| `hexo clean` | — | 清理缓存 |
| `hexo deploy` | `hexo d` | 部署到远程 |
| `hexo list post` | — | 列出所有文章 |
| `hexo list page` | — | 列出所有页面 |

### 更新主题

```bash
# 更新 NexT 主题子模块
npm run update-theme
# 等价于
git submodule update --remote
```

## 目录结构

```
├── _config.yml          # Hexo 主配置
├── package.json         # 项目依赖与脚本
├── scaffolds/           # 文章模板（post / page / draft）
├── source/
│   └── _posts/          # Markdown 博文
├── themes/
│   └── hexo-theme-next/ # NexT 主题（git submodule）
└── .github/workflows/   # CI/CD 工作流
```

## 部署

推送到 `hexo-dev` 分支触发 GitHub Actions 自动构建，并将静态文件部署到 GitHub Pages。

```bash
# 手动部署（需要 hexo-deployer-git）
npm run deploy
```

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
