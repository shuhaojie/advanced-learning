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
