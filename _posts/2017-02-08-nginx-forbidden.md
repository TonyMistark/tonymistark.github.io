---
layout: post
title:  "Nginx 禁止指定域名访问，禁止ip访问"
date:   2017-02-08 10:52:40 +0800
categories: python update
---
### 历史背景
我在使用自己的服务器玩一些服务的时候，总会有些恶意ip攻击，或者通过未设置的域名
访问（如别人把自己的域名指向了我的服务器ip，我遇到的就是这个）。

### 通过Nginx设置
比如别人通过ip或者未知域名访问你的网站的时候，你希望禁止显示任何有效内容，可以给他返回500/403等.
目前国内很多机房都要求网站主关闭空主机头，防止未备案的域名指向过来造成麻烦。

```
# 修改/etc/nginx/nginx.conf(这个目录不一定，反正就是修改nginx.conf的配置文件)
server {
    listen 80;
    server_name www.badhost.com;    # 这里是那个指定的域名
    server_name _;
    return 403;                     # 这个就是返回403错误
    }
```
当接收到ip访问或非指定域名访问时会返回403错误
