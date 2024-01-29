---
title: Decorator 装饰器模式
categories:
  - design-pattern
tags: Design Pattern
date: 2024-01-28 13:26:52
---

# Decorator 装饰器模式

## Intent 意图

**Decorator**  is a structural design pattern that lets you attach new behaviors to objects by placing these objects inside special wrapper objects that contain the behaviors.  
**装饰器**是一种结构化设计模式，它允许您将新行为附加到对象，方法是将这些对象放置在包含行为的特殊包装器对象中。


<div align="center"> <img src="/images/decorator.png"/></div>


## Problem  问题

Imagine that you’re working on a notification library which lets other programs notify their users about important events.  
假设您正在处理一个通知库，该库允许其他程序通知其用户有关重要事件。

The initial version of the library was based on the `Notifier` class that had only a few fields, a constructor and a single `send` method. The method could accept a message argument from a client and send the message to a list of emails that were passed to the notifier via its constructor. A third-party app which acted as a client was supposed to create and configure the notifier object once, and then use it each time something important happened.  
该库的初始版本基于只有几个字段、一个构造函数和一个 `send` 方法的 `Notifier` 类。该方法可以接受来自客户端的消息参数，并将消息发送到通过其构造函数传递给通知程序的电子邮件列表。作为客户端的第三方应用程序应该创建和配置一次通知程序对象，然后在每次发生重要事件时使用它。


<div align="center"> <img src="/images/decorator-problem1.png"/>A program could use the notifier class to send notifications about important events to a predefined set of emails.</br>程序可以使用notifier类将有关重要事件的通知发送到一组预定义的电子邮件。</div>


At some point, you realize that users of the library expect more than just email notifications. Many of them would like to receive an SMS about critical issues. Others would like to be notified on Facebook and, of course, the corporate users would love to get Slack notifications.在某种程度上，您意识到图书馆的用户期望的不仅仅是电子邮件通知。他们中的许多人希望收到关于关键问题的短信。其他人希望在Facebook上获得通知，当然，企业用户也希望获得Slack通知。


<div align="center"> <img src="/images/decorator-problem2.png"/>Each notification type is implemented as a notifier’s subclass.</br>每个通知类型都作为通知程序的子类实现。</div>


How hard can that be? You extended the `Notifier` class and put the additional notification methods into new subclasses. Now the client was supposed to instantiate the desired notification class and use it for all further notifications.  
这能有多难您扩展了 `Notifier` 类，并将额外的通知方法放入新的子类中。现在，客户端应该实例化所需的通知类，并将其用于所有进一步的通知。

But then someone reasonably asked you, “Why can’t you use several notification types at once? If your house is on fire, you’d probably want to be informed through every channel.”  
但是后来有人合理地问你，“为什么你不能同时使用几种通知类型？如果你的房子着火了，你可能希望通过各种渠道得到通知。“

You tried to address that problem by creating special subclasses which combined several notification methods within one class. However, it quickly became apparent that this approach would bloat the code immensely, not only the library code but the client code as well.  
您试图通过创建特殊的子类来解决这个问题，这些子类在一个类中组合了几个通知方法。然而，很快就发现这种方法会极大地膨胀代码，不仅是库代码，而且还有客户机代码。


<div align="center"> <img src="/images/decorator-problem2.png"/>Combinatorial explosion of subclasses.</br>子类的组合爆炸。</div>


You have to find some other way to structure notifications classes so that their number won’t accidentally break some Guinness record.您必须找到其他方法来构造通知类，以便它们的数量不会意外地打破吉尼斯记录。

## Solution  解决方案

Extending a class is the first thing that comes to mind when you need to alter an object’s behavior. However, inheritance has several serious caveats that you need to be aware of.  
当您需要改变对象的行为时，首先想到的是扩展类。然而，继承有几个严重的警告，你需要知道。

- Inheritance is static. You can’t alter the behavior of an existing object at runtime. You can only replace the whole object with another one that’s created from a different subclass.  
  继承是静态的。不能在运行时改变现有对象的行为。你只能用另一个从不同子类创建的对象替换整个对象。
