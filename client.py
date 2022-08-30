import asyncio
import random
import logging


class Client(asyncio.Protocol):

    def __init__(self):
        self.request_counter = 0
        self.client_tcp_timeout = None

    def connection_made(self, transport):
        self.timeout = random.uniform(0.03, 3.0)
        print('Connected to Server.')
        self.transport = transport
        self.client_tcp_timeout = loop.call_later(
            self.timeout, self.send_from_call_later)

    def data_received(self, data):
        self.data = format(data.decode())
        print(data.decode())

    def send_from_call_later(self):
        self.msg = "[{}] PING".format(self.request_counter).encode()
        self.transport.write(self.msg)
        self.timeout = random.uniform(0.03, 3.0)
        self.request_counter += 1
        self.client_tcp_timeout = loop.call_later(
            self.timeout, self.send_from_call_later)

    def connection_lost(self, exc):
        print('Connection lost!!!!!!.')


loop = asyncio.get_event_loop()

coro = loop.create_connection(Client, 'localhost', 8000)
client = loop.run_until_complete(coro)

loop.run_forever()
