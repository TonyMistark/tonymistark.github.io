---
title: Prototype
categories:
  - design-pattern
date: 2023-11-22 21:10:02
---

# Prototype 原型

## Intent 意图

**Prototype** is a creational design pattern that lets you copy existing objects without making your code dependent on their classes.
原型是一种创建性设计模式，它允许您复制现有对象，而不会使代码依赖于它们的类。
<div align="center"> <img src="/images/prototype-head.png"/></div>

## Problem 问题

Say you have an object, and you want to create an exact copy of it. How would you do it? First, you have to create a new object of the same class. Then you have to go through all the fields of the original object and copy their values over to the new object.
假设你有一个对象，并且你想创建一个精确的副本。你会怎么做？首先，您必须创建同一类的新对象。然后，您必须遍历原始对象的所有字段，并将其值复制到新对象。

Nice! But there’s a catch. Not all objects can be copied that way because some of the object’s fields may be private and not visible from outside of the object itself.
好！但有一个问题。并非所有对象都可以以这种方式复制，因为对象的某些字段可能是私有的，并且从对象本身外部不可见。
<div align="center"> <img src="/images/prototype-comic-1-en.png"/>Copying an object “from the outside” isn’t always possible.</br>“从外部”复制对象并不总是可行的。</div>
There’s one more problem with the direct approach. Since you have to know the object’s class to create a duplicate, your code becomes dependent on that class. If the extra dependency doesn’t scare you, there’s another catch. Sometimes you only know the interface that the object follows, but not its concrete class, when, for example, a parameter in a method accepts any objects that follow some interface.
直接方法还有一个问题。由于您必须知道对象的类才能创建副本，因此您的代码将依赖于该类。如果额外的依赖关系没有吓到你，还有另一个问题。有时，您只知道对象所遵循的接口，而不知道其具体类，例如，当方法中的参数接受某个接口所遵循的任何对象时。

## Solution 解决方案

The Prototype pattern delegates the cloning process to the actual objects that are being cloned. The pattern declares a common interface for all objects that support cloning. This interface lets you clone an object without coupling your code to the class of that object. Usually, such an interface contains just a single `clone` method.
Prototype 模式将克隆过程委托给正在克隆的实际对象。该模式为支持克隆的所有对象声明一个通用接口。此接口允许您克隆对象，而无需将代码耦合到该对象的类。通常，这样的接口只包含一个 `clone` 方法。

The implementation of the clone method is very similar in all classes. The method creates an object of the current class and carries over all of the field values of the old object into the new one. You can even copy private fields because most programming languages let objects access private fields of other objects that belong to the same class.
该 `clone` 方法的实现在所有类中都非常相似。该方法创建当前类的对象，并将旧对象的所有字段值转移到新对象中。您甚至可以复制私有字段，因为大多数编程语言允许对象访问属于同一类的其他对象的私有字段。

An object that supports cloning is called a prototype. When your objects have dozens of fields and hundreds of possible configurations, cloning them might serve as an alternative to subclassing.
支持克隆的对象称为原型。当您的对象具有数十个字段和数百种可能的配置时，克隆它们可以作为子类化的替代方法。
<div align="center"> <img src="/images/prototype-comic-2-en.png"/>Pre-built prototypes can be an alternative to subclassing.</br>预构建的原型可以替代子类化。</div>
Here’s how it works: you create a set of objects, configured in various ways. When you need an object like the one you’ve configured, you just clone a prototype instead of constructing a new object from scratch.
它是这样工作的：创建一组对象，以各种方式进行配置。当您需要像您配置的对象一样的对象时，您只需克隆一个原型，而不是从头开始构建一个新对象。

## Real-World Analogy 真实世界的类比

