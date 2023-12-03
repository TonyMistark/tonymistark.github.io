---
title: Adapter
categories:
  - design-pattern
tags: Design Pattern
date: 2023-12-03 16:03:51
---

# Adapter 适配器

## Intent 意图
**Adapter** is a structural design pattern that allows objects with incompatible interfaces to collaborate.
适配器是一种结构设计模式，它允许具有不兼容接口的对象进行协作。
<div align="center"> <img src="/images/adapter-header.png"/></div>

## Problem 问题
Imagine that you’re creating a stock market monitoring app. The app downloads the stock data from multiple sources in XML format and then displays nice-looking charts and diagrams for the user.
想象一下，您正在创建一个股票市场监控应用程序。该应用程序以XML格式从多个来源下载股票数据，然后为用户显示漂亮的图表和图表。

At some point, you decide to improve the app by integrating a smart 3rd-party analytics library. But there’s a catch: the analytics library only works with data in JSON format.
在某些时候，您决定通过集成智能第三方分析库来改进应用程序。但有一个问题：分析库仅适用于 JSON 格式的数据。
<div align="center"> <img src="/images/adapter-problem-en.png"/>You can’t use the analytics library “as is” because it expects the data in a format that’s incompatible with your app.</br>您不能“按原样”使用分析库，因为它需要的数据格式与您的应用不兼容。</div>
You could change the library to work with XML. However, this might break some existing code that relies on the library. And worse, you might not have access to the library’s source code in the first place, making this approach impossible.
您可以更改库以使用 XML。但是，这可能会破坏一些依赖于该库的现有代码。更糟糕的是，您可能一开始就无法访问库的源代码，从而无法使用此方法。

## Solution 解决方案
You can create an adapter. This is a special object that converts the interface of one object so that another object can understand it.
您可以创建适配器。这是一个特殊的对象，它转换一个对象的接口，以便另一个对象可以理解它。

An adapter wraps one of the objects to hide the complexity of conversion happening behind the scenes. The wrapped object isn’t even aware of the adapter. For example, you can wrap an object that operates in meters and kilometers with an adapter that converts all of the data to imperial units such as feet and miles.
适配器包装其中一个对象，以隐藏在后台发生的转换的复杂性。包装的对象甚至不知道适配器。例如，您可以使用适配器包装以米和公里为单位运行的对象，该适配器将所有数据转换为英制单位（如英尺和英里）。

Adapters can not only convert data into various formats but can also help objects with different interfaces collaborate. Here’s how it works:
适配器不仅可以将数据转换为各种格式，还可以帮助具有不同接口的对象进行协作。其工作原理如下：
1. The adapter gets an interface, compatible with one of the existing objects.
适配器获取一个接口，该接口与现有对象之一兼容。
2. Using this interface, the existing object can safely call the adapter’s methods.
使用此接口，现有对象可以安全地调用适配器的方法。
3. Upon receiving a call, the adapter passes the request to the second object, but in a format and order that the second object expects.
收到调用后，适配器将请求传递给第二个对象，但采用第二个对象期望的格式和顺序。

Sometimes it’s even possible to create a two-way adapter that can convert the calls in both directions.
有时甚至可以创建一个双向适配器，可以在两个方向上转换呼叫。
<div align="center"> <img src="/images/adapter-solution.png"/></div>
Let’s get back to our stock market app. To solve the dilemma of incompatible formats, you can create XML-to-JSON adapters for every class of the analytics library that your code works with directly. Then you adjust your code to communicate with the library only via these adapters. When an adapter receives a call, it translates the incoming XML data into a JSON structure and passes the call to the appropriate methods of a wrapped analytics object.

让我们回到我们的股票市场应用程序。为了解决格式不兼容的难题，您可以为代码直接使用的分析库的每个类创建 XML 到 JSON 适配器。然后，将代码调整为仅通过这些适配器与库通信。当适配器收到调用时，它会将传入的 XML 数据转换为 JSON 结构，并将调用传递给包装的分析对象的相应方法。

## Real-World Analogy 真实世界的类比
<div align="center"> <img src="/images/adapter-comic-1.png"/>A suitcase before and after a trip abroad.</br>出国旅行前后的行李箱。</div>
When you travel from the US to Europe for the first time, you may get a surprise when trying to charge your laptop. The power plug and sockets standards are different in different countries. That’s why your US plug won’t fit a German socket. The problem can be solved by using a power plug adapter that has the American-style socket and the European-style plug.
当您第一次从美国到欧洲旅行时，当您尝试为笔记本电脑充电时，您可能会感到惊讶。不同国家的电源插头和插座标准不同。这就是为什么您的美国插头不适合德国插座的原因。这个问题可以通过使用具有美式插座和欧式插头的电源插头适配器来解决。

