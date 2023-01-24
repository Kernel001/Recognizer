from channels.consumer import SyncConsumer
import json


class TestConsumer(SyncConsumer):
    def websocket_connect(self, event):
        self.send({"type": "websocket.accept",
                  })
        self.send({"type": "websocket.send",
                   "text": "Hello!"})

    def websocket_receive(self, event):
        print("websocket_receive")
        self.send({"type": "websocket.send",
                   "text": "Hello!"})

    def websocket_disconnect(self, event):
        print("websocket_disconnect")
