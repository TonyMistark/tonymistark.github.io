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
```Rust
enum Result<T, E> {
    Ok(T),
    Err(E),
}
```
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

#### 匹配不同的错误(Matching on Different Errors)
Listing9-4无论`File::open`因为什么失败都会报`pannic!`错误。然而，我们希望针对不同的失败原因采取不同的行动：如果`File::open`失败是因为文件不存在，我们想创建一个文件并返回新文件的句柄。如果`File::open`失败是因为其他原因--比如，因为我们没有打开文件的权限--我们仍然和Listing9-4一样`panic!`。为此，我们在`match`内添加一个内部表达式，如Listing 9-5所示。
Filename: src/main.rs
```Rust
use std::fs:File;
use std::io::ErrorKind;

fn main() {
    let greeting_file_result = File::open("hello.txt");
    let greeting_file = match greeting_file_result {
        Ok(file) => file,
        Err(error) => match error.kind() {
            ErrorKind::NotFound => match File::create("hello.txt") {
                Ok(fc) => fc,
                Err(e) => panic!("Problem creating the file: {:?}", e),
            },
            other_error => {
                panic!("Problem opening the file: {:?}", other_error);
            }
        },
    }
}
```
Listing 9-5: Handling different kinds of errors in different ways

`File::open`内部返回的`Err`的值`io::Error`，它是标准库提供的数据结构。这个数据结构有一个`kind`方法可以得到一个`io::ErrorKind`的值。枚举`io::ErrorKind`是标准库提供的，并且有不同类型的错误都对应着相应的io操作。我们使用的`ErrorKing::NotFound`枚举成员表明我们尝试打开一个不存在的文件。所以我们在`greeting_file_result`上匹配，但我们也在error.kind()上进行内部匹配。

我们希望在内部匹配中检查的条件是`error.kind()`返回的值是否为`ErrorKind`枚举的`NotFound`成员。如果是我，我们将尝试通过`File::create`创建文件，然而我们创建文件也有可能失败，在`match`内部我们需要第二个分支来处理。当文件不能创建，一个不同的错误就会被打印。`match`外部保持不变。因此，除文件不存在的情况之外都会报错。

#### 失败时 panic 的简写: unwrap 和 expect
`match` 已经很好用了，不过它可能有点冗长并且不总是能很好的表明其意图。`Result<T, E>` 类型定义了很多辅助方法来处理各种情况。其中之一叫做 `unwrap`，它的实现就类似于Listing 9-4 中的 `match` 语句。如果 `Result` 值是成员 `Ok`，`unwrap` 会返回 `Ok` 中的值。如果 `Result` 是成员 `Err`，`unwrap` 会为我们调用 `panic!`。这里是一个实践 `unwrap` 的例子：
```Rust
use std::fs:File;

fn main() {
    let greeting_file = File::open("hello.txt").unwrap();
}
```
如果我们运行这段代码，并且`hello.txt`文件不存在，我们就会看到一个错误信息来自`unwrap`方法调用了`panic!`:
```
thread 'main' panicked at 'called `Result::unwrap()` on an `Err` value: Os {
code: 2, kind: NotFound, message: "No such file or directory" }',
src/main.rs:4:49
```
同样，`expect`方法也可以自定义`panic!`的错误信息。使用`expect`而不是`unwrap`并提供友好的错误信息可以传达您的意图，并使跟踪`panic!`的来源更容易。`expect`的语法如下所示：
Filename: src/main.rs
```Rust
use std::fs:File;

fn main() {
    let greeting_file = File::open("hello.txt")
    .expect("hello.txt should be included int this project");
}
```
我们可以和使用`unwrap`一样使用`expect`来返回一个文件句柄或者调用`panic!`。错误信息通过`expect`调用`panic!`时传递，而不是`panic!`默认的错误信息，展示如下：
```
thread 'main' panicked at 'hello.txt should be included in this project: Os {
code: 2, kind: NotFound, message: "No such file or directory" }',
src/main.rs:5:10
```
#### 传递错误(Propagating Errors)
当编写一个其实先会调用一些可能会失败的操作的函数时，除了在这个函数中处理错误外，还可以选择让调用者知道这个错误并决定该如何处理。这被称为 传播（propagating）错误，这样能更好的控制代码调用，因为比起你代码所拥有的上下文，调用者可能拥有更多信息或逻辑来决定应该如何处理错误。
例如：Listing 9-6所示，一个函数读一个文件。如果文件不存在或者不能读，函数就会返回一些错误。
Filename: src/main.rs
```Rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let usename_file_result = File::open("hello.txt");

    let mut usename_file = match username_file_result {
        Ok(file) => file,
        Err(e) => return Err(e),
    };
    let mut username = String::new();

    match user_file.read_to_string(&mut username) {
        Ok(_) => Ok(username),
        Err(e) => Err(e),
    }
}

fn main() {
    read_username_from_file();
}
```
Listing 9-6: A function that returns errors to the calling code using `match`

