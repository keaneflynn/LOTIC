import cv2
from queue import Queue, Empty
from time import time

class VideoInput:
    def __init__(self, filename="", vid_dev_no=0):
        if filename != "":
            self.vid = cv2.VideoCapture(filename)
            self.is_live = False
        else:
            self.vid = cv2.VideoCapture(vid_dev_no)
            self.is_live = True
        
        self.__queue = Queue(10000)

    def start(self):
        numread = 0
        while True:
            ok, frame = self.vid.read()
            if not ok:
                return
            numread += 1
            self.__queue.put(frame)

    def read(self):
        try:
            frame = self.__queue.get(timeout=3)
        except Empty:
            frame = None
        return frame

    def get_dims(self):
        return int(self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)), int(self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def get_frame_rate(self):
        return self.vid.get(cv2.CAP_PROP_FPS)

    def stop_vid(self, a, b):
        self.vid.release()