In real life, prototypes are used for performing various tests before starting mass production of a product. However, in this case, prototypes don’t participate in any actual production, playing a passive role instead.
在现实生活中，原型用于在开始批量生产产品之前进行各种测试。然而，在这种情况下，原型不参与任何实际生产，而是扮演被动角色。
<div align="center"> <img src="/images/prototype-comic-3-en.png"/>The division of a cell.</br>细胞的分裂。</div>
Since industrial prototypes don’t really copy themselves, a much closer analogy to the pattern is the process of mitotic cell division (biology, remember?). After mitotic division, a pair of identical cells is formed. The original cell acts as a prototype and takes an active role in creating the copy.
由于工业原型并不能真正复制自己，因此与该模式更接近的类比是有丝分裂细胞分裂的过程（生物学，还记得吗？有丝分裂后，形成一对相同的细胞。原始单元充当原型，并在创建副本中发挥积极作用。

## Structure 结构
### Basic implementation 基本实现
<div align="center"> <img src="/images/prototyp-structure.png"/></div>
1. The **Prototype** interface declares the cloning methods. In most cases, it’s a single clone method.
Prototype 接口声明克隆方法。在大多数情况下，它是一种单一 clone 方法。

2. The `Concrete Prototype` class implements the cloning method. In addition to copying the original object’s data to the clone, this method may also handle some edge cases of the cloning process related to cloning linked objects, untangling recursive dependencies, etc.
Concrete Prototype 类实现克隆方法。除了将原始对象的数据复制到克隆中外，该方法还可以处理克隆过程中与克隆链接对象、解开递归依赖关系等相关的一些边缘情况。

3. The `Client` can produce a copy of any object that follows the prototype interface.
客户端可以生成遵循原型接口的任何对象的副本。

### Prototype registry implementation 原型注册表实现
<div align="center"> <img src="/images/structure-prototype-cache.png"/></div>
1. The `Prototype Registry` provides an easy way to access frequently-used prototypes. It stores a set of pre-built objects that are ready to be copied. The simplest prototype registry is a name → prototype hash map. However, if you need better search criteria than a simple name, you can build a much more robust version of the registry.
Prototype Registry 提供了一种访问常用原型的简单方法。它存储一组准备复制的预构建对象。最简单的原型注册表是 name → prototype 哈希映射。但是，如果您需要比简单名称更好的搜索条件，则可以构建更可靠的注册表版本。

##  Pseudocode 伪代码
In this example, the Prototype pattern lets you produce exact copies of geometric objects, without coupling the code to their classes.
在此示例中，Prototype 模式允许您生成几何对象的精确副本，而无需将代码耦合到其类。
<div align="center"> <img src="/images/prototype-example1.png"/>Cloning a set of objects that belong to a class hierarchy.</br>克隆属于类层次结构的一组对象。</div>

