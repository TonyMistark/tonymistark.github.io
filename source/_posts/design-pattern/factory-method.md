---
title: Factory Method
categories:
  - design-pattern
tags: Design Pattern
date: 2023-11-16 21:02:09
---
# Factory Method 
# 工厂方法
Also known as: Virtual Constructor
也称为： Virtual Constructor
## Intent 意图

Factory Method is a creational design pattern that provides an interface for creating objects in a superclass, but allows subclasses to alter the type of objects that will be created.

工厂方法是一种创建设计模式，它提供了一个接口，用于在超类中创建对象，但允许子类更改将要创建的对象的类型。
![](/images/factory-method-en.png)

Factory Method pattern
## Problem 问题
Imagine that you’re creating a logistics management application. The first version of your app can only handle transportation by trucks, so the bulk of your code lives inside the Truck class.
假设您正在创建一个物流管理应用程序。应用的第一个版本只能处理卡车运输，因此大部分代码都位于 Truck 类中。

After a while, your app becomes pretty popular. Each day you receive dozens of requests from sea transportation companies to incorporate sea logistics into the app.

一段时间后，您的应用程序变得非常受欢迎。每天，您都会收到数十个来自海运公司的请求，要求将海运物流纳入应用程序。
<div align="center"> <img src="/images/problem1-en.png"/> Adding a new class to the program isn’t that simple if the rest of the code is already coupled to existing classes.</br>如果代码的其余部分已经耦合到现有类，则向程序添加新类并不那么简单。 </div>

Great news, right? But how about the code? At present, most of your code is coupled to the `Truck` class. Adding `Ships` into the app would require making changes to the entire codebase. Moreover, if later you decide to add another type of transportation to the app, you will probably need to make all of these changes again.
好消息，对吧？但是代码呢？目前，您的大部分代码都与类 Truck 耦合。添加到 Ships 应用程序中需要对整个代码库进行更改。此外，如果您以后决定向应用程序添加另一种类型的交通工具，您可能需要再次进行所有这些更改。

As a result, you will end up with pretty nasty code, riddled with conditionals that switch the app’s behavior depending on the class of transportation objects.
结果，你最终会得到非常讨厌的代码，其中充斥着条件，这些条件根据运输对象的类别来切换应用程序的行为。

## Solution 解决方案
The Factory Method pattern suggests that you replace direct object construction calls (using the new operator) with calls to a special factory method. Don’t worry: the objects are still created via the new operator, but it’s being called from within the factory method. Objects returned by a factory method are often referred to as products.
工厂方法模式建议将直接对象构造调用（使用运 new 算符）替换为对特殊工厂方法的调用。不用担心：对象仍然是通过运算符 new 创建的，但它是从工厂方法中调用的。工厂方法返回的对象通常称为产品。

<div align="center"> <img src="/images/solution1.png"/> Subclasses can alter the class of objects being returned by the factory method.</br>子类可以更改工厂方法返回的对象的类。</div>

At first glance, this change may look pointless: we just moved the constructor call from one part of the program to another. However, consider this: now you can override the factory method in a subclass and change the class of products being created by the method.

乍一看，这种变化可能看起来毫无意义：我们只是将构造函数调用从程序的一部分移动到另一部分。但是，请考虑以下情况：现在您可以在子类中重写工厂方法，并更改该方法创建的产品类。

There’s a slight limitation though: subclasses may return different types of products only if these products have a common base class or interface. Also, the factory method in the base class should have its return type declared as this interface.

但是有一个轻微的限制：只有当这些产品具有共同的基类或接口时，子类才能返回不同类型的产品。此外，基类中的工厂方法应将其返回类型声明为此接口。

The structure of the products hierarchy
All products must follow the same interface.
所有产品必须遵循相同的界面。

<div align="center"> <img src="/images/solution1.png"/>All products must follow the same interface.</br>所有产品必须遵循相同的界面。</div>

For example, both `Truck` and `Ship` classes should implement the `Transport` interface, which declares a method called `deliver`. Each class implements this method differently: trucks deliver cargo by land, ships deliver cargo by sea. The factory method in the `RoadLogistics` class returns truck objects, whereas the factory method in the `SeaLogistics` class returns ships.
例如，和类都应该 `Truck` 实现接口 `Transport` ，该接口声明了一个名为 `deliver` . `Ship` 每个类别都以不同的方式实现这种方法：卡车通过陆路运送货物，船舶通过海上运送货物。 `RoadLogistics` 类中的 `factory` 方法返回 `truck` 对象，而 `SeaLogistics` 类中的 `factory` 方法返回 `ships`。

