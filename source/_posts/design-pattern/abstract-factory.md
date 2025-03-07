---
title: Abstract Factory
categories: design-pattern
tags: Design Pattern
date: 2023-11-20 20:16:29
---
# Abstract Factory 抽象工厂

## Intent 意图
Abstract Factory is a creational design pattern that lets you produce families of related objects without specifying their concrete classes.
抽象工厂是一种创建性设计模式，它允许您生成相关对象的族，而无需指定其具体类。
<div align="center"> <img src="/images/abstract-factory-en.png"/></div>

## Problem 问题
Imagine that you’re creating a furniture shop simulator. Your code consists of classes that represent:
想象一下，您正在创建一个家具店模拟器。代码由表示以下内容的类组成：

A family of related products, say: `Chair` + `Sofa` + `CoffeeTable`.
一系列相关产品，如：`Chair` + `Sofa` + `CoffeeTable`。

Several variants of this family. For example, products `Chair` + `Sofa` + `CoffeeTable` are available in these variants: `Modern`, `Victorian`, `ArtDeco`.
该系列的几个变体。例如，产品 `Chair` + `Sofa` + `CoffeeTable` 提供以下变体： `Modern` + `Victorian` + `ArtDeco` 。
<div align="center"> <img src="/images/abs-fac-problem2-en.png"/>Product families and their variants.</br> 产品系列及其变体。</div>

You need a way to create individual furniture objects so that they match other objects of the same family. Customers get quite mad when they receive non-matching furniture.
您需要一种方法来创建单个家具对象，以便它们与同一系列的其他对象相匹配。当客户收到不匹配的家具时，他们会非常生气。
<div align="center"> <img src="/images/abstract-factory-comic-1-en.png"/>A Modern-style sofa doesn’t match Victorian-style chairs.</div>

A Modern-style sofa doesn’t match Victorian-style chairs.
现代风格的沙发与维多利亚风格的椅子不匹配。

Also, you don’t want to change existing code when adding new products or families of products to the program. Furniture vendors update their catalogs very often, and you wouldn’t want to change the core code each time it happens.
此外，在向程序添加新产品或产品系列时，您不希望更改现有代码。家具供应商经常更新他们的目录，您不希望每次都更改核心代码。

## Solution 解决方案
The first thing the Abstract Factory pattern suggests is to explicitly declare interfaces for each distinct product of the product family (e.g., chair, sofa or coffee table). Then you can make all variants of products follow those interfaces. For example, all chair variants can implement the `Chair` interface; all coffee table variants can implement the `CoffeeTable` interface, and so on.
抽象工厂模式建议的第一件事是显式声明产品系列中每个不同产品（例如，椅子、沙发或咖啡桌）的接口。然后，您可以使产品的所有变体都遵循这些接口。例如，所有椅子变体都可以实现该 `Chair` 接口;所有咖啡桌变体都可以实现接口 `CoffeeTable` ，依此类推。
<div align="center"> <img src="/images/abs-fac-solution1.png"/>All variants of the same object must be moved to a single class hierarchy.</br>必须将同一对象的所有变体移动到单个类层次结构中。</div>

The next move is to declare the Abstract Factory—an interface with a list of creation methods for all products that are part of the product family (for example, `createChair`, `createSofa` and `createCoffeeTable`). These methods must return abstract product types represented by the interfaces we extracted previously: `Chair`, `Sofa`, `CoffeeTable` and so on.
下一步是声明抽象工厂 - 一个接口，其中包含属于产品系列的所有产品的创建方法列表（例如， `createChair` 、 `createSofa `和 `createCoffeeTable` ）。这些方法必须返回由我们之前提取的接口表示的抽象产品类型： `Chair` 、 `Sofa` 等 `CoffeeTable` 。
<div align="center"> <img src="/images/abs-fac-solution2.png"/>Each concrete factory corresponds to a specific product variant.</br>每个混凝土工厂对应一个特定的产品变型。</div>
The _Factories_ class hierarchy
Each concrete factory corresponds to a specific product variant.
每个混凝土工厂对应一个特定的产品变型。

