---
title: Proxy 代理模式
categories:
  - design-pattern
date: 2024-02-01 21:50:38
---

## 意图

**代理**是一种结构化设计模式，它允许您为另一个对象提供替代或占位符。代理控制对原始对象的访问，允许您在请求到达原始对象之前或之后执行某些操作。


<div align="center"> <img src="/images/proxy.png"/></div>


## 问题

为什么要控制对对象的访问？这里有一个例子：你有一个巨大的对象，它消耗了大量的系统资源。你有时需要它，但不总是。


<div align="center"> <img src="/images/proxy-problem-en.png"/>数据库查询可能真的很慢。</div>


你可以实现惰性初始化：只在实际需要的时候创建这个对象。对象的所有客户端都需要执行一些延迟初始化代码。不幸的是，这可能会导致大量的代码重复。

在理想情况下，我们希望将这些代码直接放入对象的类中，但这并不总是可行的。例如，类可以是封闭的第三方库的一部分。

## 解决方案

代理模式建议您创建一个具有与原始服务对象相同接口的新代理类。然后更新您的应用，使其将代理对象传递给原始对象的所有客户端。在接收到来自客户机的请求时，代理创建一个真实的服务对象，并将所有工作委托给它。


<div align="center"> <img src="/images/proxy-solution-en.png"/>代理将自己伪装成一个数据库对象。它可以在客户端或真实的数据库对象不知道的情况下处理延迟初始化和结果缓存。</div>


但有什么好处呢？如果您需要在类的主要逻辑之前或之后执行某些操作，代理允许您在不更改该类的情况下执行这些操作。由于代理实现了与原始类相同的接口，因此可以将其传递给任何需要真实的服务对象的客户端。

## 现实世界的类比


<div align="center"> <img src="/images/proxy-live-example.png"/>信用卡和现金一样可以用来付款。</div>


信用卡是银行账户的代理，银行账户是一捆现金的代理。两者都实现了相同的接口：它们可以用于进行支付。消费者感觉很好，因为没有必要随身携带大量现金。店主也很高兴，因为交易收入通过电子方式添加到商店的银行账户中，而没有丢失存款或在去银行的路上被抢劫的风险。


<div align="center"> <img src="/images/proxy-structure.png"/></div>


1. 服务接口声明服务的接口。代理必须遵循此接口，以便能够将自己伪装成服务对象。
2. Service是一个提供一些有用的业务逻辑的类。
3. Proxy类有一个指向服务对象的引用字段。在代理完成其处理之后（例如，惰性初始化、日志记录、访问控制、缓存等），它将请求传递给服务对象。通常，代理管理其服务对象的整个生命周期。
4. 客户端应该通过相同的接口与服务和代理一起工作。通过这种方式，您可以将代理传递到任何需要服务对象的代码中。

##  伪代码

此示例说明了代理模式如何帮助将延迟初始化和缓存引入第三方YouTube集成库。


<div align="center"> <img src="/images/proxy-example.png"/>使用代理缓存服务的结果。</div>


图书馆为我们提供了视频下载课。然而，这是非常低效的。如果客户端应用程序多次请求相同的视频，库只是一遍又一遍地下载它，而不是缓存和重用第一个下载的文件。

代理类实现与原始下载器相同的接口，并将所有工作委托给它。但是，它会跟踪下载的文件，并在应用多次请求同一视频时返回缓存结果。

