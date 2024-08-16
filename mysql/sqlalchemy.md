# SQLAlchemy

> 注意：SQLAlchemy是一个数据库工具，但是它不仅仅只是MySQL，还有其他类型的数据库

## 一、SQLAlchemy概述

### 1. 架构图

按照sqlalchemy官网的介绍https://docs.sqlalchemy.org/en/20/intro.html，sqlalchemy共分为三层架构

<img src="../assets/image-20240421141341206.png" alt="image-20240421141341206" style="zoom:50%;" />

- SQLAlchemy ORM：把数据的schema转化成Python类

- SQLAlchemy Core：新建engine和连接池，执行数据库的增、删、改、查等操作。

- DBAPI：这一层不属于SQLAlchemy代码，是SQLAlchemy使用的数据库(例如MySQL)驱动提供的API，例如MySQL的DBAPI就是pymysql

### 2. ORM和Core的关系

参考ChatGPT，https://chatgpt.com/share/b9457b62-4b99-45cf-b709-4c64b22cfdcd

#### （1）关系和区别

**SQLAlchemy ORM建立在SQLAlchemy Core之上**，利用了SQLAlchemy Core提供的SQL表达语言和数据库连接管理等功能。

- **抽象层次不同**：SQLAlchemy Core更接近SQL，提供了更底层和灵活的操作能力。SQLAlchemy ORM则提供了更高级别的抽象，使得开发者可以使用面向对象的方式进行数据库操作。

- **使用场景**：SQLAlchemy Core适合需要直接控制SQL查询和优化的场景，适合复杂的查询和操作。SQLAlchemy ORM适合希望简化数据库操作，提高代码可维护性的场景，尤其适用于面向对象编程。

#### （2）结合使用

SQLAlchemy Core和ORM可以结合使用，在需要直接控制SQL查询时，可以使用Core的功能，而在进行常规的数据库操作时，可以使用ORM。

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String

engine = create_engine('sqlite:///example.db')  # 创建引擎
Base = declarative_base()  # 基类

# 定义User类
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

# 创建表
Base.metadata.create_all(engine)

# 创建Session
Session = sessionmaker(bind=engine)
session = Session()

# 插入数据
session.add_all([
    User(name='Alice', age=25),
    User(name='Bob', age=30),
])
session.commit()
```

## 二、SQLAlchemy统一教程

参考https://docs.sqlalchemy.org/en/20/tutorial/index.html#sqlalchemy-unified-tutorial

### 1. Engine

Engine是SQLAlchemy的起点，Engine不仅仅是一个简单的数据库连接，它还提供了连接池和Dialect，Dialect简单而言就是你连的到底是MySQL或者PostgreSQL还是其它数据库。

- 连接池用于管理数据库连接的分配和回收，以提高数据库访问的性能和效率。
- Dialect 描述了如何与特定类型的数据库和DBAPI进行通信，它提供了一种数据库无关的方式来执行SQL语句，使得SQLAlchemy能够与多种不同类型的数据库进行交互。

```python
from sqlalchemy import create_engine
engine = create_engine("mysql+pymysql://user:password@localhost:3306/test?charset=utf8mb4", echo=True)
```

这个字符串中：

- mysql：表示我们使用的数据库是mysql数据库
- pymysql：表示我们使用的DBAPI是pymysql
- 后面的字符串，是用来如何定位数据库的

<img src="../assets/image-20240421173410725.png" alt="image-20240421173410725" style="zoom:50%;" />

**创建了Engine之后，我们就有了连接池Pool和Dialect，就可以调用DBAPI和数据库进行交互**

`create_engine` 还有很多可选参数，这里介绍几个重要的参数。

```bash
engine = create_engine('mysql+pymysql://user:password@localhost:3306/test?charset=utf8mb4',
                       echo=False,
                       pool_size=100,
                       pool_recycle=3600,
                       pool_pre_ping=True)
