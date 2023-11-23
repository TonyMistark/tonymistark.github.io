---
title: Singleton
tags: Design Pattern
categories:
  - design-pattern
date: 2023-11-23 21:08:58
---

# Singleton 单例模式

## Intent 意图
**Singleton** is a creational design pattern that lets you ensure that a class has only one instance, while providing a global access point to this instance.
Singleton 是一种创建性设计模式，它允许您确保一个类只有一个实例，同时提供此实例的全局访问点。
<div align="center"> <img src="/images/singleton-header.png"/></div>

## Problem 问题
The Singleton pattern solves two problems at the same time, violating the Single Responsibility Principle:
Singleton 模式同时解决了两个问题，违反了单一责任原则：

1. **Ensure that a class has just a single instance**. Why would anyone want to control how many instances a class has? The most common reason for this is to control access to some shared resource—for example, a database or a file.
确保一个类只有一个实例。为什么有人想要控制一个类有多少个实例？最常见的原因是控制对某些共享资源（例如数据库或文件）的访问。

Here’s how it works: imagine that you created an object, but after a while decided to create a new one. Instead of receiving a fresh object, you’ll get the one you already created.
它是这样工作的：假设你创建了一个对象，但过了一段时间决定创建一个新对象。您将获得已创建的对象，而不是接收新对象。

Note that this behavior is impossible to implement with a regular constructor since a constructor call must always return a new object by design.
请注意，此行为无法使用常规构造函数实现，因为构造函数调用必须始终返回新对象。
<div align="center"> <img src="/images/singleton-comic-1-en.png"/>Clients may not even realize that they’re working with the same object all the time.</br>客户甚至可能没有意识到他们一直在使用同一个对象。</div>

2. **Provide a global access point to that instance**.Remember those global variables that you (all right, me) used to store some essential objects? While they’re very handy, they’re also very unsafe since any code can potentially overwrite the contents of those variables and crash the app.
为该实例提供全局访问点。还记得你（好吧，我）用来存储一些基本对象的那些全局变量吗？虽然它们非常方便，但它们也非常不安全，因为任何代码都可能覆盖这些变量的内容并使应用程序崩溃。
Just like a global variable, the Singleton pattern lets you access some object from anywhere in the program. However, it also protects that instance from being overwritten by other code.
就像全局变量一样，Singleton 模式允许您从程序中的任何位置访问某些对象。但是，它还可以保护该实例不被其他代码覆盖。
There’s another side to this problem: you don’t want the code that solves problem #1 to be scattered all over your program. It’s much better to have it within one class, especially if the rest of your code already depends on it.
这个问题还有另一面：你不希望解决问题 #1 的代码分散在你的程序中。最好将它放在一个类中，特别是如果您的其余代码已经依赖于它。

Nowadays, the Singleton pattern has become so popular that people may call something a singleton even if it solves just one of the listed problems.
如今，单例模式已经变得如此流行，以至于人们可能会称某物为单例，即使它只解决了列出的问题之一。

## Solution 解决方案
All implementations of the Singleton have these two steps in common:
Singleton 的所有实现都具有以下两个共同步骤：
* Make the default constructor private, to prevent other objects from using the new operator with the Singleton class.
将默认构造函数设为私有，以防止其他对象将运 new 算符与 Singleton 类一起使用。
* Create a static creation method that acts as a constructor. Under the hood, this method calls the private constructor to create an object and saves it in a static field. All following calls to this method return the cached object.
创建一个充当构造函数的静态创建方法。在后台，此方法调用私有构造函数来创建对象并将其保存在静态字段中。对此方法的所有后续调用都将返回缓存的对象。

If your code has access to the Singleton class, then it’s able to call the Singleton’s static method. So whenever that method is called, the same object is always returned.
如果您的代码有权访问 Singleton 类，则它能够调用 Singleton 的静态方法。因此，每当调用该方法时，始终返回相同的对象。

## Real-World Analogy 真实世界的类比
The government is an excellent example of the Singleton pattern. A country can have only one official government. Regardless of the personal identities of the individuals who form governments, the title, “The Government of X”, is a global point of access that identifies the group of people in charge.
政府是辛格尔顿模式的一个很好的例子。一个国家只能有一个官方政府。无论组成政府的个人的个人身份如何，“X政府”这个头衔都是一个全球访问点，用于识别负责人群体。

## Structure 结构
<div align="center"> <img src="/images/singleton-structure-en.png"/></div>
The **Singleton** class declares the static method getInstance that returns the same instance of its own class.
**Singleton** 类声明返回其自身类的相同实例的静态方法 getInstance 。

The Singleton’s constructor should be hidden from the client code. Calling the getInstance method should be the only way of getting the Singleton object.
Singleton 的构造函数应在客户端代码中隐藏。调用该 getInstance 方法应该是获取 Singleton 对象的唯一方法。