All shape classes follow the same interface, which provides a cloning method. A subclass may call the parent’s cloning method before copying its own field values to the resulting object.
所有形状类都遵循相同的接口，该接口提供克隆方法。子类可以在将其自己的字段值复制到生成的对象之前调用父类的克隆方法。
```java
// Base prototype.
abstract class Shape is
    field X: int
    field Y: int
    field color: string

    // A regular constructor.
    constructor Shape() is
        // ...

    // The prototype constructor. A fresh object is initialized
    // with values from the existing object.
    constructor Shape(source: Shape) is
        this()
        this.X = source.X
        this.Y = source.Y
        this.color = source.color

    // The clone operation returns one of the Shape subclasses.
    abstract method clone():Shape


// Concrete prototype. The cloning method creates a new object
// in one go by calling the constructor of the current class and
// passing the current object as the constructor's argument.
// Performing all the actual copying in the constructor helps to
// keep the result consistent: the constructor will not return a
// result until the new object is fully built; thus, no object
// can have a reference to a partially-built clone.
class Rectangle extends Shape is
    field width: int
    field height: int

    constructor Rectangle(source: Rectangle) is
        // A parent constructor call is needed to copy private
        // fields defined in the parent class.
        super(source)
        this.width = source.width
        this.height = source.height

    method clone():Shape is
        return new Rectangle(this)


class Circle extends Shape is
    field radius: int

    constructor Circle(source: Circle) is
        super(source)
        this.radius = source.radius

    method clone():Shape is
        return new Circle(this)


// Somewhere in the client code.
class Application is
    field shapes: array of Shape

    constructor Application() is
        Circle circle = new Circle()
        circle.X = 10
        circle.Y = 10
        circle.radius = 20
        shapes.add(circle)

        Circle anotherCircle = circle.clone()
        shapes.add(anotherCircle)
        // The `anotherCircle` variable contains an exact copy
        // of the `circle` object.

        Rectangle rectangle = new Rectangle()
        rectangle.width = 10
        rectangle.height = 20
        shapes.add(rectangle)

    method businessLogic() is
        // Prototype rocks because it lets you produce a copy of
        // an object without knowing anything about its type.
        Array shapesCopy = new Array of Shapes.

        // For instance, we don't know the exact elements in the
        // shapes array. All we know is that they are all
        // shapes. But thanks to polymorphism, when we call the
        // `clone` method on a shape the program checks its real
        // class and runs the appropriate clone method defined
        // in that class. That's why we get proper clones
        // instead of a set of simple Shape objects.
        foreach (s in shapes) do
            shapesCopy.add(s.clone())

        // The `shapesCopy` array contains exact copies of the
        // `shape` array's children.
```
## Applicability 适用性

* **Use the Prototype pattern when your code shouldn’t depend on the concrete classes of objects that you need to copy.当代码不应依赖于需要复制的具体对象类时，请使用 Prototype 模式。**

* This happens a lot when your code works with objects passed to you from 3rd-party code via some interface. The concrete classes of these objects are unknown, and you couldn’t depend on them even if you wanted to.
当您的代码使用通过某些接口从第三方代码传递给您的对象时，这种情况经常发生。这些对象的具体类别是未知的，即使你愿意，你也不能依赖它们。

The Prototype pattern provides the client code with a general interface for working with all objects that support cloning. This interface makes the client code independent from the concrete classes of objects that it clones.
Prototype 模式为客户端代码提供了一个通用接口，用于处理支持克隆的所有对象。此接口使客户端代码独立于它克隆的对象的具体类。

* **Use the pattern when you want to reduce the number of subclasses that only differ in the way they initialize their respective objects.
如果要减少子类的数量，这些子类仅在初始化各自对象的方式上有所不同，请使用该模式。**

* Suppose you have a complex class that requires a laborious configuration before it can be used. There are several common ways to configure this class, and this code is scattered through your app. To reduce the duplication, you create several subclasses and put every common configuration code into their constructors. You solved the duplication problem, but now you have lots of dummy subclasses.
假设您有一个复杂的类，需要费力的配置才能使用它。有几种常用方法可以配置此类，并且此代码分散在应用中。为了减少重复，您可以创建多个子类，并将每个通用配置代码放入其构造函数中。您解决了重复问题，但现在您有很多虚拟子类。

The Prototype pattern lets you use a set of pre-built objects configured in various ways as prototypes. Instead of instantiating a subclass that matches some configuration, the client can simply look for an appropriate prototype and clone it.
Prototype模式允许您使用一组以各种方式配置的预构建对象作为原型。客户端可以简单地寻找一个合适的原型并克隆它，而不是实例化一个匹配某些配置的子类。

## How to Implement 如何实现
1. Create the prototype interface and declare the `clone` method in it. Or just add the method to all classes of an existing class hierarchy, if you have one.
创建原型接口并在其中声明 `clone` 方法。或者，只需将该方法添加到现有类层次结构的所有类（如果有）。