这个函数可以用更短的方式编写，但我们将从手动做很多事情开始，以探索错误处理;最后，我们将展示较短的方法。我们先看一下函数的返回类型：` Result<String, io::Error>` 。这意味着该函数返回一个类型的 `Result<T, E>` 值，其中泛型参数 `T` 已用具体类型填充，泛型类型已用具体类型 `String`填充，`E`用`io::Error`填充。

如果此函数成功且没有任何问题，则调用此函数的代码将收到一个`Ok`值，该值包含`String`此函数从文件中读取的username。如果此函数遇到任何问题，调用代码将收到一个 `Err` 值，该值包含包含有关问题所在的详细信息的实例 `io::Error` 。我们选择 `io::Error` 此函数的返回类型，因为这恰好是我们在此函数主体中调用的两个操作返回的错误值的类型： `File::open` 函数和 `read_to_string` 方法。

函数的主体从调用 `File::open` 函数开始。然后我们用类似于Listing 9-4 `match` 中的值来处理 `match` 该 `Result` 值。如果成功，模式 `File::open` 变量中的文件句柄将成为可变变量 `username_file` 中的值，函数将继续。在这种情况下 `Err` ，我们不是调用，而是使用 `return` 关键字提前完全返回函数，并从`File::open`返回的错误传递出去，模式匹配中的`e`作为该函数的错误值传递回调用 panic! 代码。

因此，如果我们在`username_file`中有一个文件句柄，那么该函数将在变量`username`中创建一个新的`String`，并调用`username_file`中文件句柄上的`read_to_string`方法来将文件的内容读入`username`。`read_to_string`方法也返回`Result`，因为它可能失败，即使`File::open`打开文件成功，读文件也有可能失败。所以我们需要另一个匹配来处理这个`Result`:如果`read_to_string`成功，那么我们的函数就成功了，我们从文件中返回username，这个username现在被`Ok`封装在`username`中。如果`read_to_string`操作失败，返回错误值的方式与处理`File::open`返回值的匹配中返回错误值的方式相同。然而，我们不需要显式`return`，因为这是函数中的最后一个表达式。

然后，调用该代码的代码将处理获取包含`username`的`Ok`值或包含`io::Error`的`Err`值。由调用代码决定如何处理这些值。如果调用代码得到一个`Err`值，它可能会调用`panic!`并使程序崩溃，使用默认username，或者从文件以外的其他地方查找username。我们没有足够的信息来了解调用代码实际尝试做什么，所以我们向上传播所有成功或错误信息，以便它正确处理。

这种传播错误的模式在Rust中非常常见，因此Rust为了方便起见提供了问号操作符`?`。

#### 传播错误的快捷方式:`?`操作符

如Listing9-7所示，实现了一个和Listing9-6相同的`read_username_from_file`的函数，但是使用了`?`操作来实现。
Filename: src/main.rs
```Rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username_file = File::open("hello.txt")?;
    let mut username = String::new();
    username_file.read_to_string(&mut username)?;
    Ok(username)
}

fn main() {
}
```
Listing 9-7: A function that returns errors to the calling code using the `?`` operator

`?`操作符放置在`Result`值之后，其工作方式与Listing 9-6中为处理`Result`值而定义的匹配表达式几乎相同。如果`Result`的值为`Ok`，则该表达式将返回`Ok`中的值，程序将继续执行。如果该值为`Err`，则整个函数将返回`Err`，就像我们使用了`return`关键字一样，因此错误值将传播到调用代码。

Listing 9-6中的匹配表达式的作用与`?`操作符所做的事情:错误值有`?`在标准库中的`From`trait中定义了from函数，该函数用于将值从一种类型转换为另一种类型。什么时候`?`操作符调用`from`函数，接收到的错误类型被转换为当前函数返回类型中定义的错误类型。当函数返回一种错误类型来表示函数可能失败的所有方式时，即使部分可能因许多不同的方式而失败，这也是有用的。

例如，我们可以修改Listing 9-7中的`read_username_from_file`函数，使其返回一个自定义的错误类型`OurError`。如果我们还为`OurError`定义`impl From<io::Error>`，从`io::Error`构造`OurError`的实例，那么`?`操作符会在`read_username_from_file`函数体中将调用`from`并转换错误类型，而无需向函数中添加任何代码。

在Listing 9-7的上下文中，`?`在`File::open`调用的末尾将把`Ok`中的值返回给变量`username_file`。如果发生错误，`?`操作符将提前返回，并向调用代码提供任何`Err`值。同样的道理也适用于`?`在`read_to_string`调用结束时。

`?`操作符消除了大量的模板代码，使这个函数的实现更简单。我们甚至可以通过在`?`之后立即连接方法调用来进一步缩短代码，如Listing 9-8所示。
Filename: src/main.rs
```Rust
use std::fs::File;
use std::io::{self, Read};

