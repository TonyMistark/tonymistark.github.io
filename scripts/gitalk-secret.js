// Gitalk client_secret 注入脚本
//
// client_secret 属于敏感信息，不进 git 仓库。
// 构建/预览时从项目根目录的 .env 读取 GITALK_CLIENT_SECRET 并注入主题配置。
//
// 本地准备：在 .env 中添加一行
//   GITALK_CLIENT_SECRET=<你的 secret>
// （.env 已被 .gitignore 排除，勿提交）

'use strict';

const fs = require('fs');
const path = require('path');

hexo.extend.filter.register('generateBefore', () => {
  const envFile = path.join(hexo.base_dir, '.env');
  if (!fs.existsSync(envFile)) return;

  const content = fs.readFileSync(envFile, 'utf8');
  const match = content.match(/^\s*GITALK_CLIENT_SECRET\s*=\s*(.+?)\s*$/m);
  if (!match) return;

  const secret = match[1].trim().replace(/^["']|["']$/g, '');
  if (!secret) return;

  const themeConfig = hexo.config.theme_config;
  if (themeConfig && themeConfig.gitalk) {
    themeConfig.gitalk.client_secret = secret;
  }
});