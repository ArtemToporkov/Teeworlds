import pickle
import sys

from game_src.entities.guns.bullets import Bullet
from game_src.entities.player import Player
from game_src.utils.enums import TypeData
from game_src.utils.serialization_tools import get_entity_type, get_entity


class ClientHandler:
    def __init__(self, conn, identifier, server):
        self.conn = conn
        self.identifier = identifier
        self.server = server
        self.running = True
        self.team = server.current_team

        # Инициализация данных клиента
        self.conn.send(pickle.dumps((self.identifier, self.server.map.to_dict())))
        if self.team != -1:
            self.server.current_team = (self.server.current_team + 1) % 2

        self.server.entities_to_send[self.identifier] = []

    def handle(self):
        while self.running:
            try:
                # Данные от пользователя
                data = pickle.loads(self.conn.recv(2048))
                self.process_data(data)

                # Данные от сервера пользователю (от других пользователей)
                reply = self.prepare_reply()
                self.conn.sendall(pickle.dumps(reply))
            except Exception:
                break

        self.cleanup()

    def process_data(self, data):
        # type_entity = getattr(sys.modules[__name__], data[TypeData.TYPE.value])
        type_entity = get_entity_type(data)
        if issubclass(type_entity, Player):
            data['id'] = self.identifier
            self.server.players[self.identifier] = data
        elif issubclass(type_entity, Bullet):
            for player_key in self.server.entities_to_send.keys():
                if player_key != self.identifier:
                    self.server.entities_to_send[player_key].append(data)
                    print('add_bullets')

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