Now, how about the product variants? For each variant of a product family, we create a separate factory class based on the `AbstractFactory` interface. A factory is a class that returns products of a particular kind. For example, the `ModernFurnitureFactory` can only create `ModernChair`, `ModernSofa` and `ModernCoffeeTable` objects.
现在，产品变体怎么样？对于产品系列的每个变体，我们基于 `AbstractFactory` 接口创建一个单独的工厂类。工厂是返回特定种类产品的类。例如，只能 `ModernFurnitureFactory` 创建 `ModernChair` 和 `ModernSofa` `ModernCoffeeTable` 对象。

The client code has to work with both factories and products via their respective abstract interfaces. This lets you change the type of a factory that you pass to the client code, as well as the product variant that the client code receives, without breaking the actual client code.
客户端代码必须通过工厂和产品各自的抽象接口进行处理。这样，您就可以更改传递给客户端代码的工厂类型，以及客户端代码接收的产品变型，而不会破坏实际的客户端代码。
<div align="center"> <img src="/images/abs-fac-solution2.png"/>The client shouldn’t care about the concrete class of the factory it works with.</br>客户不应该关心与它合作的工厂的具体类别。</div>

The client shouldn’t care about the concrete class of the factory it works with.
客户不应该关心与它合作的工厂的具体类别。

Say the client wants a factory to produce a chair. The client doesn’t have to be aware of the factory’s class, nor does it matter what kind of chair it gets. Whether it’s a Modern model or a Victorian-style chair, the client must treat all chairs in the same manner, using the abstract `Chair` interface. With this approach, the only thing that the client knows about the chair is that it implements the sitOn method in some way. Also, whichever variant of the chair is returned, it’ll always match the type of sofa or coffee table produced by the same factory object.
假设客户想要一家工厂生产一把椅子。客户不必知道工厂的等级，也不必知道它得到什么样的椅子。无论是现代模型还是维多利亚风格的椅子，客户都必须使用抽象 `Chair` 界面以相同的方式对待所有椅子。使用这种方法，客户对椅子的唯一了解是它以某种方式实现了 `sitOn` 该方法。此外，无论返回哪种椅子变体，它都将始终与同一工厂对象生产的沙发或咖啡桌类型相匹配。

There’s one more thing left to clarify: if the client is only exposed to the abstract interfaces, what creates the actual factory objects? Usually, the application creates a concrete factory object at the initialization stage. Just before that, the app must select the factory type depending on the configuration or the environment settings.
还有一件事需要澄清：如果客户端只暴露给抽象接口，那么是什么创建了实际的工厂对象？通常，应用程序在初始化阶段创建一个具体的工厂对象。在此之前，应用程序必须根据配置或环境设置选择出厂类型。

## Structure 结构
<div align="center"> <img src="/images/abs-fac-structure.png"/></br></div>

1. **Abstract Products** declare interfaces for a set of distinct but related products which make up a product family.
抽象产品声明了一组不同但相关的产品的接口，这些产品构成了一个产品系列。

2. **concrete Products** are various implementations of abstract products, grouped by variants. Each abstract product (chair/sofa) must be implemented in all given variants (Victorian/Modern).
具体产品是抽象产品的各种实现，按变体分组。每个抽象产品（椅子/沙发）都必须在所有给定的变体（维多利亚式/现代式）中实现。

3. The **Abstract Factory** interface declares a set of methods for creating each of the abstract products.
抽象工厂接口声明了一组用于创建每个抽象产品的方法。

4. **Concrete Factories** implement creation methods of the abstract factory. Each concrete factory corresponds to a specific variant of products and creates only those product variants.
具体工厂实现了抽象工厂的创建方法。每个混凝土工厂对应于产品的特定变体，并且仅创建这些产品变体。

5. **Although concrete** factories instantiate concrete products, signatures of their creation methods must return corresponding abstract products. This way the client code that uses a factory doesn’t get coupled to the specific variant of the product it gets from a factory. The Client can work with any concrete factory/product variant, as long as it communicates with their objects via abstract interfaces.
虽然具体工厂实例化了具体产品，但其创建方法的签名必须返回相应的抽象产品。这样，使用工厂的客户端代码就不会与它从工厂获得的产品的特定变体耦合。客户端可以使用任何具体的工厂/产品变体，只要它通过抽象接口与它们的对象进行通信即可。

