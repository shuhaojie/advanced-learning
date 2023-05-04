# mq

## 一、基本概念

### 1. 什么是MQ？

MQ的全称是Message Queue，字面意思是消息队列。消息队列是在消息的传输过程中**保存消息的容器**，简单来说就是消息（数据）以“管道”的形式在两个应用之间传递。

<img src="assets/image-20230504211139478.png" alt="image-20230504211139478" style="zoom:67%;" />

### 2. 什么是RabbitMQ？

可以把RabbitMQ理解为类似于MySQL的一种软件，MySQL存储关系型数据，而RabbitMQ是用来管理消息的软件，它提供接口开发给用户，用户把消息发给消息队列或者从消息队列里去取消息。

## 二、RabbitMQ工作模式

### 1. 简单模式

生产者

- 连接rabbitmq
- 创建队列
- 向指定队列插入数据

```python
import pika

# 1. 连接rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. 创建队列(声明队列), 如果队列不存在时才需要创建队列, 已经存在就不需要创建了
channel.queue_declare(queue="hello")

# 3. 往队列里插入数据
channel.basic_publish(exchange='',  # 简单模式
                      routing_key='hello',  # 指定队列
                      body=b'Hello World!')
print("[x] Sent 'Hello World!'")
```

消费者

- 连接rabbitmq
- 监听模式
- 确定回调函数

```python
import pika

# 1. 连接rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 注意，这里之所以也要去声明队列，是因为不确定publish那边是否创建了队列，因为有可能publish后执行，
# 如果没有队列，后面监听的地方会报错
channel.queue_declare(queue="hello")

# 2. 确定回调函数
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)

# 3. 确定监听队列
channel.basic_consume(queue='hello',
                      auto_ack=True, # 默认应答
                      on_message_callback=callback)

print("[*] Waiting for messages. To exit press CTRL+C")
# 启动监听, 如果队列里没有数据, 就会hang住。如果队列里有数据，会去执行回调函数
channel.start_consuming()
```

注意

1. 在消费者这边之所以也要去声明队列，是因为不确定publish那边是否创建了队列，因为有可能publish后执行，如果没有队列，后面监听的地方会报错。
2. `start_consuming`启动监听, 如果队列里没有数据, 就会hang住。如果队列里有数据，会去执行回调函数，执行完回调之后会再次处于监听状态。

### 2. 参数使用



### 3. 交换机模式



生产者并没有直接将消息发送给队列，而是通过交换机(Exchange)来作为队列和它之间的桥梁。交换机和队列之间通过routing_key来定义路由关系的。

因此可以指定exchange为空字符串，routing_key的名称为想将消息定向到的队列的名称。此外，指定`delivery_mode`为`PERSISTENT_DELIVERY_MODE`，来保证消息的持久化。
```python
channel.basic_publish(
    exchange="",
    routing_key="video",
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ),
)
```

在消费的时候，指定queue
```python
channel.basic_consume(
    queue="video", on_message_callback=callback
)
```

## 三、pika

### 1. basic_publish

将消息发布到特定的交换机，消息将被路由到交换机定义的队列，并分发给活跃的消费者。

```python
channel.basic_publish(
    exchange="",
    routing_key="video",
    body=json.dumps(message),
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
    ),
)
```

**当交换机设置为默认的空字符串时，创建的每个队列，都使用与队列名称相同的routing_key**，来自动绑定到它。

> 见官网说明<https://www.rabbitmq.com/tutorials/amqp-concepts.html#exchange-default>

### 2. basic_consume

### 3. basic_get

从mq中获取消息

```python
method_frame, header_frame, body = channel.basic_get('test')
```

如果获取到了消息，`method_frame`会是一个`pika.spec.Basic.GetOk` 对象，对象里会包含当前消息数、`delivery_tag`、`routing_key`

### 4. basic_ack

确认一条或者多条消息

```python
if method_frame:
    channel.basic_ack(method_frame.delivery_tag)
else:
    print('No message returned')
```