fn read_username_from_file() -> Result<String, io::Error> {
    let mut username = String::new();

    File::open("hello.txt")?.read_to_string(&mut username)?;

    Ok(username)
}

fn main() {
}
```
Listing 9-8: Chaining method calls after the `?` operator

我们将`username`中`String`的创建移到了函数的开头;这一点没有改变。我们没有创建一个可变的用户名文件，而是将`read_to_string`调用直接连接到`file::open("hello.txt")`的结果上。我们还有`?`当`File::open`和`read_to_string`都成功时，我们仍然返回一个包含`username`的`Ok`值，而不是返回错误。功能与Listing 9-6和Listing 9-7相同;这是一种不同的，更符合工程学的写法。

Listing 9-9 所示使用了`fs::read_to_string`将使代码更加简短。
```Rust
use std::fs;
use std::io;

fn read_username_from_file() -> Result<String, io::Error> {
    fs::read_to_string("hello.txt")
}
fn main() {
}
```
Listing 9-9: Using `fs::read_to_string` instead of opening and then reading the file

将文件读入字符串是一种相当常见的操作，因此标准库提供了方便的`fs::read_to_string`函数，该函数打开文件，创建一个新的`String`，读取文件的内容，将内容放入该`String`，并返回它。当然，使用`fs::read_to_string`并不能让我们有机会解释所有的错误处理，所以我们先用更长的方法来解释。

#### 哪里可以使用`?`操作
`?`操作符只能用于返回类型与`?`操作符兼容的函数中。这是因为`?`操作符的定义是执行从函数中提前返回一个值，方式与Listing 9-6中定义的`match`表达式相同。在Listing 9-6中，匹配使用一个`Result`值，而提前返回臂返回一个`Err(e)`值。函数的返回类型必须是`Result`，以便与此返回兼容。

在Listing 9-10中，让我们看看如果使用`?`返回类型与我们使用的值的类型不兼容的主函数中的操作符`?`:
Filename: src/main.rs
```Rust
use std::fs::File;

fn main() {
    let greeting_file = File::open("hello.txt")?;
}
```
Listing 9-10: Attempting to use the `?` in the `main` function that returns `()`` won’t compile

这段代码打开一个文件，可能会失败。`?`操作符在`File::open`返回的`Result`值之后，但是这个主函数的返回类型是`()`，而不是`Result`。当我们编译这段代码时，会得到以下错误消息:
```shell
$ cargo run
   Compiling error-handling v0.1.0 (file:///projects/error-handling)
error[E0277]: the `?` operator can only be used in a function that returns `Result` or `Option` (or another type that implements `FromResidual`)
 --> src/main.rs:4:48
  |
3 | fn main() {
  | --------- this function should return `Result` or `Option` to accept `?`
4 |     let greeting_file = File::open("hello.txt")?;
  |                                                ^ cannot use the `?` operator in a function that returns `()`
  |
  = help: the trait `FromResidual<Result<Infallible, std::io::Error>>` is not implemented for `()`

For more information about this error, try `rustc --explain E0277`.
error: could not compile `error-handling` due to previous error
```
这个错误指出我们只允许使用`?`返回`Result`、`Option`或其他实现`FromResidual`的类型的函数中的操作符。

要修复这个错误，您有两种选择。一种选择是更改函数的返回类型，使其与使用的值兼容。只要没有限制，就继续操作。另一种技术是使用`match`或`Result<T, E>`方法之一，以任何合适的方式处理`Result<T, E>`。