## Pseudocode 伪代码
This example illustrates how the **Abstract Factory** pattern can be used for creating cross-platform UI elements without coupling the client code to concrete UI classes, while keeping all created elements consistent with a selected operating system.
此示例演示如何使用抽象工厂模式创建跨平台 UI 元素，而无需将客户端代码耦合到具体的 UI 类，同时使所有创建的元素与所选操作系统保持一致。
<div align="center"> <img src="/images/abs-fac-example.png"/>The cross-platform UI classes example.</br>跨平台 UI 类示例。</div>
The same UI elements in a cross-platform application are expected to behave similarly, but look a little bit different under different operating systems. Moreover, it’s your job to make sure that the UI elements match the style of the current operating system. You wouldn’t want your program to render macOS controls when it’s executed in Windows.
跨平台应用程序中的相同 UI 元素的行为应相似，但在不同的操作系统下看起来略有不同。此外，您的工作是确保 UI 元素与当前操作系统的样式相匹配。你不希望程序在 Windows 中执行时呈现 macOS 控件。

The Abstract Factory interface declares a set of creation methods that the client code can use to produce different types of UI elements. Concrete factories correspond to specific operating systems and create the UI elements that match that particular OS.
抽象工厂接口声明了一组创建方法，客户端代码可以使用这些方法生成不同类型的 UI 元素。具体工厂对应于特定的操作系统，并创建与该特定操作系统匹配的 UI 元素。

It works like this: when an application launches, it checks the type of the current operating system. The app uses this information to create a factory object from a class that matches the operating system. The rest of the code uses this factory to create UI elements. This prevents the wrong elements from being created.
它的工作原理是这样的：当应用程序启动时，它会检查当前操作系统的类型。应用使用此信息从与操作系统匹配的类创建工厂对象。代码的其余部分使用此工厂创建 UI 元素。这样可以防止创建错误的元素。

With this approach, the client code doesn’t depend on concrete classes of factories and UI elements as long as it works with these objects via their abstract interfaces. This also lets the client code support other factories or UI elements that you might add in the future.
使用这种方法，客户端代码不依赖于工厂和 UI 元素的具体类，只要它通过其抽象接口处理这些对象即可。这也允许客户端代码支持将来可能添加的其他工厂或 UI 元素。

As a result, you don’t need to modify the client code each time you add a new variation of UI elements to your app. You just have to create a new factory class that produces these elements and slightly modify the app’s initialization code so it selects that class when appropriate.
因此，每次向应用添加新的 UI 元素变体时，都无需修改客户端代码。只需创建一个新的工厂类来生成这些元素，并稍微修改应用的初始化代码，以便它在适当的时候选择该类。
```java
// The abstract factory interface declares a set of methods that
// return different abstract products. These products are called
// a family and are related by a high-level theme or concept.
// Products of one family are usually able to collaborate among
// themselves. A family of products may have several variants,
// but the products of one variant are incompatible with the
// products of another variant.
interface GUIFactory is
    method createButton():Button
    method createCheckbox():Checkbox


// Concrete factories produce a family of products that belong
// to a single variant. The factory guarantees that the
// resulting products are compatible. Signatures of the concrete
// factory's methods return an abstract product, while inside
// the method a concrete product is instantiated.
class WinFactory implements GUIFactory is
    method createButton():Button is
        return new WinButton()
    method createCheckbox():Checkbox is
        return new WinCheckbox()

// Each concrete factory has a corresponding product variant.
class MacFactory implements GUIFactory is
    method createButton():Button is
        return new MacButton()
    method createCheckbox():Checkbox is
        return new MacCheckbox()


// Each distinct product of a product family should have a base
// interface. All variants of the product must implement this
// interface.
interface Button is
    method paint()

// Concrete products are created by corresponding concrete
// factories.
class WinButton implements Button is
    method paint() is
        // Render a button in Windows style.

class MacButton implements Button is
    method paint() is
        // Render a button in macOS style.

// Here's the base interface of another product. All products
// can interact with each other, but proper interaction is
// possible only between products of the same concrete variant.
interface Checkbox is
    method paint()

class WinCheckbox implements Checkbox is
    method paint() is
        // Render a checkbox in Windows style.

class MacCheckbox implements Checkbox is
    method paint() is
        // Render a checkbox in macOS style.


// The client code works with factories and products only
// through abstract types: GUIFactory, Button and Checkbox. This
// lets you pass any factory or product subclass to the client
// code without breaking it.
class Application is
    private field factory: GUIFactory
    private field button: Button
    constructor Application(factory: GUIFactory) is
        this.factory = factory
    method createUI() is
        this.button = factory.createButton()
    method paint() is
        button.paint()


// The application picks the factory type depending on the
// current configuration or environment settings and creates it
// at runtime (usually at the initialization stage).
class ApplicationConfigurator is
    method main() is
        config = readApplicationConfigFile()

        if (config.OS == "Windows") then
            factory = new WinFactory()
        else if (config.OS == "Mac") then
            factory = new MacFactory()
        else
            throw new Exception("Error! Unknown operating system.")

        Application app = new Application(factory)
```

