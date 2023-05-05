import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.exchange_declare(exchange="logs",
                         # 类型要改为direct
                         exchange_type="direct")

channel.basic_publish(
    exchange='logs',
    # 定义routing_key
    routing_key='info',
    body=b'Info: Hello World!')

print("[x] Sent 'Hello World!'")
