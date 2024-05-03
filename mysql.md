# mysql

## 一、事务

### 1. 事务简介

事务是**一组操作的集合，它是一个不可分割的工作单位**，事务会把所有的操作作为一个整体，一起向系统提交或撤销操作请求，**这些操作要么同时成功，要么同时失败**。

### 2. 如何开启事务

在MySQL中，事务是默认开启的`autocommit=ON`, **当执行一条DML语句，MySQL会隐式的提交事务，也就是说每一条DML语句都是在一个事务之内的**。下面的两个DML语句，相当于放在两个独立的事务中执行。

```sql
UPDATE account SET balance = balance - 10 WHERE id = 1;
UPDATE account SET balance = balance + 10 WHERE id = 2;
```

**当我们想把多条SQL语句包裹在一个事务中时**，可以使用如下的方式

```bash
begin; # 或者start transaction;
# DML语句
commit; # 或者rollback
```

当设置`autocommit=OFF`时，开启事务的方式和上面一样。

### 3. 事务和锁的关系

- 事务的隔离级别使用了锁，隐藏了加锁细节

## 二、锁



## 三、sqlalchemy

### 1. 架构图

按照sqlalchemy官网的介绍https://docs.sqlalchemy.org/en/20/intro.html，sqlalchemy共分为三层架构

<img src="assets/image-20240421141341206.png" alt="image-20240421141341206" style="zoom:50%;" />

- ORM：把数据的schema转化成Python类

- Core：新建engine和连接池，执行数据库的增、删、改、查等操作。

- DBAPI：这一层不属于SQLAlchemy代码，是SQLAlchemy使用的数据库(例如MySQL)驱动提供的API

按照sqlalchemy的官方文档，总共分这几部分介绍

<img src="assets/image-20240421144306680.png" alt="image-20240421144306680" style="zoom:50%;" />

这里重点看Core里面的Engine and Connection Use

<img src="assets/image-20240421195054066.png" alt="image-20240421195054066" style="zoom:50%;" />

### 2. Core

#### （1）Engine

参考ChatGPT对SQLAlchemy官网的翻译加解释

> 参考https://docs.sqlalchemy.org/en/20/core/engines.html#engine-configuration
>
> 参考：https://chat.openai.com/share/44a4dfb9-d5e8-4e06-af80-0d013b5f1407

- **Engine 是任何 SQLAlchemy 应用程序的起点**：Engine 是 SQLAlchemy 中用于与数据库交互的起始点。它是应用程序与实际数据库之间的桥梁，提供了一个统一的接口，用于执行 SQL 语句、管理连接池以及处理数据库连接等操作。

- **Engine 就像是数据库的“主基地”**：Engine 可以被视为应用程序与数据库之间的“主基地”。它是所有数据库交互的中心，负责处理数据库的连接、执行数据库操作，并提供了一种统一的方式来管理数据库交互。

- **Engine 提供了连接池和 Dialect**：Engine 不仅仅是一个简单的数据库连接，它还提供了连接池和 Dialect。连接池用于管理数据库连接的分配和回收，以提高数据库访问的性能和效率。Dialect 描述了如何与特定类型的数据库和 DBAPI 进行通信，它提供了一种数据库无关的方式来执行 SQL 语句，使得 SQLAlchemy 能够与多种不同类型的数据库进行交互。

参考https://foofish.net/python-sqlalchemy-engine.html这篇文档的补充说明

Engine翻译过来就是引擎的意思，汽车通过引擎来驱动，而 SQLAlchemy 是通过 Engine 来驱动，Engine 维护了一个连接池（Pool）对象和方言（Dialect）。方言简单而言就是你连的到底是MySQL或者 PostgreSQL 还是其它数据库。

**连接池很重要，因为每次发送sql查询的时候都需要先建立连接，如果程序启动的时候事先就初始化一批连接放在连接池，每次用完后又放回连接池给其它请求使用，就能大大提高查询的效率**。