## Applicability 适用性
* **Use the Abstract Factory when your code needs to work with various families of related products, but you don’t want it to depend on the concrete classes of those products—they might be unknown beforehand or you simply want to allow for future extensibility.
当您的代码需要处理各种相关产品系列，但您不希望它依赖于这些产品的具体类时，请使用抽象工厂 - 它们可能事先是未知的，或者您只是想允许将来的可扩展性。**

* The Abstract Factory provides you with an interface for creating objects from each class of the product family. As long as your code creates objects via this interface, you don’t have to worry about creating the wrong variant of a product which doesn’t match the products already created by your app.
抽象工厂为您提供了一个接口，用于从产品系列的每个类创建对象。只要您的代码通过此接口创建对象，您就不必担心创建错误的产品变体，而该变体与您的应用已创建的产品不匹配。

* **Consider implementing the Abstract Factory when you have a class with a set of Factory Methods that blur its primary responsibility.
当您有一个具有一组模糊其主要职责的工厂方法的类时，请考虑实现抽象工厂。**

* In a well-designed program each class is responsible only for one thing. When a class deals with multiple product types, it may be worth extracting its factory methods into a stand-alone factory class or a full-blown Abstract Factory implementation.
在一个精心设计的程序中，每个类只负责一件事。当一个类处理多种产品类型时，可能值得将其工厂方法提取到独立的工厂类或成熟的抽象工厂实现中。

## How to Implement 如何实现
1. Map out a matrix of distinct product types versus variants of these products.
绘制出不同产品类型与这些产品变体的矩阵。

2. Declare abstract product interfaces for all product types. Then make all concrete product classes implement these interfaces.
声明所有产品类型的抽象产品接口。然后让所有具体的产品类实现这些接口。

3. Declare the abstract factory interface with a set of creation methods for all abstract products.
声明抽象工厂接口，其中包含所有抽象产品的一组创建方法。

4. Implement a set of concrete factory classes, one for each product variant.
实现一组具体的工厂类，每个产品变型对应一个。

5. Create factory initialization code somewhere in the app. It should instantiate one of the concrete factory classes, depending on the application configuration or the current environment. Pass this factory object to all classes that construct products.
在应用的某个位置创建工厂初始化代码。它应该实例化一个具体的工厂类，具体取决于应用程序配置或当前环境。将此工厂对象传递给构造产品的所有类。

6. Scan through the code and find all direct calls to product constructors. Replace them with calls to the appropriate creation method on the factory object.
扫描代码并找到对产品构造函数的所有直接调用。将它们替换为对工厂对象上相应创建方法的调用。

## Pros and Cons 优点和缺点
### Pros 优点
* You can be sure that the products you’re getting from a factory are compatible with each other.
您可以确定您从工厂获得的产品彼此兼容。
* You avoid tight coupling between concrete products and client code.
可以避免具体产品和客户端代码之间的紧密耦合。
* Single Responsibility Principle. You can extract the product creation code into one place, making the code easier to support.
单一责任原则。您可以将产品创建代码提取到一个位置，使代码更易于支持。
* Open/Closed Principle. You can introduce new variants of products without breaking existing client code.
开/闭原理。您可以在不破坏现有客户端代码的情况下引入新的产品变体。