##  Pseudocode 伪代码
In this example, the database connection class acts as a **Singleton**. This class doesn’t have a public constructor, so the only way to get its object is to call the `getInstance` method. This method caches the first created object and returns it in all subsequent calls.
在此示例中，数据库连接类充当 Singleton。此类没有公共构造函数，因此获取其对象的唯一方法是调用该 `getInstance` 方法。此方法缓存第一个创建的对象，并在所有后续调用中返回该对象。
```java
// The Database class defines the `getInstance` method that lets
// clients access the same instance of a database connection
// throughout the program.
class Database is
    // The field for storing the singleton instance should be
    // declared static.
    private static field instance: Database

    // The singleton's constructor should always be private to
    // prevent direct construction calls with the `new`
    // operator.
    private constructor Database() is
        // Some initialization code, such as the actual
        // connection to a database server.
        // ...

    // The static method that controls access to the singleton
    // instance.
    public static method getInstance() is
        if (Database.instance == null) then
            acquireThreadLock() and then
                // Ensure that the instance hasn't yet been
                // initialized by another thread while this one
                // has been waiting for the lock's release.
                if (Database.instance == null) then
                    Database.instance = new Database()
        return Database.instance

    // Finally, any singleton should define some business logic
    // which can be executed on its instance.
    public method query(sql) is
        // For instance, all database queries of an app go
        // through this method. Therefore, you can place
        // throttling or caching logic here.
        // ...

class Application is
    method main() is
        Database foo = Database.getInstance()
        foo.query("SELECT ...")
        // ...
        Database bar = Database.getInstance()
        bar.query("SELECT ...")
        // The variable `bar` will contain the same object as
        // the variable `foo`.
```
## Applicability 适用性
* **Use the Singleton pattern when a class in your program should have just a single instance available to all clients; for example, a single database object shared by different parts of the program.当程序中的类应该只有一个实例可供所有客户端使用时，请使用单例模式;例如，由程序的不同部分共享的单个数据库对象。**

* The Singleton pattern disables all other means of creating objects of a class except for the special creation method. This method either creates a new object or returns an existing one if it has already been created.
Singleton 模式禁用除特殊创建方法之外的所有其他创建类对象的方法。此方法要么创建一个新对象，要么返回一个现有对象（如果已创建）。

* **Use the Singleton pattern when you need stricter control over global variables.当您需要对全局变量进行更严格的控制时，请使用单例模式。**

* Unlike global variables, the Singleton pattern guarantees that there’s just one instance of a class. Nothing, except for the Singleton class itself, can replace the cached instance.
与全局变量不同，单例模式保证一个类只有一个实例。除了 Singleton 类本身之外，没有任何内容可以替换缓存的实例。

Note that you can always adjust this limitation and allow creating any number of Singleton instances. The only piece of code that needs changing is the body of the `getInstance` method.
请注意，您始终可以调整此限制，并允许创建任意数量的单例实例。唯一需要更改的代码段是 `getInstance` 方法的主体。

## How to Implement 如何实现
1. Add a private static field to the class for storing the singleton instance.
在类中添加一个私有静态字段，用于存储单例实例。

2. Declare a public static creation method for getting the singleton instance.
声明用于获取单例实例的公共静态创建方法。

3. Implement “lazy initialization” inside the static method. It should create a new object on its first call and put it into the static field. The method should always return that instance on all subsequent calls.
在静态方法中实现“延迟初始化”。它应该在第一次调用时创建一个新对象，并将其放入静态字段中。该方法应始终在所有后续调用中返回该实例。

4. Make the constructor of the class private. The static method of the class will still be able to call the constructor, but not the other objects.
将类的构造函数设为私有。类的静态方法仍然能够调用构造函数，但不能调用其他对象。

5. Go over the client code and replace all direct calls to the singleton’s constructor with calls to its static creation method.
遍历客户端代码，并将对单例构造函数的所有直接调用替换为对其静态创建方法的调用。

## Pros and Cons 优点和缺点

| Pros 优点 | Cons 缺点 |
| --- | --- |
| You can be sure that a class has only a single instance.可以确定一个类只有一个实例。 | Violates the Single Responsibility Principle. The pattern solves two problems at the time.违反了单一责任原则。该模式解决了当时的两个问题。 |
| You gain a global access point to that instance.您将获得该实例的全局访问点。 | The Singleton pattern can mask bad design, for instance, when the components of the program know too much about each other.单例模式可以掩盖糟糕的设计，例如，当程序的组件彼此了解太多时。 |
| The singleton object is initialized only when it’s requested for the first time.仅当首次请求单一实例对象时，才会对其进行初始化。 | The pattern requires special treatment in a multithreaded environment so that multiple threads won’t create a singleton object several times.
该模式需要在多线程环境中进行特殊处理，以便多个线程不会多次创建单一实例对象。 |
| | It may be difficult to unit test the client code of the Singleton because many test frameworks rely on inheritance when producing mock objects. Since the constructor of the singleton class is private and overriding static methods is impossible in most languages, you will need to think of a creative way to mock the singleton. Or just don’t write the tests. Or don’t use the Singleton pattern.对 Singleton 的客户端代码进行单元测试可能很困难，因为许多测试框架在生成模拟对象时依赖于继承。由于单例类的构造函数是私有的，并且在大多数语言中不可能重写静态方法，因此您需要想出一种创造性的方法来模拟单例。或者干脆不写测试。或者不要使用单一实例模式。 |

