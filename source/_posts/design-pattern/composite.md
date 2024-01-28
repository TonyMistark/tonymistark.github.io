---
title: Composite 部分-整体模式
categories:
  - design-pattern
tags: Design Pattern
date: 2023-12-07 21:52:43
---

# Composite 部分-整体模式

Also known as: Object Tree
也称为：对象树

## Intent 意图

**Composite** is a structural design pattern that lets you compose objects into tree structures and then work with these structures as if they were individual objects.
复合是一种结构设计模式，可用于将对象组合成树结构，然后像使用单个对象一样处理这些结构。
<div align="center"> <img src="/images/composite-header.png"/></div>

## Problem 问题
Using the Composite pattern makes sense only when the core model of your app can be represented as a tree.
只有当应用的核心模型可以表示为树时，使用复合模式才有意义。

For example, imagine that you have two types of objects: `Products` and `Boxes`. A `Box` can contain several `Products` as well as a number of smaller `Boxes`. These little `Boxes` can also hold some `Products` or even smaller `Boxes`, and so on.
例如，假设您有两种类型的对象： `Products` 和 `Boxes`。 一个 `Box` 可以包含多个以及多个 `Products` 较小的 `Boxes`。这些小的也可以容纳一些 `Products` 甚至更小 `Boxes` 的 `Boxes` ，以此类推。

Say you decide to create an ordering system that uses these classes. Orders could contain simple products without any wrapping, as well as boxes stuffed with products...and other boxes. How would you determine the total price of such an order?
假设您决定创建一个使用这些类的排序系统。订单可以包含没有任何包装的简单产品，也可以包含装满产品的盒子......和其他盒子。您如何确定此类订单的总价？
<div align="center"> <img src="/images/composite-problem-en.png"/>An order might comprise various products, packaged in boxes, which are packaged in bigger boxes and so on. The whole structure looks like an upside down tree.</br>一个订单可能包括各种产品，包装在盒子里，这些产品包装在更大的盒子里，依此类推。整个结构看起来像一棵倒置的树。</div>

You could try the direct approach: unwrap all the boxes, go over all the products and then calculate the total. That would be doable in the real world; but in a program, it’s not as simple as running a loop. You have to know the classes of `Products` and `Boxes` you’re going through, the nesting level of the boxes and other nasty details beforehand. All of this makes the direct approach either too awkward or even impossible.
您可以尝试直接方法：打开所有盒子，检查所有产品，然后计算总数。这在现实世界中是可行的;但在程序中，它并不像运行循环那么简单。你必须事先知道 `Boxes` 你正在经历的 `Products` 类别、盒子的嵌套级别和其他令人讨厌的细节。所有这些都使得直接方法要么过于尴尬，甚至不可能。

## Solution 解决方案
The Composite pattern suggests that you work with `Products` and `Boxes` through a common interface which declares a method for calculating the total price.
复合模式建议您使用 `Products` 并通过 `Boxes` 一个通用接口进行工作，该接口声明了计算总价的方法。

How would this method work? For a product, it’d simply return the product’s price. For a box, it’d go over each item the box contains, ask its price and then return a total for this box. If one of these items were a smaller box, that box would also start going over its contents and so on, until the prices of all inner components were calculated. A box could even add some extra cost to the final price, such as packaging cost.
这种方法如何工作？对于产品，它只会返回产品的价格。对于一个盒子，它会检查盒子里的每件物品，询问它的价格，然后返回这个盒子的总数。如果其中一个物品是一个较小的盒子，那么该盒子也会开始检查其内容，依此类推，直到计算出所有内部组件的价格。一个盒子甚至会给最终价格增加一些额外的成本，比如包装成本。
<div align="center"> <img src="/images/composite-comic-1-en.png"/>The Composite pattern lets you run a behavior recursively over all components of an object tree.</br>Composite 模式允许您以递归方式对对象树的所有组件运行行为。</div>

The greatest benefit of this approach is that you don’t need to care about the concrete classes of objects that compose the tree. You don’t need to know whether an object is a simple product or a sophisticated box. You can treat them all the same via the common interface. When you call a method, the objects themselves pass the request down the tree.
这种方法的最大好处是，您不需要关心组成树的具体对象类。您不需要知道一个对象是简单的产品还是复杂的盒子。您可以通过通用界面对它们一视同仁。调用方法时，对象本身会将请求传递到树中。

