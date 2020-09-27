import Controller
import os
import pika
import amqpstorm
from amqpstorm import Message

RABBITMQSERVER = os.environ['AMPQ_HOST']

def on_request(message):

    pid = str(int(message.body))

    response = str(Controller.retrieve_shipping())

    properties = {
        'correlation_id': message.correlation_id
    }

    response = Message.create(message.channel, response, properties)
    response.publish(message.reply_to)

    message.ack()


CONNECTION = amqpstorm.Connection(RABBITMQSERVER, 'guest', 'guest')
CHANNEL = CONNECTION.channel()

CHANNEL.queue.declare(queue='product-shipping-service-q')
CHANNEL.basic.qos(prefetch_count=1)
CHANNEL.basic.consume(on_request, queue='product-shipping-service-q')

print(" [x] Awaiting RPC requests")
CHANNEL.start_consuming()
