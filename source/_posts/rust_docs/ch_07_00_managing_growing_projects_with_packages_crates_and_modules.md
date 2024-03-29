---
title: Ch 07.00:使用包、Crate和模块管理不断增长的项目
date: 2023-05-18 10:10
tags: Rust
layout: Rust
---
## 使用包、Crate和模块管理不断增长的项目

当你编写大型程序时，组织代码将变得越来越重要。通过相关功能进行分组，并将具有不同特性的代码分开，你将可以清楚地在哪里可以找到现实特定特性的代码，以及在哪里可以更改一个特性的工作方式。

到目前为止，我们编写的代码都只在一个文件中的一个模块中。 随着项目不断增长，你应该通过多个模块和多个文件来组织拆分你的代码。一个包可以包含多个二进制crates和一个可选的crate程序库。随着你的包的增长，你可以将部分提取到单独的crates使它变成外部依赖。本章涵盖了所有这些技巧。对于由一组相互关联的包组成的非常大的项目，Cargo提供了工作区(workspaces)，我们将在第14章"Cargo Workspaces"部分学习。

我们还将讨论封装实现的细节，这让你可以高水平重用代码：一旦你实现了一个操作，其他代码可以通过代码的公共接口调用，无需知道你的实现过程是如何运作。编写代码的方式定义了那些部分是其他代码使用的公共部分，那些代码是你保留更改权利的私有实现细节。这是另一种限制，减少你必须记住项目内容细节的数量的方法。

这里还一个相关的概念是作用域(scope)：代码所在的嵌套上下文有一组定义"in scope"的名称。当你阅读，编写和编译代码，程序设计师和编译器需要知道模块，常量或者其他有意义的项。你可以创建作用域并改变那些名称再作用域内还是在作用域外。同一个作用域不能拥有两个相同名称的项；可以使用一些工具来解决名称冲突。

Rust有许多特性允许你来管理你的代码组织结构，包括那些内容可以被公开，那些内容作为私有部分，以及程序每个作用域中的名字。这些功能。有时被称为"模块系统(the module system)"，包括：

* 包(Packages)：Cargo的一个功能，它允许你构建，测试和分享crate。
* Crates：一个模块的树形结构，它形成了库或者二进制项目。
* 模块(Modules)和Use：允许你控制组织结构的作用域和路径的私有性。
* 路径(path)：一个命名例如结构体，函数或模块等项的方式。

在本章，我们将涵盖所有这些特性，讨论他们怎样相互作用，并解释如何使用他们管理作用域。最后，你应该对模块系统有一个坚实的理解，并能够像专业人士一样使用作用域！