import asyncio
import json
from game_src.entities.guns.bullets import Bullet
from game_src.entities.player import Player
from game_src.utils.enums import TypeData
from game_src.utils.serialization_tools import get_entity_type


class ClientHandler:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, identifier, server):
        self.reader = reader
        self.writer = writer
        self.identifier = identifier
        self.server = server
        self.running = True
        self.server.entities_to_send[self.identifier] = []

    async def handle(self):
        try:
            await self.send_initial_data()

            while self.running:
                # Чтение данных от клиента
                data = await self.read_from_client()
                if data:
                    for message in data:
                        self.process_data(message)

                reply = self.prepare_reply()
                await self.send_to_client(reply)
        except Exception as e:
            print(f"Error handling client {self.identifier}: {e}")
        finally:
            self.cleanup()

    async def send_initial_data(self):
        initial_data = json.dumps({
            "id": self.identifier,
            "map": self.server.map.to_dict()
        }).encode('utf-8')
        self.writer.write(initial_data)
        await self.writer.drain()

    async def read_from_client(self):
        try:
            data = await self.reader.read(2048)
            if not data:
                self.running = False
                return None
            data = data.decode('utf-8').strip().split('\n')
            return map(json.loads, data)
        except Exception as e:
            print(f"Error reading from client {self.identifier}: {e}")
            self.running = False
            return None

    async def send_to_client(self, reply):
        try:
            self.writer.write(json.dumps(reply).encode('utf-8'))
            await self.writer.drain()
        except Exception as e:
            print(f"Error sending to client {self.identifier}: {e}")
            self.running = False

    def process_data(self, data):
        type_entity = get_entity_type(data)
        if issubclass(type_entity, Player):
            data['id'] = self.identifier
            self.server.players[self.identifier] = data
        elif issubclass(type_entity, Bullet):
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
        print(f"Lost connection with client {self.identifier}")
        self.writer.close()
        asyncio.create_task(self.writer.wait_closed())
        self.server.players.pop(self.identifier, None)
        self.running = False
