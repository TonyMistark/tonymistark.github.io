---
title: Flyweight 享元模式
categories:
  - design-pattern
tags: Design Pattern
date: 2024-01-30 21:55:21
---

# Flyweight 享元模式

## 意图

Flyweight是一种结构化的设计模式，通过在多个对象之间共享状态的公共部分，而不是保留每个对象中的所有数据，可以将更多的对象放入可用的RAM中。


<div align="center"> <img src="/images/flyweight.png"/></div>


## 问题

为了在长时间的工作后找点乐子，你决定创建一个简单的视频游戏：玩家在地图上移动并互相射击。您选择实现一个逼真的粒子系统，并使其成为游戏的独特功能。大量的子弹、导弹和爆炸产生的弹片应该在地图上到处飞，给玩家带来惊心动魄的体验。

完成后，你推送了最后一次提交，构建了游戏并将其发送给你的朋友进行测试。虽然游戏在你的机器上运行得很顺利，但你的朋友不能玩很长时间。在他的电脑上，游戏在玩了几分钟后就不断崩溃。在花了几个小时挖掘调试日志后，您发现游戏崩溃是因为RAM不足。原来你朋友的钻机比你自己的电脑功能差得多，这就是为什么问题在他的机器上出现得这么快。

实际的问题与你的粒子系统有关。每一个粒子，比如一颗子弹、一枚导弹或一块弹片，都由一个包含大量数据的单独对象来表示。在某些时候，当玩家屏幕上的大屠杀达到高潮时，新创建的粒子不再适合剩余的RAM，因此程序崩溃。


<div align="center"> <img src="/images/flyweight-problem-en.png"/></div>


## 解决方案

仔细查看 仔细查看 `Particle` 类，您可能会注意到color和sprite字段比其他字段占用更多的内存。更糟糕的是，这两个字段存储的所有粒子的数据几乎相同。例如，所有项目符号都具有相同的颜色和子画面。 类，您可能会注意到color和sprite字段比其他字段占用更多的内存。更糟糕的是，这两个字段存储的所有粒子的数据几乎相同。例如，所有项目符号都具有相同的颜色和子画面。


<div align="center"> <img src="/images/flyweight-solution1-en.png"/></div>


粒子状态的其他部分，如坐标、运动矢量和速度，对于每个粒子都是唯一的。毕竟，这些字段的值会随着时间的推移而变化。该数据表示粒子存在的始终变化的上下文，而每个粒子的颜色和子画面保持不变。

对象的这种恒定数据通常称为固有状态。它存在于物体内部;其他对象只能读取它，而不能改变它。对象的其余状态，通常被其他对象“从外部”改变，称为外部状态。

Flyweight模式建议您停止在对象内部存储外部状态。相反，你应该把这个状态传递给依赖它的特定方法。只有内在状态留在对象中，让你在不同的上下文中重用它。因此，您需要更少的这些对象，因为它们只在内在状态上有所不同，而内在状态的变化要比外在状态少得多。


<div align="center"> <img src="/images/flyweight-solution3.png"/></div>


让我们回到我们的游戏。假设我们已经从粒子类中提取了外部状态，那么只有三个不同的对象就足以代表游戏中的所有粒子：一颗子弹、一枚导弹和一块弹片。正如你现在可能已经猜到的，一个只存储固有状态的对象被称为flyweight。

#### 外部状态存储器

外在的状态向何处去？一些类应该仍然存储它，对吗？在大多数情况下，它会被移动到容器对象中，容器对象在我们应用模式之前聚合对象。

在我们的例子中，这是主要的 在我们的例子中，这是主要的 `Game` 对象，它将所有粒子存储在  对象，它将所有粒子存储在  对象，它将所有粒子存储在 `particles` 场中。要将外部状态移动到这个类中，需要创建几个数组字段来存储每个粒子的坐标、向量和速度。但这还不是全部。您需要另一个数组来存储对表示粒子的特定flyweight的引用。这些数组必须同步，以便您可以使用相同的索引访问粒子的所有数据。 场中。要将外部状态移动到这个类中，需要创建几个数组字段来存储每个粒子的坐标、向量和速度。但这还不是全部。您需要另一个数组来存储对表示粒子的特定flyweight的引用。这些数组必须同步，以便您可以使用相同的索引访问粒子的所有数据。


<div align="center"> <img src="/images/flyweight-solution4.png"/></div>


一个更优雅的解决方案是创建一个单独的上下文类，它将存储外部状态沿着对flyweight对象的引用。这种方法只需要容器类中有一个数组。

等一下！难道我们不需要像一开始那样，有很多这样的上下文对象吗？严格来说是的但问题是，这些物体比以前小得多。最消耗内存的字段已经被移到几个flyweight对象中。现在，1000个小的上下文对象可以重用一个重flyweight对象，而不是存储其数据的1000个副本。