```

- echo ：为True 时候会把sql语句打印出来，当然，你可以通过配置logger来控制输出，这里不做讨论。

- pool_size： 是连接池的大小，默认为5个，0表示连接数无限制。连接池很重要，因为每次发送sql查询的时候都需要先建立连接，如果程序启动的时候事先就初始化一批连接放在连接池，每次用完后又放回连接池给其它请求使用，就能大大提高查询的效率。

- pool_recycle： MySQL 默认情况下如果一个连接8小时内容没有任何动作（查询请求）就会自动断开链接，出现 MySQL has gone away的错误。设置了 pool_recycle 后 SQLAlchemy 就会在指定时间内回收连接。如果设置为3600 就表示 1小时后该连接会被自动回收。

- pool_pre_ping： 这是1.2新增的参数，如果值为True，那么每次从连接池中拿连接的时候，都会向数据库发送一个类似 `select 1` 的测试查询语句来判断服务器是否正常运行。当该连接出现 disconnect 的情况时，该连接连同pool中的其它连接都会被回收。

> 注意：
>
> - 构建好 `engine` 后，这时并不会立马与数据库建立真正的连接，这个被称为Lazy Connecting，当第一次被要求对数据库执行任务时才会建立连接。
>
> - `engine`一旦创建，可以直接用于与数据库交互，**也可以传递给`session`以与ORM一起使用**

### 2. 事务和DBAPI

engine构建好之后，我们就可以开始做一些基础操作了

#### （1）建立连接

前面建立Engine对象的目的，是通过connect方法来创建Connection对象，来连接到数据库。当直接使用Core时，	**Connection对象是完成与数据库的所有交互的方式**。由于 Connection 针对数据库创建了开放资源，因此最好将此对象的使用限制在特定上下文中。最好的方法是使用 Python 上下文管理器，也称为with语句。

<img src="../assets/image-20240807155130510.png" alt="image-20240807155130510" style="zoom:50%;" />

在上面的示例中，**with语句创建数据库连接并在事务中执行操作**。 Python DBAPI的默认行为是事务始终在进行中，**当连接被释放时，会发出ROLLBACK来结束事务**。事务不会自动提交；如果我们想提交数据，我们需要调用 	`Connection.commit()`，我们将在下一节中看到。

```sql
BEGIN (implicit)
select 'hello world'
[...] ()
[('hello world',)]
ROLLBACK
```

#### （2）事务提交

> 事务：把需要保证`原子性`、`隔离性`、`一致性`和`持久性`的一个或多个数据库操作称之为一个事务
>
> - 原子性：要么全部成功，要么全部失败
> - 隔离性：两次状态转换互不影响
> - 持久性：修改的数据，无论发生什么事故，都应该在磁盘上保留下来
> - 一致性：数据库状态与真实业务状态相一致。一致性是目的，而前面三个都是手段。

DBAPI连接不会自动提交。如果我们想提交一些数据怎么办？

```python
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 1, "y": 1}, {"x": 2, "y": 4}],
    )
    conn.commit()
```

上面语句等价的sql语句是

```sql
BEGIN (implicit)
CREATE TABLE some_table (x int, y int)
[...] ()
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] [(1, 1), (2, 4)]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

上面，我们执行两个 SQL 语句，为了提交我们在块中完成的工作，我们调用`Connection.commit() `方法来提交事务。之后，我们可以继续运行更多的SQL语句，并为这些语句再次调用`Connection.commit()`，SQLAlchemy 将这种风格称为**commit as you go**（随时提交）。

除了上面这种形式，还有一种方法来做提交

```python
with engine.begin() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 6, "y": 8}, {"x": 9, "y": 10}],
    )
```

上面语句等价为

```sql
BEGIN (implicit)
INSERT INTO some_table (x, y) VALUES (?, ?)
[...] [(6, 8), (9, 10)]
<sqlalchemy.engine.cursor.CursorResult object at 0x...>
COMMIT
```

使用`Engine.begin()` 方法来获取连接，而不是 `Engine.connect() `方法。此方法将管理连接的范围，并且还将事务内的所有内容包含在事务内，如果成功，则在末尾使用 COMMIT；如果引发异常，则在末尾使ROLLBACK。这种风格称为**begin once**（开始一次）

#### （3）基础知识

##### ~ 获取行

```python
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

Result 有很多用于获取和转换行的方法，例如前面介绍的`Result.all() `方法，下面我们举例说明访问行的多种方法。

- **Tuple Assignment**

这是最符合 Python 习惯的风格，即在收到变量时按位置将变量分配给每一行

```python
result = conn.execute(text("select x, y from some_table"))

