from typing import Optional, List

import cv2
import numpy as np

from BSTColor import BSTColor

BOX_SIZE = 15
VERTICAL_OFFSET = 40

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
        if color.hue < self.value.hue:
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
        cv2.putText(img=canvas,
                    text=self.value.letter,
                    org = (mid_x-BOX_SIZE//2+4,y+10),
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.33,
                    color = (0,0,0))
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
            self.rightNode.drawSelfInBox(canvas=canvas, min_x=mid_x, max_x=max_x, y=y + VERTICAL_OFFSET)

    def getColorsInOrder(self, list:List[BSTColor]):
        if self.leftNode is not None:
            self.leftNode.getColorsInOrder(list)
        list.append(self.value)
        if self.rightNode is not None:
            self.rightNode.getColorsInOrder(list)

class ColorTree:
    def __init__(self):
        self.root : Optional[ColorTreeNode] = None

    def add(self,color: BSTColor):
        if self.root is None:
            self.root = ColorTreeNode(color = color)
        else:
            self.root.add(color)

    def drawSelf(self, canvas:np.ndarray):
        if self.root is None:
            return
        self.root.drawSelfInBox(canvas, min_x=0, max_x = canvas.shape[1], y=25)

    def getColorsInOrder(self, list:List[BSTColor]):
        if self.root is not None:
            self.root.getColorsInOrder(list)
