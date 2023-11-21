---
title: Builder
categories:
  - design-patter
tags: Design Pattern
date: 2023-11-21 20:42:48
---
# Builder 建造者

## Intent 意图

**Builder** is a creational design pattern that lets you construct complex objects step by step. The pattern allows you to produce different types and representations of an object using the same construction code.
**Builder** 是一种创建性设计模式，可让您逐步构建复杂的对象。该模式允许您使用相同的构造代码生成对象的不同类型和表示形式。
<div align="center"> <img src="/images/builder-en.png"/></div>

## Problem 问题

Imagine a complex object that requires laborious, step-by-step initialization of many fields and nested objects. Such initialization code is usually buried inside a monstrous constructor with lots of parameters. Or even worse: scattered all over the client code.
想象一个复杂的对象，需要费力地逐步初始化许多字段和嵌套对象。这种初始化代码通常隐藏在具有大量参数的可怕构造函数中。或者更糟糕的是：分散在客户端代码中。
<div align="center"> <img src="/images/builder-problem1.png"/>You might make the program too complex by creating a subclass for every possible configuration of an object.</通过为对象的每个可能配置创建一个子类，可能会使程序过于复杂。></div>

For example, let’s think about how to create a `House` object. To build a simple house, you need to construct four walls and a floor, install a door, fit a pair of windows, and build a roof. But what if you want a bigger, brighter house, with a backyard and other goodies (like a heating system, plumbing, and electrical wiring)?
例如，让我们考虑如何创建一个 `House` 对象。要建造一个简单的房子，你需要建造四面墙和一个地板，安装一扇门，安装一对窗户，并建造一个屋顶。但是，如果您想要一个更大、更明亮的房子，有后院和其他好东西（如供暖系统、管道和电线）怎么办？

The simplest solution is to extend the base `House` class and create a set of subclasses to cover all combinations of the parameters. But eventually you’ll end up with a considerable number of subclasses. Any new parameter, such as the porch style, will require growing this hierarchy even more.
最简单的解决方案是扩展基 `House` 类并创建一组子类以涵盖参数的所有组合。但最终你会得到相当多的子类。任何新参数（例如门廊样式）都需要进一步扩展此层次结构。

There’s another approach that doesn’t involve breeding subclasses. You can create a giant constructor right in the base `House` class with all possible parameters that control the house object. While this approach indeed eliminates the need for subclasses, it creates another problem.
还有另一种方法不涉及育种子类。您可以直接在基 `House` 类中创建一个巨大的构造函数，其中包含控制 house 对象的所有可能参数。虽然这种方法确实消除了对子类的需求，但它产生了另一个问题。
<div align="center"> <img src="/images/builder-problem2.png"/>The constructor with lots of parameters has its downside: not all the parameters are needed at all times.</br>具有大量参数的构造函数有其缺点：并非所有参数都是必需的。</div>

In most cases most of the parameters will be unused, making **the constructor calls pretty ugly**. For instance, only a fraction of houses have swimming pools, so the parameters related to swimming pools will be useless nine times out of ten.
在大多数情况下，大多数参数将处于未使用状态，这使得构造函数调用非常丑陋。例如，只有一小部分房屋有游泳池，因此与游泳池相关的参数十有八九将毫无用处。

## Solution 解决方案

The Builder pattern suggests that you extract the object construction code out of its own class and move it to separate objects called builders.
Builder 模式建议您将对象构造代码从其自己的类中提取出来，并将其移动到称为生成器的单独对象中。
<div align="center"> <img src="/images/builder-solution1.png"/>The Builder pattern lets you construct complex objects step by step. The Builder doesn’t allow other objects to access the product while it’s being built.</br>Builder 模式允许您逐步构建复杂的对象。Builder 不允许其他对象在构建产品时访问产品。</div>

The pattern organizes object construction into a set of steps (`buildWalls`, `buildDoor`, etc.). To create an object, you execute a series of these steps on a builder object. The important part is that you don’t need to call all of the steps. You can call only those steps that are necessary for producing a particular configuration of an object.
该模式将对象构造组织为一组步骤（`buildWalls`, `buildDoor` 等）。要创建对象，请在生成器对象上执行一系列这些步骤。重要的是，您不需要调用所有步骤。您只能调用生成对象的特定配置所需的那些步骤。

Some of the construction steps might require different implementation when you need to build various representations of the product. For example, walls of a cabin may be built of wood, but the castle walls must be built with stone.
当您需要构建产品的各种表示形式时，某些构造步骤可能需要不同的实现。例如，小屋的墙壁可以用木头建造，但城堡的墙壁必须用石头建造。