for x, y in result:
    ...
```

- **Integer Index** 

元组是 Python 序列，因此也可以进行常规整数访问

```python
result = conn.execute(text("select x, y from some_table"))

for row in result:
    x = row[0]
```

- **Attribute Name** 

元组具有与每列名称匹配的动态属性名称，这些名称通常是 SQL 语句分配给每行中的列的名称。

```python
result = conn.execute(text("select x, y from some_table"))

for row in result:
    y = row.y  # 直接点出y
		print(f"Row: {row.x} {y}")
```

- **Mapping Access**

不做过多解释

```python
result = conn.execute(text("select x, y from some_table"))

for dict_row in result.mappings():
    x = dict_row["x"]
    y = dict_row["y"]
```

##### ~ 传参

`Connection.execute() `方法也接受参数，这些参数称为绑定参数。如果我们希望将 SELECT 语句限制为仅满足特定条件的行，例如“y”值大于传递给函数的特定值的行

```python
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table WHERE y > :y"), {"y": 2})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

##### ~ 传多个参数

例如下面的例子，可以传递多个参数

```python
with engine.connect() as conn:
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 11, "y": 12}, {"x": 13, "y": 14}],
    )
    conn.commit()
```

#### （4）ORM Session

上述示例也适用于ORM的使用，**使用ORM时的基本事务/数据库交互对象称为会话**。在SQLAlchemy 中，该对象的使用方式与Connection非常相似，**在使用Session时，它在内部引用Connection，并使用Connection发出 SQL**。

<img src="../assets/image-20240809110903710.png" alt="image-20240809110903710" style="zoom:50%;" />

注意：虽然session是ORM独有的，**但是它也可以和非ORM结构使用**，例如下面的例子

```python
from sqlalchemy.orm import Session

stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

也可以用于DML语句

```python
with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()
```

### 3. 数据库元数据

#### （1）Table 对象设置元数据

在 SQLAlchemy 中，最常见的数据库元数据基础对象被称为元数据（MetaData）、表（Table）和列（Column）。

- `MetaData` 对象：这是根对象，**用于管理数据库中的所有表格，它充当了所有 `Table` 对象的容器。**

- `Table` 对象：每个 `Table` 对象对应数据库中的一个表格，包含表格的结构信息，如列（`Column`）

- `Column` 对象：`Column` 对象定义了表格中的各个列。

##### ~ 表对象元素

在关系数据库中，数据是存储在表格 (Table) 中的。表格是数据库中的基本结构，用于存放和查询数据。在 SQLAlchemy 中，数据库表格被映射为一个 Python 对象，这个对象也叫做 `Table`。

为了开始使用 SQLAlchemy 的表达式语言 (Expression Language)，需要构建代表数据库表格的 `Table` 对象。可以通过三种方式构建：

- 直接使用 `Table` 构造函数：可以通过编程方式直接构建 `Table` 对象。
- 间接使用 ORM 映射类：可以通过使用 ORM（对象关系映射）映射类来间接定义表格的元数据

- 还有一个选项是通过“反射” (Reflection)： 从现有的数据库中加载一些或全部的表格信息。

无论你选择哪种方式开始，首先需要一个 `MetaData` 对象，这是用来存放表格的集合。创建 `MetaData` 对象，创建方式如下：

```python
from sqlalchemy import MetaData
metadata_obj = MetaData()
```

一旦我们有了一个 `MetaData` 对象，我们就可以开始声明一些 `Table` 对象了。

```python
from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String),
)
```

有了上面的定义之后，我们如果希望对user_account这个表进行操作，只需要使用`user_account` 这个 Python 变量即可。

##### ~ 约束

上面定义了一个primary_key主键约束，下面我们再定义一个外键约束

```python
from sqlalchemy import ForeignKey
address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String, nullable=False),
)
```

##### ~ 建表

> Emit：发送
> DDL：数据库定义语言

上面我们定义了两张表，接下来我们可以使用 `MetaData.create_all()` 方法，用于将 `MetaData` 对象中包含的所有表格（即所有 `Table` 对象）在数据库中创建出来。

结合上面的代码，下面这个代码就会创建`user_account`和`address`两张表

```python
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import ForeignKey
from sqlalchemy import Table, Column, Integer, String

