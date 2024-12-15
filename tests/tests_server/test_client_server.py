import asyncio
import json
import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from game_src.entities.guns.bullets import Bullet
from game_src.entities.player import Player
from web.server_src.client import ClientHandler


class TestClientHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.reader = AsyncMock()
        self.writer = AsyncMock()
        self.server = MagicMock()
        self.server.map.to_dict.return_value = {"test": "map_data"}
        self.server.entities_to_send = {}
        self.server.players = {}
        self.identifier = 1
        self.client_handler = ClientHandler(self.reader, self.writer, self.identifier, self.server)

    async def test_send_initial_data(self):
        await self.client_handler.send_initial_data()

        self.writer.write.assert_called_once_with(json.dumps({
            "id": self.client_handler.identifier,
            "map": self.server.map.to_dict()
        }).encode('utf-8'))
        self.writer.drain.assert_called_once()

    async def test_read_from_client(self):
        self.reader.read.return_value = b'{"key": "value"}\n'

        data = await self.client_handler.read_from_client()

        self.assertIsNotNone(data)
        data_list = list(data)
        self.assertEqual(len(data_list), 1)
        self.assertEqual(data_list[0], {"key": "value"})

    async def test_read_from_client_empty_data(self):
        self.reader.read.return_value = b''

        data = await self.client_handler.read_from_client()

        self.assertIsNone(data)
        self.assertFalse(self.client_handler.running)

    async def test_send_to_client(self):
        reply = {"response": "test"}
        await self.client_handler.send_to_client(reply)

        self.writer.write.assert_called_once_with(json.dumps(reply).encode('utf-8'))
        self.writer.drain.assert_called_once()

    def test_process_data_player(self):
        data = {"type_entity": "Player", "name": "TestPlayer"}
        with patch('game_src.utils.serialization_tools.get_entity_type', return_value=Player):
            self.client_handler.process_data(data)

        self.assertEqual(self.server.players[self.client_handler.identifier], {
            "type_entity": "Player",
            "name": "TestPlayer",
            "id": self.client_handler.identifier
        })

    def test_prepare_reply(self):
        self.server.players = {1: {"type": "Player1"}, 2: {"type": "Player2"}}
        self.server.entities_to_send = {1: [{"type": "Bullet"}], 2: []}

        reply = self.client_handler.prepare_reply()

        self.assertEqual(reply, [{"type": "Player2"}, {"type": "Bullet"}])
        self.assertEqual(self.server.entities_to_send[1], [])

    async def test_cleanup(self):
        self.server.players = {1: {"type": "Player"}}

        try:
            await self.client_handler.cleanup()
        except Exception:
            pass
        self.writer.close.assert_called_once()
        self.assertNotIn(1, self.server.players)
        self.assertFalse(self.client_handler.running)


if __name__ == "__main__":
    unittest.main()
