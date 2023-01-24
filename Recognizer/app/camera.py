import cv2


class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        print('camera created')

    def __del__(self):
        self.video.release()
        print('camera destroyed')

    def getFrame(self):
        success, image = self.video.read()
        image = cv2.resize(image, (640, 480), interpolation=cv2.INTER_LINEAR)
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()