<div align="center"> <img src="/images/solution2.png"/>As long as all product classes implement a common interface, you can pass their objects to the client code without breaking it.</br>只要所有产品类都实现一个通用接口，就可以将其对象传递给客户端代码，而不会中断它。</div>

The code that uses the factory method (often called the client code) doesn’t see a difference between the actual products returned by various subclasses. The client treats all the products as abstract `Transport`. The client knows that all transport objects are supposed to have the `deliver` method, but exactly how it works isn’t important to the client.
使用工厂方法的代码（通常称为客户端代码）看不到各个子类返回的实际产品之间的差异。客户将所有产品视为抽象 `Transport` 产品。客户端知道所有传输对象都应该具有该 `deliver` 方法，但其工作方式对客户端来说并不重要。

## Structure 结构
<div align="center"> <img src="/images/structure.png"/></div>

#### 1.Prodcut
The Product declares the interface, which is common to all objects that can be produced by the creator and its subclasses.

Product 声明接口，该接口对于创建者及其子类可以生成的所有对象都是通用的。

#### 2.Concrete Products
Concrete Products are different implementations of the product interface.
具体产品是产品接口的不同实现。

#### 3.Creator
The Creator class declares the factory method that returns new product objects. It’s important that the return type of this method matches the product interface.

Creator 类声明返回新产品对象的工厂方法。此方法的返回类型必须与产品接口匹配，这一点很重要。

You can declare the factory method as abstract to force all subclasses to implement their own versions of the method. As an alternative, the base factory method can return some default product type.

您可以声明工厂方法，以 abstract 强制所有子类实现其自己的方法版本。或者，基工厂方法可以返回一些默认产品类型。

Note, despite its name, product creation is not the primary responsibility of the creator. Usually, the creator class already has some core business logic related to products. The factory method helps to decouple this logic from the concrete product classes. Here is an analogy: a large software development company can have a training department for programmers. However, the primary function of the company as a whole is still writing code, not producing programmers.

请注意，尽管它的名字，产品创建并不是创建者的主要责任。通常，creator 类已经有一些与产品相关的核心业务逻辑。工厂方法有助于将此逻辑与具体的产品类分离。打个比方：一家大型软件开发公司可以有一个程序员培训部门。然而，整个公司的主要职能仍然是编写代码，而不是培养程序员。

#### 4.Concrete Creators
Concrete Creators override the base factory method so it returns a different type of product.
Concrete Creators 会重写基本工厂方法，因此它会返回不同类型的产品。

Note that the factory method doesn’t have to create new instances all the time. It can also return existing objects from a cache, an object pool, or another source.
请注意，工厂方法不必一直创建新实例。它还可以从缓存、对象池或其他源返回现有对象。

## Pseudocode 伪代码
This example illustrates how the Factory Method can be used for creating cross-platform UI elements without coupling the client code to concrete UI classes.

此示例演示如何使用 Factory 方法创建跨平台 UI 元素，而无需将客户端代码耦合到具体的 UI 类。

<div align="center"> <img src="/images/example.png"/>The cross-platform dialog example.</br>跨平台对话框示例。</div>

The base `Dialog` class uses different UI elements to render its window. Under various operating systems, these elements may look a little bit different, but they should still behave consistently. A button in Windows is still a button in Linux.
基 `Dialog` 类使用不同的 UI 元素来呈现其窗口。在各种操作系统下，这些元素可能看起来略有不同，但它们的行为仍应一致。Windows 中的按钮仍然是 Linux 中的按钮。

When the factory method comes into play, you don’t need to rewrite the logic of the `Dialog` class for each operating system. If we declare a factory method that produces buttons inside the base `Dialog` class, we can later create a subclass that returns Windows-styled buttons from the factory method. The subclass then inherits most of the code from the base class, but, thanks to the factory method, can render Windows-looking buttons on the screen.
当工厂方法发挥作用时，无需为每个操作系统重写 `Dialog` 类的逻辑。如果我们声明一个在基 `Dialog` 类中生成按钮的工厂方法，我们稍后可以创建一个子类，该子类从工厂方法返回 Windows 样式的按钮。然后，该子类从基类继承大部分代码，但是，由于工厂方法，可以在屏幕上呈现具有 Windows 外观的按钮。