engine = create_engine('mysql+pymysql://root:805115148@localhost:3306/auth?charset=utf8mb4',
                       echo=True,
                       pool_size=100,
                       pool_recycle=3600,
                       pool_pre_ping=True)

metadata_obj = MetaData()

user_table = Table(
    "user_account",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(30)),
    Column("fullname", String(30)),
)


address_table = Table(
    "address",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("user_id", ForeignKey("user_account.id"), nullable=False),
    Column("email_address", String(30), nullable=False),
)

metadata_obj.create_all(engine)
```

#### （2）ORM 定义表元数据

当使用ORM(Object Related Mapper，对象关系映射)时，定义数据库表的元数据(Metadata)和映射类(`Mapper Class`)通常是一起进行的。映射类是指我们想要创建的Python类，这些类的属性将与数据库表中的列关联。最常见的方法是声明式（`declarative`）风格，这种风格允许我们同时声明自定义类和表的元数据。

##### ~ Base类

在使用SQLAlchemy的ORM时，`MetaData`对象仍然存在，但它与一个专门用于ORM的结构（通常称为`Declarative Base`）相关联。Declarative Base是SQLAlchemy中用于定义ORM模型类的基础类

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```

这个Base类就是Declarative Base，当我们创建继承自`Base`的新类时，**每个新类都会被映射到数据库中的一个表或其他结构。Declarative Base引用了一个自动为我们创建的`MetaData`集合，也就是说，如果我们没有手动指定一个`MetaData`，SQLAlchemy会自动为我们生成一个。这个`MetaData`可以通过`DeclarativeBase.metadata`类级属性访问。也就是说，我们可以通过`Base.metadata`访问和操作这个`MetaData`对象。当我们创建新的映射类时，每个类都会引用这个`MetaData`集合中的一个`Table`对象（和上一讲一样）

```python
>>> Base.metadata
MetaData()
```

Declarative Base不仅与`MetaData`关联，还与一个名为`registry`的集合关联，registry是SQLAlchemy ORM的核心“映射配置”单元，负责管理和协调ORM映射类的配置。

```python
>>> Base.registry
<sqlalchemy.orm.decl_api.registry object at 0x...>
```

##### ~ 定义映射类(重点)

当我们建立了Base类之后，就可以开始定义ORM映射类，以映射数据库中的`user_account`和`address`表

```python
from typing import List
from typing import Optional
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]] = mapped_column(String(255))
    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str] = mapped_column(String(255))
    user_id = mapped_column(ForeignKey("user_account.id"))
    user: Mapped[User] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
```

关于上面定义的说明

（1）每个ORM类都引用了一个`Table`对象，这个对象是在声明式映射过程中自动生成的。`Table`对象代表数据库中的一张表，并与ORM类关联。**这个`Table`对象的名称是通过将一个字符串赋值给ORM类的`__tablename__`属性来指定的**，这个字符串通常是数据库中表的名称。一旦ORM类被创建，这个生成的`Table`对象就可以通过ORM类的`__table__`属性访问。换句话说，`__table__`属性让我们能够直接访问ORM类关联的`Table`对象。下图中的address_table就是一个Table对象，和上一节咱们创建的对象是一致的。

<img src="../assets/image-20240813164119014.png" alt="image-20240813164119014" style="zoom:30%;" />

（2）要在数据库表中定义列，我们使用`mapped_column()`这个构造函数，这个函数用于将类属性映射到数据库表的列。`mapped_column()`通常与基于`Mapped`类型的类型注解一起使用。类型注解用于指定属性的数据类型，例如整数、字符串等。`mapped_column()`会生成`Column`对象，而这些`Column`对象会用于构建`Table`对象。

（3）对于只有简单数据类型且没有其他选项（如主键、唯一性约束等）的列，我们可以仅使用`Mapped`类型注解来定义，而不必使用`mapped_column()`。

（4）一个字段可以定义为空，例如上面的`fullname: Mapped[Optional[str]]`，它表达的意思是这个字段可以为空，也可以是str。等效于`Union[str, None]`

