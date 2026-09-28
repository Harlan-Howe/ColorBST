from typing import List

import cv2
import numpy as np

from BSTColor import BSTColor
from ColorTree import ColorTree


class ColorBSTDisplay:
    def __init__(self, t: ColorTree):
        self.colorList  = []
        self.dimensions = (800,1000,3)
        self.tree = t

    def display(self, wait_for_key:bool = True):
        canvas = np.zeros(shape=self.dimensions, dtype=np.uint8)

        self.draw_row_of_boxes_for_list(canvas, self.colorList, 0)

        # if len(self.colorList) > 0:
        #     width_per_box = self.dimensions[1]//len(self.colorList)
        #     for i in range(len(self.colorList)):
        #         cv2.rectangle(img=canvas, pt1=(i*width_per_box,0),pt2=((i+1)*width_per_box,20), color=self.colorList[i].BGR,thickness=-1)
        #         cv2.putText(img=canvas,
        #                     text=self.colorList[i].letter,
        #                     org=(i * width_per_box + 10, 15),
        #                     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #                     fontScale=0.33,
        #                     color=(0, 0, 0))
        self.tree.drawSelf(canvas)

        sorted_colors = []
        self.tree.getColorsInOrder(sorted_colors)

        self.draw_row_of_boxes_for_list(canvas, sorted_colors, 600)


        cv2.imshow("Display", canvas)
        if wait_for_key:
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    def draw_row_of_boxes_for_list(self, canvas: np.ndarray, list_to_draw: List[BSTColor], y:int):
        if len(list_to_draw) > 0:
            width_per_box = self.dimensions[1]//len(list_to_draw)
            for i in range(len(list_to_draw)):
                cv2.rectangle(img=canvas, pt1=(i*width_per_box,y),pt2=((i+1)*width_per_box,y+20), color=list_to_draw[i].BGR,thickness=-1)
                cv2.putText(img=canvas,
                            text=list_to_draw[i].letter,
                            org=(i * width_per_box + 10, y+15),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.33,
                            color=(0, 0, 0))