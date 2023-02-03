import concurrent

from channels.consumer import SyncConsumer
from django.shortcuts import render
import json
import base64
from .camera import VideoCamera
from .models import Source, Target


# rtsp://admin:Bxe7nNa0@192.168.30.253:7070/stream1 проходная
# rtsp://admin:Bxe7nNa0@192.168.30.223:7070/stream1 коридор на 2 этаж

class TestConsumer(SyncConsumer):
    def __init__(self):
        print("Creating Test Consumer")
        super().__init__()
        self.source = VideoCamera()

    def websocket_connect(self, event):
        print("websocket_connect")
        self.send({"type": "websocket.accept"})

    # IN {type: ... text:...}
    def websocket_receive(self, event):
        jsonStr = json.loads(event['text'])
        print("Operation: {}".format(jsonStr['oper']))
        if jsonStr['oper'] == "source.add":
            newSource = Source.objects.create(ip_adress=jsonStr['data']['ipAdress'],
                                              video_feed_name=jsonStr['data']['feedName'],
                                              name=jsonStr['data']['descr'])
            newSource.save()

        if jsonStr['oper'] == "target.add":
            decoded = base64.decodebytes(jsonStr['data']['target_photo'].encode('ascii'))
            processedImg = self.source.ai.getImageFromByte(decoded, jsonStr['data']['target_name'])
            vector = self.source.ai.getRecoVector(decoded)

            newTarget = Target.objects.create(target_name=jsonStr['data']['target_name'],
                                              target_photo=base64.b64encode(decoded),
                                              target_recognizer_photo=base64.b64encode(processedImg),
                                              targer_reco_vector=vector)
            newTarget.save()
        if jsonStr['oper'] == "stream.start":
            source = Source.objects.get(id=jsonStr['data']['sourceID'])
            print("Source is: {}".format(source))
            self.source.startStream(source.ip_adress, source.video_feed_name, self.framecallback)

        if jsonStr['oper'] == "stream.stop":
            self.source.stopStream()

    def websocket_disconnect(self, event):
        print("websocket_disconnect")
        self.source.stopStream()

    def framecallback(self, data):
        self.send({"type": "websocket.send",
                   "bytes": bytes(data['data'])})