### Cons 缺点
* The code may become more complicated than it should be, since a lot of new interfaces and classes are introduced along with the pattern.
代码可能会变得比应有的更复杂，因为许多新的接口和类与模式一起引入。

## Relations with Other Patterns 与其他模式的关系
* Many designs start by using **Factory Method** (less complicated and more customizable via subclasses) and evolve toward **Abstract Factory**, **Prototype**, or **Builder** (more flexible, but more complicated).
许多设计从使用工厂方法（不那么复杂，通过子类更可定制）开始，然后发展到抽象工厂、原型或构建器（更灵活，但更复杂）。

* **Builder** focuses on constructing complex objects step by step.** Abstract Factory** specializes in creating families of related objects. **Abstract Factory** returns the product immediately, whereas Builder lets you run some additional construction steps before fetching the product.
Builder 专注于逐步构建复杂的对象。Abstract Factory专门用于创建相关对象的族。Abstract Factory 会立即返回产品，而 Builder 允许您在获取产品之前运行一些额外的构造步骤。

* **Abstract Factory** classes are often based on a set of **Factory Methods**, but you can also use **Prototype** to compose the methods on these classes.
抽象工厂类通常基于一组工厂方法，但您也可以使用 Prototype 来组合这些类的方法。

* **Abstract Factory** can serve as an alternative to **Facade** when you only want to hide the way the subsystem objects are created from the client code.
抽象工厂可以作为 Facade 的替代方法，当您只想从客户端代码中隐藏子系统对象的创建方式时。

* You can use **Abstract Factory** along with **Bridge**. This pairing is useful when some abstractions defined by Bridge can only work with specific implementations. In this case, Abstract Factory can encapsulate these relations and hide the complexity from the client code.
您可以将 Abstract Factory 与 Bridge 一起使用。当 Bridge 定义的某些抽象只能与特定实现一起使用时，这种配对非常有用。在这种情况下，抽象工厂可以封装这些关系，并从客户端代码中隐藏复杂性。

* **Abstract Factories**, **Builders** and **Prototypes** can all be implemented as **Singletons**.
抽象工厂、构建器和原型都可以作为单例实现。

## Code Examples 示例代码

### Python

