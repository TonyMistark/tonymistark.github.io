### Readme
#### Install hexo
所有必备的应用程序安装完成后，即可使用 npm 安装 Hexo。
```
$ npm install -g hexo-cli
```
进阶安装和使用
对于熟悉 npm 的进阶用户，可以仅局部安装 hexo 包。
```
$ npm install hexo
```
#### 创建自己的博客项目，这里先不赘述，看文档： https://hexo.io/zh-cn/docs/

#### Install Theme Next
先fork https://github.com/theme-next/hexo-theme-next 然后 clone 自己的项目，这样自己可以修改并进行版本记录
```
$ git clone git@github.com:TonyMistark/hexo-theme-next.git themes/hexo-theme-next
```
然后编辑配置文件`_config.yml`
```
theme: hexo-theme-next
```
#### 根据配置`_config.yml`安装next的插件
##### Install sitemap
```
$ npm install hexo-generator-sitemap --save
```
##### _config.yml sitemap
```
sitemap:
  path: 
    - sitemap.xml
    - sitemap.txt
  template: ./sitemap_template.xml
  template_txt: ./sitemap_template.txt
  rel: false
  tags: true
  categories: true
```
##### Install hexo word counter
```
$ npm install hexo-word-counter
$ hexo clean
```
##### _config.yml hexo word counter
```
# https://github.com/next-theme/hexo-word-counter
symbols_count_time:
  symbols: true
  time: true
  total_symbols: true
  total_time: true
  exclude_codeblock: false
  wpm: 275
  suffix: "mins."
```

##### Install hexo-auto-category
```
$ npm install hexo-auto-category --save
```
##### _config.yml hexo-auto-category
```
# Generate categories from directory-tree
# Dependencies: https://github.com/xu-song/hexo-auto-category
# depth: the max_depth of directory-tree you want to generate, should > 0
# multiple: multiple category hierarchies
auto_category:
 enable: true
 multiple: false
 depth: 
```
##### Install hexo-generator-feed
```
$ npm install hexo-generator-feed --save
```
##### _config.yml hexo-generator-feed
```
feed:
  enable: true
  type:
    - atom
    - rss2
  path:
    - ./atom.xml
    - ./rss2.xml
  limit: 20
  hub:
  content:
  content_limit: 140
  content_limit_delim: ' '
  order_by: -date
  icon: icon.png
  autodiscovery: true
  template:
```

#### 发布配置
```
# Deployment
## Docs: https://hexo.io/docs/one-command-deployment
deploy:
  type: git
  repo: https://github.com/TonyMistark/tonymistark.github.io
  branch: hexo
```
