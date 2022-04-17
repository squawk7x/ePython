'''
Async Echo Server by Dave Beazley - Python Distilled
'''
# !/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
from socket import *

clients = []


async def echo_server(address):    # adress = (host, port)
    ''' echo server waiting for connections '''
    loop = asyncio.get_event_loop()
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    print('Server listening at', address)
    with sock:
        while True:
            client, addr = await loop.sock_accept(sock)
            print('Connection from', addr)
            loop.create_task(echo_handler(loop, client))
            clients.append(client)
            print('Now online:', clients)
    print('Server stopped')


async def echo_handler(loop, client):
    ''' echo handler sends message back to all clients'''
    with client:
        while True:
            data = await loop.sock_recv(client, 10000)
            if not data:
                clients.remove(client)
                print('Someone left:', client)
                break
            for clt in clients:
                # await loop.sock_sendall(clt, b'Got:' + data)
                await loop.sock_sendall(clt, data)

    print('Connection closed')

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.create_task(echo_server(('', 54321)))
    loop.run_forever()
