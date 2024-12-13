import asyncio
import socket
import time
from _thread import *
from os.path import join
from tkinter import filedialog

from game_src.entities.map.map import Map

from web.server_src.client import ClientHandler


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = False
        self.free_id = 0

        self.map = Map()

        self.players = dict()
        self.entities_to_send = dict()
        self.socket = None
        self.clock = None
        self.mode = 0

    async def run(self):
        if self.map is None:
            print('Map is not defined')
            return

        self.running = True
        server = await asyncio.start_server(self.handle_client, self.ip, self.port)
        print(f"Server started on {self.ip}:{self.port}")

        async with server:
            await server.serve_forever()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f"Connected to: {addr}")

        client_handler = ClientHandler(reader, writer, self.free_id, self)
        self.free_id += 1
        await client_handler.handle()

    def stop(self):
        self.running = False
        if self.socket is not None:
            self.socket.close()
