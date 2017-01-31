#!/usr/bin/env python
from __future__ import print_function
import redis
import datetime
import time

def ping_redis(ip, port, count):
    # redis.Redis was compatible with Python 2.6 
    redis_db = redis.Redis(host=ip, port=port, db=0, socket_timeout=5)

    for number in range(count):
        start = time.time() * 1000
        
        # If the connection fails, catching the exception is the only way to continue safely
        try:
            # ping() should return a Boolean
            result = redis_db.ping()
        except:
            result = None

        end = time.time() * 1000

        total_time = (end - start)

        print(datetime.datetime.now(), end="")
        print(" Time: {0:10.0f} ms".format(total_time), end="")

        if result:
            print(" Connected")
        else:
            print(" FAILED Connection")


if __name__ == '__main__':
    ping_redis('127.0.0.1', 6379, 3)
