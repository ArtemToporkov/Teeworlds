import asyncio
import json
import time
from game_src.entities.guns.bullets import Bullet
from game_src.entities.player import Player
from game_src.utils.serialization_tools import get_entity_type


class ClientHandler:
    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, identifier, server):
        self.reader = reader
        self.writer = writer
        self.identifier = identifier
        self.server = server
        self.running = True
        self.input_queue = asyncio.Queue()  # Очередь для входящих сообщений
        self.output_queue = asyncio.Queue()  # Очередь для исходящих сообщений
        self.server.entities_to_send[self.identifier] = []

    async def handle(self):
        try:
            await self.send_initial_data()

            receive_task = asyncio.create_task(self.receive_loop())
            process_task = asyncio.create_task(self.process_loop())
            send_task = asyncio.create_task(self.send_loop())

            await asyncio.gather(receive_task, process_task, send_task)
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

    async def receive_loop(self):
        """Постоянно принимает данные от клиента и кладёт их в очередь."""
        try:
            while self.running:
                data = await self.reader.read(2048)
                if not data:
                    self.running = False
                    break
                messages = data.decode('utf-8').strip().split('\n')
                for message in messages:
                    await self.input_queue.put(json.loads(message))
        except Exception as e:
            print(f"Error reading from client {self.identifier}: {e}")
            self.running = False

    async def process_loop(self):
        """Обрабатывает данные из очереди input_queue."""
        while self.running:
            try:
                data = await self.input_queue.get()
                self.process_data(data)
            except Exception as e:
                print(f"Error processing data for client {self.identifier}: {e}")

    async def send_loop(self):
        """Готовит и отправляет данные клиенту."""
        while self.running:
            try:
                # Подготавливаем ответ
                reply = [
                    item for key, item in self.server.players.items() if key != self.identifier
                ]
                reply += self.server.entities_to_send[self.identifier]
                if reply:
                    self.server.entities_to_send[self.identifier].clear()
                    print(reply)

                    # Кладём ответ в очередь
                    await self.output_queue.put(reply)

                # Отправляем данные из output_queue
                data_to_send = await self.output_queue.get()
                if data_to_send:
                    print(data_to_send)
                    self.writer.write(json.dumps(data_to_send).encode('utf-8') + b'\n')
                    await self.writer.drain()
            except Exception as e:
                print(f"Error sending to client {self.identifier}: {e}")
                self.running = False

    def process_data(self, data):
        """Обрабатывает сообщение от клиента."""
        type_entity = get_entity_type(data)
        if issubclass(type_entity, Player):
            data['id'] = self.identifier
            self.server.players[self.identifier] = data
        elif issubclass(type_entity, Bullet):
            for player_key in self.server.entities_to_send.keys():
                if player_key != self.identifier:
                    self.server.entities_to_send[player_key].append(data)

    def cleanup(self):
        """Освобождает ресурсы при завершении работы."""
        print(f"Lost connection with client {self.identifier}")
        self.writer.close()
        asyncio.create_task(self.writer.wait_closed())
        self.server.players.pop(self.identifier, None)
        self.running = False
