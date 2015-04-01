#!/usr/bin/env python
import pika
import sys
import optparse
import json

parser = optparse.OptionParser()
parser.add_option("-s", "--script", action="store", dest="script_id", type="int")
parser.add_option("-u", "--user", action="store", dest="user_id", type="int")
parser.add_option("-c", "--completed", action="store", dest="completed", type="int")
parser.add_option("-q", "--quit", action="store", dest="quit", default=None)

options, args = parser.parse_args()

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
if options.quit is None:
    metadata = [{"script_id":options.script_id, "user_id":options.user_id, "completed":options.completed}] 
    body = json.dumps(metadata)
else:
    body = "quit"

msg_props = pika.BasicProperties()
msg_props.content_type = "application/json"

channel.basic_publish(body=body,
                        exchange="server-requests",
                        properties=msg_props,
                        routing_key="")