For this pattern to work, the base `Dialog` class must work with abstract buttons: a base class or an interface that all concrete buttons follow. This way the code within `Dialog` remains functional, whichever type of buttons it works with.
要使此模式起作用，基类必须使用抽象按钮：所有具体按钮都遵循的基 `Dialog` 类或接口。这样，无论使用哪种类型的按钮，其中 `Dialog` 的代码都可以正常工作。

Of course, you can apply this approach to other UI elements as well. However, with each new factory method you add to the `Dialog`, you get closer to the Abstract Factory pattern. Fear not, we’ll talk about this pattern later.
当然，您也可以将此方法应用于其他 UI 元素。但是，随着您添加到 `Dialog` 的每个新工厂方法，您都更接近抽象工厂模式。不要害怕，我们稍后会讨论这种模式。

```java
// The creator class declares the factory method that must
// return an object of a product class. The creator's subclasses
// usually provide the implementation of this method.
class Dialog is
    // The creator may also provide some default implementation
    // of the factory method.
    abstract method createButton():Button

    // Note that, despite its name, the creator's primary
    // responsibility isn't creating products. It usually
    // contains some core business logic that relies on product
    // objects returned by the factory method. Subclasses can
    // indirectly change that business logic by overriding the
    // factory method and returning a different type of product
    // from it.
    method render() is
        // Call the factory method to create a product object.
        Button okButton = createButton()
        // Now use the product.
        okButton.onClick(closeDialog)
        okButton.render()


// Concrete creators override the factory method to change the
// resulting product's type.
class WindowsDialog extends Dialog is
    method createButton():Button is
        return new WindowsButton()

class WebDialog extends Dialog is
    method createButton():Button is
        return new HTMLButton()


// The product interface declares the operations that all
// concrete products must implement.
interface Button is
    method render()
    method onClick(f)

// Concrete products provide various implementations of the
// product interface.
class WindowsButton implements Button is
    method render(a, b) is
        // Render a button in Windows style.
    method onClick(f) is
        // Bind a native OS click event.

class HTMLButton implements Button is
    method render(a, b) is
        // Return an HTML representation of a button.
    method onClick(f) is
        // Bind a web browser click event.


class Application is
    field dialog: Dialog

    // The application picks a creator's type depending on the
    // current configuration or environment settings.
    method initialize() is
        config = readApplicationConfigFile()

        if (config.OS == "Windows") then
            dialog = new WindowsDialog()
        else if (config.OS == "Web") then
            dialog = new WebDialog()
        else
            throw new Exception("Error! Unknown operating system.")

    // The client code works with an instance of a concrete
    // creator, albeit through its base interface. As long as
    // the client keeps working with the creator via the base
    // interface, you can pass it any creator's subclass.
    method main() is
        this.initialize()
        dialog.render()
```

## Applicability 适用性
**Use the Factory Method when you don’t know beforehand the exact types and dependencies of the objects your code should work with.**
**当您事先不知道代码应使用的对象的确切类型和依赖项时，请使用工厂方法。**

The Factory Method separates product construction code from the code that actually uses the product. Therefore it’s easier to extend the product construction code independently from the rest of the code.

Factory 方法将产品构造代码与实际使用产品的代码分开。因此，独立于代码的其余部分扩展产品构造代码更容易。

For example, to add a new product type to the app, you’ll only need to create a new creator subclass and override the factory method in it.

例如，要向应用添加新的产品类型，只需创建一个新的创建者子类并重写其中的工厂方法。

**Use the Factory Method when you want to provide users of your library or framework with a way to extend its internal components.**
**如果要为库或框架的用户提供扩展其内部组件的方法，请使用工厂方法。**

Inheritance is probably the easiest way to extend the default behavior of a library or framework. But how would the framework recognize that your subclass should be used instead of a standard component?
继承可能是扩展库或框架默认行为的最简单方法。但是，框架如何识别应该使用您的子类而不是标准组件呢？

The solution is to reduce the code that constructs components across the framework into a single factory method and let anyone override this method in addition to extending the component itself.
解决方案是将跨框架构造组件的代码简化为单个工厂方法，并允许任何人在扩展组件本身之外重写此方法。

Let’s see how that would work. Imagine that you write an app using an open source UI framework. Your app should have round buttons, but the framework only provides square ones. You extend the standard `Button` class with a glorious `RoundButton` subclass. But now you need to tell the main `UIFramework` class to use the new button subclass instead of a default one.
让我们看看这将如何工作。想象一下，你使用开源 UI 框架编写一个应用。你的应用应该有圆形按钮，但框架只提供方形按钮。你用一个光荣的 `RoundButton` 子类扩展了标准 Button 类。但是现在你需要告诉主 `UIFramework` 类使用新的按钮子类，而不是默认的子类。

