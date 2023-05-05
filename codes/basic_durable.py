import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# 创建持久化队列
channel.queue_declare(queue="hello", durable=True)

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body=b'Hello World!',
                      # 让消息持久化
                      properties=pika.BasicProperties(
                          delivery_mode=2,
                      ))
print("[x] Sent 'Hello World!'")