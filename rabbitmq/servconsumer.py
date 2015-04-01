#!/usr/bin/env python
import pika, sys
import json
import random

rabbitUser = "guest"
rabbitPass = "guest"
rabbitHost = "localhost"

host = "localhost"
username = "sanitizedthis"
password = "sanitizedthis"
db_name = "sanitizedthis"

# This will be replaced by a JSON call to initialize an instance
available_ip = ["192.168.1.90",
                "192.168.1.91",
                "192.168.1.92",
                "192.168.1.93",
                "192.168.1.84"]

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
        results = json.loads(body)
        print "Processing..."
        script_id=results[0]["script_id"],
        user_id=results[0]["user_id"],
        print "IP address...{0}".format(random.choice(available_ip))
        print "Script name: {0}".format(script_id)
        print "User name: {0}".format(user_id)
        print "Completed request, sending email..."

    return

channel.basic_consume(msg_consumer,
                        queue="server-init",
                        consumer_tag="server-initializer")
channel.start_consuming()