#### Flyweight和不变性

由于同一个flyweight对象可以在不同的上下文中使用，因此必须确保其状态不能被修改。一个flyweight应该只初始化它的状态一次，通过构造函数参数。它不应该向其他对象公开任何setter或公共字段。

#### Flyweight工厂

为了更方便地访问各种flyweight，您可以创建一个工厂方法来管理现有flyweight对象的池。该方法从客户端接受所需flyweight的内部状态，查找与此状态匹配的现有flyweight对象，如果找到则返回它。如果没有，则创建一个新的flyweight并将其添加到池中。

有几种选择可以放置这种方法。最明显的地方是flyweight容器。或者，您可以创建一个新的工厂类。或者你可以让工厂方法静态化，并把它放在一个实际的flyweight类中。

## 结构


<div align="center"> <img src="/images/flyweight-structure.png"/></div>


1. Flyweight模式仅仅是一种优化。在应用它之前，请确保您的程序确实存在与内存中同时存在大量类似对象相关的RAM消耗问题。确保这个问题不能以任何其他有意义的方式解决。
2. Flyweight类包含原始对象的状态中可以在多个对象之间共享的部分。同一个flyweight对象可以在许多不同的上下文中使用。存储在flyweight中的状态称为intrinsic。传递给flyweight方法的状态称为extrinsic。
3. Context类包含外部状态，在所有原始对象中是唯一的。当上下文与其中一个flyweight对象配对时，它表示原始对象的完整状态。
4. 通常，原始对象的行为保留在flyweight类中。在这种情况下，无论谁调用flyweight的方法，都必须将外部状态的适当位传递到方法的参数中。另一方面，行为可以被移动到上下文类，它将链接的flyweight仅仅作为一个数据对象。
5. 客户端计算或存储flyweights的外部状态。从客户端的角度来看，flyweight是一个模板对象，可以在运行时通过将一些上下文数据传递到其方法的参数中进行配置。
6. Flyweight Factory管理现有的Flyweight。使用工厂，客户不直接创建flyweights。相反，它们调用工厂，向其传递所需flyweight的内部状态位。工厂检查以前创建的flyweights，并返回一个与搜索条件匹配的现有flyweights，或者如果没有找到任何内容，则创建一个新的flyweights。

##  伪代码

在本例中，Flyweight模式有助于在画布上渲染数百万个树对象时减少内存使用。


<div align="center"> <img src="/images/flyweight-example.png"/></div>


该模式从主类 该模式从主类 `Tree` 中提取重复的固有状态，并将其移动到flyweight类  中提取重复的固有状态，并将其移动到flyweight类  中提取重复的固有状态，并将其移动到flyweight类 `TreeType` 中。

现在，不再将相同的数据存储在多个对象中，而是将其保存在几个flyweight对象中，并链接到适当的 现在，不再将相同的数据存储在多个对象中，而是将其保存在几个flyweight对象中，并链接到适当的 `Tree` 对象，这些对象充当上下文。客户端代码使用flyweight工厂创建新的树对象，该工厂封装了搜索正确对象并在需要时重用它的复杂性。 对象，这些对象充当上下文。客户端代码使用flyweight工厂创建新的树对象，该工厂封装了搜索正确对象并在需要时重用它的复杂性。

现在，不再将相同的数据存储在多个对象中，而是将其保存在几个flyweight对象中，并链接到适当的 现在，不再将相同的数据存储在多个对象中，而是将其保存在几个flyweight对象中，并链接到适当的 `Tree` 对象，这些对象充当上下文。客户端代码使用flyweight工厂创建新的树对象，该工厂封装了搜索正确对象并在需要时重用它的复杂性。 对象，这些对象充当上下文。客户端代码使用flyweight工厂创建新的树对象，该工厂封装了搜索正确对象并在需要时重用它的复杂性。

```java
// The flyweight class contains a portion of the state of a
// tree. These fields store values that are unique for each
// particular tree. For instance, you won't find here the tree
// coordinates. But the texture and colors shared between many
// trees are here. Since this data is usually BIG, you'd waste a
// lot of memory by keeping it in each tree object. Instead, we
// can extract texture, color and other repeating data into a
// separate object which lots of individual tree objects can
// reference.
class TreeType is
    field name
    field color
    field texture
    constructor TreeType(name, color, texture) { ... }
    method draw(canvas, x, y) is
        // 1. Create a bitmap of a given type, color & texture.
        // 2. Draw the bitmap on the canvas at X and Y coords.

// Flyweight factory decides whether to re-use existing
// flyweight or to create a new object.
class TreeFactory is
    static field treeTypes: collection of tree types
    static method getTreeType(name, color, texture) is
        type = treeTypes.find(name, color, texture)
        if (type == null)
            type = new TreeType(name, color, texture)
            treeTypes.add(type)
        return type

// The contextual object contains the extrinsic part of the tree
// state. An application can create billions of these since they
// are pretty small: just two integer coordinates and one
// reference field.
class Tree is
    field x,y
    field type: TreeType
    constructor Tree(x, y, type) { ... }
    method draw(canvas) is
        type.draw(canvas, this.x, this.y)

// The Tree and the Forest classes are the flyweight's clients.
// You can merge them if you don't plan to develop the Tree
// class any further.
class Forest is
    field trees: collection of Trees

    method plantTree(x, y, name, color, texture) is
        type = TreeFactory.getTreeType(name, color, texture)
        tree = new Tree(x, y, type)
        trees.add(tree)

    method draw(canvas) is
        foreach (tree in trees) do
            tree.draw(canvas)
```