```python
from __future__ import annotations
from abc import ABC, abstractmethod


class AbstractFactory(ABC):
    """
    The Abstract Factory interface declares a set of methods that return
    different abstract products. These products are called a family and are
    related by a high-level theme or concept. Products of one family are usually
    able to collaborate among themselves. A family of products may have several
    variants, but the products of one variant are incompatible with products of
    another.
    """
    @abstractmethod
    def create_product_a(self) -> AbstractProductA:
        pass

    @abstractmethod
    def create_product_b(self) -> AbstractProductB:
        pass


class ConcreteFactory1(AbstractFactory):
    """
    Concrete Factories produce a family of products that belong to a single
    variant. The factory guarantees that resulting products are compatible. Note
    that signatures of the Concrete Factory's methods return an abstract
    product, while inside the method a concrete product is instantiated.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA1()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB1()


class ConcreteFactory2(AbstractFactory):
    """
    Each Concrete Factory has a corresponding product variant.
    """

    def create_product_a(self) -> AbstractProductA:
        return ConcreteProductA2()

    def create_product_b(self) -> AbstractProductB:
        return ConcreteProductB2()


class AbstractProductA(ABC):
    """
    Each distinct product of a product family should have a base interface. All
    variants of the product must implement this interface.
    """

    @abstractmethod
    def useful_function_a(self) -> str:
        pass


"""
Concrete Products are created by corresponding Concrete Factories.
"""


class ConcreteProductA1(AbstractProductA):
    def useful_function_a(self) -> str:
        return "The result of the product A1."


class ConcreteProductA2(AbstractProductA):
    def useful_function_a(self) -> str:
        return "The result of the product A2."


class AbstractProductB(ABC):
    """
    Here's the the base interface of another product. All products can interact
    with each other, but proper interaction is possible only between products of
    the same concrete variant.
    """
    @abstractmethod
    def useful_function_b(self) -> None:
        """
        Product B is able to do its own thing...
        """
        pass

    @abstractmethod
    def another_useful_function_b(self, collaborator: AbstractProductA) -> None:
        """
        ...but it also can collaborate with the ProductA.

        The Abstract Factory makes sure that all products it creates are of the
        same variant and thus, compatible.
        """
        pass


"""
Concrete Products are created by corresponding Concrete Factories.
"""


class ConcreteProductB1(AbstractProductB):
    def useful_function_b(self) -> str:
        return "The result of the product B1."

    """
    The variant, Product B1, is only able to work correctly with the variant,
    Product A1. Nevertheless, it accepts any instance of AbstractProductA as an
    argument.
    """

    def another_useful_function_b(self, collaborator: AbstractProductA) -> str:
        result = collaborator.useful_function_a()
        return f"The result of the B1 collaborating with the ({result})"


class ConcreteProductB2(AbstractProductB):
    def useful_function_b(self) -> str:
        return "The result of the product B2."

    def another_useful_function_b(self, collaborator: AbstractProductA):
        """
        The variant, Product B2, is only able to work correctly with the
        variant, Product A2. Nevertheless, it accepts any instance of
        AbstractProductA as an argument.
        """
        result = collaborator.useful_function_a()
        return f"The result of the B2 collaborating with the ({result})"


def client_code(factory: AbstractFactory) -> None:
    """
    The client code works with factories and products only through abstract
    types: AbstractFactory and AbstractProduct. This lets you pass any factory
    or product subclass to the client code without breaking it.
    """
    product_a = factory.create_product_a()
    product_b = factory.create_product_b()

    print(f"{product_b.useful_function_b()}")
    print(f"{product_b.another_useful_function_b(product_a)}", end="")


if __name__ == "__main__":
    """
    The client code can work with any concrete factory class.
    """
    print("Client: Testing client code with the first factory type:")
    client_code(ConcreteFactory1())

    print("\n")

    print("Client: Testing the same client code with the second factory type:")
    client_code(ConcreteFactory2())
```

### Output.txt: Exception result
```
Client: Testing client code with the first factory type:
The result of the product B1.
The result of the B1 collaborating with the (The result of the product A1.)

Client: Testing the same client code with the second factory type:
The result of the product B2.
The result of the B2 collaborating with the (The result of the product A2.)
```
### Rust

#### GUI Elements Factory GUI 元素工厂
This example illustrates how a GUI framework can organize its classes into independent libraries:
此示例说明了 GUI 框架如何将其类组织到独立的库中：

1. The gui library defines interfaces for all the components.
该 gui 库定义了所有组件的接口。
It has no external dependencies.
它没有外部依赖关系。
2. The windows-gui library provides Windows implementation of the base GUI.
该 windows-gui 库提供基本 GUI 的 Windows 实现。
Depends on gui.
取决于 gui 。
3. The macos-gui library provides Mac OS implementation of the base GUI.
该 macos-gui 库提供基本 GUI 的 Mac OS 实现。
Depends on gui.
取决于 gui 。
The app is a client application that can use several implementations of the GUI framework, depending on the current environment or configuration. However, most of the app code doesn’t depend on specific types of GUI elements. All the client code works with GUI elements through abstract interfaces (traits) defined by the gui lib.
是一个 app 客户端应用程序，可以使用 GUI 框架的多个实现，具体取决于当前环境或配置。但是，大多数 app 代码并不依赖于特定类型的 GUI 元素。所有客户端代码都通过 gui 库定义的抽象接口（特征）与 GUI 元素一起使用。

There are two approaches to implementing abstract factories in Rust:
在 Rust 中实现抽象工厂有两种方法：
1.using generics (static dispatch)
使用泛型（静态调度）
2.using dynamic allocation (dynamic dispatch)
使用动态分配（动态调度）