## Relations with Other Patterns 与其他模式的关系
* A **Facade** class can often be transformed into a **Singleton** since a single facade object is sufficient in most cases. 
Facade 类通常可以转换为 Singleton，因为在大多数情况下，单个 Facade 对象就足够了。

* **Flyweight** would resemble **Singleton** if you somehow managed to reduce all shared states of the objects to just one flyweight object. But there are two fundamental differences between these patterns:
如果你以某种方式设法将对象的所有共享状态减少到一个蝇量级对象，那么 Flyweight 将类似于 Singleton。但这些模式之间有两个根本区别：
    1. There should be only one Singleton instance, whereas a Flyweight class can have multiple instances with different intrinsic states.
应该只有一个 Singleton 实例，而 Flyweight 类可以有多个具有不同内部状态的实例。
    2. The Singleton object can be mutable. Flyweight objects are immutable.
Singleton 对象可以是可变的。轻量级对象是不可变的。
* Abstract Factories, Builders and Prototypes can all be implemented as Singletons.
抽象工厂、构建器和原型都可以作为单例实现。

## Code Examples 代码示例

### Python: Navie Singleton 简单版
It’s pretty easy to implement a sloppy Singleton. You just need to hide the constructor and implement a static creation method.
实现一个草率的 Singleton 非常容易。你只需要隐藏构造函数并实现一个静态创建方法。

The same class behaves incorrectly in a multithreaded environment. Multiple threads can call the creation method simultaneously and get several instances of Singleton class.
同一类在多线程环境中的行为不正确。多个线程可以同时调用创建方法，并获取 Singleton 类的多个实例。
#### main.py: Conceptual example
```python
class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    def some_business_logic(self):
        """
        Finally, any singleton should define some business logic, which can be
        executed on its instance.
        """

        # ...


if __name__ == "__main__":
    # The client code.

    s1 = Singleton()
    s2 = Singleton()

    if id(s1) == id(s2):
        print("Singleton works, both variables contain the same instance.")
    else:
        print("Singleton failed, variables contain different instances.")
```
#### Output.txt: Execution result
```
Singleton works, both variables contain the same instance.
```

### Python: Thread-safe Singleton 线程安全单例
To fix the problem, you have to synchronize threads during the first creation of the Singleton object.
若要解决此问题，必须在首次创建 Singleton 对象期间同步线程。

#### main.py: Conceptual example
```python
from threading import Lock, Thread


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(metaclass=SingletonMeta):
    value: str = None
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, value: str) -> None:
        self.value = value

    def some_business_logic(self):
        """
        Finally, any singleton should define some business logic, which can be
        executed on its instance.
        """


def test_singleton(value: str) -> None:
    singleton = Singleton(value)
    print(singleton.value)


if __name__ == "__main__":
    # The client code.

    print("If you see the same value, then singleton was reused (yay!)\n"
          "If you see different values, "
          "then 2 singletons were created (booo!!)\n\n"
          "RESULT:\n")

    process1 = Thread(target=test_singleton, args=("FOO",))
    process2 = Thread(target=test_singleton, args=("BAR",))
    process1.start()
    process2.start()
```
#### Output.txt: Execution result
```
If you see the same value, then singleton was reused (yay!)
If you see different values, then 2 singletons were created (booo!!)

RESULT:

FOO
FOO
```

### Rust specifics
By definition, Singleton is a global mutable object. In Rust this is a `static mut` item. Thus, to avoid all sorts of concurrency issues, the function or block that is either reading or writing to a mutable static variable should be marked as an `unsafe` block.
根据定义，Singleton 是一个全局可变对象。在 Rust 中， static mut 这是一个项目。因此，为了避免各种并发问题，应将读取或写入可变静态变量的函数或块标记为 `unsafe` 块。