## 适用性

- **只有当你的程序必须支持大量的对象，而这些对象几乎不能容纳在可用的RAM中时，才使用Flyweight模式。**
- 应用该模式的好处在很大程度上取决于如何以及在何处使用它。它在以下情况下最有用：

  - 应用程序需要产生大量的类似对象
  - 这会耗尽目标设备上的所有可用RAM
  - 对象包含可以在多个对象之间提取和共享的重复状态


## 如何实现

1. 将一个类的字段分成两部分，这两部分将成为一个flyweight：

   - 内部状态：包含跨多个对象复制的不变数据的字段
   - 外部状态：包含每个对象唯一的上下文数据的字段

2. 将表示内部状态的字段保留在类中，但要确保它们是不可变的。它们应该只在构造函数内部取初始值。
3. 检查使用外部状态字段的方法。对于方法中使用的每个字段，引入一个新参数并使用它来代替字段。
4. 或者，创建一个工厂类来管理flyweights池。它应该在创建新的flyweight之前检查现有的flyweight。一旦工厂到位，客户端必须通过它请求flyweight。他们应该通过将其内在状态传递给工厂来描述所需的flyweight。
5. 客户端必须存储或计算外部状态（上下文）的值，以便能够调用flyweight对象的方法。为了方便起见，可以将外部状态沿着飞权引用字段一起移动到单独的上下文类。

## 利弊

| 利√                                                 | 弊×                                                                                       |
| --------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| 你可以保存大量的RAM，假设你的程序有很多类似的对象。 | 当每次有人调用flyweight方法时都需要重新计算一些上下文数据时，您可能会在CPU周期上牺牲RAM。 |
|                                                     | 代码变得更加复杂。新的团队成员总是想知道为什么实体的状态以这种方式分离。                  |

## 与其他模式的关系

- 您可以将复合树的共享叶节点实现为Flyweights，以保存一些RAM。
- Flyweight展示了如何制作许多小对象，而Facade展示了如何制作代表整个子系统的单个对象。
- 如果你设法将对象的所有共享状态减少到一个flyweight对象，那么Flyweight就类似于Singleton。但这些模式之间有两个根本区别：

  - 应该只有一个Singleton实例，而Flyweight类可以有多个具有不同内部状态的实例。
  - Singleton对象可以是可变的。Flyweight对象是不可变的。


## 代码示例

# Python中的Flyweight模式

Flyweight是一种结构化设计模式，它允许程序通过保持低内存消耗来支持大量对象。

该模式通过在多个对象之间共享对象状态的一部分来实现。换句话说，Flyweight通过缓存不同对象使用的相同数据来节省RAM。

## 概念示例

这个例子说明了Flyweight设计模式的结构。它侧重于回答这些问题：

- 它由哪些类组成？
- 这些班级扮演什么角色？
- 模式中的元素是以什么方式联系在一起的？

#### main.py：概念性示例