（5）在 SQLAlchemy 中，使用类型注解并不是强制性的。你可以在定义映射列时使用更显式的类型对象（如 `Integer` 和 `String`），以及其他参数（如 `nullable=False`），而不需要使用类型注解。

使用类型注解：

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id: int = mapped_column(Integer, primary_key=True)
    name: str = mapped_column(String(50))
    age: int = mapped_column(Integer, nullable=False)
```

不使用类型注解：**这个也是老版本中经典的写法，推荐还是用这种方式。**

```python
from sqlalchemy import Integer, String
from sqlalchemy.orm import mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(50))
    age = mapped_column(Integer, nullable=False)
```

（6）`relationship()` 用于定义模型之间的关系。比如在 SQLAlchemy 中，你可以用 `relationship()` 来设置两个表之间的关联。

（7）上面创建的类，会自动给一个`__init__`方法，此方法的默认形式接受所有属性名称作为可选关键字参数

```python
sandy = User(name="sandy", fullname="Sandy Cheeks")
```

（8）`__repr__`方法是为了让我们获得一个可读性更好的字符串

##### ~ 建表

有了前面的基础，这里直接使用即可建表

```python
Base.metadata.create_all(engine)
```

#### （3）表反射

表反射（table reflection）是指通过读取数据库的当前状态，生成相应的 `Table` 对象。简单来说，它是从已有数据库结构中反向生成Python中的数据结构。与手动定义列和约束不同，这里通过 `Table.autoload_with` 参数来指定目标数据库引擎（`Engine`）。这个参数会自动从数据库中加载表的列和约束等信息，而不需要手动定义这些结构。

```python
from sqlalchemy import Table, MetaData
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://root:805115148@localhost:3306/auth?charset=utf8mb4", echo=True)
metadata_obj = MetaData()
some_table = Table("some_table", metadata_obj, autoload_with=engine)
print(some_table.columns.keys())
stmt = insert(some_table).values(x=10, y=20)
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
```

### 4. 处理数据

#### （1）Insert语句

当使用Core以及使用ORM进行批量操作时，直接使用`insert()`函数生成 SQL INSERT 语句, 该函数生成一个新的 `Insert` 实例，它代表 SQL 中的INSERT语句，它将新数据添加到表中

##### ~ insert表达式

下面是一个简单的insert语句

```python
from sqlalchemy import insert
stmt = insert(user_table).values(name="spongebob", fullname="Spongebob Squarepants")
```

这里的stmt就是一个`Insert` 实例，我们可以直接打印来看sql语句长啥样

```python
>>> print(stmt)
INSERT INTO user_account (name, fullname) VALUES (:name, :fullname)
```

这个sql字符串实际上是由Compiled对象来生成的，我们可以通过

```
compiled = stmt.compile()
```

上面我们的插入构造是“参数化”构造的一个示例，如之前在发送参数`VALUES (:name, :fullname)`，要查看名称和全名绑定参数，这些也可以从 Compiled 构造中获得：

```python
>>> compiled.params
{'name': 'spongebob', 'fullname': 'Spongebob Squarepants'}
```

##### ~ 执行insert语句

```
with engine.connect() as conn:
    result = conn.execute(stmt)
    conn.commit()
```

在上面的简单形式中，INSERT 语句不返回任何行，如果只插入一行，我们可以使用 `inserted_primary_key` 获取主键

```python
>>> result.inserted_primary_key
(1,)
```

##### ~ 不使用values语句

前面我们显示的使用了`values`方法来插入数据，其实这个不是必要的，也可以不用

```python
with engine.connect() as conn:
    result = conn.execute(
        insert(user_table),
        [
            {"name": "sandy", "fullname": "Sandy Cheeks"},
            {"name": "patrick", "fullname": "Patrick Star"},
        ],
    )
    conn.commit()
```

下面这个语句页可以插入

##### ~ returning

对于一些数据库支持insert之后returning，但是mysql不支持，不做过多赘叙

##### ~ from_select

该功能使用不多，不做赘叙

#### （2）select语句（重点）

##### ~ select表达式

和前面的`insert`表达式比较类似

```python
from sqlalchemy import select
stmt = select(user_table).where(user_table.c.name == "spongebob")
print(stmt)
```

执行`select`语句

```python
with engine.connect() as conn:
    for row in conn.execute(stmt):
        print(row)
