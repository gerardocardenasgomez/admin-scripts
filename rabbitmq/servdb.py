#!/usr/bin/env python
import pika, sys
import json
import mysqlinsert

rabbitUser = "guest"
rabbitPass = "guest"
rabbitHost = "localhost"

host = "localhost"
username = "sanitizedthis"
password = "sanitizedthis"
db_name = "sanitizedthis"

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
        mysqlinsert.db_insert(host=host,
                                username=username,
                                password=password,
                                db_name=db_name,
                                script_id=results[0]["script_id"],
                                user_id=results[0]["user_id"],
                                completed=results[0]["completed"])
        print "Processed a job!"
    return

channel.basic_consume(msg_consumer,
                        queue="server-init",
                        consumer_tag="server-initializer")
channel.start_consuming()
