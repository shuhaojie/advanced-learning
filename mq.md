# mq

## 一、基本概念

### 1. 什么是MQ？

MQ的全称是Message Queue，字面意思是消息队列。消息队列是在消息的传输过程中**保存消息的容器**，简单来说就是消息（数据）以“管道”的形式在两个应用之间传递。

<img src="/Users/shuhaojie/Library/Application Support/typora-user-images/image-20230504162442782.png" alt="image-20230504162442782" style="zoom:67%;" />

### 2. 什么是RabbitMQ？



## 二、消息

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