'''
server and multiple clients with multiprocessing
'''

import socket
from multiprocessing import Process


def echo_server(address=54321):
    ''' echo_server '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        Process(target=echo_handler, args=(client, addr)).start()


def echo_handler(client, addr):
    ''' echo_handler '''
    print('Connection from', addr)
    with client:
        while True:
            data = client.recv(100000)
            if not data:
                break
            client.sendall(data)
    print('Connection closed')


if __name__ == '__main__':
    echo_server(('', 54300))
