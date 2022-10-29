from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image

class Camera:
    def __init__(self):
        # use pi camera
        self.camera = PiCamera()
        self.camera.resolution = (2560, 1920)

    def capture(self):
        raw_capture = PiRGBArray(self.camera)
        self.camera.capture(raw_capture, format="rgb")
        frame = raw_capture.array

        return Image.fromarray(frame) # pillow image