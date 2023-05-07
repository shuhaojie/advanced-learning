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