In this case, you can create several different builder classes that implement the same set of building steps, but in a different manner. Then you can use these builders in the construction process (i.e., an ordered set of calls to the building steps) to produce different kinds of objects.
在这种情况下，您可以创建多个不同的生成器类，这些类以不同的方式实现同一组生成步骤。然后，您可以在构造过程中使用这些构建器（即，对构建步骤的一组有序调用）来生成不同类型的对象。
<div align="center"> <img src="/images/builder-comic-1-en.png"/>Different builders execute the same task in various ways.</br>不同的构建器以不同的方式执行相同的任务。</div>

For example, imagine a builder that builds everything from wood and glass, a second one that builds everything with stone and iron and a third one that uses gold and diamonds. By calling the same set of steps, you get a regular house from the first builder, a small castle from the second and a palace from the third. However, this would only work if the client code that calls the building steps is able to interact with builders using a common interface.
例如，想象一个建筑商用木头和玻璃建造所有东西，第二个建筑商用石头和铁建造所有东西，第三个建筑商使用黄金和钻石建造所有东西。通过调用相同的步骤，您可以从第一个建筑商那里获得普通房屋，从第二个建造者那里获得一座小城堡，从第三个建造者那里获得一座宫殿。但是，仅当调用生成步骤的客户端代码能够使用通用接口与构建器交互时，这才有效。

## Director

You can go further and extract a series of calls to the builder steps you use to construct a product into a separate class called director. The director class defines the order in which to execute the building steps, while the builder provides the implementation for those steps.
您可以更进一步，将对用于将产品构造到称为 director 的单独类的构建器步骤的一系列调用中提取出来。director 类定义执行生成步骤的顺序，而生成器则提供这些步骤的实现。
<div align="center"> <img src="/images/builder-comic-2-en.png"/>The director knows which building steps to execute to get a working product.</br>主管知道要执行哪些构建步骤才能获得工作产品。</div>

Having a director class in your program isn’t strictly necessary. You can always call the building steps in a specific order directly from the client code. However, the director class might be a good place to put various construction routines so you can reuse them across your program.
在您的课程中开设director类并不是绝对必要的。您始终可以直接从客户端代码按特定顺序调用生成步骤。但是，director 类可能是放置各种构造例程的好地方，以便您可以在程序中重用它们。

In addition, the director class completely hides the details of product construction from the client code. The client only needs to associate a builder with a director, launch the construction with the director, and get the result from the builder.
此外，director 类在客户端代码中完全隐藏了产品构造的细节。客户端只需将构建器与控制器关联，与控制器一起启动构造，并从构建器获取结果。

## Structure 结构

<div align="center"> <img src="/images/builder-structure.png"/></div>

1. The **Builder** interface declares product construction steps that are common to all types of builders.
Builder 界面声明了所有类型的构建器通用的产品构建步

2. **Concrete** Builders provide different implementations of the construction steps. Concrete builders may produce products that don’t follow the common interface.
混凝土建造者提供施工步骤的不同实施。混凝土建筑商可能会生产不遵循通用接口的产品。

3. **Products** are resulting objects. Products constructed by different builders don’t have to belong to the same class hierarchy or interface.
产品是结果对象。由不同构建器构建的产品不必属于相同的类层次结构或接口。

4. The **Director** class defines the order in which to call construction steps, so you can create and reuse specific configurations of products.
Director 类定义调用构造步骤的顺序，以便您可以创建和重用产品的特定配置。

5. The **Client** must associate one of the builder objects with the director. Usually, it’s done just once, via parameters of the director’s constructor. Then the director uses that builder object for all further construction. However, there’s an alternative approach for when the client passes the builder object to the production method of the director. In this case, you can use a different builder each time you produce something with the director.
客户端必须将其中一个构建器对象与控制器相关联。通常，它只通过控制器构造函数的参数完成一次。然后，director 使用该构建器对象进行所有进一步的构造。但是，当客户端将生成器对象传递给控制器的生产方法时，还有另一种方法。在这种情况下，每次与director一起制作内容时，都可以使用不同的构建器。

##  Pseudocode 伪代码

This example of the **Builder** pattern illustrates how you can reuse the same object construction code when building different types of products, such as cars, and create the corresponding manuals for them.
此 Builder 模式示例说明了如何在构建不同类型的产品（如汽车）时重用相同的对象构造代码，并为它们创建相应的手册。
<div align="center"> <img src="/images/builder-example-en.png"/>The example of step-by-step construction of cars and the user guides that fit those car models.</br>汽车的分步构造示例以及适合这些汽车型号的用户指南。</div>

A car is a complex object that can be constructed in a hundred different ways. Instead of bloating the `Car` class with a huge constructor, we extracted the car assembly code into a separate car builder class. This class has a set of methods for configuring various parts of a car.
汽车是一个复杂的物体，可以用一百种不同的方式建造。我们没有使用庞大的构造函数来膨胀类 `Car` ，而是将汽车装配代码提取到一个单独的 car builder 类中。此类具有一组用于配置汽车各个部分的方法。

