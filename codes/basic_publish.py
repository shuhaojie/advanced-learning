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