## Structure 结构
### Object adapter 对象适配器
This implementation uses the object composition principle: the adapter implements the interface of one object and wraps the other one. It can be implemented in all popular programming languages.
此实现使用对象组合原则：适配器实现一个对象的接口并包装另一个对象。它可以用所有流行的编程语言实现。
<div align="center"> <img src="/images/adapter-structure-object-adapter.png"/></div>

1. The Client is a class that contains the existing business logic of the program.
Client 是一个包含程序现有业务逻辑的类。

2. The Client Interface describes a protocol that other classes must follow to be able to collaborate with the client code.
客户端接口描述了其他类必须遵循的协议，以便能够与客户端代码进行协作。

3. The Service is some useful class (usually 3rd-party or legacy). The client can’t use this class directly because it has an incompatible interface.
服务是一些有用的类（通常是第三方或旧版）。客户端不能直接使用此类，因为它具有不兼容的接口。

4. The **Adapter** is a class that’s able to work with both the client and the service: it implements the client interface, while wrapping the service object. The adapter receives calls from the client via the client interface and translates them into calls to the wrapped service object in a format it can understand.
Adapter 是一个能够同时使用客户端和服务的类：它实现客户端接口，同时包装服务对象。适配器通过客户端接口接收来自客户端的调用，并以它可以理解的格式将其转换为对包装的服务对象的调用。

5. The client code doesn’t get coupled to the concrete adapter class as long as it works with the adapter via the client interface. Thanks to this, you can introduce new types of adapters into the program without breaking the existing client code. This can be useful when the interface of the service class gets changed or replaced: you can just create a new adapter class without changing the client code.
只要客户端代码通过客户端接口与适配器一起使用，它就不会耦合到具体的适配器类。因此，您可以在不破坏现有客户端代码的情况下将新类型的适配器引入程序。当服务类的接口被更改或替换时，这可能很有用：您可以只创建一个新的适配器类，而无需更改客户端代码。

### Class adapter 类适配器
This implementation uses inheritance: the adapter inherits interfaces from both objects at the same time. Note that this approach can only be implemented in programming languages that support multiple inheritance, such as C++.
此实现使用继承：适配器同时从两个对象继承接口。请注意，此方法只能在支持多重继承的编程语言（如 C++）中实现。
<div align="center"> <img src="/images/adapter-structure-class-adapter.png"/></div>

1. The Class Adapter doesn’t need to wrap any objects because it inherits behaviors from both the client and the service. The adaptation happens within the overridden methods. The resulting adapter can be used in place of an existing client class.
类适配器不需要包装任何对象，因为它从客户端和服务继承行为。适应发生在被覆盖的方法中。生成的适配器可用于代替现有的客户端类。

## Pseudocode 伪代码
This example of the **Adapter** pattern is based on the classic conflict between square pegs and round holes.
此适配器模式示例基于方形钉子和圆孔之间的经典冲突。
<div align="center"> <img src="/images/adapter-example.png"/>Adapting square pegs to round holes.</br>使方钉适应圆孔。</div>
The Adapter pretends to be a round peg, with a radius equal to a half of the square’s diameter (in other words, the radius of the smallest circle that can accommodate the square peg).
适配器假装是一个圆钉，其半径等于正方形直径的一半（换句话说，可以容纳方形钉的最小圆的半径）。

```java
// Say you have two classes with compatible interfaces:
// RoundHole and RoundPeg.
class RoundHole is
    constructor RoundHole(radius) { ... }

    method getRadius() is
        // Return the radius of the hole.

    method fits(peg: RoundPeg) is
        return this.getRadius() >= peg.getRadius()

class RoundPeg is
    constructor RoundPeg(radius) { ... }

    method getRadius() is
        // Return the radius of the peg.


// But there's an incompatible class: SquarePeg.
class SquarePeg is
    constructor SquarePeg(width) { ... }

    method getWidth() is
        // Return the square peg width.


// An adapter class lets you fit square pegs into round holes.
// It extends the RoundPeg class to let the adapter objects act
// as round pegs.
class SquarePegAdapter extends RoundPeg is
    // In reality, the adapter contains an instance of the
    // SquarePeg class.
    private field peg: SquarePeg

    constructor SquarePegAdapter(peg: SquarePeg) is
        this.peg = peg

    method getRadius() is
        // The adapter pretends that it's a round peg with a
        // radius that could fit the square peg that the adapter
        // actually wraps.
        return peg.getWidth() * Math.sqrt(2) / 2


// Somewhere in client code.
hole = new RoundHole(5)
rpeg = new RoundPeg(5)
hole.fits(rpeg) // true

small_sqpeg = new SquarePeg(5)
large_sqpeg = new SquarePeg(10)
hole.fits(small_sqpeg) // this won't compile (incompatible types)

small_sqpeg_adapter = new SquarePegAdapter(small_sqpeg)
large_sqpeg_adapter = new SquarePegAdapter(large_sqpeg)
hole.fits(small_sqpeg_adapter) // true
hole.fits(large_sqpeg_adapter) // false
```