When you’re given a choice between static and dynamic dispatch, there is rarely a clear-cut correct answer. You’ll want to use static dispatch in your libraries and dynamic dispatch in your binaries. In a library, you want to allow your users to decide what kind of dispatch is best for them since you don’t know what their needs are. If you use dynamic dispatch, they’re forced to do the same, whereas if you use static dispatch, they can choose whether to use dynamic dispatch or not.
当您在静态调度和动态调度之间做出选择时，很少有明确的正确答案。您需要在库中使用静态调度，在二进制文件中使用动态调度。在图书馆中，您希望允许用户决定哪种调度最适合他们，因为您不知道他们的需求是什么。如果您使用动态调度，他们将被迫执行相同的操作，而如果您使用静态调度，则可以选择是否使用动态调度。

#### gui: Abstract Factory and Abstract Products gui：抽象工厂和抽象产品

* gui/lib.rs
```rust
pub trait Button {
    fn press(&self);
}

pub trait Checkbox {
    fn switch(&self);
}

/// Abstract Factory defined using generics.
pub trait GuiFactory {
    type B: Button;
    type C: Checkbox;

    fn create_button(&self) -> Self::B;
    fn create_checkbox(&self) -> Self::C;
}

/// Abstract Factory defined using Box pointer.
pub trait GuiFactoryDynamic {
    fn create_button(&self) -> Box<dyn Button>;
    fn create_checkbox(&self) -> Box<dyn Checkbox>;
}
```
* macos-gui: One family of products
file: macos-gui/lib.rs
```rust
pub mod button;
pub mod checkbox;
pub mod factory;
```
* windows-gui: Another family of products
file: windows-gui/lib.rs
```rust
pub mod button;
pub mod checkbox;
pub mod factory;
```

#### Static dispatch 静态调度
Here, the abstract factory is implemented via generics which lets the compiler create a code that does NOT require dynamic dispatch in runtime.
在这里，抽象工厂是通过泛型实现的，它允许编译器创建不需要在运行时动态调度的代码。

* app: Client code with static dispatch
file: app/main.rs
```rust
mod render;

use render::render;

use macos_gui::factory::MacFactory;
use windows_gui::factory::WindowsFactory;

fn main() {
    let windows = true;

    if windows {
        render(WindowsFactory);
    } else {
        render(MacFactory);
    }
}
```
file: app/render.rs
```rust
//! The code demonstrates that it doesn't depend on a concrete
//! factory implementation.

use gui::GuiFactory;

// Renders GUI. Factory object must be passed as a parameter to such the
// generic function with factory invocation to utilize static dispatch.
pub fn render(factory: impl GuiFactory) {
    let button1 = factory.create_button();
    let button2 = factory.create_button();
    let checkbox1 = factory.create_checkbox();
    let checkbox2 = factory.create_checkbox();

    use gui::{Button, Checkbox};

    button1.press();
    button2.press();
    checkbox1.switch();
    checkbox2.switch();
}
```
#### Dynamic dispatch 动态调度
If a concrete type of abstract factory is not known at the compilation time, then is should be implemented using Box pointers.
如果在编译时不知道抽象工厂的具体类型，则应使用 Box 指针实现。

* app-dyn: Client code with dynamic dispatch
file: app-dyn/main.rs
```rust
mod render;

use render::render;

use gui::GuiFactoryDynamic;
use macos_gui::factory::MacFactory;
use windows_gui::factory::WindowsFactory;

fn main() {
    let windows = false;

    // Allocate a factory object in runtime depending on unpredictable input.
    let factory: &dyn GuiFactoryDynamic = if windows {
        &WindowsFactory
    } else {
        &MacFactory
    };

    // Factory invocation can be inlined right here.
    let button = factory.create_button();
    button.press();

    // Factory object can be passed to a function as a parameter.
    render(factory);
}
```
file: app-dyn/render.rs
```rust
//! The code demonstrates that it doesn't depend on a concrete
//! factory implementation.

use gui::GuiFactoryDynamic;

/// Renders GUI.
pub fn render(factory: &dyn GuiFactoryDynamic) {
    let button1 = factory.create_button();
    let button2 = factory.create_button();
    let checkbox1 = factory.create_checkbox();
    let checkbox2 = factory.create_checkbox();

    button1.press();
    button2.press();
    checkbox1.switch();
    checkbox2.switch();
}
```

#### Output
```
Windows button has pressed
Windows button has pressed
Windows checkbox has switched
Windows checkbox has switched
```
