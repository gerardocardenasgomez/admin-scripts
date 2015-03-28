#!/usr/bin/env python
import pika, sys

rabbitUser = "guest"
rabbitPass = "guest"

rabbitHost = "localhost"

credentials = pika.PlainCredentials(rabbitUser, rabbitPass)
conn_params = pika.ConnectionParameters(rabbitHost, credentials = credentials)
conn_broker = pika.BlockingConnection(conn_params)

channel = conn_broker.channel()

channel.exchange_declare(exchange="server-requests",
                        type="fanout",
                        passive=False,
                        durable=True,
                        auto_delete=False)

channel.queue_declare(queue="server-init")
channel.queue_bind(queue="server-init",
                    exchange="server-requests")

def msg_consumer(channel, method, header, body):
    channel.basic_ack(delivery_tag=method.delivery_tag)
    if body == "quit":
        channel.basic_cancel(consumer_tag="server-initializer")
        channel.stop_consuming()
    else:
        print body
    return

channel.basic_consume(msg_consumer,
                        queue="server-init",
                        consumer_tag="server-initializer")
channel.start_consuming()