```java
// The interface of a remote service.
interface ThirdPartyYouTubeLib is
    method listVideos()
    method getVideoInfo(id)
    method downloadVideo(id)

// The concrete implementation of a service connector. Methods
// of this class can request information from YouTube. The speed
// of the request depends on a user's internet connection as
// well as YouTube's. The application will slow down if a lot of
// requests are fired at the same time, even if they all request
// the same information.
class ThirdPartyYouTubeClass implements ThirdPartyYouTubeLib is
    method listVideos() is
        // Send an API request to YouTube.

    method getVideoInfo(id) is
        // Get metadata about some video.

    method downloadVideo(id) is
        // Download a video file from YouTube.

// To save some bandwidth, we can cache request results and keep
// them for some time. But it may be impossible to put such code
// directly into the service class. For example, it could have
// been provided as part of a third party library and/or defined
// as `final`. That's why we put the caching code into a new
// proxy class which implements the same interface as the
// service class. It delegates to the service object only when
// the real requests have to be sent.
class CachedYouTubeClass implements ThirdPartyYouTubeLib is
    private field service: ThirdPartyYouTubeLib
    private field listCache, videoCache
    field needReset

    constructor CachedYouTubeClass(service: ThirdPartyYouTubeLib) is
        this.service = service

    method listVideos() is
        if (listCache == null || needReset)
            listCache = service.listVideos()
        return listCache

    method getVideoInfo(id) is
        if (videoCache == null || needReset)
            videoCache = service.getVideoInfo(id)
        return videoCache

    method downloadVideo(id) is
        if (!downloadExists(id) || needReset)
            service.downloadVideo(id)

// The GUI class, which used to work directly with a service
// object, stays unchanged as long as it works with the service
// object through an interface. We can safely pass a proxy
// object instead of a real service object since they both
// implement the same interface.
class YouTubeManager is
    protected field service: ThirdPartyYouTubeLib

    constructor YouTubeManager(service: ThirdPartyYouTubeLib) is
        this.service = service

    method renderVideoPage(id) is
        info = service.getVideoInfo(id)
        // Render the video page.

    method renderListPanel() is
        list = service.listVideos()
        // Render the list of video thumbnails.

    method reactOnUserInput() is
        renderVideoPage()
        renderListPanel()

// The application can configure proxies on the fly.
class Application is
    method init() is
        aYouTubeService = new ThirdPartyYouTubeClass()
        aYouTubeProxy = new CachedYouTubeClass(aYouTubeService)
        manager = new YouTubeManager(aYouTubeProxy)
        manager.reactOnUserInput()
```

## 适用性

使用代理模式的方法有很多种。让我们来看看最流行的用法。

- **惰性初始化（虚拟代理）。这是当您有一个重量级的服务对象时，它总是处于运行状态，浪费系统资源，即使您只是偶尔需要它。**
- 您可以将对象的初始化延迟到真正需要的时候，而不是在应用启动时创建对象。
- **访问控制（保护代理）。这是当您希望只有特定的客户端能够使用服务对象时;例如，当您的对象是操作系统的关键部分，而客户端是各种启动的应用程序（包括恶意应用程序）时。**
- 只有当客户端的凭据符合某些条件时，代理才能将请求传递给服务对象。
- **远程服务的本地执行（远程代理）。这是当服务对象位于远程服务器上时。**
- 在这种情况下，代理通过网络传递客户端请求，处理与网络一起工作的所有讨厌的细节。
- **日志请求（日志代理）。这是您想要保留对服务对象的请求历史记录的时候。**
- 代理可以在将请求传递给服务之前记录每个请求。
- **缓存请求结果（缓存代理）。这是当您需要缓存客户端请求的结果并管理此缓存的生命周期时，特别是当结果非常大时。**
- 代理可以为总是产生相同结果的重复请求实现缓存。代理可以使用请求的参数作为该高速缓存键。
- **聪明的参考。这是您需要在没有客户端使用重量级对象时能够解除该对象的时候。**
- 代理可以跟踪获得对服务对象或其结果的引用的客户端。有时，代理可能会检查客户端并检查它们是否仍然处于活动状态。如果客户端列表为空，则代理可能会解除服务对象并释放底层系统资源。代理还可以跟踪客户机是否修改了服务对象。然后，未更改的对象可以被其他客户端重用。

## 如何实现

