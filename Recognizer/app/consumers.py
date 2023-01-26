from channels.consumer import SyncConsumer
from django.shortcuts import render
import json
from .models import Source

class TestConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("websocket_connect")
        self.send({"type": "websocket.accept"})

        self.send({"type": "websocket.send",
                   "text": "Hello!"})

    # IN {type: ... text:...}
    def websocket_receive(self, event):
        jsonStr = json.loads(event['text'])
        print(jsonStr)
        if jsonStr['oper'] == "source.add":
            newSource = Source.objects.create(ip_adress=jsonStr['data']['ipAdress'],
                                              video_feed_name=jsonStr['data']['feedName'],
                                              name=jsonStr['data']['descr'])
            newSource.save()

    def websocket_disconnect(self, event):
        print("websocket_disconnect")
