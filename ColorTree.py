from typing import Optional

import cv2
import numpy as np

from BSTColor import BSTColor

BOX_SIZE = 10
VERTICAL_OFFSET = 20

class ColorTreeNode:
    def __init__(self,
                 color:Optional[(BSTColor)] = None,
                 left: Optional[(ColorTreeNode)]= None,
                 right:Optional[(ColorTreeNode)]= None):
        self.value = color
        self.leftNode = left
        self.rightNode = right
        print(f"Just made a node with color: {color}")

    def add(self, color:BSTColor):
        if color.brt < self.value.brt:
            if self.leftNode is None:
                self.leftNode = ColorTreeNode(color = color)
            else:
                self.leftNode.add(color)
        else:
            if self.rightNode is None:
                self.rightNode = ColorTreeNode(color = color)
            else:
                self.rightNode.add(color)

    def drawSelfInBox(self, canvas: np.ndarray, min_x: int, max_x: int, y: int):
        if self.value is None:
            return
        mid_x = (min_x+max_x)//2
        cv2.rectangle(img=canvas,
                      pt1=(mid_x-BOX_SIZE//2,y),
                      pt2=(mid_x+BOX_SIZE//2, y+BOX_SIZE),
                      color=self.value.BGR,
                      thickness=-1)
        if self.leftNode is not None:
            left_mid = (min_x+mid_x)//2
            cv2.line(img=canvas,
                     pt1=(mid_x,y+BOX_SIZE),
                     pt2=(left_mid, y+VERTICAL_OFFSET),
                     color=(255,255,255),
                     thickness=1)
            self.leftNode.drawSelfInBox(canvas=canvas, min_x=min_x, max_x=mid_x, y = y+VERTICAL_OFFSET)
        if self.rightNode is not None:
            right_mid = (mid_x + max_x) // 2
            cv2.line(img=canvas,
                     pt1=(mid_x, y + BOX_SIZE),
                     pt2=(right_mid, y + VERTICAL_OFFSET),
                     color=(255, 255, 255),
                     thickness=1)
            self.leftNode.drawSelfInBox(canvas=canvas, min_x=mid_x, max_x=max_x, y=y + VERTICAL_OFFSET)


class ColorTree:
    def __init__(self):
        self.root = None

    def add(self,color: BSTColor):
        if self.root is None:
            self.root = ColorTreeNode(color = color)
        else:
            self.root.add(color)

    def drawSelf(self, canvas:np.ndarray):
        if self.root is None:
            return
        self.root.drawSelfInBox(canvas, min_x=0, max_x = canvas.shape[1], y=25)