If the client code needs to assemble a special, fine-tuned model of a car, it can work with the builder directly. On the other hand, the client can delegate the assembly to the director class, which knows how to use a builder to construct several of the most popular models of cars.
如果客户端代码需要组装一个特殊的、微调的汽车模型，它可以直接与构建器一起使用。另一方面，客户端可以将程序集委托给 director 类，该类知道如何使用构建器来构造几种最流行的汽车模型。

You might be shocked, but every car needs a manual (seriously, who reads them?). The manual describes every feature of the car, so the details in the manuals vary across the different models. That’s why it makes sense to reuse an existing construction process for both real cars and their respective manuals. Of course, building a manual isn’t the same as building a car, and that’s why we must provide another builder class that specializes in composing manuals. This class implements the same building methods as its car-building sibling, but instead of crafting car parts, it describes them. By passing these builders to the same director object, we can construct either a car or a manual.
您可能会感到震惊，但每辆车都需要一本手册（说真的，谁会读它们？手册描述了汽车的每个功能，因此手册中的细节因不同车型而异。这就是为什么在真实汽车及其各自的手册中重复使用现有的制造过程是有意义的。当然，构建手册与构建汽车不同，这就是为什么我们必须提供另一个专门编写手册的构建者类。该类实现了与其汽车制造同级相同的构建方法，但不是制作汽车零件，而是描述它们。通过将这些构建器传递给同一个 director 对象，我们可以构造汽车或手册。

The final part is fetching the resulting object. A metal car and a paper manual, although related, are still very different things. We can’t place a method for fetching results in the director without coupling the director to concrete product classes. Hence, we obtain the result of the construction from the builder which performed the job.
最后一部分是获取生成的对象。金属汽车和纸质手册虽然相关，但仍然是非常不同的东西。如果不将控制器与具体的产品类耦合，我们就无法在控制器中放置获取结果的方法。因此，我们从执行工作的建筑商那里获得施工结果。

```java
// Using the Builder pattern makes sense only when your products
// are quite complex and require extensive configuration. The
// following two products are related, although they don't have
// a common interface.
class Car is
    // A car can have a GPS, trip computer and some number of
    // seats. Different models of cars (sports car, SUV,
    // cabriolet) might have different features installed or
    // enabled.

class Manual is
    // Each car should have a user manual that corresponds to
    // the car's configuration and describes all its features.


// The builder interface specifies methods for creating the
// different parts of the product objects.
interface Builder is
    method reset()
    method setSeats(...)
    method setEngine(...)
    method setTripComputer(...)
    method setGPS(...)

// The concrete builder classes follow the builder interface and
// provide specific implementations of the building steps. Your
// program may have several variations of builders, each
// implemented differently.
class CarBuilder implements Builder is
    private field car:Car

    // A fresh builder instance should contain a blank product
    // object which it uses in further assembly.
    constructor CarBuilder() is
        this.reset()

    // The reset method clears the object being built.
    method reset() is
        this.car = new Car()

    // All production steps work with the same product instance.
    method setSeats(...) is
        // Set the number of seats in the car.

    method setEngine(...) is
        // Install a given engine.

    method setTripComputer(...) is
        // Install a trip computer.

    method setGPS(...) is
        // Install a global positioning system.

    // Concrete builders are supposed to provide their own
    // methods for retrieving results. That's because various
    // types of builders may create entirely different products
    // that don't all follow the same interface. Therefore such
    // methods can't be declared in the builder interface (at
    // least not in a statically-typed programming language).
    //
    // Usually, after returning the end result to the client, a
    // builder instance is expected to be ready to start
    // producing another product. That's why it's a usual
    // practice to call the reset method at the end of the
    // `getProduct` method body. However, this behavior isn't
    // mandatory, and you can make your builder wait for an
    // explicit reset call from the client code before disposing
    // of the previous result.
    method getProduct():Car is
        product = this.car
        this.reset()
        return product

// Unlike other creational patterns, builder lets you construct
// products that don't follow the common interface.
class CarManualBuilder implements Builder is
    private field manual:Manual

    constructor CarManualBuilder() is
        this.reset()

    method reset() is
        this.manual = new Manual()

    method setSeats(...) is
        // Document car seat features.

    method setEngine(...) is
        // Add engine instructions.

    method setTripComputer(...) is
        // Add trip computer instructions.

    method setGPS(...) is
        // Add GPS instructions.

    method getProduct():Manual is
        // Return the manual and reset the builder.


// The director is only responsible for executing the building
// steps in a particular sequence. It's helpful when producing
// products according to a specific order or configuration.
// Strictly speaking, the director class is optional, since the
// client can control builders directly.
class Director is
    // The director works with any builder instance that the
    // client code passes to it. This way, the client code may
    // alter the final type of the newly assembled product.
    // The director can construct several product variations
    // using the same building steps.
    method constructSportsCar(builder: Builder) is
        builder.reset()
        builder.setSeats(2)
        builder.setEngine(new SportEngine())
        builder.setTripComputer(true)
        builder.setGPS(true)

    method constructSUV(builder: Builder) is
        // ...


// The client code creates a builder object, passes it to the
// director and then initiates the construction process. The end
// result is retrieved from the builder object.
class Application is

    method makeCar() is
        director = new Director()

        CarBuilder builder = new CarBuilder()
        director.constructSportsCar(builder)
        Car car = builder.getProduct()

        CarManualBuilder builder = new CarManualBuilder()
        director.constructSportsCar(builder)

        // The final product is often retrieved from a builder
        // object since the director isn't aware of and not
        // dependent on concrete builders and products.
        Manual manual = builder.getProduct()
```