## Real-World Analogy 真实世界的类比
<div align="center"> <img src="/images/composite-live-example.png"/>An example of a military structure.</br>军事结构的一个例子。</div>
Armies of most countries are structured as hierarchies. An army consists of several divisions; a division is a set of brigades, and a brigade consists of platoons, which can be broken down into squads. Finally, a squad is a small group of real soldiers. Orders are given at the top of the hierarchy and passed down onto each level until every soldier knows what needs to be done.
大多数国家的军队都是等级制度。一支军队由几个师组成;一个师是一组旅，一个旅由排组成，排可以分解成小队。最后，小队是一小群真正的士兵。命令在等级制度的顶端下达，并向下传递到每个级别，直到每个士兵都知道需要做什么。

## Structure 结构
<div align="center"> <img src="/images/composite-structure-en.png"/></div>

1. The **Component** interface describes operations that are common to both simple and complex elements of the tree.
**Component** 接口描述树的简单元素和复杂元素通用的操作。

2. The Leaf is a basic element of a tree that doesn’t have sub-elements.
叶子是树的基本元素，没有子元素。

Usually, leaf components end up doing most of the real work, since they don’t have anyone to delegate the work to.
通常，叶子组件最终会完成大部分实际工作，因为它们没有人可以将工作委派给它们。

3. The **Container** (aka composite) is an element that has sub-elements: leaves or other containers. A container doesn’t know the concrete classes of its children. It works with all sub-elements only via the component interface.
容器（又名复合）是一个具有子元素的元素：树叶或其他容器。容器不知道其子项的具体类。它仅通过组件接口处理所有子元素。

Upon receiving a request, a container delegates the work to its sub-elements, processes intermediate results and then returns the final result to the client.
收到请求后，容器将工作委托给其子元素，处理中间结果，然后将最终结果返回给客户端。

4. The **Client** works with all elements through the component interface. As a result, the client can work in the same way with both simple or complex elements of the tree.
客户端通过组件接口处理所有元素。因此，客户端可以以相同的方式处理树的简单或复杂元素。

## Pseudocode 伪代码

In this example, the **Composite** pattern lets you implement stacking of geometric shapes in a graphical editor.
在此示例中，复合模式允许您在图形编辑器中实现几何形状的堆叠。
<div align="center"> <img src="/images/composite-example1.png"/>The geometric shapes editor example.</br>几何形状编辑器示例。</div>

The `CompoundGraphic` class is a container that can comprise any number of sub-shapes, including other compound shapes. A compound shape has the same methods as a simple shape. However, instead of doing something on its own, a compound shape passes the request recursively to all its children and “sums up” the result.
该 `CompoundGraphic` 类是一个容器，可以包含任意数量的子形状，包括其他复合形状。复合形状与简单形状具有相同的方法。但是，复合形状不是自己执行某些操作，而是以递归方式将请求传递给其所有子项，并“汇总”结果。

The client code works with all shapes through the single interface common to all shape classes. Thus, the client doesn’t know whether it’s working with a simple shape or a compound one. The client can work with very complex object structures without being coupled to concrete classes that form that structure.
客户端代码通过所有形状类通用的单个接口处理所有形状。因此，客户不知道它是在处理简单形状还是复合形状。客户端可以使用非常复杂的对象结构，而无需与构成该结构的具体类耦合。
```Java
// The component interface declares common operations for both
// simple and complex objects of a composition.
interface Graphic is
    method move(x, y)
    method draw()

// The leaf class represents end objects of a composition. A
// leaf object can't have any sub-objects. Usually, it's leaf
// objects that do the actual work, while composite objects only
// delegate to their sub-components.
class Dot implements Graphic is
    field x, y

    constructor Dot(x, y) { ... }

    method move(x, y) is
        this.x += x, this.y += y

    method draw() is
        // Draw a dot at X and Y.

// All component classes can extend other components.
class Circle extends Dot is
    field radius

    constructor Circle(x, y, radius) { ... }

    method draw() is
        // Draw a circle at X and Y with radius R.

// The composite class represents complex components that may
// have children. Composite objects usually delegate the actual
// work to their children and then "sum up" the result.
class CompoundGraphic implements Graphic is
    field children: array of Graphic

    // A composite object can add or remove other components
    // (both simple or complex) to or from its child list.
    method add(child: Graphic) is
        // Add a child to the array of children.

    method remove(child: Graphic) is
        // Remove a child from the array of children.

    method move(x, y) is
        foreach (child in children) do
            child.move(x, y)

    // A composite executes its primary logic in a particular
    // way. It traverses recursively through all its children,
    // collecting and summing up their results. Since the
    // composite's children pass these calls to their own
    // children and so forth, the whole object tree is traversed
    // as a result.
    method draw() is
        // 1. For each child component:
        //     - Draw the component.
        //     - Update the bounding rectangle.
        // 2. Draw a dashed rectangle using the bounding
        // coordinates.


// The client code works with all the components via their base
// interface. This way the client code can support simple leaf
// components as well as complex composites.
class ImageEditor is
    field all: CompoundGraphic

    method load() is
        all = new CompoundGraphic()
        all.add(new Dot(1, 2))
        all.add(new Circle(5, 3, 10))
        // ...

    // Combine selected components into one complex composite
    // component.
    method groupSelected(components: array of Graphic) is
        group = new CompoundGraphic()
        foreach (component in components) do
            group.add(component)
            all.remove(component)
        all.add(group)
        // All components will be drawn.
        all.draw()
```