To achieve this, you create a subclass `UIWithRoundButtons` from a base framework class and override its createButton method. While this method returns `Button` objects in the base class, you make your subclass return `RoundButton` objects. Now use the `UIWithRoundButtons` class instead of `UIFramework`. And that’s about it!
为此，可以从基框架类创建一个子类 `UIWithRoundButtons` 并重写其 createButton 方法。当此方法返回基类中的对象时，您可以使子类返回 Button `RoundButton` 对象。现在使用类 `UIWithRoundButtons` 而不是 `UIFramework` .仅此而已！

**Use the Factory Method when you want to save system resources by reusing existing objects instead of rebuilding them each time.**
**如果要通过重用现有对象而不是每次都重新生成它们来节省系统资源，请使用工厂方法。**

You often experience this need when dealing with large, resource-intensive objects such as database connections, file systems, and network resources.
在处理大型资源密集型对象（如数据库连接、文件系统和网络资源）时，您经常会遇到这种需求。

Let’s think about what has to be done to reuse an existing object:
让我们考虑一下重用现有对象必须做些什么：

* First, you need to create some storage to keep track of all of the created objects.
首先，您需要创建一些存储来跟踪所有创建的对象。
* When someone requests an object, the program should look for a free object inside that pool.
当有人请求某个对象时，程序应该在该池中查找一个空闲对象。
* … and then return it to the client code.
...，然后将其返回给客户端代码。
* If there are no free objects, the program should create a new one (and add it to the pool).
如果没有空闲对象，程序应创建一个新对象（并将其添加到池中）。

That’s a lot of code! And it must all be put into a single place so that you don’t pollute the program with duplicate code.
这是一大堆代码！而且必须将它们全部放在一个地方，这样您就不会用重复的代码污染程序。

Probably the most obvious and convenient place where this code could be placed is the constructor of the class whose objects we’re trying to reuse. However, a constructor must always return **new objects** by definition. It can’t return existing instances.
放置此代码的最明显和最方便的位置可能是我们尝试重用其对象的类的构造函数。但是，根据定义，构造函数必须始终返回**new objects**。它无法返回现有实例。

Therefore, you need to have a regular method capable of creating new objects as well as reusing existing ones. That sounds very much like a factory method.
因此，您需要有一个能够创建新对象以及重用现有对象的常规方法。这听起来很像工厂方法。

## How to Implement 如何实现

* Make all products follow the same interface. This interface should declare methods that make sense in every product.
使所有产品都遵循相同的界面。此接口应声明在每个产品中都有意义的方法。

* Add an empty factory method inside the creator class. The return type of the method should match the common product interface.
在 creator 类中添加一个空的工厂方法。方法的返回类型应与通用产品接口匹配。

* In the creator’s code find all references to product constructors. One by one, replace them with calls to the factory method, while extracting the product creation code into the factory method.
在创建者的代码中，找到对产品构造函数的所有引用。将它们逐个替换为对工厂方法的调用，同时将产品创建代码提取到工厂方法中。

You might need to add a temporary parameter to the factory method to control the type of returned product.
您可能需要向工厂方法添加临时参数，以控制返回产品的类型。

At this point, the code of the factory method may look pretty ugly. It may have a large `switch` statement that picks which product class to instantiate. But don’t worry, we’ll fix it soon enough.
在这一点上，工厂方法的代码可能看起来很丑陋。它可能有一个大 `switch` 语句，用于选择要实例化的产品类。但别担心，我们会尽快修复它。

* Now, create a set of creator subclasses for each type of product listed in the factory method. Override the factory method in the subclasses and extract the appropriate bits of construction code from the base method.
现在，为 factory 方法中列出的每种类型的产品创建一组创建者子类。重写子类中的工厂方法，并从基方法中提取适当的构造代码位。

* If there are too many product types and it doesn’t make sense to create subclasses for all of them, you can reuse the control parameter from the base class in subclasses.
如果产品类型太多，并且为所有产品类型创建子类没有意义，则可以在子类中重用基类中的控制参数。

