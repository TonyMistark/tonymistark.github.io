---
layout: post
title:  "初识celery"
date:   20167-01-01 12:52:40 +0800
categories: python update
---

#### 异步任务
异步任务是web开发中一个很常见的方法。对于一些耗时耗资源的操作，往往从主应用中
隔离，通过异步的方式执行。简而言之，做一个注册的功能，在用户使用邮箱注册成功之
后，需要给该邮箱发送一封激活邮件。如果直接放在应用中，则调用发邮件的过程会遇到
网络IO的阻塞，比好优雅的方式则是使用异步任务，应用在业务逻辑中触发一个异步任务。

Celery是一个异步任务的调度工具。它是Python写的库，但是它实现的通讯协议也可以
使用ruby，php，javascript等调用。异步任务除了消息队列的后台执行的方式，还是
一种则是跟进时间的计划任务。下面将会介绍如何使用celery实现这两种需求。

#### Celery broker 和 backend
开始了解celery的时候一定会有redis、rabbitmq这样的词儿，必然会一头雾水，然而
这正是celery设计的玄妙之处，简单来说，rabbitmq是一个采用Erlang写的强大的消
息队列工具。在celery中可以扮演broker的角色。那么broker究竟是什么鬼呢？

broker是一个消息传输的中间件，可以理解为一个邮箱。每当应用程序调用celery的异
步任务的时候，会向broker传递消息，而后celery的worker将会取到消息，进行对应的
程序执行。那么，这个邮箱可以看成是一个消息队列。那么什么又是backend，通常程序
发送的消息，发完就完了，可能都不知道对方是否接受了。为此，celery实现了一个
backend，用于存储这些消息以及celery执行的一些消息和结果。对于 brokers，官方
推荐是rabbitmq和redis，至于backend，就是数据库啦。为了简单起见，我们都用redis。