错误信息中还提到`?`也可以与`Option<T>`值一起使用。就像使用`?`在`Result`中，您只能使用`?`在返回一个`Option`的函数中使用`Option`。`?`操作符在`Option<T>`上调用时的行为与在`Result<T, E>`上调用时的行为相似:如果值为`None`，则在该点将提前从函数返回`None`。如果值是`Some`，则`Some`中的值是表达式的结果值，函数继续执行。Listing 9-11给出了一个函数示例，该函数查找给定格式中第一行的最后一个字符：
```Rust
fn last_char_of_first_line(text: &str) -> Option<char> {
    text.lines().next()?.chars().last()
}

fn main() {
    assert_eq!(
        last_char_of_first_line("Hello, world\nHow are you today?"),
        Some('d')
    );

    assert_eq!(last_char_of_first_line(""), None);
    assert_eq!(last_char_of_first_line("\nhi"), None);
}
```
Listing 9-11: Using the `?` operator on an `Option<T>` value

这个函数返回`Option<char>`，因为有可能有字符，但也有可能没有。这段代码接受`text`字符串切片参数并对其调用`lines`方法，该方法返回一个遍历字符串中的行的迭代器。因为这个函数想要检查第一行，所以它在迭代器上调用`next`以从迭代器中获取第一个值。如果`text`是空字符串，对`next`的调用将返回`None`，在这种情况下我们使用`?`停止并从第一行的最后一个字符返回`None`。如果`text`不是空字符串，`next`将返回一个`Some`值, 其中包含`text`中第一行的字符串切片。

`?`操作符提取字符串切片，然后调用该字符串切片上的`chars`来获取其字符的迭代器。我们对第一行的最后一个字符感兴趣，因此调用`last`来返回迭代器中的最后一项。这是一个选项，因为第一行可能是空字符串，例如，如果文本以空行开头，但在其他行上有字符，如`“\nhi”`。但是，如果第一行有最后一个字符，它将在`Some`变体中返回。`?`运算符在中间给了我们一种简洁的方式来表达这个逻辑，允许我们实现

注意，您可以使用`?`操作符对返回`Result`的函数中的`Result`进行操作，您可以使用?操作符在返回`Option`的函数中对`Option`进行操作，但不能混合匹配。`?`操作符不会自动将`Result`转换为`Option`，反之亦然;在这些情况下，您可以使用诸如`Result`上的`ok`方法或`Option`上的`ok_or`方法来显式地进行转换。

到目前为止，我们使用的所有主要函数都是`return()`。`main`函数的特殊之处在于它是可执行程序的入口和出口点，它的返回类型是有限制的，这样程序才能按照预期的方式运行。

幸运的是，`main`也可以返回`Result<()， E>`。Listing 9-12拥有Listing 9-10的代码，但我们将`main`的返回类型更改为`Result<()`， `Box<dyn Error>>`，并在末尾添加返回值`Ok(())`。这段代码现在可以编译了:

```Rust
use std::error::Error;
use std::fs::File;

fn main() -> Result<(), Box<dyn Error>> {
    let greeting_file = File::open("hello.txt")?;

    Ok(())
}
```
Listing 9-12: Changing main to return `Result<(), E>` allows the use of the `?` operator on `Result` values

`Box<dyn Error>`类型是一个`trait`对象，我们将在第17章使用允许不同类型值的`trait`对象一节中讨论它。现在，您可以读取`Box<dyn Error>`来表示任何类型的错误。使用`?`允许在错误类型为`Box<dyn error >`的主函数中返回`Result`值，因为它允许提前返回任何`Err`值。即使这个主函数的主体只会返回`std::io::Error`类型的错误，通过指定`Box<dyn Error>`，即使将返回其他错误的更多代码添加到main的主体中，该签名仍然是正确的。

当`main`函数返回`Result<()， E>`时，如果`main`函数返回`Ok(())`，可执行程序将以`0`的值退出;如果`main`函数返回`Err`值，可执行程序将以非`0`的值退出。用C编写的可执行程序在退出时返回整数:成功退出的程序返回整数`0`，出错的程序返回非0的整数。Rust还从可执行文件返回整数，以与此约定兼容。

main函数可以返回任何实现`std::process::Termination` trait的类型，它包含一个可以返回`ExitCode`的函数`report`。有关为您自己的类型实现`Termination`特性的更多信息，请参阅标准库文档。

到现在，我们已经详细讨论了调用`panic!`或者返回`Result`。