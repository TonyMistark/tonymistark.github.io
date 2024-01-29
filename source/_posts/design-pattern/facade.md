---
title: Facade 门面（外观）模式
categories:
  - design-pattern
date: 2024-01-29 22:15:32
---

## 意图

Facade是一种结构化设计模式，它为库、框架或任何其他复杂的类集提供了一个简化的接口。


<div align="center"> <img src="/images/facade.png"/></div>


## 问题

设想一下，您必须让代码处理属于复杂库或框架的大量对象。通常，您需要初始化所有这些对象，跟踪依赖关系，以正确的顺序执行方法，等等。

因此，类的业务逻辑将与第三方类的实现细节紧密耦合，从而难以理解和维护。

## 解决方案

Facade是一个类，它为包含许多移动部件的复杂子系统提供简单的接口。与直接使用子系统相比，外观可能提供有限的功能。但是，它只包含客户真正关心的那些功能。

Having a facade is handy when you need to integrate your app with a sophisticated library that has dozens of features, but you just need a tiny bit of its functionality.  
当你需要将你的应用与一个复杂的库集成时，拥有一个外观是很方便的，这个库有几十个功能，但你只需要它的一小部分功能。

例如，一个将猫的搞笑短视频上传到社交媒体的应用程序可能会使用专业的视频转换库。然而，它真正需要的只是一个带有单一方法 `encode(filename, format)` 的类。在创建这样一个类并将其与视频转换库连接之后，您将拥有第一个外观。

## 现实世界的类比


<div align="center"> <img src="/images/facade-live-example.png"/>通过电话订购。</div>


当你打电话给一家商店下电话订单时，接线员是你对商店所有服务和部门的门面。运营商为您提供一个简单的语音界面，用于订购系统、支付网关和各种交付服务。

## 结构


<div align="center"> <img src="/images/facade-structure.png"/></div>


1. **Facade**提供了对子系统功能的特定部分的方便访问。它知道在哪里引导客户的请求，以及如何操作所有的活动部件。
2. 可以创建一个**Additional Facade**类，以防止使用不相关的功能污染单个facade，这些功能可能会使其成为另一个复杂的结构。客户端和其他立面都可以使用其他立面。
3. **复杂子系统**由几十个不同的对象组成。为了让它们都做一些有意义的事情，你必须深入研究子系统的实现细节，比如以正确的顺序初始化对象，并以正确的格式为它们提供数据。子系统类不知道facade的存在。他们在系统内运作，并直接相互合作。
4. 客户端使用facade而不是直接调用子系统对象。

## 伪代码

在本例中，Facade模式简化了与复杂视频转换框架的交互。


<div align="center"> <img src="/images/facade-example1.png"/>在一个facade类中隔离多个依赖项的示例。</div>


与其让你的代码直接与几十个框架类一起工作，不如创建一个facade类来封装这些功能，并将其隐藏在代码的其余部分中。这种结构还可以帮助您最大限度地减少升级到框架的未来版本或用另一个版本替换它的工作。你在应用中唯一需要改变的是facade方法的实现。

```java
// These are some of the classes of a complex 3rd-party video
// conversion framework. We don't control that code, therefore
// can't simplify it.

class VideoFile
// ...

class OggCompressionCodec
// ...

class MPEG4CompressionCodec
// ...

class CodecFactory
// ...

class BitrateReader
// ...

class AudioMixer
// ...


// We create a facade class to hide the framework's complexity
// behind a simple interface. It's a trade-off between
// functionality and simplicity.
class VideoConverter is
    method convert(filename, format):File is
        file = new VideoFile(filename)
        sourceCodec = (new CodecFactory).extract(file)
        if (format == "mp4")
            destinationCodec = new MPEG4CompressionCodec()
        else
            destinationCodec = new OggCompressionCodec()
        buffer = BitrateReader.read(filename, sourceCodec)
        result = BitrateReader.convert(buffer, destinationCodec)
        result = (new AudioMixer()).fix(result)
        return new File(result)

// Application classes don't depend on a billion classes
// provided by the complex framework. Also, if you decide to
// switch frameworks, you only need to rewrite the facade class.
class Application is
    method main() is
        convertor = new VideoConverter()
        mp4 = convertor.convert("funny-cats-video.ogg", "mp4")
        mp4.save()

```

## 适用性

- **当您需要一个有限但直接的接口到一个复杂的子系统时，请使用Facade模式。**
- 通常，子系统会随着时间的推移变得更加复杂。即使应用设计模式通常也会导致创建更多的类。子系统可能变得更加灵活，更容易在各种上下文中重用，但它需要从客户端获得的配置和样板代码的数量越来越大。Facade试图通过提供子系统最常用功能的快捷方式来解决这个问题，以满足大多数客户的需求。
- 当你想把一个子系统组织成层时，使用Facade。
- 创建外观以定义子系统每个级别的入口点。您可以通过要求多个子系统仅通过外观进行通信来减少它们之间的耦合。例如，让我们回到我们的视频转换框架。它可以分为两个层次：视频和音频相关。对于每一层，您可以创建一个外观，然后使每一层的类通过这些外观相互通信。这种方法看起来与Mediator模式非常相似。

