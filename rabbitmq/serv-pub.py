#!/usr/bin/env python
import pika
import sys
import optparse
import json

parser = optparse.OptionParser()
parser.add_option("-s", "--server", action="store", dest="host")
parser.add_option("-t", "--ticket", action="store", dest="ticket", type="int")
parser.add_option("-u", "--user", action="store", dest="user", type="int")
parser.add_option("-l", "--limit", action="store", dest="limit", type="int")

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

metadata = [{"server":options.host, "ticket":options.ticket, "user":options.user, "limit":options.limit}] 
json_metadata = json.dumps(metadata)

msg_props = pika.BasicProperties()
msg_props.content_type = "application/json"

channel.basic_publish(body=json_metadata,
                        exchange="server-requests",
                        properties=msg_props,
                        routing_key="")