2. A prototype class must define the alternative constructor that accepts an object of that class as an argument. The constructor must copy the values of all fields defined in the class from the passed object into the newly created instance. If you’re changing a subclass, you must call the parent constructor to let the superclass handle the cloning of its private fields.
原型类必须定义接受该类的对象作为参数的替代构造函数。构造函数必须将类中定义的所有字段的值从传递的对象复制到新创建的实例中。如果要更改子类，则必须调用父构造函数，让超类处理其私有字段的克隆。

If your programming language doesn’t support method overloading, you won’t be able to create a separate “prototype” constructor. Thus, copying the object’s data into the newly created clone will have to be performed within the `clone` method. Still, having this code in a regular constructor is safer because the resulting object is returned fully configured right after you call the `new` operator.
如果你的编程语言不支持方法重载，你将无法创建单独的“原型”构造函数。因此，必须在 `clone` 该方法中将对象的数据复制到新创建的克隆中。不过，在常规构造函数中使用此代码更安全，因为在调用 `new` 运算符后立即返回完全配置的结果对象。

3. The cloning method usually consists of just one line: running a `new` operator with the prototypical version of the constructor. Note, that every class must explicitly override the cloning method and use its own class name along with the `new` operator. Otherwise, the cloning method may produce an object of a parent class.
克隆方法通常只包含一行：使用构造函数的原型版本运行运 `new` 算符。请注意，每个类都必须显式覆盖克隆方法，并使用自己的类名和 `new` 运算符。否则，克隆方法可能会生成父类的对象。

4. Optionally, create a centralized prototype registry to store a catalog of frequently used prototypes.
（可选）创建一个集中式原型注册表来存储常用原型的目录。

You can implement the registry as a new factory class or put it in the base prototype class with a static method for fetching the prototype. This method should search for a prototype based on search criteria that the client code passes to the method. The criteria might either be a simple string tag or a complex set of search parameters. After the appropriate prototype is found, the registry should clone it and return the copy to the client.
您可以将注册表实现为新的工厂类，也可以使用用于获取原型的静态方法将其放在基原型类中。此方法应根据客户端代码传递给该方法的搜索条件搜索原型。条件可以是简单的字符串标记，也可以是一组复杂的搜索参数。找到适当的原型后，注册表应克隆它并将副本返回给客户端。

Finally, replace the direct calls to the subclasses’ constructors with calls to the factory method of the prototype registry.
最后，将对子类构造函数的直接调用替换为对原型注册表的工厂方法的调用。

## Pros and Cons 优点和缺点
* You can clone objects without coupling to their concrete classes.
您可以克隆对象，而无需耦合到其具体类。

| Pros 优点 | Cons 缺点 |
| --- | --- |
|You can clone objects without coupling to their concrete classes.您可以克隆对象，而无需耦合到其具体类。 |Cloning complex objects that have circular references might be very tricky.克隆具有循环引用的复杂对象可能非常棘手。 |
|You can get rid of repeated initialization code in favor of cloning pre-built prototypes.您可以摆脱重复的初始化代码，转而克隆预构建的原型。 | |
|You can produce complex objects more conveniently.您可以更方便地生成复杂的对象。 | |
|You get an alternative to inheritance when dealing with configuration presets for complex objects.在处理复杂对象的配置预设时，您可以获得继承的替代方法。 | |

## Relations with Other Patterns 与其他模式的关系
* Many designs start by using `Factory Method` (less complicated and more customizable via subclasses) and evolve toward `Abstract Factory`, Prototype, or Builder (more flexible, but more complicated).
许多设计从使用工厂方法（不那么复杂，通过子类更可定制）开始，然后发展到抽象工厂、原型或构建器（更灵活，但更复杂）。

* `Abstract Factory` classes are often based on a set of `Factory Methods`, but you can also use `Prototype` to compose the methods on these classes.
抽象工厂类通常基于一组工厂方法，但您也可以使用 Prototype 来组合这些类的方法。

* `Prototype` can help when you need to save copies of `Commands` into history.
当您需要将命令的副本保存到历史记录中时，Prototype 可以提供帮助。

