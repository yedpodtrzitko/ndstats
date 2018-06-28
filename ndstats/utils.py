import redis

from django.conf import settings
from ndstats.parser import LogParser
from ndstats.queue import RedisQueue


def handle_log():
    parser = LogParser()

    # abuse the connection to get/set lock
    r = redis.Redis()
    if r.get(settings.QUEUE_LOCK):
        return

    r.setex('ndlock', True, 10)
    q = RedisQueue(settings.QUEUE_NAME, namespace='redismq:')
    while q.qsize():
        line = q.get_nowait()
        if line:
            try:
                parser.parse_raw_line(line)
            except Exception as e:
                print(e)

    r.delete(settings.QUEUE_LOCK)