<img src="assets/image-20240421173410725.png" alt="image-20240421173410725" style="zoom:50%;" />



创建engine可以用`create_engine`方法

```python
from sqlalchemy import create_engine
engine = create_engine('mysql://user:password@localhost:3306/test?charset=utf8mb4')
```

`create_engine` 还有很多可选参数，这里介绍几个重要的参数。

```bash
engine = create_engine('mysql://user:password@localhost:3306/test?charset=utf8mb4',
                       echo=False
                       pool_size=100,
                       pool_recycle=3600,
                       pool_pre_ping=True)
```

- **echo** ：为True 时候会把sql语句打印出来，当然，你可以通过配置logger来控制输出，这里不做讨论。

- **pool_size**： 是连接池的大小，默认为5个，0表示连接数无限制

- **pool_recycle**： MySQL 默认情况下如果一个连接8小时内容没有任何动作（查询请求）就会自动断开链接，出现 MySQL has gone away的错误。设置了 pool_recycle 后 SQLAlchemy 就会在指定时间内回收连接。如果设置为3600 就表示 1小时后该连接会被自动回收。

**pool_pre_ping** ： 这是1.2新增的参数，如果值为True，那么每次从连接池中拿连接的时候，都会向数据库发送一个类似 `select 1` 的测试查询语句来判断服务器是否正常运行。当该连接出现 disconnect 的情况时，该连接连同pool中的其它连接都会被回收。

构建好 `engine` 对象的同时，`Pool`和`Dialect`也创建好了，但是这时候并不会立马与数据库建立真正的连接，只有调用 `engine.connect()` 或者 `engine.begin()` 执行SQL请求的时候，才会建立真正的连接。因此 `engine`和`Pool`的行为称之为延迟初始化，等真正要派上用场的时候才去建立连接。

`engine`一旦创建，就可以直接用于与数据库交互，**也可以传递给`session`以与ORM一起使用**。

#### （2）Connection Pooling

为什么要使用连接池，这篇文章https://www.cockroachlabs.com/blog/what-is-connection-pooling/给了非常透彻的说明。在一个常见的数据库连接中，其大体步骤是这样的：

1. 应用程序使用数据库驱动程序打开一个连接。 
2. 打开一个网络套接字来连接应用程序和数据库。
3.  对用户进行身份验证。
4.  操作完成，连接可能会被关闭。 
5. 关闭网络套接字。

可以看到，这是一个非常繁琐的操作，然后如果不关闭连接，又会浪费很多资源。连接池就是去解决这个问题的。

### 3. ORM

在sqlalchemy中，**session是用来处理ORM的**。

> 参考https://blog.csdn.net/2301_78316786/article/details/132178490

让我们先来谈谈什么是“Session”。在你逛超市或者餐厅的时候，你可能会遇到一种叫做“前台”的东西。你知道那是干什么的吗？它是用来暂存你买的东西，这样你就可以从容地结账，而不必抱着满满一购物车的商品。

数据库的“Session”就像这个前台。当你对数据库进行操作时，你的操作会先被放在一个地方，这个地方就是“Session”。你可以把它想象成快递公司的一个大箱子，你的包裹先被放进这个箱子里，然后快递员会再处理它。

在SQLAlchemy中，Session扮演的角色就是这样。当你创建了一些对象，比如新的数据库记录，你并没有直接把它们添加到数据库中。相反，你把它们放到了Session中。然后，你可以对Session进行操作，比如提交（commit）操作，这会把Session中的所有更改应用到数据库中。

这就好比你在餐厅工作，客人点了一份汉堡。你不会立刻去做，而是把它写在订单上，然后等到一桌订单都写好了，你才会开始制作汉堡。Session就像是这张订单，它可以暂存你的操作，然后一次性提交。

现在让我们来看看一些代码示例。首先，我们需要创建一个Session。