* Designs that make heavy use of `Composite` and `Decorator` can often benefit from using `Prototype`. Applying the pattern lets you clone complex structures instead of re-constructing them from scratch.
大量使用 Composite 和 Decorator 的设计通常可以从使用 Prototype 中受益。通过应用该模式，您可以克隆复杂的结构，而不是从头开始重新构建它们。

* `Prototype` isn’t based on inheritance, so it doesn’t have its drawbacks. On the other hand, Prototype requires a complicated initialization of the cloned object. `Factory Method` is based on inheritance but doesn’t require an initialization step.
原型不是基于继承的，所以它没有缺点。另一方面，Prototype 需要对克隆对象进行复杂的初始化。工厂方法基于继承，但不需要初始化步骤。

* Sometimes `Prototype` can be a simpler alternative to `Memento`. This works if the object, the state of which you want to store in the history, is fairly straightforward and doesn’t have links to external resources, or the links are easy to re-establish.
有时，Prototype 可以成为 Memento 的更简单替代品。如果要存储在历史记录中的对象的状态相当简单，并且没有指向外部资源的链接，或者链接易于重新建立，则此方法有效。

* `Abstract Factories`, `Builders` and `Prototypes` can all be implemented as `Singletons`.
抽象工厂、构建器和原型都可以作为单例实现。

## Code Examples 代码示例
### Python Conceptual example
```python
import copy


class SelfReferencingEntity:
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


class SomeComponent:
    """
    Python provides its own interface of Prototype via `copy.copy` and
    `copy.deepcopy` functions. And any class that wants to implement custom
    implementations have to override `__copy__` and `__deepcopy__` member
    functions.
    """

    def __init__(self, some_int, some_list_of_objects, some_circular_ref):
        self.some_int = some_int
        self.some_list_of_objects = some_list_of_objects
        self.some_circular_ref = some_circular_ref

    def __copy__(self):
        """
        Create a shallow copy. This method will be called whenever someone calls
        `copy.copy` with this object and the returned value is returned as the
        new shallow copy.
        """

        # First, let's create copies of the nested objects.
        some_list_of_objects = copy.copy(self.some_list_of_objects)
        some_circular_ref = copy.copy(self.some_circular_ref)

        # Then, let's clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(
            self.some_int, some_list_of_objects, some_circular_ref
        )
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo=None):
        """
        Create a deep copy. This method will be called whenever someone calls
        `copy.deepcopy` with this object and the returned value is returned as
        the new deep copy.

        What is the use of the argument `memo`? Memo is the dictionary that is
        used by the `deepcopy` library to prevent infinite recursive copies in
        instances of circular references. Pass it to all the `deepcopy` calls
        you make in the `__deepcopy__` implementation to prevent infinite
        recursions.
        """
        if memo is None:
            memo = {}

        # First, let's create copies of the nested objects.
        some_list_of_objects = copy.deepcopy(self.some_list_of_objects, memo)
        some_circular_ref = copy.deepcopy(self.some_circular_ref, memo)

        # Then, let's clone the object itself, using the prepared clones of the
        # nested objects.
        new = self.__class__(
            self.some_int, some_list_of_objects, some_circular_ref
        )
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new


if __name__ == "__main__":

    list_of_objects = [1, {1, 2, 3}, [1, 2, 3]]
    circular_ref = SelfReferencingEntity()
    component = SomeComponent(23, list_of_objects, circular_ref)
    circular_ref.set_parent(component)

    shallow_copied_component = copy.copy(component)

    # Let's change the list in shallow_copied_component and see if it changes in
    # component.
    shallow_copied_component.some_list_of_objects.append("another object")
    if component.some_list_of_objects[-1] == "another object":
        print(
            "Adding elements to `shallow_copied_component`'s "
            "some_list_of_objects adds it to `component`'s "
            "some_list_of_objects."
        )
    else:
        print(
            "Adding elements to `shallow_copied_component`'s "
            "some_list_of_objects doesn't add it to `component`'s "
            "some_list_of_objects."
        )

    # Let's change the set in the list of objects.
    component.some_list_of_objects[1].add(4)
    if 4 in shallow_copied_component.some_list_of_objects[1]:
        print(
            "Changing objects in the `component`'s some_list_of_objects "
            "changes that object in `shallow_copied_component`'s "
            "some_list_of_objects."
        )
    else:
        print(
            "Changing objects in the `component`'s some_list_of_objects "
            "doesn't change that object in `shallow_copied_component`'s "
            "some_list_of_objects."
        )

    deep_copied_component = copy.deepcopy(component)

    # Let's change the list in deep_copied_component and see if it changes in
    # component.
    deep_copied_component.some_list_of_objects.append("one more object")
    if component.some_list_of_objects[-1] == "one more object":
        print(
            "Adding elements to `deep_copied_component`'s "
            "some_list_of_objects adds it to `component`'s "
            "some_list_of_objects."
        )
    else:
        print(
            "Adding elements to `deep_copied_component`'s "
            "some_list_of_objects doesn't add it to `component`'s "
            "some_list_of_objects."
        )

    # Let's change the set in the list of objects.
    component.some_list_of_objects[1].add(10)
    if 10 in deep_copied_component.some_list_of_objects[1]:
        print(
            "Changing objects in the `component`'s some_list_of_objects "
            "changes that object in `deep_copied_component`'s "
            "some_list_of_objects."
        )
    else:
        print(
            "Changing objects in the `component`'s some_list_of_objects "
            "doesn't change that object in `deep_copied_component`'s "
            "some_list_of_objects."
        )

    print(
        f"id(deep_copied_component.some_circular_ref.parent): "
        f"{id(deep_copied_component.some_circular_ref.parent)}"
    )
    print(
        f"id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent): "
        f"{id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent)}"
    )
    print(
        "^^ This shows that deepcopied objects contain same reference, they "
        "are not cloned repeatedly."
    )
```