## 如何实施

1. 检查是否有可能提供比现有子系统已经提供的接口更简单的接口。如果这个接口使客户机代码独立于许多子系统的类，那么您就走对了路。
2. 在一个新的facade类中decompose并实现这个接口。facade应该将客户端代码的调用重定向到子系统的适当对象。facade应该负责初始化子系统并管理其进一步的生命周期，除非客户端代码已经这样做了。
3. 要从模式中获得全部好处，请使所有客户机代码仅通过外观与子系统通信。现在，客户端代码受到保护，不受子系统代码中任何更改的影响。例如，当子系统升级到新版本时，您只需要修改外观中的代码。
4. 如果外观变得太大，考虑将其行为的一部分提取到一个新的、改进的外观类中。

## 利弊

- 利：您可以将代码与子系统的复杂性隔离开来。
-  弊：facade可以成为耦合到应用程序的所有类的god对象。

## 与其他模式的关系

- Facade为现有对象定义了一个新的接口，而Adapter试图使现有接口可用。Adapter通常只包装一个对象，而Facade则处理整个对象子系统。
- 当您只想隐藏从客户端代码创建子系统对象的方式时，抽象工厂可以作为Facade的替代方案。
- Flyweight展示了如何制作许多小对象，而Facade展示了如何制作代表整个子系统的单个对象。
- Facade和Mediator有着类似的工作：它们试图组织许多紧密耦合的类之间的协作。

  - Facade为对象子系统定义了一个简化的接口，但它没有引入任何新功能。子系统本身不知道facade。子系统内的对象可以直接通信。
  - Mediator集中系统组件之间的通信。组件只知道中介对象，不直接通信。

- Facade类通常可以转换为Singleton，因为在大多数情况下，单个facade对象就足够了。
- Facade与Proxy类似，都缓冲一个复杂的实体并自己初始化它。与Facade不同，Proxy与其服务对象具有相同的接口，这使得它们可以互换。

## 代码示例

# Python中的Facade

Facade是一种结构化设计模式，它为复杂的类、库或框架系统提供了一个简化的（但有限的）接口。

虽然Facade降低了应用程序的整体复杂性，但它也有助于将不需要的依赖项移到一个地方。

## 概念示例

这个例子说明了Facade设计模式的结构。它侧重于回答这些问题：

- 它由哪些类组成？
- 这些班级扮演什么角色？
- 模式中的元素是以什么方式联系在一起的？

#### main.py：概念性示例

```python
from __future__ import annotations


class Facade:
    """
    The Facade class provides a simple interface to the complex logic of one or
    several subsystems. The Facade delegates the client requests to the
    appropriate objects within the subsystem. The Facade is also responsible for
    managing their lifecycle. All of this shields the client from the undesired
    complexity of the subsystem.
    """

    def __init__(self, subsystem1: Subsystem1, subsystem2: Subsystem2) -> None:
        """
        Depending on your application's needs, you can provide the Facade with
        existing subsystem objects or force the Facade to create them on its
        own.
        """

        self._subsystem1 = subsystem1 or Subsystem1()
        self._subsystem2 = subsystem2 or Subsystem2()

    def operation(self) -> str:
        """
        The Facade's methods are convenient shortcuts to the sophisticated
        functionality of the subsystems. However, clients get only to a fraction
        of a subsystem's capabilities.
        """

        results = []
        results.append("Facade initializes subsystems:")
        results.append(self._subsystem1.operation1())
        results.append(self._subsystem2.operation1())
        results.append("Facade orders subsystems to perform the action:")
        results.append(self._subsystem1.operation_n())
        results.append(self._subsystem2.operation_z())
        return "\n".join(results)


class Subsystem1:
    """
    The Subsystem can accept requests either from the facade or client directly.
    In any case, to the Subsystem, the Facade is yet another client, and it's
    not a part of the Subsystem.
    """

    def operation1(self) -> str:
        return "Subsystem1: Ready!"

    # ...

    def operation_n(self) -> str:
        return "Subsystem1: Go!"


class Subsystem2:
    """
    Some facades can work with multiple subsystems at the same time.
    """

    def operation1(self) -> str:
        return "Subsystem2: Get ready!"

    # ...

    def operation_z(self) -> str:
        return "Subsystem2: Fire!"


def client_code(facade: Facade) -> None:
    """
    The client code works with complex subsystems through a simple interface
    provided by the Facade. When a facade manages the lifecycle of the
    subsystem, the client might not even know about the existence of the
    subsystem. This approach lets you keep the complexity under control.
    """

    print(facade.operation(), end="")


if __name__ == "__main__":
    # The client code may have some of the subsystem's objects already created.
    # In this case, it might be worthwhile to initialize the Facade with these
    # objects instead of letting the Facade create new instances.
    subsystem1 = Subsystem1()
    subsystem2 = Subsystem2()
    facade = Facade(subsystem1, subsystem2)
    client_code(facade)
```