- Subclasses can have just one parent class. In most languages, inheritance doesn’t let a class inherit behaviors of multiple classes at the same time.  
  子类只能有一个父类。在大多数语言中，继承不会让一个类同时继承多个类的行为。

One of the ways to overcome these caveats is by using *Aggregation* or *Composition*  instead of *Inheritance*. Both of the alternatives work almost the same way: one object *has a* reference to another and delegates it some work, whereas with inheritance, the object itself *is* able to do that work, inheriting the behavior from its superclass.  
克服这些警告的方法之一是使用聚合或组合而不是继承。这两种替代方法的工作方式几乎相同：一个对象引用另一个对象并委托它一些工作，而继承，对象本身能够完成这项工作，从其超类继承行为。

With this new approach you can easily substitute the linked “helper” object with another, changing the behavior of the container at runtime. An object can use the behavior of various classes, having references to multiple objects and delegating them all kinds of work. Aggregation/composition is the key principle behind many design patterns, including Decorator. On that note, let’s return to the pattern discussion.  
使用这种新方法，您可以轻松地将链接的“helper”对象替换为另一个对象，从而在运行时更改容器的行为。一个对象可以使用各种类的行为，引用多个对象并将各种工作委托给它们。聚合/组合是许多设计模式背后的关键原则，包括Decorator。在这一点上，让我们回到模式讨论。


<div align="center"> <img src="/images/decorator-solution1.png"/>Inheritance vs. Aggregation</br>继承与聚合</div>


“Wrapper” is the alternative nickname for the Decorator pattern that clearly expresses the main idea of the pattern. A *wrapper* is an object that can be linked with some *target* object. The wrapper contains the same set of methods as the target and delegates to it all requests it receives. However, the wrapper may alter the result by doing something either before or after it passes the request to the target.  
“Wrapper”是Decorator模式的另一个昵称，它清楚地表达了该模式的主要思想。包装器是可以与某个目标对象链接的对象。包装器包含与目标相同的方法集，并将其接收的所有请求委托给它。但是，包装器可以在将请求传递给目标之前或之后执行某些操作，从而改变结果。

When does a simple wrapper become the real decorator? As I mentioned, the wrapper implements the same interface as the wrapped object. That’s why from the client’s perspective these objects are identical. Make the wrapper’s reference field accept any object that follows that interface. This will let you cover an object in multiple wrappers, adding the combined behavior of all the wrappers to it.  
什么时候简单的包装器变成了真实的装饰器？正如我提到的，包装器实现了与被包装对象相同的接口。这就是为什么从客户的角度来看，这些对象是相同的。使包装器的引用字段接受该接口后面的任何对象。这将允许您在多个包装器中覆盖一个对象，并将所有包装器的组合行为添加到该对象中。

In our notifications example, let’s leave the simple email notification behavior inside the base `Notifier` class, but turn all other notification methods into decorators.  
在我们的通知示例中，让我们将简单的电子邮件通知行为留在基类 `Notifier` 中，但将所有其他通知方法转换为装饰器。


<div align="center"> <img src="/images/decorator-solution2.png"/>Various notification methods become decorators.</br>各种通知方法成为装饰器。</div>


The client code would need to wrap a basic notifier object into a set of decorators that match the client’s preferences. The resulting objects will be structured as a stack.客户机代码需要将一个基本的通知程序对象包装到一组符合客户机偏好的装饰器中。生成的对象将被构造为堆栈。


<div align="center"> <img src="/images/decorator-solution2.png"/>Apps might configure complex stacks of notification decorators.</br>应用程序可能会配置复杂的通知装饰器堆栈。</div>


The last decorator in the stack would be the object that the client actually works with. Since all decorators implement the same interface as the base notifier, the rest of the client code won’t care whether it works with the “pure” notifier object or the decorated one.  
堆栈中的最后一个装饰器将是客户端实际使用的对象。由于所有装饰器都实现了与基本通知器相同的接口，因此客户端代码的其余部分不会关心它是与“纯”通知器对象一起工作还是与装饰的通知器对象一起工作。

