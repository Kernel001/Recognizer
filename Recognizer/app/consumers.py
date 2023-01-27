from channels.consumer import SyncConsumer
from django.shortcuts import render
import json
import base64
from .RecoCore import RecoUtils
from .models import Source, Target

class TestConsumer(SyncConsumer):
    def __init__(self):
        print("Creating Test Consumer")
        super().__init__()
        self.cvutil = RecoUtils()

    def websocket_connect(self, event):
        print("websocket_connect")
        self.send({"type": "websocket.accept"})

        self.send({"type": "websocket.send",
                   "text": "Hello!"})

    # IN {type: ... text:...}
    def websocket_receive(self, event):
        jsonStr = json.loads(event['text'])
        if jsonStr['oper'] == "source.add":
            newSource = Source.objects.create(ip_adress=jsonStr['data']['ipAdress'],
                                              video_feed_name=jsonStr['data']['feedName'],
                                              name=jsonStr['data']['descr'])
            newSource.save()

        if jsonStr['oper'] == "target.add":
            decoded = base64.decodebytes(jsonStr['data']['target_photo'].encode('ascii'))
            processedImg = self.cvutil.getImageFromByte(decoded, jsonStr['data']['target_name'])

            newTarget = Target.objects.create(target_name = jsonStr['data']['target_name'],
                                              target_photo = base64.b64encode(decoded),
                                              target_recognizer_photo = base64.b64encode(processedImg))
            newTarget.save()

    def websocket_disconnect(self, event):
        print("websocket_disconnect")