##  Applicability 适用性

* **Use the Builder pattern to get rid of a “telescoping constructor”. 使用 Builder 模式来摆脱“伸缩构造函数”。**

* Say you have a constructor with ten optional parameters. Calling such a beast is very inconvenient; therefore, you overload the constructor and create several shorter versions with fewer parameters. These constructors still refer to the main one, passing some default values into any omitted parameters.
假设您有一个包含十个可选参数的构造函数。召唤这样的野兽是很不方便的;因此，重载构造函数，并使用较少的参数创建多个较短的版本。这些构造函数仍然引用主构造函数，将一些默认值传递到任何省略的参数中。

```java
class Pizza {
    Pizza(int size) { ... }
    Pizza(int size, boolean cheese) { ... }
    Pizza(int size, boolean cheese, boolean pepperoni) { ... }
    // ...
```
Creating such a monster is only possible in languages that support method overloading, such as C# or Java.只有在支持方法重载的语言（如 C# 或 Java）中才能创建这样的怪物。

The Builder pattern lets you build objects step by step, using only those steps that you really need. After implementing the pattern, you don’t have to cram dozens of parameters into your constructors anymore.
Builder 模式允许您逐步构建对象，仅使用您真正需要的那些步骤。实现该模式后，您不必再将数十个参数塞入构造函数中。

* **Use the Builder pattern when you want your code to be able to create different representations of some product (for example, stone and wooden houses).当您希望代码能够创建某些产品（例如，石头和木屋）的不同表示形式时，请使用 Builder 模式。**

* The Builder pattern can be applied when construction of various representations of the product involves similar steps that differ only in the details.
当构建产品的各种表示形式涉及仅在细节上有所不同的类似步骤时，可以应用构建器模式。

The base builder interface defines all possible construction steps, and concrete builders implement these steps to construct particular representations of the product. Meanwhile, the director class guides the order of construction.
基础构建器界面定义了所有可能的构建步骤，具体构建器实现这些步骤来构建产品的特定表示。同时，director类指导施工顺序。

* **Use the Builder to construct Composite trees or other complex objects.使用构建器构建复合树或其他复杂对象。**

* The Builder pattern lets you construct products step-by-step. You could defer execution of some steps without breaking the final product. You can even call steps recursively, which comes in handy when you need to build an object tree.
Builder 模式允许您逐步构建产品。您可以在不破坏最终产品的情况下延迟某些步骤的执行。您甚至可以递归调用步骤，这在需要构建对象树时会派上用场。

A builder doesn’t expose the unfinished product while running construction steps. This prevents the client code from fetching an incomplete result.
构建器在运行构造步骤时不会暴露未完成的产品。这样可以防止客户端代码提取不完整的结果。

## How to Implement 如何实现

1. Make sure that you can clearly define the common construction steps for building all available product representations. Otherwise, you won’t be able to proceed with implementing the pattern.
确保您可以清楚地定义用于构建所有可用产品表示的常见构造步骤。否则，您将无法继续实现该模式。

2. Declare these steps in the base builder interface.
在基础构建器界面中声明这些步骤。

3. Create a concrete builder class for each of the product representations and implement their construction steps.
为每个产品表示形式创建一个具体的构建器类，并实现其构造步骤。

Don’t forget about implementing a method for fetching the result of the construction. The reason why this method can’t be declared inside the builder interface is that various builders may construct products that don’t have a common interface. Therefore, you don’t know what would be the return type for such a method. However, if you’re dealing with products from a single hierarchy, the fetching method can be safely added to the base interface.
不要忘记实现一个获取构造结果的方法。无法在生成器接口中声明此方法的原因是，各种生成器可能会构造没有通用接口的产品。因此，您不知道这种方法的返回类型是什么。但是，如果您要处理来自单个层次结构的产品，则可以安全地将提取方法添加到基本界面。