1. 如果没有预先存在的服务接口，则创建一个以使代理和服务对象可互换。从服务类中提取接口并不总是可行的，因为您需要更改服务的所有客户端以使用该接口。计划B是使代理成为服务类的子类，这样它将继承服务的接口。
2. 创建代理类。它应该有一个用于存储服务引用的字段。通常，代理创建和管理其服务的整个生命周期。在极少数情况下，服务由客户端通过构造函数传递给代理。
3. 根据代理方法的用途实现它们。在大多数情况下，在完成一些工作之后，代理应该将工作委托给服务对象。
4. 考虑引入一种创建方法，该方法决定客户机获取的是代理服务还是真实的服务。这可以是代理类中的简单静态方法，也可以是成熟的工厂方法。
5. 考虑为服务对象实现惰性初始化。

## 利弊

| √ 利                                                        | × 弊                                             |
| ----------------------------------------------------------- | ------------------------------------------------ |
| 您可以在客户端不知道的情况下控制服务对象。                  | 代码可能会变得更复杂，因为你需要引入很多新的类。 |
| 当客户机不关心服务对象时，您可以管理它的生命周期。          | 服务的响应可能会延迟。                           |
| 即使服务对象未准备好或不可用，代理也可以工作。              |                                                  |
| 开放/封闭原则。您可以引入新的代理，而无需更改服务或客户端。 |                                                  |

## 与其他模式的关系

- 使用Adapter，您可以通过不同的接口访问现有对象。使用Proxy，接口保持不变。使用Decorator，您可以通过增强的接口访问对象。
- Facade与Proxy类似，都缓冲一个复杂的实体并自己初始化它。与Facade不同，Proxy与其服务对象具有相同的接口，这使得它们可以互换。
- Decorator和Proxy具有类似的结构，但意图非常不同。这两种模式都建立在组合原则上，其中一个对象应该将一些工作委托给另一个对象。不同之处在于，Proxy通常自己管理其服务对象的生命周期，而Decorators的组成始终由客户端控制。

## 代码示例

# Python中的代理

代理是一种结构化设计模式，它提供一个对象，作为客户端使用的真实的服务对象的替代品。代理接收客户端请求，做一些工作（访问控制，缓存等）。然后将请求传递给服务对象。

代理对象具有与服务相同的接口，这使得它在传递给客户端时可以与真实的对象互换。

## 概念示例

这个例子说明了代理设计模式的结构。它侧重于回答这些问题：

- 它由哪些类组成？
- 这些班级扮演什么角色？
- 模式中的元素是以什么方式联系在一起的？

#### main.py：概念性示例

```python
from abc import ABC, abstractmethod


class Subject(ABC):
    """
    The Subject interface declares common operations for both RealSubject and
    the Proxy. As long as the client works with RealSubject using this
    interface, you'll be able to pass it a proxy instead of a real subject.
    """

    @abstractmethod
    def request(self) -> None:
        pass


class RealSubject(Subject):
    """
    The RealSubject contains some core business logic. Usually, RealSubjects are
    capable of doing some useful work which may also be very slow or sensitive -
    e.g. correcting input data. A Proxy can solve these issues without any
    changes to the RealSubject's code.
    """

    def request(self) -> None:
        print("RealSubject: Handling request.")


class Proxy(Subject):
    """
    The Proxy has an interface identical to the RealSubject.
    """

    def __init__(self, real_subject: RealSubject) -> None:
        self._real_subject = real_subject

    def request(self) -> None:
        """
        The most common applications of the Proxy pattern are lazy loading,
        caching, controlling the access, logging, etc. A Proxy can perform one
        of these things and then, depending on the result, pass the execution to
        the same method in a linked RealSubject object.
        """

        if self.check_access():
            self._real_subject.request()
            self.log_access()

    def check_access(self) -> bool:
        print("Proxy: Checking access prior to firing a real request.")
        return True

    def log_access(self) -> None:
        print("Proxy: Logging the time of request.", end="")


def client_code(subject: Subject) -> None:
    """
    The client code is supposed to work with all objects (both subjects and
    proxies) via the Subject interface in order to support both real subjects
    and proxies. In real life, however, clients mostly work with their real
    subjects directly. In this case, to implement the pattern more easily, you
    can extend your proxy from the real subject's class.
    """

    # ...

    subject.request()

    # ...


if __name__ == "__main__":
    print("Client: Executing the client code with a real subject:")
    real_subject = RealSubject()
    client_code(real_subject)

    print("")

    print("Client: Executing the same client code with a proxy:")
    proxy = Proxy(real_subject)
    client_code(proxy)

```

