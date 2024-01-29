import asyncio, json
import websockets
from websockets import WebSocketServerProtocol


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server = None
        self.clients = set()
        self.loop = asyncio.get_event_loop()
        self.clients_lock = asyncio.Lock()
        self.captures = set()

# region Public
        
    def run(self):
        self.loop.run_until_complete(self._start())
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            print("Server shutdown requested.")
        finally:
            self.loop.run_until_complete(self._stop())

    def add_capture(self, capture):
        self.captures.add(capture)

        capture.set_on_chat_message(self._receive_chat_message)
        capture.set_on_like_message(self._receive_like_message)
        capture.set_on_member_message(self._receive_member_message)
        capture.set_on_gift_message(self._receive_gift_message)
        capture.set_on_social_message(self._receive_social_message)
        capture.set_on_room_user_seq_message(self._receive_room_user_seq_message)
        capture.set_on_update_fan_ticket_message(self._receive_update_fan_ticket_message)
        capture.set_on_common_text_message(self._receive_common_text_message)
        capture.set_on_product_change_message(self._receive_product_change_message)
        capture.set_on_fansclub_message(self._receive_fansclub_message)
        capture.set_on_control_message(self._receive_control_message)

    def remove_capture(self, capture):
        self.captures.remove(capture)

# endregion

# region Handle 

    async def _start(self):
        self.server = await websockets.serve(self._handler, self.host, self.port)
        print(f"Server started on ws://{self.host}:{self.port}")
        for capture in self.captures:
            await capture.async_start()

    async def _stop(self):
        if self.server:
            for ws in self.clients:
                await ws.close(code=1001, reason='Server shutting down')
            for capture in self.captures:
                capture.stop()

            self.captures.clear()
            self.clients.clear()
            await self.server.close()
            await self.server.wait_closed()
            self.server = None

        self.loop.stop()
        print("Server has been stopped.")

    async def _handler(self, websocket: WebSocketServerProtocol, path: str):
        async with self.clients_lock:
            self.clients.add(websocket)
        print(f"New connection from client at {path}")

        try:
            async for message in websocket:
                pass
        except websockets.ConnectionClosed as e:
            print(f"Connection closed with client at {path}, reason: {e.reason}, code: {e.code}")
        except Exception as e:
            print(f"An error occurred with client at {path}: {e}")
        finally:
            async with self.clients_lock:
                if websocket in self.clients:
                    self.clients.remove(websocket)
            await websocket.close()
            print(f"Connection with client at {path} has been properly closed.")

    async def _send_message(self, websocket: WebSocketServerProtocol, message: str):
        try:
            if not websocket.closed:
                await websocket.send(message)
        except Exception:
            raise
        
    async def _forward_message(self, message: dict):
        if not self.clients:
            return

        async with self.clients_lock:
            clients_copy = self.clients.copy()

        message_str = json.dumps(message)
        tasks = [asyncio.create_task(self._send_message(client, message_str)) for client in clients_copy]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for client, result in zip(clients_copy, results):
            if isinstance(result, Exception):
                print(f"Error sending message to {client.id}: {result}")
            else:
                print(f"Message sent to {client.id}: {message}")

# endregion

# region Receive Messages
    
    def _receive_chat_message(self, message: dict):
        asyncio.ensure_future(self._forward_message(message))
        
    def _receive_like_message(self, message: dict):
        asyncio.ensure_future(self._forward_message(message))

    def _receive_member_message(self, message: dict):
        asyncio.ensure_future(self._forward_message(message))

    def _receive_gift_message(self, message: dict):
        asyncio.ensure_future(self._forward_message(message))

    def _receive_social_message(self, message: dict):
        pass

    def _receive_room_user_seq_message(self, message: dict):
        asyncio.ensure_future(self._forward_message(message))

    def _receive_update_fan_ticket_message(self, message: dict):
        pass

    def _receive_common_text_message(self, message: dict):
        pass

    def _receive_product_change_message(self, message: dict):
        pass

    def _receive_fansclub_message(self, message: dict):
        asyncio.ensure_future(self._forward_message(message))

    def _receive_control_message(self, message: dict):
        pass

# endregion