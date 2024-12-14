import asyncio
import json
import socket

class Network:
    def __init__(self, ip, port):
        self.addr = (ip, port)
        self.reader = None
        self.writer = None

    async def connect(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(self.addr[0], self.addr[1])
            data_from_server = await self.receive()
            return json.loads(data_from_server)
        except Exception as e:
            print(f"Connection error: {e}")

    async def send(self, data):
        try:
            self.writer.write((json.dumps(data) + '\n').encode('utf-8'))
            # print('send')
            await self.writer.drain()
        except Exception as e:
            print(f"Send error: {e}")

    async def receive(self):
        try:
            data = await self.reader.read(2048)
            return data.decode('utf-8')
        except Exception as e:
            print(f"Receive error: {e}")
