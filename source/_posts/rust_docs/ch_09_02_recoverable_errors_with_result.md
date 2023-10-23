---
title: Ch 09.02:带有结果的可恢复错误
categories: Rust
date: 2023-10-18 19:35
tags: Rust
layout: Rust
---
### 带有结果的可恢复错误

大多数错误并不严重到需要程序完全停止。有时，当一个函数失败时，其原因可以很容易地解释和响应。例如，如果您尝试打开一个文件，但由于该文件不存在而导致该操作失败，那么您可能希望创建该文件，而不是终止该进程。

回到第二章`Result`的枚举定义里，有两个成员，`Ok` 和`Err`,如下：
···Rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
···
`T`和`E`是泛型参数：我们将在第十章详细讨论。目前你需要知道当成功时返回枚举成员`Ok`，当失败时返回枚举成员`Err`。由于`Result`具有这些泛型类型参数，因此我们可以在许多不同的情况下使用`Result`类型及其上定义的函数，其中我们希望返回的成功值和错误值可能不同。

我们来调用一个返回值类型为`Result`的函数，因为调用可能会失败。如Listing 9-3我们尝试打开一个文件。
Filename: src/main.rs
```Rust
use std::fs::File;
fn main() {
    let greeting_file_result = File::opend("hello.txt);
}
```
Listing 9-3 Openging a file

`File::open`的返回值是一个`Result<T, E>`。泛型参数`T`已经被`File::open`实现，并填入了成功的值，`std::fs::File`是一个文件句柄(file handle)。类型`E`的错误值是`std::io::Error`。`File::open`返回类型意思是如果成功就会返回一个文件句柄，并且可以进行读写。这个函数也有可能会调用失败：例如，文件不存在，或者没有权限访问。`File::open`函数需要有个方式告诉我们是成功或者失败，同时返回给我们文件句柄或者错误信息。这个信息正是Result枚举所传达的。

因此，当`File::open`调用成功，变量`greeting_file_result`的值将会是成员`Ok`并包含一个文件句柄。如果失败，`greeting_file_result`就是一个`Err`的实例并包含更多错误信息来展示到底发生了什么错误。

我们需要在Listing9-3中根据`File::open`的返回值来添加额外的代码。如Listing9-4中所示，这是一个基本的`Result`的处理工具，就是使用`match`表达式（我们已经在第六章中讲过了）。
Filename:src/main.rs
```Rust
use std::fs::File;
fn main() {
    let greeting_file_result = File::open("hello.txt");
    let greeting_file = match greeting_file_result {
        Ok(file) => file,
        Err(error) => panic!("Problem opening the file: {:?}", error),
    };
}
```
Listing 9-4: Using a match expression to handle the `Result` variants that might be returned

请注意，与Option enum一样，`Result`枚举及其成员也通过prelude进入了作用域，因此我们不需要在匹配分支中的Ok和Err成员之前指定`Result::`。

当结果为`Ok`时，这段代码将返回`Ok`中的`file`，然后我们将该文件句柄值赋给变量`greeting_file`。在`match`之后，我们可以使用文件句柄进行读写了。
`match`的另外一个分支就会从`File::open`中得到一个`Err`的值。在这个示例中，我们现在调用`panic!`宏(macro)。如果没有一个叫`hello.txt`的文件在当前文件夹，并且运行了这段代码，我们就会看到如下来自`panic!`宏的错误输出:
```
$ cargo run
   Compiling error-handling v0.1.0 (file:///projects/error-handling)
    Finished dev [unoptimized + debuginfo] target(s) in 0.73s
     Running `target/debug/error-handling`
thread 'main' panicked at 'Problem opening the file: Os { code: 2, kind: NotFound, message: "No such file or directory" }', src/main.rs:8:23
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```
像往常一样，这个输出告诉我们哪里出了问题。