```python
import json
from typing import Dict


class Flyweight():
    """
    The Flyweight stores a common portion of the state (also called intrinsic
    state) that belongs to multiple real business entities. The Flyweight
    accepts the rest of the state (extrinsic state, unique for each entity) via
    its method parameters.
    """

    def __init__(self, shared_state: str) -> None:
        self._shared_state = shared_state

    def operation(self, unique_state: str) -> None:
        s = json.dumps(self._shared_state)
        u = json.dumps(unique_state)
        print(f"Flyweight: Displaying shared ({s}) and unique ({u}) state.", end="")


class FlyweightFactory():
    """
    The Flyweight Factory creates and manages the Flyweight objects. It ensures
    that flyweights are shared correctly. When the client requests a flyweight,
    the factory either returns an existing instance or creates a new one, if it
    doesn't exist yet.
    """

    _flyweights: Dict[str, Flyweight] = {}

    def __init__(self, initial_flyweights: Dict) -> None:
        for state in initial_flyweights:
            self._flyweights[self.get_key(state)] = Flyweight(state)

    def get_key(self, state: Dict) -> str:
        """
        Returns a Flyweight's string hash for a given state.
        """

        return "_".join(sorted(state))

    def get_flyweight(self, shared_state: Dict) -> Flyweight:
        """
        Returns an existing Flyweight with a given state or creates a new one.
        """

        key = self.get_key(shared_state)

        if not self._flyweights.get(key):
            print("FlyweightFactory: Can't find a flyweight, creating new one.")
            self._flyweights[key] = Flyweight(shared_state)
        else:
            print("FlyweightFactory: Reusing existing flyweight.")

        return self._flyweights[key]

    def list_flyweights(self) -> None:
        count = len(self._flyweights)
        print(f"FlyweightFactory: I have {count} flyweights:")
        print("\n".join(map(str, self._flyweights.keys())), end="")


def add_car_to_police_database(
    factory: FlyweightFactory, plates: str, owner: str,
    brand: str, model: str, color: str
) -> None:
    print("\n\nClient: Adding a car to database.")
    flyweight = factory.get_flyweight([brand, model, color])
    # The client code either stores or calculates extrinsic state and passes it
    # to the flyweight's methods.
    flyweight.operation([plates, owner])


if __name__ == "__main__":
    """
    The client code usually creates a bunch of pre-populated flyweights in the
    initialization stage of the application.
    """

    factory = FlyweightFactory([
        ["Chevrolet", "Camaro2018", "pink"],
        ["Mercedes Benz", "C300", "black"],
        ["Mercedes Benz", "C500", "red"],
        ["BMW", "M5", "red"],
        ["BMW", "X6", "white"],
    ])

    factory.list_flyweights()

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "M5", "red")

    add_car_to_police_database(
        factory, "CL234IR", "James Doe", "BMW", "X1", "red")

    print("\n")

    factory.list_flyweights()
```

#### 执行结果

````
FlyweightFactory: I have 5 flyweights:
Camaro2018_Chevrolet_pink
C300_Mercedes Benz_black
C500_Mercedes Benz_red
BMW_M5_red
BMW_X6_white

Client: Adding a car to database.
FlyweightFactory: Reusing existing flyweight.
Flyweight: Displaying shared (["BMW", "M5", "red"]) and unique (["CL234IR", "James Doe"]) state.

Client: Adding a car to database.
FlyweightFactory: Can't find a flyweight, creating new one.
Flyweight: Displaying shared (["BMW", "X1", "red"]) and unique (["CL234IR", "James Doe"]) state.

FlyweightFactory: I have 6 flyweights:
Camaro2018_Chevrolet_pink
C300_Mercedes Benz_black
C500_Mercedes Benz_red
BMW_M5_red
BMW_X6_white
BMW_X1_red
````

# Rust中的Flyweight模式

Flyweight是一种结构化设计模式，它允许程序通过保持低内存消耗来支持大量对象。

该模式通过在多个对象之间共享对象状态的一部分来实现。换句话说，Flyweight通过缓存不同对象使用的相同数据来节省RAM。

## 字符的Flyweight

在这个例子中，我们将为字符创建一个Flyweight模式，在这个模式中我们共享共同的字符对象以保存内存。

```rust
// Flyweight Character trait
trait Character {
    fn display(&self);
}

// Concrete Character implementation
struct ConcreteCharacter {
    symbol: char,
}

impl Character for ConcreteCharacter {
    fn display(&self) {
        println!("Character: {}", self.symbol);
    }
}

// Flyweight factory for characters
struct CharacterFactory {
    characters: std::collections::HashMap<char, Box<dyn Character>>,
}

impl CharacterFactory {
    fn new() -> Self {
        CharacterFactory {
            characters: std::collections::HashMap::new(),
        }
    }

    fn get_character(&mut self, symbol: char) -> &Box<dyn Character> {
        self.characters
            .entry(symbol)
            .or_insert(Box::new(ConcreteCharacter { symbol }))
    }
}

// Usage
fn main() {
    let mut character_factory = CharacterFactory::new();

    let char_a = character_factory.get_character('A');
    let char_b = character_factory.get_character('B');
    let char_a2 = character_factory.get_character('A'); // Reusing 'A'

    char_a.display();
    char_b.display();
    char_a2.display(); // The same instance as 'A'
}
```

在这个例子中：

我们定义了一个包含 我们定义了一个包含 `display` 方法的  方法的  方法的 `Character` trait。

`ConcreteCharacter` 结构体实现了  结构体实现了  结构体实现了 `Character` trait，并表示一个具体的字符对象。 trait，并表示一个具体的字符对象。

`CharacterFactory` 结构体充当一个flyweight工厂，用于创建和管理角色对象。它使用HashMap来存储共享的角色对象。 结构体充当一个flyweight工厂，用于创建和管理角色对象。它使用HashMap来存储共享的角色对象。