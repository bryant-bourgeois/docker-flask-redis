import ddtrace.profiling.auto
import time
import random

import redis
from flask import Flask
from ddtrace import tracer
from ddtrace import patch_all

patch_all()

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            hits = cache.incr('hits')
            return hits
            
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = 0
    for i in range(1, 10000):
        key = random.randint(1,2000)
        val = random.randint(1,2000)
        cache.mset({key: val})
        count = get_hit_count()
    return 'Hello World! I have been seen {} times.\n'.format(count)
