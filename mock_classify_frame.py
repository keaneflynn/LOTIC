from time import time

class MockFrameClassifier:
    def __init__(self):
        self.start_time = time()
    def classify(self, frame):
        if int((time() - self.start_time) / 10) % 2 == 0:
            return frame.copy(), True
        return frame, False