For instance, imagine that you have the following hierarchy of classes: the base `Mail` class with a couple of subclasses: `AirMail` and `GroundMail`; the `Transport` classes are `Plane`, `Truck` and `Train`. While the `AirMail` class only uses `Plane` objects, `GroundMail` may work with both `Truck` and `Train` objects. You can create a new subclass (say `TrainMail`) to handle both cases, but there’s another option. The client code can pass an argument to the factory method of the `GroundMail` class to control which product it wants to receive.
例如，假设您有以下类层次结构：具有几个子类的基 `Mail` 类： `AirMail` 和 `GroundMail` ; `Transport` 这些类是 `Plane`,  `Truck`和 `Train` 。虽然该 `AirMail` 类仅使用 `Plane` 对象， `GroundMail` 但可以同时 `Truck` 使用和 `Train` 对象。您可以创建一个新的子类（例如 `TrainMail` ）来处理这两种情况，但还有另一种选择。客户端代码可以将参数传递给 `GroundMail` 类的工厂方法，以控制它要接收的产品。

* If, after all of the extractions, the base factory method has become empty, you can make it abstract. If there’s something left, you can make it a default behavior of the method.
如果在所有提取之后，基本工厂方法已变为空，则可以将其抽象化。如果还剩下一些东西，可以将其设置为方法的默认行为。

## Pros and Cons 优点和缺点

####  Pros 优点
* You avoid tight coupling between the creator and the concrete products.
您可以避免创建者和具体产品之间的紧密耦合。
* Single Responsibility Principle. You can move the product creation code into one place in the program, making the code easier to support.
单一责任原则。您可以将产品创建代码移动到程序中的一个位置，使代码更易于支持。
* Open/Closed Principle. You can introduce new types of products into the program without breaking existing client code.
开/闭原理。您可以在不破坏现有客户端代码的情况下将新类型的产品引入程序。

#### Cons 缺点
The code may become more complicated since you need to introduce a lot of new subclasses to implement the pattern. The best case scenario is when you’re introducing the pattern into an existing hierarchy of creator classes.
代码可能会变得更加复杂，因为您需要引入许多新的子类来实现该模式。最好的情况是将模式引入到创建者类的现有层次结构中。

## Relations with Other Patterns 与其他模式的关系
* Many designs start by using Factory Method (less complicated and more customizable via subclasses) and evolve toward Abstract Factory, Prototype, or Builder (more flexible, but more complicated).
许多设计从使用工厂方法（不那么复杂，通过子类更可定制）开始，然后发展到抽象工厂、原型或构建器（更灵活，但更复杂）。

* Abstract Factory classes are often based on a set of Factory Methods, but you can also use Prototype to compose the methods on these classes.
抽象工厂类通常基于一组工厂方法，但您也可以使用 Prototype 来组合这些类的方法。

* You can use Factory Method along with Iterator to let collection subclasses return different types of iterators that are compatible with the collections.
可以将工厂方法与迭代器一起使用，让集合子类返回与集合兼容的不同类型的迭代器。

* Prototype isn’t based on inheritance, so it doesn’t have its drawbacks. On the other hand, Prototype requires a complicated initialization of the cloned object. Factory Method is based on inheritance but doesn’t require an initialization step.
原型不是基于继承的，所以它没有缺点。另一方面，Prototype 需要对克隆对象进行复杂的初始化。工厂方法基于继承，但不需要初始化步骤。

* Factory Method is a specialization of Template Method. At the same time, a Factory Method may serve as a step in a large Template Method.
工厂方法是模板方法的专业化。同时，工厂方法可以作为大型模板方法中的一个步骤。