## Applicability 适用性

* ** Use the Composite pattern when you have to implement a tree-like object structure. 当必须实现树状对象结构时，请使用 Composite 模式。**

* The Composite pattern provides you with two basic element types that share a common interface: simple leaves and complex containers. A container can be composed of both leaves and other containers. This lets you construct a nested recursive object structure that resembles a tree.
Composite 模式为您提供了两种共享通用接口的基本元素类型：简单叶子和复杂容器。容器可以由叶子和其他容器组成。这使您可以构造类似于树的嵌套递归对象结构。

* **Use the pattern when you want the client code to treat both simple and complex elements uniformly. 如果希望客户端代码统一处理简单元素和复杂元素，请使用该模式。**

* All elements defined by the Composite pattern share a common interface. Using this interface, the client doesn’t have to worry about the concrete class of the objects it works with.
Composite 模式定义的所有元素共享一个公共接口。使用此接口，客户端不必担心它所处理的对象的具体类。

## How to Implement 如何实现

1. Make sure that the core model of your app can be represented as a tree structure. Try to break it down into simple elements and containers. Remember that containers must be able to contain both simple elements and other containers.
确保应用的核心模型可以表示为树结构。尝试将其分解为简单的元素和容器。请记住，容器必须能够同时包含简单元素和其他容器。

2. Declare the component interface with a list of methods that make sense for both simple and complex components.
使用对简单和复杂组件都有意义的方法列表声明组件接口。

3. Create a leaf class to represent simple elements. A program may have multiple different leaf classes.
创建一个叶类来表示简单元素。一个程序可以有多个不同的叶类。

Create a container class to represent complex elements. In this class, provide an array field for storing references to sub-elements. The array must be able to store both leaves and containers, so make sure it’s declared with the component interface type.
创建一个容器类来表示复杂元素。在此类中，提供一个数组字段，用于存储对子元素的引用。数组必须能够存储叶子和容器，因此请确保使用组件接口类型声明它。

4. While implementing the methods of the component interface, remember that a container is supposed to be delegating most of the work to sub-elements.
在实现组件接口的方法时，请记住，容器应该将大部分工作委托给子元素。

5. Finally, define the methods for adding and removal of child elements in the container.
最后，定义在容器中添加和删除子元素的方法。

Keep in mind that these operations can be declared in the component interface. This would violate the Interface Segregation Principle because the methods will be empty in the leaf class. However, the client will be able to treat all the elements equally, even when composing the tree.
请记住，这些操作可以在组件接口中声明。这将违反接口隔离原则，因为方法在叶类中为空。但是，客户端将能够平等地对待所有元素，即使在组成树时也是如此。

## Pros and Cons 优点和缺点

| Pros 优点 | Cons 缺点 |
| --- | --- |
| You can work with complex tree structures more conveniently: use polymorphism and recursion to your advantage. 您可以更方便地使用复杂的树结构：使用多态性和递归来发挥自己的优势。 | It might be difficult to provide a common interface for classes whose functionality differs too much. In certain scenarios, you’d need to overgeneralize the component interface, making it harder to comprehend.可能很难为功能差异太大的类提供通用接口。在某些情况下，需要过度概括组件接口，使其更难理解。|
| Open/Closed Principle. You can introduce new element types into the app without breaking the existing code, which now works with the object tree. 开/闭原理。您可以在不破坏现有代码的情况下将新的元素类型引入应用程序，这些代码现在适用于对象树。 |  |

## Relations with Other Patterns 与其他模式的关系