4.  Think about creating a director class. It may encapsulate various ways to construct a product using the same builder object.
考虑创建一个director类。它可以封装使用相同的构建器对象构建产品的各种方法。

5. The client code creates both the builder and the director objects. Before construction starts, the client must pass a builder object to the director. Usually, the client does this only once, via parameters of the director’s class constructor. The director uses the builder object in all further construction. There’s an alternative approach, where the builder is passed to a specific product construction method of the director.
客户端代码创建生成器和控制器对象。在构造开始之前，客户端必须将生成器对象传递给控制器。通常，客户端仅通过 director 类构造函数的参数执行此操作一次。director 在所有进一步的构造中使用 builder 对象。还有另一种方法，将构建器传递给主管的特定产品构建方法。

6. The construction result can be obtained directly from the director only if all products follow the same interface. Otherwise, the client should fetch the result from the builder.
只有当所有产品都遵循相同的接口时，才能直接从director那里获得施工结果。否则，客户端应从构建器获取结果。

## Pros and Cons 优点和缺点

### Pros 优点
* You can construct objects step-by-step, defer construction steps or run steps recursively.
您可以逐步构造对象、延迟构造步骤或递归运行步骤。

* You can reuse the same construction code when building various representations of products.
在构建产品的各种表示形式时，您可以重复使用相同的构造代码。

* Single Responsibility Principle. You can isolate complex construction code from the business logic of the product.
单一责任原则。您可以将复杂的构造代码与产品的业务逻辑隔离开来。

### 缺点
* The overall complexity of the code increases since the pattern requires creating multiple new classes.
代码的整体复杂性增加，因为该模式需要创建多个新类。

##  Relations with Other Patterns 与其他模式的关系

* Many designs start by using **Factory Method **(less complicated and more customizable via subclasses) and evolve toward **Abstract Factory**, **Prototype**, or **Builder** (more flexible, but more complicated).
许多设计从使用工厂方法（不那么复杂，通过子类更可定制）开始，然后发展到抽象工厂、原型或构建器（更灵活，但更复杂）。

* **Builder** focuses on constructing complex objects step by step. **Abstract Factory** specializes in creating families of related objects. **Abstract Factory** returns the product immediately, whereas Builder lets you run some additional construction steps before fetching the product.
Builder 专注于逐步构建复杂的对象。Abstract Factory专门用于创建相关对象的族。Abstract Factory 会立即返回产品，而 Builder 允许您在获取产品之前运行一些额外的构造步骤。

* You can use **Builder** when creating complex **Composite** trees because you can program its construction steps to work recursively.
在创建复杂的复合树时，可以使用 Builder，因为您可以对其构造步骤进行编程以递归方式工作。

* You can combine **Builder** with **Bridge**: the director class plays the role of the abstraction, while different builders act as implementations.
您可以将 Builder 与 Bridge 结合使用：director 类扮演抽象的角色，而不同的构建器充当实现。

* **Abstract Factories**, **Builders** and **Prototypes** can all be implemented as **Singletons**.
抽象工厂、构建器和原型都可以作为单例实现。

## Code Examples 代码示例

### python Conceptual Example 概念示例
This example illustrates the structure of the Builder design pattern. It focuses on answering these questions:
此示例说明了 Builder 设计模式的结构。它侧重于回答以下问题：

* What classes does it consist of?
它由哪些类组成？
* What roles do these classes play?
这些课程扮演什么角色？
* In what way the elements of the pattern are related?
模式的元素以何种方式相关？