We could apply the same approach to other behaviors such as formatting messages or composing the recipient list. The client can decorate the object with any custom decorators, as long as they follow the same interface as the others.  
我们可以将相同的方法应用于其他行为，例如格式化消息或编写收件人列表。客户端可以使用任何自定义装饰器来装饰对象，只要它们遵循与其他装饰器相同的接口即可。

## Real-World Analogy  现实世界的类比


<div align="center"> <img src="/images/decorator-comic-1.png"/>You get a combined effect from wearing multiple pieces of clothing.</br>你会从穿多件衣服中得到一个综合效果。</div>


Wearing clothes is an example of using decorators. When you’re cold, you wrap yourself in a sweater. If you’re still cold with a sweater, you can wear a jacket on top. If it’s raining, you can put on a raincoat. All of these garments “extend” your basic behavior but aren’t part of you, and you can easily take off any piece of clothing whenever you don’t need it.  
穿衣服是使用装饰器的一个例子。当你冷的时候，你会把自己裹在毛衣里。如果你穿毛衣还是觉得冷，你可以在上面穿一件夹克。如果下雨，你可以穿上雨衣。所有这些衣服都“延伸”了你的基本行为，但不是你的一部分，你可以在不需要的时候轻松地脱掉任何一件衣服。

## Structure  结构




<div align="center"> <img src="/images/decorator-structure1.png"/></div>


1. The **Component** declares the common interface for both wrappers and wrapped objects.  
   组件声明了包装器和包装对象的公共接口。
2. **Concrete Component** is a class of objects being wrapped. It defines the basic behavior, which can be altered by decorators.  
   具体组件是一个被包装的对象类。它定义了基本的行为，可以由装饰器修改。
3. The **Base Decorator** class has a field for referencing a wrapped object. The field’s type should be declared as the component interface so it can contain both concrete components and decorators. The base decorator delegates all operations to the wrapped object.  
   BaseDecorator类有一个用于引用包装对象的字段。字段的类型应该被声明为组件接口，这样它就可以包含具体的组件和装饰器。基本装饰器将所有操作委托给包装对象。
4. **Concrete Decorators** define extra behaviors that can be added to components dynamically. Concrete decorators override methods of the base decorator and execute their behavior either before or after calling the parent method.  
   具体装饰器定义了可以动态添加到组件的额外行为。具体装饰器覆盖基本装饰器的方法，并在调用父方法之前或之后执行它们的行为。
5. The **Client** can wrap components in multiple layers of decorators, as long as it works with all objects via the component interface.  
   客户端可以将组件包装在多层装饰器中，只要它通过组件接口与所有对象一起工作。

##  Pseudocode  伪代码

In this example, the In this example, the **Decorator** pattern lets you compress and encrypt sensitive data independently from the code that actually uses this data. pattern lets you compress and encrypt sensitive data independently from the code that actually uses this data.在本例中，Decorator模式允许您独立于实际使用敏感数据的代码来压缩和加密这些数据。


<div align="center"> <img src="/images/decorator-example1.png"/>The encryption and compression decorators example.</br>加密和压缩装饰器示例。</div>


The application wraps the data source object with a pair of decorators. Both wrappers change the way the data is written to and read from the disk:  
应用程序用一对装饰器包装数据源对象。这两种包装器都改变了数据写入磁盘和从磁盘读取的方式：

- Just before the data is **written to disk**, the decorators encrypt and compress it. The original class writes the encrypted and protected data to the file without knowing about the change.  
  就在数据写入磁盘之前，装饰器加密并压缩数据。原始类将加密和保护的数据写入文件，而不知道更改。
- Right after the data is **read from disk**, it goes through the same decorators, which decompress and decode it.  
  在从磁盘读取数据之后，它会经过相同的装饰器，这些装饰器会对数据进行加密和解码。

The decorators and the data source class implement the same interface, which makes them all interchangeable in the client code.  
装饰器和数据源类实现了相同的接口，这使得它们在客户端代码中可以互换。