* You can use **Builder** when creating complex **Composite** trees because you can program its construction steps to work recursively.
在创建复杂的复合树时，可以使用 Builder，因为您可以对其构造步骤进行编程以递归方式工作。

* Chain of **Responsibility** is often used in conjunction with **Composite**. In this case, when a leaf component gets a request, it may pass it through the chain of all of the parent components down to the root of the object tree.
责任链通常与复合结合使用。在这种情况下，当叶组件收到请求时，它可能会通过所有父组件的链向下传递到对象树的根目录。

* You can use **Iterators** to traverse **Composite** trees.
可以使用迭代器遍历复合树。

* You can use Visitor to execute an operation over an entire **Composite** tree.
您可以使用 Visitor 对整个复合树执行操作。

* You can implement shared leaf nodes of the **Composite** tree as **Flyweights** to save some RAM.
您可以将复合树的共享叶节点实现为轻量级，以节省一些 RAM。

* **Composite** and **Decorator** have similar structure diagrams since both rely on recursive composition to organize an open-ended number of objects.
Composite 和 Decorator 具有相似的结构图，因为两者都依赖于递归组合来组织开放数量的对象。
A Decorator is like a Composite but only has one child component. There’s another significant difference: Decorator adds additional responsibilities to the wrapped object, while Composite just “sums up” its children’s results.
装饰器类似于 Composite，但只有一个子组件。还有另一个显著的区别：Decorator 为包装的对象添加了额外的职责，而 Composite 只是“汇总”其子对象的结果。
However, the patterns can also cooperate: you can use Decorator to extend the behavior of a specific object in the Composite tree.
但是，这些模式也可以协同工作：您可以使用 Decorator 来扩展 **Composite** 树中特定对象的行为。

* Designs that make heavy use of **Composite** and **Decorator** can often benefit from using **Prototype**. Applying the pattern lets you clone complex structures instead of re-constructing them from scratch.
大量使用 **Composite** 和 **Decorator** 的设计通常可以从使用 **Prototype** 中受益。通过应用该模式，您可以克隆复杂的结构，而不是从头开始重新构建它们。

##  Code Examples 代码示例

### Python Conceptual Example 概念示例
This example illustrates the structure of the Composite design pattern. It focuses on answering these questions:
此示例阐释了 Composite 设计模式的结构。它侧重于回答以下问题：

* What classes does it consist of?
它由哪些类组成？
* What roles do these classes play?
这些课程扮演什么角色？
* In what way the elements of the pattern are related?
模式的元素以何种方式相关？

#### main.py
```python
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List


class Component(ABC):
    """
    The base Component class declares common operations for both simple and
    complex objects of a composition.
    """

    @property
    def parent(self) -> Component:
        return self._parent

    @parent.setter
    def parent(self, parent: Component):
        """
        Optionally, the base Component can declare an interface for setting and
        accessing a parent of the component in a tree structure. It can also
        provide some default implementation for these methods.
        """

        self._parent = parent

    """
    In some cases, it would be beneficial to define the child-management
    operations right in the base Component class. This way, you won't need to
    expose any concrete component classes to the client code, even during the
    object tree assembly. The downside is that these methods will be empty for
    the leaf-level components.
    """

    def add(self, component: Component) -> None:
        pass

    def remove(self, component: Component) -> None:
        pass

    def is_composite(self) -> bool:
        """
        You can provide a method that lets the client code figure out whether a
        component can bear children.
        """

        return False

    @abstractmethod
    def operation(self) -> str:
        """
        The base Component may implement some default behavior or leave it to
        concrete classes (by declaring the method containing the behavior as
        "abstract").
        """

        pass


class Leaf(Component):
    """
    The Leaf class represents the end objects of a composition. A leaf can't
    have any children.

    Usually, it's the Leaf objects that do the actual work, whereas Composite
    objects only delegate to their sub-components.
    """

    def operation(self) -> str:
        return "Leaf"


class Composite(Component):
    """
    The Composite class represents the complex components that may have
    children. Usually, the Composite objects delegate the actual work to their
    children and then "sum-up" the result.
    """

    def __init__(self) -> None:
        self._children: List[Component] = []

    """
    A composite object can add or remove other components (both simple or
    complex) to or from its child list.
    """

    def add(self, component: Component) -> None:
        self._children.append(component)
        component.parent = self

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def operation(self) -> str:
        """
        The Composite executes its primary logic in a particular way. It
        traverses recursively through all its children, collecting and summing
        their results. Since the composite's children pass these calls to their
        children and so forth, the whole object tree is traversed as a result.
        """

        results = []
        for child in self._children:
            results.append(child.operation())
        return f"Branch({'+'.join(results)})"


def client_code(component: Component) -> None:
    """
    The client code works with all of the components via the base interface.
    """

    print(f"RESULT: {component.operation()}", end="")


def client_code2(component1: Component, component2: Component) -> None:
    """
    Thanks to the fact that the child-management operations are declared in the
    base Component class, the client code can work with any component, simple or
    complex, without depending on their concrete classes.
    """

    if component1.is_composite():
        component1.add(component2)

    print(f"RESULT: {component1.operation()}", end="")


if __name__ == "__main__":
    # This way the client code can support the simple leaf components...
    simple = Leaf()
    print("Client: I've got a simple component:")
    client_code(simple)
    print("\n")

    # ...as well as the complex composites.
    tree = Composite()

    branch1 = Composite()
    branch1.add(Leaf())
    branch1.add(Leaf())

    branch2 = Composite()
    branch2.add(Leaf())

    tree.add(branch1)
    tree.add(branch2)

    print("Client: Now I've got a composite tree:")
    client_code(tree)
    print("\n")

    print("Client: I don't need to check the components classes even when managing the tree:")
    client_code2(tree, simple)
```