main.py: 概念示例
```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any


class Builder(ABC):
    """
    The Builder interface specifies methods for creating the different parts of
    the Product objects.
    """

    @property
    @abstractmethod
    def product(self) -> None:
        pass

    @abstractmethod
    def produce_part_a(self) -> None:
        pass

    @abstractmethod
    def produce_part_b(self) -> None:
        pass

    @abstractmethod
    def produce_part_c(self) -> None:
        pass


class ConcreteBuilder1(Builder):
    """
    The Concrete Builder classes follow the Builder interface and provide
    specific implementations of the building steps. Your program may have
    several variations of Builders, implemented differently.
    """

    def __init__(self) -> None:
        """
        A fresh builder instance should contain a blank product object, which is
        used in further assembly.
        """
        self.reset()

    def reset(self) -> None:
        self._product = Product1()

    @property
    def product(self) -> Product1:
        """
        Concrete Builders are supposed to provide their own methods for
        retrieving results. That's because various types of builders may create
        entirely different products that don't follow the same interface.
        Therefore, such methods cannot be declared in the base Builder interface
        (at least in a statically typed programming language).

        Usually, after returning the end result to the client, a builder
        instance is expected to be ready to start producing another product.
        That's why it's a usual practice to call the reset method at the end of
        the `getProduct` method body. However, this behavior is not mandatory,
        and you can make your builders wait for an explicit reset call from the
        client code before disposing of the previous result.
        """
        product = self._product
        self.reset()
        return product

    def produce_part_a(self) -> None:
        self._product.add("PartA1")

    def produce_part_b(self) -> None:
        self._product.add("PartB1")

    def produce_part_c(self) -> None:
        self._product.add("PartC1")


class Product1():
    """
    It makes sense to use the Builder pattern only when your products are quite
    complex and require extensive configuration.

    Unlike in other creational patterns, different concrete builders can produce
    unrelated products. In other words, results of various builders may not
    always follow the same interface.
    """

    def __init__(self) -> None:
        self.parts = []

    def add(self, part: Any) -> None:
        self.parts.append(part)

    def list_parts(self) -> None:
        print(f"Product parts: {', '.join(self.parts)}", end="")


class Director:
    """
    The Director is only responsible for executing the building steps in a
    particular sequence. It is helpful when producing products according to a
    specific order or configuration. Strictly speaking, the Director class is
    optional, since the client can control builders directly.
    """

    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> Builder:
        return self._builder

    @builder.setter
    def builder(self, builder: Builder) -> None:
        """
        The Director works with any builder instance that the client code passes
        to it. This way, the client code may alter the final type of the newly
        assembled product.
        """
        self._builder = builder

    """
    The Director can construct several product variations using the same
    building steps.
    """

    def build_minimal_viable_product(self) -> None:
        self.builder.produce_part_a()

    def build_full_featured_product(self) -> None:
        self.builder.produce_part_a()
        self.builder.produce_part_b()
        self.builder.produce_part_c()


if __name__ == "__main__":
    """
    The client code creates a builder object, passes it to the director and then
    initiates the construction process. The end result is retrieved from the
    builder object.
    """

    director = Director()
    builder = ConcreteBuilder1()
    director.builder = builder

    print("Standard basic product: ")
    director.build_minimal_viable_product()
    builder.product.list_parts()

    print("\n")

    print("Standard full featured product: ")
    director.build_full_featured_product()
    builder.product.list_parts()

    print("\n")

    # Remember, the Builder pattern can be used without a Director class.
    print("Custom product: ")
    builder.produce_part_a()
    builder.produce_part_b()
    builder.product.list_parts()
```

### Output.txt: Execution result
```
Standard basic product:
Product parts: PartA1

Standard full featured product:
Product parts: PartA1, PartB1, PartC1

Custom product:
Product parts: PartA1, PartB1
```

### Rust 示例：Car & car manual builders

This slightly synthetic example illustrates how you can use the `Builder` pattern to construct totally different products using the same building process. For example, the trait Builder declares steps for assembling a car. However, depending on the builder implementation, a constructed object can be something different, for example, a car manual. The resulting manual will contain instructions from each building step, making it accurate and up-to-date.
这个略微合成的示例说明了如何使用 Builder 模式，通过相同的构建过程来构建完全不同的产品。例如，该特征 `Builder` 声明了组装汽车的步骤。但是，根据构建器实现的不同，构造的对象可以是不同的对象，例如汽车手册。由此产生的手册将包含每个构建步骤的说明，使其准确和最新。

The **Builder** design pattern is not the same as the **Fluent Interface** idiom (that relies on method chaining), although Rust developers sometimes use those terms interchangeably.
Builder 设计模式与 Fluent Interface 习惯用语（依赖于方法链）不同，尽管 Rust 开发人员有时会互换使用这些术语。

1. Fluent Interface is a way to chain methods for constructing or modifying an object using the following approach:
Fluent Interface 是一种使用以下方法链接用于构造或修改对象的方法的方法：
```rust
let car = Car::default().places(5).gas(30)
```
It’s pretty elegant way to construct an object. Still, such a code may not be an instance of the Builder pattern.
这是构造对象的非常优雅的方式。不过，这样的代码可能不是 Builder 模式的实例。

2. While the **Builder** pattern also suggests constructing object step by step, it also lets you build different types of products using the same construction process.
虽然 **Builder** 模式还建议逐步构建对象，但它也允许您使用相同的构建过程构建不同类型的产品。

