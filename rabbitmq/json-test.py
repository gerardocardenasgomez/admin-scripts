#!/usr/bin/env python
import json

metadata = [{"server":"localhost", "ticket":22, "user":1, "limit":60}]
json_metadata = json.dumps(metadata)

result = json.loads(json_metadata)

host = result[0]["server"]
username = result[0]["sanitizedthis"
password = "sanitizedthis"
db_name = "sanitizedthis"
script_id = 2
user_id = 1
completed = 0
