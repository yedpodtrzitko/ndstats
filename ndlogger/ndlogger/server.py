#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import socket
import select
from .queue import RedisQueue


def serve_forever():
    # bot stuff produce too much noise, throw it straight away
    # Jenkins<3><BOT><EMPIRE>
    re_bot = re.compile(r'"(.*?)<(\d+)><BOT><(.*?)>"')

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 27500))

    q = RedisQueue('ndstats')
    print('about to serve')
    while 1:
        inputs, outputs, exceptions = select.select([s], [], [], 2)
        if inputs:
            try:
                data, origin = s.recvfrom(1024)
                line = data.decode('utf-8', 'ignore').strip()
                if re_bot.search(line):
                    continue

                x = "%s|%s" % (origin[0], line)
            except Exception:
                pass
            else:
                q.put(x)


if __name__ == '__main__':
    serve_forever()
