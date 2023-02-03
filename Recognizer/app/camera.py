import cv2
import av
import time
from .RecoCore import RecoUtils


class VideoCamera(object):
    def __init__(self):
        self.video = None
        self.streaming = False
        self.ai = RecoUtils()
        print('camera created')

    def __del__(self):
        if self.video is not None:
            self.video.release()
        print('camera destroyed')

    # input example
    # rtsp://admin:Bxe7nNa0@192.168.30.253:7070/stream1 проходная
    # rtsp://admin:Bxe7nNa0@192.168.30.223:7070/stream1 коридор на 2 этаж
    def startStream(self, source, stream, frameCallback):
        print("Stream start: {addr} {chName}".format(addr=source, chName=stream))
        # self.video = cv2.VideoCapture("rtsp://admin:Bxe7nNa0@{addr}:7070/{chName}".format(addr=source, chName=stream))
        dicOption = {'buffer_size': '1024000', 'rtsp_transport': 'tcp', 'stimeout': '20000000', 'max_delay': '300000'}
        self.video = av.open("rtsp://admin:Bxe7nNa0@{addr}:7070/{chName}".format(addr=source, chName=stream), 'r',
                             format=None, options=dicOption, metadata_errors='strict')
        self.video.streams.video[0].thread_type = "AUTO"
        print(self.video.dumps_format())
        self.streaming = True
        self.callback = frameCallback
        index = 0
        perfCount = {'getFrame': 0, 'faceDetect': 0, 'vectorCalc': 0, 'imProcess': 0, 'send': 0}
        lastFrameTime = 0
        try:
            for frame in self.video.decode():
                perfCount['getFrame'] = time.perf_counter() - lastFrameTime
                if not self.streaming:
                    break
                index += 1
                image = frame.to_ndarray(format='bgr24')
                st_time = time.perf_counter()
                faces = self.ai.getDetectedFace(image)
                perfCount['faceDetect'] = time.perf_counter() - st_time
                if faces is not None:
                    st_time = time.perf_counter()
                    vector = self.ai.getRecoVector(image, faces)
                    perfCount['vectorCalc'] = time.perf_counter() - st_time
                image = self.ai.drawFaceRect(image, faces, perfData=perfCount)

                st_time = time.perf_counter()
                image = self.ai.image_resize(image, width=800)
                ret, jpeg = cv2.imencode('.jpg', image)
                perfCount['imProcess'] = time.perf_counter() - st_time

                st_time = time.perf_counter()
                self.callback({'type': 'original', 'data': jpeg})
                perfCount['send'] = time.perf_counter() - st_time
                lastFrameTime = time.perf_counter()
                # TODO we need to async sleep here!
        except Exception as ex:
            print(ex)
            self.streaming = False

            # success, image = self.video.read()
            # if success:
            #     faces = self.ai.getDetectedFace(image)
            #     if faces is not None:
            #         vector = self.ai.getRecoVector(image, faces)
            #         image = self.ai.drawFaceRect(image, faces)
            #     image = self.ai.image_resize(image, width=800)
            #     ret, jpeg = cv2.imencode('.jpg', image)
            #     self.callback({'type': 'original', 'data': jpeg})
            # else:
            #     break

    def stopStream(self):
        print("Stream stop")
        self.streaming = False
        self.callback = None
        if self.video is not None:
            if self.video.isOpened():
                self.video.release()