```

使用orm来做查询，是如下形式

```python
stmt = select(User).where(User.name == "spongebob")
with Session(engine) as session:
    for row in session.execute(stmt):
        print(row)
```

##### ~ select选择

`select`函数可以接受任意数量的参数，这些参数通常是列对象 (`Column`) 或者表对象 (`Table`)。

```python
print(select(user_table))
```

这句对应的sql语句其实是

```sql
SELECT user_account.id, user_account.name, user_account.fullname FROM user_account
```

也可以选择具体的列

```
print(select(user_table.c.name, user_table.c.fullname))
```

对应的sql语句是

```sql
SELECT user_account.name, user_account.fullname FROM user_account
```

或者也可以使用下面的形式，和上面是等效的

```python
print(select(user_table.c["name", "fullname"]))
```

##### ~ ORM选择

在ORM中，可以通过如下的方式进行选择

```python
print(select(User))
```

拿到的row只有一个对象，可通过如下形式拿到

```python
row[0]
```

`Session.scalars()` 是 SQLAlchemy 中推荐的一种便捷方法，用于直接执行查询并返回结果。它会返回一个 `ScalarResult` 对象。

```python
from sqlalchemy.orm import Session

with Session(engine) as session:
    stmt = select(User)
    result = session.execute(stmt)
    users = result.scalars().all()
```

这一节后面还有很多东西，篇幅所限，不过度学习，后面按需学习即可

#### （3）update语句

最基础的update语句

```
from sqlalchemy import update
stmt = (
    update(user_table)
    .where(user_table.c.name == "patrick")
    .values(fullname="Patrick the Star")
)
print(stmt)
```

#### （4）delete 语句

最基础的delete语句

```python
from sqlalchemy import delete
stmt = delete(user_table).where(user_table.c.name == "patrick")
print(stmt)
```

### 5. 使用ORM操作数据(重点)

### 6. 使用ORM相关对象

 

## 三、SQLAlchemy Core

#### （1）Schema/Types

#### （2）SQL Expression Language

它和ORM有点像，但又不太一样

#### （3）Engine

#### （4）Connection Pooling

为什么要使用连接池，这篇文章https://www.cockroachlabs.com/blog/what-is-connection-pooling/ 给了非常透彻的说明。在一个常见的数据库连接中，其大体步骤是这样的：

1. 应用程序使用数据库驱动程序打开一个连接。 
2. 打开一个网络套接字来连接应用程序和数据库。
3. 对用户进行身份验证。
4. 操作完成，连接可能会被关闭。 
5. 关闭网络套接字。

可以看到，这是一个非常繁琐的操作，然后如果不关闭连接，又会浪费很多资源。连接池就是去解决这个问题的。

#### （5）Dialect



### 4. SQLAlchemy ORM

在sqlalchemy中，**session是用来处理ORM的**。

> 参考https://blog.csdn.net/2301_78316786/article/details/132178490

让我们先来谈谈什么是“Session”。在你逛超市或者餐厅的时候，你可能会遇到一种叫做“前台”的东西。你知道那是干什么的吗？它是用来暂存你买的东西，这样你就可以从容地结账，而不必抱着满满一购物车的商品。

数据库的“Session”就像这个前台。当你对数据库进行操作时，你的操作会先被放在一个地方，这个地方就是“Session”。你可以把它想象成快递公司的一个大箱子，你的包裹先被放进这个箱子里，然后快递员会再处理它。

在SQLAlchemy中，Session扮演的角色就是这样。当你创建了一些对象，比如新的数据库记录，你并没有直接把它们添加到数据库中。相反，你把它们放到了Session中。然后，你可以对Session进行操作，比如提交（commit）操作，这会把Session中的所有更改应用到数据库中。

这就好比你在餐厅工作，客人点了一份汉堡。你不会立刻去做，而是把它写在订单上，然后等到一桌订单都写好了，你才会开始制作汉堡。Session就像是这张订单，它可以暂存你的操作，然后一次性提交。

现在让我们来看看一些代码示例。首先，我们需要创建一个Session。