#### Output.txt: Execution result
```
Client: I've got a simple component:
RESULT: Leaf

Client: Now I've got a composite tree:
RESULT: Branch(Branch(Leaf+Leaf)+Branch(Leaf))

Client: I don't need to check the components classes even when managing the tree:
RESULT: Branch(Branch(Leaf+Leaf)+Branch(Leaf)+Leaf)
```

### Rust: Files and Folders 文件和文件夹
Let’s try to understand the Composite pattern with an example of an operating system’s file system. In the file system, there are two types of objects: files and folders. There are cases when files and folders should be treated to be the same way. This is where the Composite pattern comes in handy.
让我们尝试通过操作系统文件系统的示例来理解 Composite 模式。在文件系统中，有两种类型的对象：文件和文件夹。在某些情况下，文件和文件夹应以相同的方式处理。这就是复合模式派上用场的地方。

File and Directory are both of the trait Component with a single search method. For a file, it will just look into the contents of the file; for a folder, it will go through all files of that folder to find that keyword.
File 并且 Directory 都 trait Component 使用单一 search 方法。对于文件，它只会查看文件的内容;对于文件夹，它将遍历该文件夹的所有文件以查找该关键字。

#### fs/mod.rs
```Rust
mod file;
mod folder;

pub use file::File;
pub use folder::Folder;

pub trait Component {
    fn search(&self, keyword: &str);
}
```

#### fs/file.rs
```Rust
use super::Component;

pub struct File {
    name: &'static str,
}

impl File {
    pub fn new(name: &'static str) -> Self {
        Self { name }
    }
}

impl Component for File {
    fn search(&self, keyword: &str) {
        println!("Searching for keyword {} in file {}", keyword, self.name);
    }
}
```

#### fs/folder.rs
```Rust
use super::Component;

pub struct Folder {
    name: &'static str,
    components: Vec<Box<dyn Component>>,
}

impl Folder {
    pub fn new(name: &'static str) -> Self {
        Self {
            name,
            components: vec![],
        }
    }

    pub fn add(&mut self, component: impl Component + 'static) {
        self.components.push(Box::new(component));
    }
}

impl Component for Folder {
    fn search(&self, keyword: &str) {
        println!(
            "Searching recursively for keyword {} in folder {}",
            keyword, self.name
        );

        for component in self.components.iter() {
            component.search(keyword);
        }
    }
}
```

#### main.rs
```Rust
mod fs;

use fs::{Component, File, Folder};

fn main() {
    let file1 = File::new("File 1");
    let file2 = File::new("File 2");
    let file3 = File::new("File 3");

    let mut folder1 = Folder::new("Folder 1");
    folder1.add(file1);

    let mut folder2 = Folder::new("Folder 2");
    folder2.add(file2);
    folder2.add(file3);
    folder2.add(folder1);

    folder2.search("rose");
}
```

#### Output 输出
```
Searching recursively for keyword rose in folder Folder 2
Searching for keyword rose in file File 2
Searching for keyword rose in file File 3
Searching recursively for keyword rose in folder Folder 1
Searching for keyword rose in file File 1
------------------------------------
```