### builders: Builders builders
#### builders/mod.rs
```rust
mod car;
mod car_manual;

use crate::components::{CarType, Engine, GpsNavigator, Transmission};

/// Builder defines how to assemble a car.
pub trait Builder {
    type OutputType;
    fn set_car_type(&mut self, car_type: CarType);
    fn set_seats(&mut self, seats: u16);
    fn set_engine(&mut self, engine: Engine);
    fn set_transmission(&mut self, transmission: Transmission);
    fn set_gsp_navigator(&mut self, gps_navigator: GpsNavigator);
    fn build(self) -> Self::OutputType;
}

pub use car::CarBuilder;
pub use car_manual::CarManualBuilder;
```
#### builders/car.rs
```rust
use crate::{
    cars::Car,
    components::{CarType, Engine, GpsNavigator, Transmission},
};

use super::Builder;

pub const DEFAULT_FUEL: f64 = 5f64;

#[derive(Default)]
pub struct CarBuilder {
    car_type: Option<CarType>,
    engine: Option<Engine>,
    gps_navigator: Option<GpsNavigator>,
    seats: Option<u16>,
    transmission: Option<Transmission>,
}

impl Builder for CarBuilder {
    type OutputType = Car;

    fn set_car_type(&mut self, car_type: CarType) {
        self.car_type = Some(car_type);
    }

    fn set_engine(&mut self, engine: Engine) {
        self.engine = Some(engine);
    }

    fn set_gsp_navigator(&mut self, gps_navigator: GpsNavigator) {
        self.gps_navigator = Some(gps_navigator);
    }

    fn set_seats(&mut self, seats: u16) {
        self.seats = Some(seats);
    }

    fn set_transmission(&mut self, transmission: Transmission) {
        self.transmission = Some(transmission);
    }

    fn build(self) -> Car {
        Car::new(
            self.car_type.expect("Please, set a car type"),
            self.seats.expect("Please, set a number of seats"),
            self.engine.expect("Please, set an engine configuration"),
            self.transmission.expect("Please, set up transmission"),
            self.gps_navigator,
            DEFAULT_FUEL,
        )
    }
}
```

#### builders/car_manual.rs

```rust
use crate::{
    cars::Manual,
    components::{CarType, Engine, GpsNavigator, Transmission},
};

use super::Builder;

#[derive(Default)]
pub struct CarManualBuilder {
    car_type: Option<CarType>,
    engine: Option<Engine>,
    gps_navigator: Option<GpsNavigator>,
    seats: Option<u16>,
    transmission: Option<Transmission>,
}

/// Builds a car manual instead of an actual car.
impl Builder for CarManualBuilder {
    type OutputType = Manual;

    fn set_car_type(&mut self, car_type: CarType) {
        self.car_type = Some(car_type);
    }

    fn set_engine(&mut self, engine: Engine) {
        self.engine = Some(engine);
    }

    fn set_gsp_navigator(&mut self, gps_navigator: GpsNavigator) {
        self.gps_navigator = Some(gps_navigator);
    }

    fn set_seats(&mut self, seats: u16) {
        self.seats = Some(seats);
    }

    fn set_transmission(&mut self, transmission: Transmission) {
        self.transmission = Some(transmission);
    }

    fn build(self) -> Manual {
        Manual::new(
            self.car_type.expect("Please, set a car type"),
            self.seats.expect("Please, set a number of seats"),
            self.engine.expect("Please, set an engine configuration"),
            self.transmission.expect("Please, set up transmission"),
            self.gps_navigator,
        )
    }
}
```

#### cars: Products

##### cars/mod.rs

```rust
mod car;
mod manual;

pub use car::Car;
pub use manual::Manual;
```

##### cars/car.rs
```rust
use crate::components::{CarType, Engine, GpsNavigator, Transmission};

pub struct Car {
    car_type: CarType,
    seats: u16,
    engine: Engine,
    transmission: Transmission,
    gps_navigator: Option<GpsNavigator>,
    fuel: f64,
}

impl Car {
    pub fn new(
        car_type: CarType,
        seats: u16,
        engine: Engine,
        transmission: Transmission,
        gps_navigator: Option<GpsNavigator>,
        fuel: f64,
    ) -> Self {
        Self {
            car_type,
            seats,
            engine,
            transmission,
            gps_navigator,
            fuel,
        }
    }

    pub fn car_type(&self) -> CarType {
        self.car_type
    }

    pub fn fuel(&self) -> f64 {
        self.fuel
    }

    pub fn set_fuel(&mut self, fuel: f64) {
        self.fuel = fuel;
    }

    pub fn seats(&self) -> u16 {
        self.seats
    }

    pub fn engine(&self) -> &Engine {
        &self.engine
    }

    pub fn transmission(&self) -> &Transmission {
        &self.transmission
    }

    pub fn gps_navigator(&self) -> &Option<GpsNavigator> {
        &self.gps_navigator
    }
}
```

##### cars/manual.rs

