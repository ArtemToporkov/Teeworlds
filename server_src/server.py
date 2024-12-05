import socket
import time
from _thread import *
from os.path import join
from tkinter import filedialog

from artem_lox_zatichki.map.map import Map

from server_src.client import ClientHandler
from server_src.events_on_map import BuffSpawner, EventGenerator


class Server:
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.running = False
        self.free_id = 0

        self.map_lines = None
        self.map = Map()

        self.players = dict()
        self.entities_to_send = dict()  # key - to whom player
        self.socket = None
        self.clock = None
        self.current_team = -1
        self.mode = 0

        self.buff_spawner = BuffSpawner(self.map, self.entities_to_send)
        self.event_generator = EventGenerator(self.entities_to_send)

    def run(self):
        if self.map_lines is None:
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
        start_new_thread(self.buff_spawner.spawn_buffs, ())
        start_new_thread(self.event_generator.start_event, ())
        # server_status.config(text="Server is running")
        while self.running:
            try:
                conn, addr = self.socket.accept()
                print("Connected to:", addr)
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

    def select_map(self):
        file_path = filedialog.askopenfilename(
            initialdir=join("assets", "maps"), filetypes=(("TXT files", "*.txt"),)
        )
        with open(file_path, "r") as f:
            self.map_lines = f.readlines()
        self.map.load_from_list(self.map_lines, w_sprites=False)

