import Controller
import os
import pika

RABBITMQSERVER = os.environ['AMPQ_HOST']

def on_request(ch, method, props, body):
    pid = int(body)

    response = Controller.retrieve_shipping()

    ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id=props.correlation_id), body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQSERVER,credentials=pika.PlainCredentials('guest','guest')))

channel = connection.channel()
channel.queue_declare(queue='product-shipping-service-q')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='product-shipping-service-q', on_message_callback=on_request)

channel.start_consuming()