## Applicability 适用性
* **Use the Adapter class when you want to use some existing class, but its interface isn’t compatible with the rest of your code.
如果要使用某些现有类，但其接口与代码的其余部分不兼容，请使用 Adapter 类。**

* The Adapter pattern lets you create a middle-layer class that serves as a translator between your code and a legacy class, a 3rd-party class or any other class with a weird interface.
适配器模式允许您创建一个中间层类，该类充当代码与旧类、第三方类或任何其他具有奇怪接口的类之间的转换器。

* **Use the pattern when you want to reuse several existing subclasses that lack some common functionality that can’t be added to the superclass.
如果要重用多个现有的子类，这些子类缺少一些无法添加到超类的通用功能，请使用该模式。**

* You could extend each subclass and put the missing functionality into new child classes. However, you’ll need to duplicate the code across all of these new classes, which smells really bad.
您可以扩展每个子类，并将缺少的功能放入新的子类中。但是，您需要在所有这些新类中复制代码，这闻起来非常难闻。

The much more elegant solution would be to put the missing functionality into an adapter class. Then you would wrap objects with missing features inside the adapter, gaining needed features dynamically. For this to work, the target classes must have a common interface, and the adapter’s field should follow that interface. This approach looks very similar to the Decorator pattern.
更优雅的解决方案是将缺少的功能放入适配器类中。然后，将缺少特征的对象包装在适配器内，动态获得所需的特征。为此，目标类必须具有通用接口，并且适配器的字段应遵循该接口。此方法看起来与 Decorator 模式非常相似。

## How to Implement 如何实现
1. Make sure that you have at least two classes with incompatible interfaces:确保至少有两个接口不兼容的类：
    * A useful service class, which you can’t change (often 3rd-party, legacy or with lots of existing dependencies).
一个有用的服务类，您无法更改（通常是第三方、旧版或具有大量现有依赖项）。
    * One or several client classes that would benefit from using the service class.
一个或多个客户端类，这些类将从使用服务类中受益。

2. Declare the client interface and describe how clients communicate with the service.
声明客户端接口并描述客户端如何与服务通信。

3. Create the adapter class and make it follow the client interface. Leave all the methods empty for now.
创建适配器类，并使其遵循客户端接口。暂时将所有方法留空。

4. Add a field to the adapter class to store a reference to the service object. The common practice is to initialize this field via the constructor, but sometimes it’s more convenient to pass it to the adapter when calling its methods.
向适配器类添加一个字段，以存储对服务对象的引用。通常的做法是通过构造函数初始化此字段，但有时在调用适配器的方法时将其传递给适配器会更方便。

5. One by one, implement all methods of the client interface in the adapter class. The adapter should delegate most of the real work to the service object, handling only the interface or data format conversion.
在适配器类中逐个实现客户端接口的所有方法。适配器应将大部分实际工作委托给服务对象，仅处理接口或数据格式转换。

6. Clients should use the adapter via the client interface. This will let you change or extend the adapters without affecting the client code.
客户端应通过客户端接口使用适配器。这将允许您更改或扩展适配器，而不会影响客户端代码。

## Pros and Cons 优点和缺点

| Pros 优点 | Cons 缺点 |
| --- | --- |
| Single Responsibility Principle. You can separate the interface or data conversion code from the primary business logic of the program. 单一责任原则。您可以将接口或数据转换代码与程序的主要业务逻辑分开。| The overall complexity of the code increases because you need to introduce a set of new interfaces and classes. Sometimes it’s simpler just to change the service class so that it matches the rest of your code. 代码的整体复杂性增加，因为您需要引入一组新的接口和类。有时，只需更改服务类以使其与代码的其余部分匹配即可更简单。 |
| Open/Closed Principle. You can introduce new types of adapters into the program without breaking the existing client code, as long as they work with the adapters through the client interface. 开/闭原理。您可以在不破坏现有客户端代码的情况下将新类型的适配器引入程序，只要它们通过客户端接口与适配器一起使用即可。|  |

