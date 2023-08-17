---
title: 总结
date: 2023-08-17 16:29:S
tags: Rust
layout: Rust
---
### 总结

现在我们学习了如何使用枚举创建自定义类型。我们也展示了标准库的`Option<T>`类型是如何帮助你利用类型系统来避免出错的。当枚举值包含数据时，你可以根据你需要处理多少种情况来选择使用`mathc`或者`if let`来提取或者使用这些值。

你的Rust程序现在能够使用结构体和枚举在你自己的作用域内表现其内容了。在你的API中使用定义类型保证了类型安全：编译器会确保你的函数只会得到它期望的类型的值。

为了提供一个有条理的API给你的用户，它使用起来很简单易懂，值暴露了你的用户需要的东西，现在我们准备开始学习Rust的模块。
