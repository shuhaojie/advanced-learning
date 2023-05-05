import pika

# 1. 连接rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 和简单模式一样，怕生产者事先没有创建交换机，这里做一下创建
channel.exchange_declare(
    exchange="logs",
    exchange_type="fanout"
)

# 2. 创建队列
result = channel.queue_declare(
    # 不自己取队列名称, 系统随机创建队列名称
    "",
    exclusive=True
)
# 可以拿到系统自动创建的队列名称
queue_name = result.method.queue
print(queue_name)
# 3. 将指定队列绑定到交换机上
channel.queue_bind(
    exchange='logs',
    queue=queue_name
)


#  和前面一样, 确定回调函数
def callback(ch, method, properties, body):
    print("[x] Received %r" % body)


#  和前面一样, 确定监听队列
channel.basic_consume(
    queue=queue_name,
    auto_ack=True,
    on_message_callback=callback
)
print("[*] Waiting for messages. To exit press CTRL+C")
# 和前面一样, 开始监听
channel.start_consuming()