For this reason, the Singleton pattern can be percieved as unsafe. However, the pattern is still widely used in practice. A good read-world example of Singleton is a `log` crate that introduces `log!`, `debug!` and other logging macros, which you can use throughout your code after setting up a concrete logger instance, such as `env_logger`. As we can see, `env_logger` uses log::set_boxed_logger under the hood, which has an `unsafe` block to set up a global logger object.
因此，Singleton 模式可能被认为是不安全的。然而，该模式在实践中仍然被广泛使用。Singleton 的一个很好的读取世界示例是一个 log crate，它引入了 log! 和其他 debug! 日志记录宏，在设置具体的记录器实例（如 `env_logger`）后，您可以在整个代码中使用这些宏。正如我们所看到的， `env_logger` 在后台使用 log：：set_boxed_logger，它有一个 unsafe 用于设置全局记录器对象的块。
* In order to provide safe and usable access to a singleton object, introduce an API hiding unsafe blocks under the hood.
为了提供对单例对象的安全且可用的访问，请在后台引入一个隐藏 `unsafe` 块的 API。

* See the thread about a mutable Singleton on Stackoverflow for more information.
有关更多信息，请参阅 Stackoverflow 上有关可变 Singleton 的线程。

Starting with Rust 1.63, `Mutex::new` is `const`, you can use global static Mutex locks without needing lazy initialization. See the Singleton using `Mutex` example below.
从 Rust 1.63 开始，您可以使用全局静态 Mutex 锁， `Mutex::new` `const` 而无需延迟初始化。请参阅下面的使用互斥锁的单例示例。

#### Safe Singleton 安全单例
A pure safe way to implement Singleton in Rust is using no global variables at all and passing everything around through function arguments. The oldest living variable is an object created at the start of the `main()`.
在 Rust 中实现 Singleton 的一个纯粹安全的方法是完全不使用全局变量，并通过函数参数传递所有内容。最早的活变量是在 的开头创建的对象 `main()` 。

#### safe.rs
```rust
//! A pure safe way to implement Singleton in Rust is using no static variables
//! and passing everything around through function arguments.
//! The oldest living variable is an object created at the start of the `main()`.

fn change(global_state: &mut u32) {
    *global_state += 1;
}

fn main() {
    let mut global_state = 0u32;

    change(&mut global_state);

    println!("Final state: {}", global_state);
}
```

#### Output
```
Final state: 1
```

#### Lazy Singleton 惰性单例模式
This is a singleton implementation via `lazy_static!`, which allows declaring a static variable with lazy initialization at first access. It is actually implemented via `unsafe` with `static mut` manipulation, however, it keeps your code clear of `unsafe` blocks.
这是一个单例实现，它 lazy_static! 允许在首次访问时使用延迟初始化声明静态变量。它实际上 `unsafe` 是通过 `static mut` 操作实现的，但是，它使您的代码没有 `unsafe` 块。

#### lazy.rs
```rust
//! Taken from: https://stackoverflow.com/questions/27791532/how-do-i-create-a-global-mutable-singleton
//!
//! Rust doesn't really allow a singleton pattern without `unsafe` because it
//! doesn't have a safe mutable global state.
//!
//! `lazy-static` allows declaring a static variable with lazy initialization
//! at first access. It is actually implemented via `unsafe` with `static mut`
//! manipulation, however, it keeps your code clear of `unsafe` blocks.
//!
//! `Mutex` provides safe access to a single object.

use lazy_static::lazy_static;
use std::sync::Mutex;

lazy_static! {
    static ref ARRAY: Mutex<Vec<u8>> = Mutex::new(vec![]);
}

fn do_a_call() {
    ARRAY.lock().unwrap().push(1);
}

fn main() {
    do_a_call();
    do_a_call();
    do_a_call();

    println!("Called {}", ARRAY.lock().unwrap().len());
}
```

#### Output
```
Called 3
```

#### Singleton using Mutex 使用互斥锁的单例
Starting with `Rust 1.63`, it can be easier to work with global mutable singletons, although it’s still preferable to avoid global variables in mostcases.
从 开始 `Rust 1.63` ，使用全局可变单例会更容易，尽管在大多数情况下仍然最好避免全局变量。

Now that `Mutex::new` is `const`, you can use global static `Mutex` locks without needing lazy initialization.
现在 `Mutex::new` ，您可以使用全局静态 `Mutex `锁 `const` ，而无需延迟初始化。
#### mutex.rs
```rust
//! ructc 1.63
//! https://stackoverflow.com/questions/27791532/how-do-i-create-a-global-mutable-singleton
//!
//! Starting with Rust 1.63, it can be easier to work with global mutable
//! singletons, although it's still preferable to avoid global variables in most
//! cases.
//!
//! Now that `Mutex::new` is `const`, you can use global static `Mutex` locks
//! without needing lazy initialization.

use std::sync::Mutex;

static ARRAY: Mutex<Vec<i32>> = Mutex::new(Vec::new());

fn do_a_call() {
    ARRAY.lock().unwrap().push(1);
}

fn main() {
    do_a_call();
    do_a_call();
    do_a_call();

    println!("Called {} times", ARRAY.lock().unwrap().len());
}
```
#### Output
```
Called 3 times
```
