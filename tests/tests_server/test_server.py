import unittest
from unittest.mock import MagicMock, patch
from game_src.entities.guns.bullets import BlowingBullet
from game_src.entities.map.map import Map
from geometry.vector import Vector
from web.server_src.event_generator import EventGenerator
from web.server_src.server import Server
import asyncio


class TestServer(unittest.IsolatedAsyncioTestCase):
    @patch('web.server_src.server.Map.load_from_file')
    def setUp(self, a):
        self.ip = "127.0.0.1"
        a.return_value = Map.load_from_file('../maps/first level.json')
        self.port = 8000
        self.server = Server(self.ip, self.port)

    @patch("web.server_src.event_generator.EventGenerator.start_event")
    @patch("asyncio.start_server")
    async def test_run(self, mock_start_server, mock_start_event):
        mock_server_instance = MagicMock()
        mock_start_server.return_value = mock_server_instance
        mock_start_event.serve_forever = None

        self.server.map = MagicMock()

        try:
            await self.server.run()
        except Exception:
            pass

        self.assertTrue(self.server.running)
        mock_start_event.assert_not_called()
        mock_start_server.assert_called_once_with(self.server.handle_client, self.ip, self.port)
        print("Server started test passed")

    @patch("web.server_src.server.ClientHandler")
    async def test_handle_client(self, mock_client_handler):
        # Проверяем обработку подключения клиента
        reader = MagicMock()
        writer = MagicMock()

        mock_handler_instance = MagicMock()
        mock_client_handler.return_value = mock_handler_instance

        try:
            await self.server.handle_client(reader, writer)
        except Exception:
            pass

        mock_client_handler.assert_called_once_with(reader, writer, self.server.free_id - 1, self.server)
        mock_handler_instance.handle.assert_called_once()
        print("Handle client test passed")

    @patch("socket.socket")
    def test_stop(self, mock_socket):
        # Проверяем остановку сервера
        self.server.socket = mock_socket
        self.server.stop()

        self.assertFalse(self.server.running)
        mock_socket.close.assert_called_once()
        print("Server stop test passed")


if __name__ == "__main__":
    unittest.main()