```java
// The component interface defines operations that can be
// altered by decorators.
interface DataSource is
    method writeData(data)
    method readData():data

// Concrete components provide default implementations for the
// operations. There might be several variations of these
// classes in a program.
class FileDataSource implements DataSource is
    constructor FileDataSource(filename) { ... }

    method writeData(data) is
        // Write data to file.

    method readData():data is
        // Read data from file.

// The base decorator class follows the same interface as the
// other components. The primary purpose of this class is to
// define the wrapping interface for all concrete decorators.
// The default implementation of the wrapping code might include
// a field for storing a wrapped component and the means to
// initialize it.
class DataSourceDecorator implements DataSource is
    protected field wrappee: DataSource

    constructor DataSourceDecorator(source: DataSource) is
        wrappee = source

    // The base decorator simply delegates all work to the
    // wrapped component. Extra behaviors can be added in
    // concrete decorators.
    method writeData(data) is
        wrappee.writeData(data)

    // Concrete decorators may call the parent implementation of
    // the operation instead of calling the wrapped object
    // directly. This approach simplifies extension of decorator
    // classes.
    method readData():data is
        return wrappee.readData()

// Concrete decorators must call methods on the wrapped object,
// but may add something of their own to the result. Decorators
// can execute the added behavior either before or after the
// call to a wrapped object.
class EncryptionDecorator extends DataSourceDecorator is
    method writeData(data) is
        // 1. Encrypt passed data.
        // 2. Pass encrypted data to the wrappee's writeData
        // method.

    method readData():data is
        // 1. Get data from the wrappee's readData method.
        // 2. Try to decrypt it if it's encrypted.
        // 3. Return the result.

// You can wrap objects in several layers of decorators.
class CompressionDecorator extends DataSourceDecorator is
    method writeData(data) is
        // 1. Compress passed data.
        // 2. Pass compressed data to the wrappee's writeData
        // method.

    method readData():data is
        // 1. Get data from the wrappee's readData method.
        // 2. Try to decompress it if it's compressed.
        // 3. Return the result.


// Option 1. A simple example of a decorator assembly.
class Application is
    method dumbUsageExample() is
        source = new FileDataSource("somefile.dat")
        source.writeData(salaryRecords)
        // The target file has been written with plain data.

        source = new CompressionDecorator(source)
        source.writeData(salaryRecords)
        // The target file has been written with compressed
        // data.

        source = new EncryptionDecorator(source)
        // The source variable now contains this:
        // Encryption > Compression > FileDataSource
        source.writeData(salaryRecords)
        // The file has been written with compressed and
        // encrypted data.


// Option 2. Client code that uses an external data source.
// SalaryManager objects neither know nor care about data
// storage specifics. They work with a pre-configured data
// source received from the app configurator.
class SalaryManager is
    field source: DataSource

    constructor SalaryManager(source: DataSource) { ... }

    method load() is
        return source.readData()

    method save() is
        source.writeData(salaryRecords)
    // ...Other useful methods...


// The app can assemble different stacks of decorators at
// runtime, depending on the configuration or environment.
class ApplicationConfigurator is
    method configurationExample() is
        source = new FileDataSource("salary.dat")
        if (enabledEncryption)
            source = new EncryptionDecorator(source)
        if (enabledCompression)
            source = new CompressionDecorator(source)

        logger = new SalaryManager(source)
        salary = logger.load()
    // ...
```

## Applicability  适用性

- Use the Decorator pattern when you need to be able to assign extra behaviors to objects at runtime without breaking the code that uses these objects.  
  当您需要能够在运行时为对象分配额外的行为而不破坏使用这些对象的代码时，请使用装饰器模式。

- The Decorator lets you structure your business logic into layers, create a decorator for each layer and compose objects with various combinations of this logic at runtime. The client code can treat all these objects in the same way, since they all follow a common interface.  
  Decorator允许您将业务逻辑结构化到层中，为每一层创建一个装饰器，并在运行时使用此逻辑的各种组合来组合对象。客户端代码可以以相同的方式处理所有这些对象，因为它们都遵循一个公共接口。

- Use the pattern when it’s awkward or not possible to extend an object’s behavior using inheritance.  
  当难以或不可能使用继承扩展对象的行为时，请使用该模式。