### Output.txt: Execution result
```
Adding elements to `shallow_copied_component`'s some_list_of_objects adds it to `component`'s some_list_of_objects.
Changing objects in the `component`'s some_list_of_objects changes that object in `shallow_copied_component`'s some_list_of_objects.
Adding elements to `deep_copied_component`'s some_list_of_objects doesn't add it to `component`'s some_list_of_objects.
Changing objects in the `component`'s some_list_of_objects doesn't change that object in `deep_copied_component`'s some_list_of_objects.
id(deep_copied_component.some_circular_ref.parent): 4429472784
id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent): 4429472784
^^ This shows that deepcopied objects contain same reference, they are not cloned repeatedly.
```

### Rust Built-in Clone trait 内置克隆特征
Rust has a built-in `std::clone::Clone` trait with many implementations for various types (via `#[derive(Clone)]`). Thus, the Prototype pattern is ready to use out of the box.
Rust 有一个内置 `std::clone::Clone` 的特性，具有许多针对各种类型的实现（通过 `#[derive(Clone)]` ）。因此，原型模式可以开箱即用。

#### main.rs
```rust
#[derive(Clone)]
struct Circle {
    pub x: u32,
    pub y: u32,
    pub radius: u32,
}

fn main() {
    let circle1 = Circle {
        x: 10,
        y: 15,
        radius: 10,
    };

    // Prototype in action.
    let mut circle2 = circle1.clone();
    circle2.radius = 77;

    println!("Circle 1: {}, {}, {}", circle1.x, circle1.y, circle1.radius);
    println!("Circle 2: {}, {}, {}", circle2.x, circle2.y, circle2.radius);
}
```

### Output
```
Circle 1: 10, 15, 10
Circle 2: 10, 15, 77
```



