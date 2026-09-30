import random
import numpy as np
import cv2


class BSTColor:

    def __init__(self):
        self.__BGR = (random.randint(32, 255), random.randint(32, 255), random.randint(32, 255))
        one_pixel = np.uint8([[self.__BGR]]) #  makes a 1 x 1 pixel graphic with the color
        HSB = cv2.cvtColor(one_pixel, cv2.COLOR_RGB2HSV) #  makes a new, equivalent graphic in HSV format
        self.__hue = HSB[0][0][0]  # now poll the pixel at (0,0) (the only pixel there is)
        self.__sat = HSB[0][0][1]
        self.__brt = HSB[0][0][2]

        self.__letter = chr(ord("A") + random.randint(0, 25))
        print (self.__letter)

    @property
    def BGR_color(self):
        return self.__BGR

    @property
    def hue(self):
        return self.__hue

    @property
    def saturation(self):
        return self.__sat

    @property
    def brightness(self):
        return self.__brt

    @property
    def letter(self):
        return self.__letter

    def __repr__(self) -> str:
        return f"My BGR is {self.__BGR}, which corresponds to {self.__hue=} {self.__sat=} {self.__brt=}"

