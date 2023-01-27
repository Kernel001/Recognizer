import cv2
import numpy as np
from django.contrib.staticfiles import finders

class RecoUtils():
    def __init__(self):
        print("Creating RecoUtils")

        self.detector = cv2.FaceDetectorYN.create(finders.find('app/ainet/face_detection_yunet_2022mar.onnx'),
                                                  "", (1024, 768), 0.9, 0.3, 5000)
        self.recognizer = cv2.FaceRecognizerSF.create(finders.find('app/ainet/face_recognition_sface_2021dec.onnx'), "")

    def getImageFromByte(self, inbytes, tag):
        nparr = np.frombuffer(inbytes, dtype=np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img = cv2.GaussianBlur(img, (7, 7), 0)

        box = self.getDetectedFace(img)
        feature = self.getRecoVector(img, box)

        cv2.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 1)
        cv2.putText(img, tag, (box[0], box[1]+20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        retImg = cv2.imencode(".jpg", img)[1]
        return retImg
    def getDetectedFace(self, image):
        imgWidth = int(image.shape[1])
        imgHeight = int(image.shape[0])

        self.detector.setInputSize((imgWidth, imgHeight))
        faces = self.detector.detect(image)
        if faces[1] is not None:
            for idx, face in enumerate(faces[1]):
                coords = face[:-1].astype(np.int32)
                if coords[0] < 0 or coords[1] < 0:  # Странная херь, но кооординаты рожи иногда отрицательные бывают...
                    break
                return coords
        return None
    def getRecoVector(self, image, box=None):
        if box is None:
            box = self.getDetectedFace(image)
        roi_img = image[box[1]: box[1] + box[3], box[0]: box[0] + box[2]]
        feature = self.recognizer.feature(roi_img)

    def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
        dim = None
        (h, w) = image.shape[:2]
        if width is None and height is None:
            return image

        if width is None:
            r = height / float(h)
            dim = (int(w * r), height)
        else:
            r = width / float(w)
            dim = (width, int(h * r))

        resized = cv2.resize(image, dim, interpolation = inter)
        return resized