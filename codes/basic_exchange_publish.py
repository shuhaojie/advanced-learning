import pika

# 1. 连接rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 2. 声明交换机
channel.exchange_declare(
    # 交换机名称
    exchange="logs",
    # 交换机模式：发布订阅模式
    exchange_type="fanout"
)

# 3. 往交换机里插入数据
channel.basic_publish(
    # 往logs交换机插入数据
    exchange='logs',
    # 不涉及队列，置空
    routing_key='',
    body=b'Hello World!')

print("[x] Sent 'Hello World!'")
