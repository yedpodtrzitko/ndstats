import socket

from os.path import join, dirname

TCP_IP = "0.0.0.0"
TCP_PORT = 27500

with open(join(dirname(__file__), 'log.txt'), 'rb') as fp:
    print('file opened, pushing')
    for line in fp:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('got socket', sock)
        sock.connect((TCP_IP, TCP_PORT))
        print('connected')
        sock.send(line)
        print('line sent')
        sock.close()
