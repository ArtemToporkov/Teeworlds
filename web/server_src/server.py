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
        self.current_team = -1
        self.mode = 0

    def run(self):
        if self.map is None:
            print('Map is not define')
            return
        self.clock = time.time()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            str(e)
        self.socket.listen(2)
        print("Waiting for a connection, Server Started")

        self.running = True
        # start_new_thread(self.buff_spawner.spawn_buffs, ())
        # start_new_thread(self.event_generator.start_event, ())
        # server_status.config(text="Server is running")
        while self.running:
            try:
                conn, addr = self.socket.accept()  # получаем сокет через который можно общаться с новым клиентом
                print("Connected to:", addr)
                # free_id - будущий id игрока
                client_handler = ClientHandler(conn, self.free_id, self)
                self.free_id += 1
                start_new_thread(client_handler.handle, ())
            except socket.error:
                pass
        print("Server stopped")
        # server_status.config(text="Server is not running")
        self.free_id = 0
        self.players = dict()
        self.entities_to_send = dict()

    def stop(self):
        self.running = False
        if self.socket is not None:
            self.socket.close()