## Relations with Other Patterns 与其他模式的关系

* Bridge is usually designed up-front, letting you develop parts of an application independently of each other. On the other hand, Adapter is commonly used with an existing app to make some otherwise-incompatible classes work together nicely.
Bridge 通常是预先设计的，允许您彼此独立地开发应用程序的各个部分。另一方面，Adapter 通常与现有应用程序一起使用，以使一些不兼容的类很好地协同工作。

* Adapter provides a completely different interface for accessing an existing object. On the other hand, with the Decorator pattern the interface either stays the same or gets extended. In addition, Decorator supports recursive composition, which isn’t possible when you use Adapter.
适配器提供了一个完全不同的接口来访问现有对象。另一方面，使用 Decorator 模式，界面要么保持不变，要么得到扩展。此外，Decorator 支持递归组合，这在使用 Adapter 时是不可能的。

* With Adapter you access an existing object via different interface. With Proxy, the interface stays the same. With Decorator you access the object via an enhanced interface.
使用 Adapter，您可以通过不同的接口访问现有对象。使用 Proxy，界面保持不变。使用 Decorator，您可以通过增强的界面访问对象。

* Facade defines a new interface for existing objects, whereas Adapter tries to make the existing interface usable. Adapter usually wraps just one object, while Facade works with an entire subsystem of objects.
Facade 为现有对象定义了一个新的接口，而 Adapter 则试图使现有接口可用。Adapter 通常只包装一个对象，而 Facade 则处理对象的整个子系统。

* Bridge, State, Strategy (and to some degree Adapter) have very similar structures. Indeed, all of these patterns are based on composition, which is delegating work to other objects. However, they all solve different problems. A pattern isn’t just a recipe for structuring your code in a specific way. It can also communicate to other developers the problem the pattern solves.
桥接、状态、策略（在某种程度上还有适配器）具有非常相似的结构。事实上，所有这些模式都是基于构图的，而构图是将工作委托给其他对象。但是，它们都解决了不同的问题。模式不仅仅是以特定方式构建代码的秘诀。它还可以向其他开发人员传达该模式解决的问题。

## Code Examples 代码示例

### Python: Conceptual Example (via inheritance) 概念示例（通过继承）
This example illustrates the structure of the Adapter design pattern. It focuses on answering these questions:
此示例阐释了适配器设计模式的结构。它侧重于回答以下问题：

* What classes does it consist of?
它由哪些类组成？
* What roles do these classes play?
这些课程扮演什么角色？
* In what way the elements of the pattern are related?
模式的元素以何种方式相关？

### main.py：概念示例
```python
class Target:
    """
    The Target defines the domain-specific interface used by the client code.
    """

    def request(self) -> str:
        return "Target: The default target's behavior."


class Adaptee:
    """
    The Adaptee contains some useful behavior, but its interface is incompatible
    with the existing client code. The Adaptee needs some adaptation before the
    client code can use it.
    """

    def specific_request(self) -> str:
        return ".eetpadA eht fo roivaheb laicepS"


class Adapter(Target, Adaptee):
    """
    The Adapter makes the Adaptee's interface compatible with the Target's
    interface via multiple inheritance.
    """

    def request(self) -> str:
        return f"Adapter: (TRANSLATED) {self.specific_request()[::-1]}"


def client_code(target: "Target") -> None:
    """
    The client code supports all classes that follow the Target interface.
    """

    print(target.request(), end="")


if __name__ == "__main__":
    print("Client: I can work just fine with the Target objects:")
    target = Target()
    client_code(target)
    print("\n")

    adaptee = Adaptee()
    print("Client: The Adaptee class has a weird interface. "
          "See, I don't understand it:")
    print(f"Adaptee: {adaptee.specific_request()}", end="\n\n")

    print("Client: But I can work with it via the Adapter:")
    adapter = Adapter()
    client_code(adapter)
```
### Output.txt: Execution result
```
Client: I can work just fine with the Target objects:
Target: The default target's behavior.

Client: The Adaptee class has a weird interface. See, I don't understand it:
Adaptee: .eetpadA eht fo roivaheb laicepS

Client: But I can work with it via the Adapter:
Adapter: (TRANSLATED) Special behavior of the Adaptee.
```

### Python: Conceptual Example (via object composition) 概念示例（通过对象组合）
This example illustrates the structure of the Adapter design pattern. It focuses on answering these questions:
此示例阐释了适配器设计模式的结构。它侧重于回答以下问题：

