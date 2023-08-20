---
layout: notes
title: Hexo 添加分类和标签
date: 2023-08-20 16:02:39
categories: notes
---

### 创建“分类”选项

生成“分类”页并添加tpye属性,进入博客目录。执行命令下方命令
```
$ hexo new page categories
```
categories文件夹下会有index.md这个文件，打开后默认内容是这样的：
```
---
title: categories
date: 2023-08-20 15:33:52
---
```
添加type: "categories"到内容中，添加后是这样的：
```
---
title: categories
date: 2023-08-20 15:33:52
type: categories
---
```
保存并关闭文件。
打开需要添加分类的文章，为其添加categories属性。下方的categories:Hexo表示这篇文章添加到到“Hexo”这个分类。注意：一篇文章只会添加到一个分类中，如果是多个默认放到第一个分类中。
```
---
title: Hello Rust
date: 2017-05-26 12:12:57
categories: Rust学习资料
---
```
至此，成功给文章添加分类，点击首页的“分类”可以看到该分类下的所有文章。当然，只有添加了categories: xxx的文章才会被收录到首页的“分类”中。

### 创建“标签”选项
生成“标签”页并添加tpye属性
```
$ hexo new page tags
```
在tags文件夹下，找到index.md这个文件，打开后默认内容是这样的：
```
---
title: tags
date: 2023-08-20 15:40:07
---
```

添加type: "tags"到内容中，添加后是这样的：
```
---
title: tags
date: 2023-08-20 15:40:07
type: tag
---
```
保存并关闭文件。

给文章添加“tags”属性,打开需要添加标签的文章，为其添加tags属性。
```
---
title: Hello Rust
date: 2017-05-26 12:12:57
categories: Rust学习资料
tag: Rust
---
```