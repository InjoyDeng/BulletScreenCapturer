import  websocket

class TestClient:
    def start(self):
        ws = websocket.WebSocketApp("ws://127.0.0.1:12321",
                        on_open=self._ws_on_open,
                        on_message=self._ws_on_message,
                        on_error=self._ws_on_error,
                        on_close=self._ws_on_close)
        try:
            ws.run_forever()
        except Exception:
            self.stop()
            raise

    def _ws_on_open(self, ws):
        print("WebSocket connection opened")

    def _ws_on_message(self, ws, message):
        print("Received message:", message)

    def _ws_on_error(self, ws, error):
        print("WebSocket error:", error)

    def _ws_on_close(self, ws):
        print("WebSocket connection closed")


if __name__ == "__main__":
    client = TestClient()
    client.start()