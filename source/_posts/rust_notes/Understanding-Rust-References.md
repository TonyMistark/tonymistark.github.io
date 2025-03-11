---
title: Rust 中的指针详解：引用、裸指针与智能指针
categories:
  - rust_notes
date: 2025-03-11 11:44:56
tags:
---


## A Comprehensive Guide to Pointers in Rust: References, Raw Pointers, and Smart Pointers

在 Rust 中，指针是用于引用内存地址的类型。Rust 提供了多种指针类型，每种类型都有不同的所有权、借用和生命周期语义。以下是 Rust 中常见的指针类型及其详细讲解：

### 1. 引用（References）
引用是 Rust 中最常见的指针类型，分为不可变引用（`&T`）和可变引用（`&mut T`）。

- **不可变引用 (`&T`)**:
  - 允许多个不可变引用同时存在。
  - 不能通过不可变引用修改数据。
  - 生命周期由编译器自动推断或显式指定。

  ```rust
  let x = 5;
  let y = &x; // y 是一个不可变引用
  println!("{}", *y); // 解引用 y 获取值
  ```

- **可变引用 (`&mut T`)**:
  - 同一时间只能有一个可变引用。
  - 可以通过可变引用修改数据。
  - 生命周期由编译器自动推断或显式指定。

  ```rust
  let mut x = 5;
  let y = &mut x; // y 是一个可变引用
  *y += 1; // 通过 y 修改 x 的值
  println!("{}", x); // 输出 6
  ```

### 2. 裸指针（Raw Pointers）
裸指针是不安全的指针类型，分为不可变裸指针（`*const T`）和可变裸指针（`*mut T`）。

- **不可变裸指针 (`*const T`)**:
  - 不保证指针的有效性。
  - 不能通过不可变裸指针修改数据。
  - 通常用于与 C 代码交互或实现底层抽象。

  ```rust
  let x = 5;
  let y = &x as *const i32; // y 是一个不可变裸指针
  unsafe {
      println!("{}", *y); // 解引用裸指针需要 unsafe 块
  }
  ```

- **可变裸指针 (`*mut T`)**:
  - 不保证指针的有效性。
  - 可以通过可变裸指针修改数据。
  - 通常用于与 C 代码交互或实现底层抽象。

  ```rust
  let mut x = 5;
  let y = &mut x as *mut i32; // y 是一个可变裸指针
  unsafe {
      *y += 1; // 通过 y 修改 x 的值
  }
  println!("{}", x); // 输出 6
  ```

### 3. 智能指针（Smart Pointers）
智能指针是 Rust 中提供的一种高级指针类型，它们不仅包含指针，还包含额外的元数据和功能。

- **`Box<T>`**:
  - 用于在堆上分配内存。
  - 拥有所有权，当 `Box` 离开作用域时，会自动释放内存。
  - 适用于单一所有权场景。

  ```rust
  let x = Box::new(5); // x 是一个 Box，指向堆上的整数 5
  println!("{}", *x); // 解引用 Box 获取值
  ```

- **`Rc<T>`**:
  - 引用计数智能指针，允许多个所有者。
  - 适用于共享所有权场景。
  - 只能用于单线程环境。

  ```rust
  use std::rc::Rc;

  let x = Rc::new(5); // x 是一个 Rc，指向堆上的整数 5
  let y = Rc::clone(&x); // y 是 x 的一个克隆，引用计数增加
  println!("{}", *y); // 解引用 Rc 获取值
  ```

- **`Arc<T>`**:
  - 原子引用计数智能指针，允许多个所有者。
  - 适用于多线程环境。
  - 类似于 `Rc<T>`，但使用原子操作保证线程安全。

  ```rust
  use std::sync::Arc;

  let x = Arc::new(5); // x 是一个 Arc，指向堆上的整数 5
  let y = Arc::clone(&x); // y 是 x 的一个克隆，引用计数增加
  println!("{}", *y); // 解引用 Arc 获取值
  ```

- **`RefCell<T>`**:
  - 提供内部可变性，允许在不可变引用的情况下修改数据。
  - 适用于单线程环境。
  - 在运行时检查借用规则。

  ```rust
  use std::cell::RefCell;

  let x = RefCell::new(5); // x 是一个 RefCell，包含整数 5
  let mut y = x.borrow_mut(); // 获取可变引用
  *y += 1; // 修改值
  println!("{}", *y); // 输出 6
  ```

- **`Mutex<T>`**:
  - 提供线程安全的内部可变性。
  - 适用于多线程环境。
  - 在访问数据时加锁，保证线程安全。

  ```rust
  use std::sync::Mutex;

  let x = Mutex::new(5); // x 是一个 Mutex，包含整数 5
  let mut y = x.lock().unwrap(); // 获取锁并修改值
  *y += 1; // 修改值
  println!("{}", *y); // 输出 6
  ```

### 4. 函数指针（Function Pointers）
函数指针是指向函数的指针类型，通常用于将函数作为参数传递或存储在数据结构中。

```rust
fn add(a: i32, b: i32) -> i32 {
    a + b
}

let f: fn(i32, i32) -> i32 = add; // f 是一个函数指针，指向 add 函数
println!("{}", f(1, 2)); // 调用函数指针
```

### 5. 切片（Slices）
切片是对数组或向量的一部分的引用，包含一个指针和长度信息。

```rust
let arr = [1, 2, 3, 4, 5];
let slice = &arr[1..3]; // slice 是一个切片，引用 arr 的第 2 和第 3 个元素
println!("{:?}", slice); // 输出 [2, 3]
```

### 总结
Rust 提供了多种指针类型，每种类型都有不同的用途和语义。引用是最常用的指针类型，提供了安全的借用和生命周期管理。裸指针用于底层操作，但需要小心使用。智能指针提供了更高级的内存管理功能，适用于不同的所有权和并发场景。函数指针和切片则用于特定的编程模式。理解这些指针类型及其适用场景是掌握 Rust 内存管理和安全性的关键。
