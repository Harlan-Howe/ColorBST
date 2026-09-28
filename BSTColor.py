import random
import numpy as np
import cv2


class BSTColor:

    def __init__(self):
        self.BGR = (random.randint(32, 255), random.randint(32, 255), random.randint(32, 255))
        one_pixel = np.uint8([[self.BGR]]) #  makes a 1 x 1 pixel graphic with the color
        self.HSB = cv2.cvtColor(one_pixel, cv2.COLOR_RGB2HSV) #  makes a new, equivalent graphic in HSV format
        self.hue = self.HSB[0][0][0]  # now poll the pixel at (0,0) (the only pixel there is)
        self.sat = self.HSB[0][0][1]
        self.brt = self.HSB[0][0][2]

        self.letter = chr(ord("A")+random.randint(0,25))
        print (self.letter)

    def __repr__(self) -> str:
        return f"My BGR is {self.BGR}, which corresponds to {self.hue=} {self.sat=} {self.brt=}"

