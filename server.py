import asyncio
import random
import time
import logging
import re


class Server(asyncio.Protocol):

    connection_list = []

    def __init__(self):
        self.response_counter = 0
        self.server_tcp_timeout = None

    def connection_made(self, transport):
        self.peername = transport.get_extra_info('peername')
        print('connection from {}'.format(self.peername))
        self.connection_list.append(self.peername)
        self.transport = transport
        # asyncio.create_task(self.keep_alive_message())

    def data_received(self, data):
        self.msg = data.decode()
        print(self.msg)
        self.need_to_ans = random.randint(1, 10)
        if self.need_to_ans < 10:
            self.make_response(self.msg)
        else:
            print("IGNORED")

    def make_response(self, message):
        self.timeout = random.uniform(0.01, 1.0)
        time.sleep(self.timeout)
        self.request_num = re.findall(r"\[\s*\+?(-?\d+)\s*\]", message)
        self.ans = "[{}/{}] PONG ({})".format(
            self.response_counter, self.request_num[0], self.client_number()).encode()
        self.transport.write(self.ans)
        self.response_counter += 1

    def client_number(self):
        self.client_num = None
        for clients in self.connection_list:
            if clients[1] == self.transport.get_extra_info("peername")[1]:
                self.client_num = self.connection_list.index(clients) + 1
        return self.client_num

    async def keep_alive_message(self):
        self.keep = "[{}] KEEPALIVE".format(self.connection_list[0]).encode()
        self.transport.write(self.keep)
        await asyncio.sleep(5.0)
        self.server_tcp_timeout = loop.call_later(
            self.timeout, self.keep_alive_message)


loop = asyncio.get_event_loop()
coro = loop.create_server(Server, 'localhost', 8000)
server = loop.run_until_complete(coro)

print('serving on {}'.format(server.sockets[0].getsockname()))

try:
    loop.run_forever()
except KeyboardInterrupt:
    print("exit")
finally:
    server.close()
    loop.close()