## Code Examples 代码示例
* python
```python
from __future__ import annotations
from abc import ABC, abstractmethod


class Creator(ABC):
    """
    The Creator class declares the factory method that is supposed to return an
    object of a Product class. The Creator's subclasses usually provide the
    implementation of this method.
    """

    @abstractmethod
    def factory_method(self):
        """
        Note that the Creator may also provide some default implementation of
        the factory method.
        """
        pass

    def some_operation(self) -> str:
        """
        Also note that, despite its name, the Creator's primary responsibility
        is not creating products. Usually, it contains some core business logic
        that relies on Product objects, returned by the factory method.
        Subclasses can indirectly change that business logic by overriding the
        factory method and returning a different type of product from it.
        """

        # Call the factory method to create a Product object.
        product = self.factory_method()

        # Now, use the product.
        result = f"Creator: The same creator's code has just worked with {product.operation()}"

        return result


"""
Concrete Creators override the factory method in order to change the resulting
product's type.
"""


class ConcreteCreator1(Creator):
    """
    Note that the signature of the method still uses the abstract product type,
    even though the concrete product is actually returned from the method. This
    way the Creator can stay independent of concrete product classes.
    """

    def factory_method(self) -> Product:
        return ConcreteProduct1()


class ConcreteCreator2(Creator):
    def factory_method(self) -> Product:
        return ConcreteProduct2()


class Product(ABC):
    """
    The Product interface declares the operations that all concrete products
    must implement.
    """

    @abstractmethod
    def operation(self) -> str:
        pass


"""
Concrete Products provide various implementations of the Product interface.
"""


class ConcreteProduct1(Product):
    def operation(self) -> str:
        return "{Result of the ConcreteProduct1}"


class ConcreteProduct2(Product):
    def operation(self) -> str:
        return "{Result of the ConcreteProduct2}"


def client_code(creator: Creator) -> None:
    """
    The client code works with an instance of a concrete creator, albeit through
    its base interface. As long as the client keeps working with the creator via
    the base interface, you can pass it any creator's subclass.
    """

    print(f"Client: I'm not aware of the creator's class, but it still works.\n"
          f"{creator.some_operation()}", end="")


if __name__ == "__main__":
    print("App: Launched with the ConcreteCreator1.")
    client_code(ConcreteCreator1())
    print("\n")

    print("App: Launched with the ConcreteCreator2.")
    client_code(ConcreteCreator2())
```
**Output.txt: Execution result**
```python
App: Launched with the ConcreteCreator1.
Client: I'm not aware of the creator's class, but it still works.
Creator: The same creator's code has just worked with {Result of the ConcreteProduct1}

App: Launched with the ConcreteCreator2.
Client: I'm not aware of the creator's class, but it still works.
Creator: The same creator's code has just worked with {Result of the ConcreteProduct2}
```


* Rust
**gui.rs:Prodcut & Creator**
```rust
pub trait Button {
    fn render(&self);
    fn on_click(&self);
}

/// Dialog has a factory method `create_button`.
///
/// It creates different buttons depending on a factory implementation.
pub trait Dialog {
    /// The factory method. It must be overridden with a concrete implementation.
    fn create_button(&self) -> Box<dyn Button>;

    fn render(&self) {
        let button = self.create_button();
        button.render();
    }

    fn refresh(&self) {
        println!("Dialog - Refresh");
    }
}
```
html_gui.rs: Concrete creator
```rust
use crate::gui::{Button, Dialog};

pub struct HtmlButton;

impl Button for HtmlButton {
    fn render(&self) {
        println!("<button>Test Button</button>");
        self.on_click();
    }

    fn on_click(&self) {
        println!("Click! Button says - 'Hello World!'");
    }
}

pub struct HtmlDialog;

impl Dialog for HtmlDialog {
    /// Creates an HTML button.
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(HtmlButton)
    }
}
```
**windows_gui.rs: Another concrete creator**
```rust
use crate::gui::{Button, Dialog};

pub struct WindowsButton;

impl Button for WindowsButton {
    fn render(&self) {
        println!("Drawing a Windows button");
        self.on_click();
    }

    fn on_click(&self) {
        println!("Click! Hello, Windows!");
    }
}

pub struct WindowsDialog;

impl Dialog for WindowsDialog {
    /// Creates a Windows button.
    fn create_button(&self) -> Box<dyn Button> {
        Box::new(WindowsButton)
    }
}
```

**init.rs: Initialization code**
```rust
use crate::gui::Dialog;
use crate::html_gui::HtmlDialog;
use crate::windows_gui::WindowsDialog;

pub fn initialize() -> &'static dyn Dialog {
    // The dialog type is selected depending on the environment settings or configuration.
    if cfg!(windows) {
        println!("-- Windows detected, creating Windows GUI --");
        &WindowsDialog
    } else {
        println!("-- No OS detected, creating the HTML GUI --");
        &HtmlDialog
    }
}
```
**main.rs: Client code main.rs**
```rust
mod gui;
mod html_gui;
mod init;
mod windows_gui;

use init::initialize;

fn main() {
    // The rest of the code doesn't depend on specific dialog types, because
    // it works with all dialog objects via the abstract `Dialog` trait
    // which is defined in the `gui` module.
    let dialog = initialize();
    dialog.render();
    dialog.refresh();
}
```

**Output**
```rust
<button>Test Button</button>
Click! Button says - 'Hello World!'
Dialog - Refresh
```
