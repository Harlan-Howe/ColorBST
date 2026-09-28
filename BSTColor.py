import random
import numpy as np
import cv2


class BSTColor:

    def __init__(self):
        self.BGR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        one_pixel = np.uint8([[self.BGR]])
        self.HSB = cv2.cvtColor(one_pixel, cv2.COLOR_RGB2HSV)
        self.hue = self.HSB[0][0][0]
        self.sat = self.HSB[0][0][1]
        self.brt = self.HSB[0][0][2]

    def __repr__(self) -> str:
        return f"My BGR is {self.BGR}, which corresponds to {self.hue=} {self.sat=} {self.brt=}"

