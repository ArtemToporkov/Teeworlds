import pickle
import sys

from artem_lox_zatichki.entities.bullets import Bullet
from artem_lox_zatichki.entities.player import Player


class ClientHandler:
    def __init__(self, conn, identifier, server):
        self.conn = conn
        self.identifier = identifier
        self.server = server
        self.running = True
        self.team = server.current_team

        # Инициализация данных клиента
        self.conn.send(pickle.dumps((self.identifier, server.map_lines, self.team)))
        if self.team != -1:
            self.server.current_team = (self.server.current_team + 1) % 2

        self.server.entities_to_send[self.identifier] = []

    def handle(self):
        while self.running:
            try:
                # Получение данных от клиента
                data = pickle.loads(self.conn.recv(2048))
                self.process_data(data)

                # Формирование ответа
                reply = self.prepare_reply()
                self.conn.sendall(pickle.dumps(reply))
            except Exception:
                break

        # Закрытие соединения
        self.cleanup()

    def process_data(self, data):
        type = getattr(sys.modules[__name__], data.type)
        if issubclass(type, Player):
            data.id = self.identifier
            self.server.players[self.identifier] = data
        elif issubclass(type, Bullet):
            for player_key in self.server.entities_to_send.keys():
                if player_key != self.identifier:
                    self.server.entities_to_send[player_key].append(data)

    def prepare_reply(self):
        reply = [
            item for key, item in self.server.players.items() if key != self.identifier
        ]
        reply += self.server.entities_to_send[self.identifier]
        self.server.entities_to_send[self.identifier].clear()
        return reply

    def cleanup(self):
        print("Lost connection")
        self.conn.close()
        self.server.players.pop(self.identifier, None)
        self.running = False
