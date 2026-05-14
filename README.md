# tonymistark.github.io

个人技术博客，基于 [Hexo](https://hexo.io/) 构建，使用 [NexT](https://github.com/theme-next/hexo-theme-next) 主题，托管于 GitHub Pages。

> 作者：Ice（米超）— Python 后端工程师，base 深圳。

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

## 本地开发

```bash
# 克隆项目（含主题子模块）
git clone --recurse-submodules https://github.com/TonyMistark/tonymistark.github.io.git
cd tonymistark.github.io

# 如果已克隆但未初始化子模块
git submodule update --init --recursive

# 安装依赖
npm install

# 启动本地开发服务器（默认 http://localhost:4000）
npm run server

# 构建静态文件
npm run build

# 清理构建缓存
npm run clean
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
