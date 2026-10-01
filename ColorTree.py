from typing import Optional, List

import cv2
import numpy as np

from BSTColor import BSTColor


class ColorTree:
    def __init__(self):
        self.root: Optional[ColorTreeNode] = None

    def add(self, color: BSTColor):
        if self.root is None:
            self.root = ColorTreeNode(color=color)
            self.root.isSelected = True
        else:
            self.root.add(color)

    def draw_self(self, canvas: np.ndarray):
        if self.root is None:
            return
        self.root.draw_self_in_box(canvas, min_x=0, max_x=canvas.shape[1], y=115)

    def put_colors_in_list_forward(self, list: List[BSTColor]):
        if self.root is not None:
            self.root.get_colors_in_order(list)

    def put_colors_in_list_reversed(self, list: List[BSTColor]):
        if self.root is not None:
            self.root.get_colors_in_reverse_order(list)

    def get_depth(self) -> int:
        if self.root is None:
            return -1
        else:
            return self.root.get_depth() - 1

    def find(self, target: BSTColor) -> bool:
        if self.root is None:
            return False
        return self.root.find(target)

    def remove(self, target: BSTColor) -> bool:
        if self.root is None:
            return False

        return False  # replace this with your code.

# =============================================================================================
# =============================================================================================

BOX_SIZE = 15
VERTICAL_OFFSET = 40

class ColorTreeNode:

    display = None  # a link to the ColorBSTDisplay, so we can reveal updates.

    def __init__(self,
                 color:Optional[(BSTColor)] = None,
                 left: Optional[(ColorTreeNode)]= None,
                 right:Optional[(ColorTreeNode)]= None):
        self.value = color
        self.leftNode = left
        self.rightNode = right
        self.isSelected = False
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

    def draw_self_in_box(self, canvas: np.ndarray, min_x: int, max_x: int, y: int):
        if self.value is None:
            return
        mid_x = (min_x+max_x)//2
        cv2.rectangle(img=canvas,
                      pt1=(mid_x - BOX_SIZE // 2, y),
                      pt2=(mid_x + BOX_SIZE // 2, y + BOX_SIZE),
                      color=self.value.BGR_color,
                      thickness=-1)
        cv2.putText(img=canvas,
                    text=self.value.letter,
                    org = (mid_x-BOX_SIZE//2+4,y+10),
                    fontFace= cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=0.33,
                    color = (0,0,0))
        if self.isSelected:
            cv2.rectangle(img=canvas,
                          pt1=(mid_x - BOX_SIZE // 2-1, y-1),
                          pt2=(mid_x + BOX_SIZE // 2+1, y + BOX_SIZE+1),
                          color=(255,255,255),
                          thickness=2)
        if self.leftNode is not None:
            left_mid = (min_x + mid_x)//2
            cv2.line(img=canvas,
                     pt1=(mid_x,y+BOX_SIZE),
                     pt2=(left_mid, y+VERTICAL_OFFSET),
                     color=(255,255,255),
                     thickness=1)
            self.leftNode.draw_self_in_box(canvas=canvas, min_x=min_x, max_x=mid_x, y =y + VERTICAL_OFFSET)
        if self.rightNode is not None:
            right_mid = (mid_x + max_x) // 2
            cv2.line(img=canvas,
                     pt1=(mid_x, y + BOX_SIZE),
                     pt2=(right_mid, y + VERTICAL_OFFSET),
                     color=(255, 255, 255),
                     thickness=1)
            self.rightNode.draw_self_in_box(canvas=canvas, min_x=mid_x, max_x=max_x, y=y + VERTICAL_OFFSET)

    def get_colors_in_order(self, list:List[BSTColor]):
        if self.value is None:
            return
        if self.leftNode is not None:
            self.leftNode.get_colors_in_order(list)
        list.append(self.value)
        if self.rightNode is not None:
            self.rightNode.get_colors_in_order(list)

    def get_colors_in_reverse_order(self, list:List[BSTColor]):
        if self.value is None:
            return
        if self.rightNode is not None:
            self.rightNode.get_colors_in_reverse_order(list)
        list.append(self.value)
        if self.leftNode is not None:
            self.leftNode.get_colors_in_reverse_order(list)

    def get_depth(self) -> int:
        d=1
        l=0
        r=0
        if self.leftNode is not None:
            l = self.leftNode.get_depth()
        if self.rightNode is not None:
            r = self.rightNode.get_depth()
        return d + max(l, r)

    def find(self, target: BSTColor) -> bool:
        return False