- Many programming languages have the `final` keyword that can be used to prevent further extension of a class. For a final class, the only way to reuse the existing behavior would be to wrap the class with your own wrapper, using the Decorator pattern.  
  许多编程语言都有 `final` 关键字，可以用来防止类的进一步扩展。对于最后一个类，重用现有行为的唯一方法是使用自己的包装器（使用Decorator模式）包装该类。

## How to Implement 如何实施

1. Make sure your business domain can be represented as a primary component with multiple optional layers over it.  
   确保您的业务域可以表示为一个主要组件，在其上有多个可选层。
2. Figure out what methods are common to both the primary component and the optional layers. Create a component interface and declare those methods there.  
   找出主要组件和可选层共有的方法。创建一个组件接口并在那里声明这些方法。
3. Create a concrete component class and define the base behavior in it.  
   创建一个具体的组件类，并在其中定义基本行为。
4. Create a base decorator class. It should have a field for storing a reference to a wrapped object. The field should be declared with the component interface type to allow linking to concrete components as well as decorators. The base decorator must delegate all work to the wrapped object.  
   创建一个基本装饰器类。它应该有一个用于存储对包装对象的引用的字段。该字段应该用组件接口类型声明，以允许链接到具体的组件以及装饰器。基本装饰器必须将所有工作委托给包装对象。
5. Make sure all classes implement the component interface.  
   确保所有类都实现组件接口。
6. Create concrete decorators by extending them from the base decorator. A concrete decorator must execute its behavior before or after the call to the parent method (which always delegates to the wrapped object).  
   通过从基本装饰器扩展它们来创建具体的装饰器。一个具体的装饰器必须在调用父方法之前或之后执行它的行为（父方法总是委托给被包装的对象）。
7. The client code must be responsible for creating decorators and composing them in the way the client needs.  
   客户端代码必须负责创建装饰器并以客户端需要的方式组合它们。

##  Pros and Cons  
利弊

-  You can extend an object’s behavior without making a new subclass.  
  你可以扩展一个对象的行为而不需要创建一个新的子类。
-  You can add or remove responsibilities from an object at runtime.  
  您可以在运行时添加或删除对象的责任。
-  You can combine several behaviors by wrapping an object into multiple decorators.  
  通过将一个对象包装到多个装饰器中，可以联合收割机组合多种行为。
-  *Single Responsibility Principle*. You can divide a monolithic class that implements many possible variants of behavior into several smaller classes.  
  单一责任原则。您可以将实现许多可能的行为变体的单体类划分为几个较小的类。

-  It’s hard to remove a specific wrapper from the wrappers stack.  
  很难从wrapper堆栈中删除特定的wrapper。
-  It’s hard to implement a decorator in such a way that its behavior doesn’t depend on the order in the decorators stack.  
  很难实现一个装饰器，使其行为不依赖于装饰器堆栈中的顺序。
-  The initial configuration code of layers might look pretty ugly.  
  层的初始配置代码可能看起来很难看。

##  Relations with Other Patterns  
与其他模式的关系