```rust
use crate::components::{CarType, Engine, GpsNavigator, Transmission};

pub struct Manual {
    car_type: CarType,
    seats: u16,
    engine: Engine,
    transmission: Transmission,
    gps_navigator: Option<GpsNavigator>,
}

impl Manual {
    pub fn new(
        car_type: CarType,
        seats: u16,
        engine: Engine,
        transmission: Transmission,
        gps_navigator: Option<GpsNavigator>,
    ) -> Self {
        Self {
            car_type,
            seats,
            engine,
            transmission,
            gps_navigator,
        }
    }
}

impl std::fmt::Display for Manual {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        writeln!(f, "Type of car: {:?}", self.car_type)?;
        writeln!(f, "Count of seats: {}", self.seats)?;
        writeln!(
            f,
            "Engine: volume - {}; mileage - {}",
            self.engine.volume(),
            self.engine.mileage()
        )?;
        writeln!(f, "Transmission: {:?}", self.transmission)?;
        match self.gps_navigator {
            Some(_) => writeln!(f, "GPS Navigator: Functional")?,
            None => writeln!(f, "GPS Navigator: N/A")?,
        };
        Ok(())
    }
}
```

#### components.rs: Product components
```rust
#[derive(Copy, Clone, Debug)]
pub enum CarType {
    CityCar,
    SportsCar,
    Suv,
}

#[derive(Debug)]
pub enum Transmission {
    SingleSpeed,
    Manual,
    Automatic,
    SemiAutomatic,
}

pub struct Engine {
    volume: f64,
    mileage: f64,
    started: bool,
}

impl Engine {
    pub fn new(volume: f64, mileage: f64) -> Self {
        Self {
            volume,
            mileage,
            started: false,
        }
    }

    pub fn on(&mut self) {
        self.started = true;
    }

    pub fn off(&mut self) {
        self.started = false;
    }

    pub fn started(&self) -> bool {
        self.started
    }

    pub fn volume(&self) -> f64 {
        self.volume
    }

    pub fn mileage(&self) -> f64 {
        self.mileage
    }

    pub fn go(&mut self, mileage: f64) {
        if self.started() {
            self.mileage += mileage;
        } else {
            println!("Cannot go(), you must start engine first!");
        }
    }
}

pub struct GpsNavigator {
    route: String,
}

impl GpsNavigator {
    pub fn new() -> Self {
        Self::from_route(
            "221b, Baker Street, London  to Scotland Yard, 8-10 Broadway, London".into(),
        )
    }

    pub fn from_route(route: String) -> Self {
        Self { route }
    }

    pub fn route(&self) -> &String {
        &self.route
    }
}
```

####  director.rs: Directors
```rust
use crate::{
    builders::Builder,
    components::{CarType, Engine, GpsNavigator, Transmission},
};

/// Director knows how to build a car.
///
/// However, a builder can build a car manual instead of an actual car,
/// everything depends on the concrete builder.
pub struct Director;

impl Director {
    pub fn construct_sports_car(builder: &mut impl Builder) {
        builder.set_car_type(CarType::SportsCar);
        builder.set_seats(2);
        builder.set_engine(Engine::new(3.0, 0.0));
        builder.set_transmission(Transmission::SemiAutomatic);
        builder.set_gsp_navigator(GpsNavigator::new());
    }

    pub fn construct_city_car(builder: &mut impl Builder) {
        builder.set_car_type(CarType::CityCar);
        builder.set_seats(2);
        builder.set_engine(Engine::new(1.2, 0.0));
        builder.set_transmission(Transmission::Automatic);
        builder.set_gsp_navigator(GpsNavigator::new());
    }

    pub fn construct_suv(builder: &mut impl Builder) {
        builder.set_car_type(CarType::Suv);
        builder.set_seats(4);
        builder.set_engine(Engine::new(2.5, 0.0));
        builder.set_transmission(Transmission::Manual);
        builder.set_gsp_navigator(GpsNavigator::new());
    }
}
```
#### main.rs: Client code
```rust
#![allow(unused)]

mod builders;
mod cars;
mod components;
mod director;

use builders::{Builder, CarBuilder, CarManualBuilder};
use cars::{Car, Manual};
use director::Director;

fn main() {
    let mut car_builder = CarBuilder::default();

    // Director gets the concrete builder object from the client
    // (application code). That's because application knows better which
    // builder to use to get a specific product.
    Director::construct_sports_car(&mut car_builder);

    // The final product is often retrieved from a builder object, since
    // Director is not aware and not dependent on concrete builders and
    // products.
    let car: Car = car_builder.build();
    println!("Car built: {:?}\n", car.car_type());

    let mut manual_builder = CarManualBuilder::default();

    // Director may know several building recipes.
    Director::construct_city_car(&mut manual_builder);

    // The final car manual.
    let manual: Manual = manual_builder.build();
    println!("Car manual built:\n{}", manual);
}
```

### Output
```
Car built: SportsCar

Car manual built:
Type of car: CityCar
Count of seats: 2
Engine: volume - 1.2; mileage - 0
Transmission: Automatic
GPS Navigator: Functional
```

