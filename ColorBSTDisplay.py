import cv2
import numpy as np

from ColorTree import ColorTree


class ColorBSTDisplay:
    def __init__(self, t: ColorTree):
        self.colorList  = []
        self.dimensions = (800,800,3)
        self.tree = t

    def display(self):
        canvas = np.zeros(shape=self.dimensions, dtype=np.uint8)

        if len(self.colorList) > 0:
            widthPerBox = self.dimensions[1]//len(self.colorList)
            for i in range(len(self.colorList)):
                cv2.rectangle(img=canvas, pt1=(i*widthPerBox,0),pt2=((i+1)*widthPerBox,10), color=self.colorList[i].BGR,thickness=-1)

        self.tree.drawSelf(canvas)

        cv2.imshow("Display", canvas)
        cv2.waitKey(0)
        cv2.destroyAllWindows()