####   
Output.txt：执行结果

````
Client: Executing the client code with a real subject:
RealSubject: Handling request.

Client: Executing the same client code with a proxy:
Proxy: Checking access prior to firing a real request.
RealSubject: Handling request.
Proxy: Logging the time of request.

````

# Rust中的代理

代理是一种结构化设计模式，它提供一个对象，作为客户端使用的真实的服务对象的替代品。代理接收客户端请求，做一些工作（访问控制，缓存等）。然后将请求传递给服务对象。

## 概念示例：Nginx代理

Web服务器（如Nginx）可以充当应用服务器的代理：

- 它提供对应用服务器的受控访问。
- 它可以进行速率限制。
- 它可以做请求缓存。

#### **server.rs**

```rust
mod application;
mod nginx;

pub use nginx::NginxServer;

pub trait Server {
    fn handle_request(&mut self, url: &str, method: &str) -> (u16, String);
}
```

#### server/application.rs 

```rust
use super::Server;

pub struct Application;

impl Server for Application {
    fn handle_request(&mut self, url: &str, method: &str) -> (u16, String) {
        if url == "/app/status" && method == "GET" {
            return (200, "Ok".into());
        }

        if url == "/create/user" && method == "POST" {
            return (201, "User Created".into());
        }

        (404, "Not Ok".into())
    }
}
```

#### **server/nginx.rs**

```rust
use std::collections::HashMap;

use super::{application::Application, Server};

/// NGINX server is a proxy to an application server.
pub struct NginxServer {
    application: Application,
    max_allowed_requests: u32,
    rate_limiter: HashMap<String, u32>,
}

impl NginxServer {
    pub fn new() -> Self {
        Self {
            application: Application,
            max_allowed_requests: 2,
            rate_limiter: HashMap::default(),
        }
    }

    pub fn check_rate_limiting(&mut self, url: &str) -> bool {
        let rate = self.rate_limiter.entry(url.to_string()).or_insert(1);

        if *rate > self.max_allowed_requests {
            return false;
        }

        *rate += 1;
        true
    }
}

impl Server for NginxServer {
    fn handle_request(&mut self, url: &str, method: &str) -> (u16, String) {
        if !self.check_rate_limiting(url) {
            return (403, "Not Allowed".into());
        }

        self.application.handle_request(url, method)
    }
}
```

#### **main.rs**

```rust
mod server;

use crate::server::{NginxServer, Server};

fn main() {
    let app_status = &"/app/status".to_string();
    let create_user = &"/create/user".to_string();

    let mut nginx = NginxServer::new();

    let (code, body) = nginx.handle_request(app_status, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", app_status, code, body);

    let (code, body) = nginx.handle_request(app_status, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", app_status, code, body);

    let (code, body) = nginx.handle_request(app_status, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", app_status, code, body);

    let (code, body) = nginx.handle_request(create_user, "POST");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", create_user, code, body);

    let (code, body) = nginx.handle_request(create_user, "GET");
    println!("Url: {}\nHttpCode: {}\nBody: {}\n", create_user, code, body);
}
```

### 输出

````
Url: /app/status
HttpCode: 200
Body: Ok

Url: /app/status
HttpCode: 200
Body: Ok

Url: /app/status
HttpCode: 403
Body: Not Allowed

Url: /create/user
HttpCode: 201
Body: User Created

Url: /create/user
HttpCode: 404
Body: Not Ok
````

