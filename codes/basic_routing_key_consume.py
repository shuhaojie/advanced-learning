import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange="logs",
                         # 类型要改为direct
                         exchange_type="direct")

result = channel.queue_declare("", exclusive=True)
queue_name = result.method.queue

channel.queue_bind(
    exchange='logs',
    queue=queue_name,
    # 确定要监听的关键字
    routing_key='error'
)


def callback(ch, method, properties, body):
    print("[x] Received %r" % body)


channel.basic_consume(queue=queue_name, auto_ack=True, on_message_callback=callback)
print("[*] Waiting for messages. To exit press CTRL+C")
channel.start_consuming()