#### Output.txt：执行结果

````
Facade initializes subsystems:
Subsystem1: Ready!
Subsystem2: Get ready!
Facade orders subsystems to perform the action:
Subsystem1: Go!
Subsystem2: Fire!
````

# **Facade** in Rust

Facade是一种结构化设计模式，它为复杂的类、库或框架系统提供了一个简化的（但有限的）接口。

虽然Facade降低了应用程序的整体复杂性，但它也有助于将不需要的依赖项移到一个地方。

## 概念示例

`pub struct WalletFacade` 在其API背后隐藏了复杂的逻辑。一个方法 `add_money_to_wallet` 在后台与账户、代码、钱包、通知和账本进行交互。

#### **wallet_facade.rs**

```rust
use crate::{
    account::Account, ledger::Ledger, notification::Notification, security_code::SecurityCode,
    wallet::Wallet,
};

/// Facade hides a complex logic behind the API.
pub struct WalletFacade {
    account: Account,
    wallet: Wallet,
    code: SecurityCode,
    notification: Notification,
    ledger: Ledger,
}

impl WalletFacade {
    pub fn new(account_id: String, code: u32) -> Self {
        println!("Starting create account");

        let this = Self {
            account: Account::new(account_id),
            wallet: Wallet::new(),
            code: SecurityCode::new(code),
            notification: Notification,
            ledger: Ledger,
        };

        println!("Account created");
        this
    }

    pub fn add_money_to_wallet(
        &mut self,
        account_id: &String,
        security_code: u32,
        amount: u32,
    ) -> Result<(), String> {
        println!("Starting add money to wallet");
        self.account.check(account_id)?;
        self.code.check(security_code)?;
        self.wallet.credit_balance(amount);
        self.notification.send_wallet_credit_notification();
        self.ledger.make_entry(account_id, "credit".into(), amount);
        Ok(())
    }

    pub fn deduct_money_from_wallet(
        &mut self,
        account_id: &String,
        security_code: u32,
        amount: u32,
    ) -> Result<(), String> {
        println!("Starting debit money from wallet");
        self.account.check(account_id)?;
        self.code.check(security_code)?;
        self.wallet.debit_balance(amount);
        self.notification.send_wallet_debit_notification();
        self.ledger.make_entry(account_id, "debit".into(), amount);
        Ok(())
    }
}
```

#### **wallet.rs**

```rust
pub struct Wallet {
    balance: u32,
}

impl Wallet {
    pub fn new() -> Self {
        Self { balance: 0 }
    }

    pub fn credit_balance(&mut self, amount: u32) {
        self.balance += amount;
    }

    pub fn debit_balance(&mut self, amount: u32) {
        self.balance
            .checked_sub(amount)
            .expect("Balance is not sufficient");
    }
}

```

#### **account.rs**

```rust
pub struct Account {
    name: String,
}

impl Account {
    pub fn new(name: String) -> Self {
        Self { name }
    }

    pub fn check(&self, name: &String) -> Result<(), String> {
        if &self.name != name {
            return Err("Account name is incorrect".into());
        }

        println!("Account verified");
        Ok(())
    }
}
```

#### **ledger.rs**

```rust
pub struct Ledger;

impl Ledger {
    pub fn make_entry(&mut self, account_id: &String, txn_type: String, amount: u32) {
        println!(
            "Make ledger entry for accountId {} with transaction type {} for amount {}",
            account_id, txn_type, amount
        );
    }
}
```

#### **notification.rs**

```rust
pub struct Notification;

impl Notification {
    pub fn send_wallet_credit_notification(&self) {
        println!("Sending wallet credit notification");
    }

    pub fn send_wallet_debit_notification(&self) {
        println!("Sending wallet debit notification");
    }
}

```

####  **security_code.rs**

```rust
pub struct SecurityCode {
    code: u32,
}

impl SecurityCode {
    pub fn new(code: u32) -> Self {
        Self { code }
    }

    pub fn check(&self, code: u32) -> Result<(), String> {
        if self.code != code {
            return Err("Security code is incorrect".into());
        }

        println!("Security code verified");
        Ok(())
    }
}

```

####  **main.rs**

```rust
mod account;
mod ledger;
mod notification;
mod security_code;
mod wallet;
mod wallet_facade;

use wallet_facade::WalletFacade;

fn main() -> Result<(), String> {
    let mut wallet = WalletFacade::new("abc".into(), 1234);
    println!();

    // Wallet Facade interacts with the account, code, wallet, notification and
    // ledger behind the scenes.
    wallet.add_money_to_wallet(&"abc".into(), 1234, 10)?;
    println!();

    wallet.deduct_money_from_wallet(&"abc".into(), 1234, 5)
}

```

### 输出

````
Starting create account
Account created

Starting add money to wallet
Account verified
Security code verified
Sending wallet credit notification
Make ledger entry for accountId abc with transaction type credit for amount 10

Starting debit money from wallet
Account verified
Security code verified
Sending wallet debit notification
Make ledger entry for accountId abc with transaction type debit for amount 5

````