* What classes does it consist of?
它由哪些类组成？
* What roles do these classes play?
这些课程扮演什么角色？
* In what way the elements of the pattern are related?
模式的元素以何种方式相关？

### main.py：概念示例
```python
class Target:
    """
    The Target defines the domain-specific interface used by the client code.
    """

    def request(self) -> str:
        return "Target: The default target's behavior."


class Adaptee:
    """
    The Adaptee contains some useful behavior, but its interface is incompatible
    with the existing client code. The Adaptee needs some adaptation before the
    client code can use it.
    """

    def specific_request(self) -> str:
        return ".eetpadA eht fo roivaheb laicepS"


class Adapter(Target):
    """
    The Adapter makes the Adaptee's interface compatible with the Target's
    interface via composition.
    """

    def __init__(self, adaptee: Adaptee) -> None:
        self.adaptee = adaptee

    def request(self) -> str:
        return f"Adapter: (TRANSLATED) {self.adaptee.specific_request()[::-1]}"


def client_code(target: Target) -> None:
    """
    The client code supports all classes that follow the Target interface.
    """

    print(target.request(), end="")


if __name__ == "__main__":
    print("Client: I can work just fine with the Target objects:")
    target = Target()
    client_code(target)
    print("\n")

    adaptee = Adaptee()
    print("Client: The Adaptee class has a weird interface. "
          "See, I don't understand it:")
    print(f"Adaptee: {adaptee.specific_request()}", end="\n\n")

    print("Client: But I can work with it via the Adapter:")
    adapter = Adapter(adaptee)
    client_code(adapter)
```
### Output.txt: Execution result
```
Client: I can work just fine with the Target objects:
Target: The default target's behavior.

Client: The Adaptee class has a weird interface. See, I don't understand it:
Adaptee: .eetpadA eht fo roivaheb laicepS

Client: But I can work with it via the Adapter:
Adapter: (TRANSLATED) Special behavior of the Adaptee.
```

### Adapter in Rust Rust 中的适配器
In this example, the `trait SpecificTarget` is incompatible with a `call` function which accepts `trait Target` only.
在此示例中，与 `trait SpecificTarget` 仅接受 `call` `trait Target` 的函数不兼容。
```Rust
fn call(target: impl Target);
```
The adapter helps to pass the incompatible interface to the `call` function.
适配器有助于将不兼容的接口传递给 `call` 函数。
```Rust
let target = TargetAdapter::new(specific_target);
call(target);
```

#### adapter.rs

```Rust
use crate::{adaptee::SpecificTarget, Target};

/// Converts adaptee's specific interface to a compatible `Target` output.
pub struct TargetAdapter {
    adaptee: SpecificTarget,
}

impl TargetAdapter {
    pub fn new(adaptee: SpecificTarget) -> Self {
        Self { adaptee }
    }
}

impl Target for TargetAdapter {
    fn request(&self) -> String {
        // Here's the "adaptation" of a specific output to a compatible output.
        self.adaptee.specific_request().chars().rev().collect()
    }
}
```

#### adaptee.rs
```Rust
pub struct SpecificTarget;

impl SpecificTarget {
    pub fn specific_request(&self) -> String {
        ".tseuqer cificepS".into()
    }
}
```

#### target.rs
```Rust
pub trait Target {
    fn request(&self) -> String;
}

pub struct OrdinaryTarget;

impl Target for OrdinaryTarget {
    fn request(&self) -> String {
        "Ordinary request.".into()
    }
}
```

#### main.rs
```Rust
mod adaptee;
mod adapter;
mod target;

use adaptee::SpecificTarget;
use adapter::TargetAdapter;
use target::{OrdinaryTarget, Target};

/// Calls any object of a `Target` trait.
///
/// To understand the Adapter pattern better, imagine that this is
/// a client code, which can operate over a specific interface only
/// (`Target` trait only). It means that an incompatible interface cannot be
/// passed here without an adapter.
fn call(target: impl Target) {
    println!("'{}'", target.request());
}

fn main() {
    let target = OrdinaryTarget;

    print!("A compatible target can be directly called: ");
    call(target);

    let adaptee = SpecificTarget;

    println!(
        "Adaptee is incompatible with client: '{}'",
        adaptee.specific_request()
    );

    let adapter = TargetAdapter::new(adaptee);

    print!("But with adapter client can call its method: ");
    call(adapter);
}
```

### Output 输出
```
A compatible target can be directly called: 'Ordinary request.'
Adaptee is incompatible with client: '.tseuqer cificepS'
But with adapter client can call its method: 'Specific request.'
```