- [Adapter](https://refactoring.guru/design-patterns/adapter) provides a completely different interface for accessing an existing object. On the other hand, with the [Decorator](https://refactoring.guru/design-patterns/decorator) pattern the interface either stays the same or gets extended. In addition, *Decorator* supports recursive composition, which isn’t possible when you use *Adapter*.  
  Adapter为访问现有对象提供了一个完全不同的接口。另一方面，对于Decorator模式，接口要么保持不变，要么得到扩展。此外，Decorator支持递归组合，这在使用Adapter时是不可能的。
- With [Adapter](https://refactoring.guru/design-patterns/adapter) you access an existing object via different interface. With [Proxy](https://refactoring.guru/design-patterns/proxy), the interface stays the same. With [Decorator](https://refactoring.guru/design-patterns/decorator) you access the object via an enhanced interface.  
  使用Adapter，您可以通过不同的接口访问现有对象。使用Proxy，接口保持不变。使用Decorator，您可以通过增强的接口访问对象。
- [Chain of Responsibility](https://refactoring.guru/design-patterns/chain-of-responsibility) and [Decorator](https://refactoring.guru/design-patterns/decorator) have very similar class structures. Both patterns rely on recursive composition to pass the execution through a series of objects. However, there are several crucial differences.  
  Chain of Responsibility和Decorator具有非常相似的类结构。这两种模式都依赖于递归组合来通过一系列对象传递执行。然而，有几个关键的区别。

  The *CoR* handlers can execute arbitrary operations independently of each other. They can also stop passing the request further at any point. On the other hand, various *Decorators* can extend the object’s behavior while keeping it consistent with the base interface. In addition, decorators aren’t allowed to break the flow of the request.  
CoR处理程序可以彼此独立地执行任意操作。他们也可以在任何时候停止进一步传递请求。另一方面，各种装饰器可以扩展对象的行为，同时保持它与基接口的一致性。此外，装饰器不允许中断请求流。

- [Composite](https://refactoring.guru/design-patterns/composite) and [Decorator](https://refactoring.guru/design-patterns/decorator) have similar structure diagrams since both rely on recursive composition to organize an open-ended number of objects.  
  Composite和Decorator具有类似的结构图，因为它们都依赖于递归组合来组织开放数量的对象。

  A *Decorator* is like a *Composite* but only has one child component. There’s another significant difference: *Decorator* adds additional responsibilities to the wrapped object, while *Composite* just “sums up” its children’s results.  
Decorator类似于Composite，但只有一个子组件。还有另一个显著的区别：Decorator为包装的对象添加了额外的责任，而Composite只是“总结”其子对象的结果。

  However, the patterns can also cooperate: you can use *Decorator* to extend the behavior of a specific object in the *Composite* tree.  
然而，模式也可以合作：您可以使用Decorator来扩展Composite树中特定对象的行为。

- Designs that make heavy use of [Composite](https://refactoring.guru/design-patterns/composite) and [Decorator](https://refactoring.guru/design-patterns/decorator) can often benefit from using [Prototype](https://refactoring.guru/design-patterns/prototype). Applying the pattern lets you clone complex structures instead of re-constructing them from scratch.  
  大量使用Composite和Decorator的设计通常可以从使用Prototype中受益。应用该模式可以克隆复杂的结构，而不是从头开始重新构造它们。
- [Decorator](https://refactoring.guru/design-patterns/decorator) lets you change the skin of an object, while [Strategy](https://refactoring.guru/design-patterns/strategy) lets you change the guts.  
  Decorator允许您更改对象的皮肤，而Strategy允许您更改内部。
- [Decorator](https://refactoring.guru/design-patterns/decorator) and [Proxy](https://refactoring.guru/design-patterns/proxy) have similar structures, but very different intents. Both patterns are built on the composition principle, where one object is supposed to delegate some of the work to another. The difference is that a *Proxy* usually manages the life cycle of its service object on its own, whereas the composition of *Decorators* is always controlled by the client.  
  Decorator和Proxy具有类似的结构，但意图非常不同。这两种模式都建立在组合原则上，其中一个对象应该将一些工作委托给另一个对象。不同之处在于，Proxy通常自己管理其服务对象的生命周期，而Decorators的组成始终由客户端控制。

# **Decorator** in Python Python中的Decorator

**Decorator** is a structural pattern that allows adding new behaviors to objects dynamically by placing them inside special wrapper objects, called *decorators*.  
装饰器是一种结构化模式，它允许通过将对象放置在特殊的包装器对象（称为装饰器）中来动态地向对象添加新行为。

Using decorators you can wrap objects countless number of times since both target objects and decorators follow the same interface. The resulting object will get a stacking behavior of all wrappers.  
使用装饰器，你可以无数次地包装对象，因为目标对象和装饰器都遵循相同的接口。结果对象将获得所有包装器的堆叠行为。

## Conceptual Example 概念示例

This example illustrates the structure of the **Decorator** design pattern. It focuses on answering these questions:  
这个例子说明了装饰器设计模式的结构。它侧重于回答这些问题：

- What classes does it consist of?  
  它由哪些类组成？
- What roles do these classes play?  
  这些班级扮演什么角色？
- In what way the elements of the pattern are related?  
  模式中的元素是以什么方式联系在一起的？

#### main.py：概念性示例

```python
class Component():
    """
    The base Component interface defines operations that can be altered by
    decorators.
    """

    def operation(self) -> str:
        pass


class ConcreteComponent(Component):
    """
    Concrete Components provide default implementations of the operations. There
    might be several variations of these classes.
    """

    def operation(self) -> str:
        return "ConcreteComponent"


class Decorator(Component):
    """
    The base Decorator class follows the same interface as the other components.
    The primary purpose of this class is to define the wrapping interface for
    all concrete decorators. The default implementation of the wrapping code
    might include a field for storing a wrapped component and the means to
    initialize it.
    """

    _component: Component = None

    def __init__(self, component: Component) -> None:
        self._component = component

    @property
    def component(self) -> Component:
        """
        The Decorator delegates all work to the wrapped component.
        """

        return self._component

    def operation(self) -> str:
        return self._component.operation()


class ConcreteDecoratorA(Decorator):
    """
    Concrete Decorators call the wrapped object and alter its result in some
    way.
    """

    def operation(self) -> str:
        """
        Decorators may call parent implementation of the operation, instead of
        calling the wrapped object directly. This approach simplifies extension
        of decorator classes.
        """
        return f"ConcreteDecoratorA({self.component.operation()})"


class ConcreteDecoratorB(Decorator):
    """
    Decorators can execute their behavior either before or after the call to a
    wrapped object.
    """

    def operation(self) -> str:
        return f"ConcreteDecoratorB({self.component.operation()})"


def client_code(component: Component) -> None:
    """
    The client code works with all objects using the Component interface. This
    way it can stay independent of the concrete classes of components it works
    with.
    """

    # ...

    print(f"RESULT: {component.operation()}", end="")

    # ...


if __name__ == "__main__":
    # This way the client code can support both simple components...
    simple = ConcreteComponent()
    print("Client: I've got a simple component:")
    client_code(simple)
    print("\n")

    # ...as well as decorated ones.
    #
    # Note how decorators can wrap not only simple components but the other
    # decorators as well.
    decorator1 = ConcreteDecoratorA(simple)
    decorator2 = ConcreteDecoratorB(decorator1)
    print("Client: Now I've got a decorated component:")
    client_code(decorator2)
```

#### Output.txt：执行结果

````
Client: I've got a simple component:
RESULT: ConcreteComponent

Client: Now I've got a decorated component:
RESULT: ConcreteDecoratorB(ConcreteDecoratorA(ConcreteComponent))
````

# **Decorator** in Rust 饰Rust

**Decorator** is a structural pattern that allows adding new behaviors to objects dynamically by placing them inside special wrapper objects, called *decorators*.  
装饰器是一种结构化模式，它允许通过将对象放置在特殊的包装器对象（称为装饰器）中来动态地向对象添加新行为。

Using decorators you can wrap objects countless number of times since both target objects and decorators follow the same interface. The resulting object will get a stacking behavior of all wrappers.  
使用装饰器，你可以无数次地包装对象，因为目标对象和装饰器都遵循相同的接口。结果对象将获得所有包装器的堆叠行为。

## Input streams decoration  
输入流装饰

There is a ***practical example***  in Rust’s standard library for input/output operations.  
在Rust的标准库中有一个实际的输入/输出操作示例。

A buffered reader decorates a vector reader adding buffered behavior.  
缓冲读取器装饰添加缓冲行为的向量读取器。

```rust
let mut input = BufReader::new(Cursor::new("Input data"));
input.read(&mut buf).ok();

```

#### **main.rs**

```rust
use std::io::{BufReader, Cursor, Read};

fn main() {
    let mut buf = [0u8; 10];

    // A buffered reader decorates a vector reader which wraps input data.
    let mut input = BufReader::new(Cursor::new("Input data"));

    input.read(&mut buf).ok();

    print!("Read from a buffered reader: ");

    for byte in buf {
        print!("{}", char::from(byte));
    }

    println!();
}

```

### Output 输出

```rust
Read from a buffered reader: Input data
```

