import cv2
import numpy as np

class FrameClassifier:
    def __init__(self, interpreter, min_conf_threshold):
        self.interpreter = interpreter
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()
        self.width = input_details[0]['shape'][2]
        self.height = input_details[0]['shape'][1]
        self.index = input_details[0]['index']
        self.bounding_box_tensor_idx = output_details[0]['index']
        self.class_tensor_idx = output_details[1]['index']
        self.confidence_tensor_idx = output_details[2]['index']
        self.min_conf_thresh = min_conf_thresh

    def classify(self, frame):
        img_h = len(frame)
        img_w = len(frame[0])
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (self.width, self.height))
        input_data = np.expand_dims(frame_resized, axis=0)

        self.interpreter.set_tensor(self.index, input_data)
        self.interpreter.invoke()

        boxes = interpreter.get_tensor(output_details[0]['index'])[0] # Bounding box coordinates of detected objects
        classes = interpreter.get_tensor(output_details[1]['index'])[0] # Class index of detected objects
        scores = interpreter.get_tensor(output_details[2]['index'])[0] # Confidence of detected objects

        found = False

        for i in range(len(scores)):
            if ((scores[i] > self.min_conf_threshold) and (scores[i] <= 1.0)):

                found = True

                # Get bounding box coordinates and draw box
                # Interpreter can return coordinates that are outside of image dimensions, need to force them to be within image using max() and min()
                ymin = int(max(1,(boxes[i][0] * self.img_h)))
                xmin = int(max(1,(boxes[i][1] * self.img_w)))
                ymax = int(min(self.img_h,(boxes[i][2] * self.img_h)))
                xmax = int(min(self.img_w,(boxes[i][3] * self.img_w)))
                
                cv2.rectangle(frame, (xmin,ymin), (xmax,ymax), (10, 255, 0), 4)

        return frame, found
