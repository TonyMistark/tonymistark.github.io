---
layout: ubuntu
title: ubuntu 只保留最近一周的日志
date: 2023-08-18 15:32:38
tags:
---

### 只保留最近一周的日志
```
// 只保留最近一周的日志
journalctl --vacuum-time=1w
```
* 只保留最多500M日志
```
journalctl --vacuum-size=500M
```