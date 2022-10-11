import websocket

class ClientSocketManager:
    WS_PIVOT_LEVEL_SCANNER = "ws://127.0.0.1:8002"
    WS_VOLUME_SCANNER = "ws://127.0.0.1:8003"

    def __init__(self):
        self.ws = websocket.WebSocket()

    def connect(self, url):
        self.ws.connect(url)

    def send(self, data):
        self.ws.send(data)