from typing import Optional, List

import cv2
import numpy as np

from BSTColor import BSTColor

"""
Note: this file contains two classes, ColorTree and ColorTreeNode.
"""
class ColorTree:
    def __init__(self):
        self.root: Optional[ColorTreeNode] = None

    def add(self, color: BSTColor) -> None:
        """
        adds a new node with the given color to the tree.
        :param color: the BSTColor item to add
        """
        #  I have written this method for you, but you will need to write the content of ColorTreeNode.add().
        if self.root is None:
            self.root = ColorTreeNode(color=color)
            self.root.isSelected = True
        else:
            self.root.add(color)

    def isEmpty(self) -> bool:
        return self.root is None

    def draw_self(self, canvas: np.ndarray) -> None:
        """
        Draws a representation of the tree in the canvas
        :param canvas: the 2d x 3color ndarray in which to draw.
        """
        # I have written this method for you.
        if self.root is None:
            return
        self.root.draw_self_in_box(canvas, min_x=0, max_x=canvas.shape[1], y=115)

    def put_colors_in_list_forward(self, list: List[BSTColor]) -> None:
        """
        fills the given list with the contents of this tree in least -> greatest order.
        :param list: a list in which to put the BSTColors held by this tree.
        """
        # I have written this method for you, but it relies on ColorTreeNode.get_colors_in_order(), which you will need
        # to complete.
        if self.root is not None:
            self.root.get_colors_in_order(list)

    def put_colors_in_list_reversed(self, list: List[BSTColor]) -> None:
        """
        fills the given list with the contents of this tree in greatest -> least order.
        :param list: a list in which to put the BSTColors held by this tree.
        """
        # I have written this method for you, but it relies on ColorTreeNode.get_colors_in_reverse_order(), which you
        # will need to complete.
        if self.root is not None:
            self.root.get_colors_in_reverse_order(list)

    def get_depth(self) -> int:
        """
        calculates the max depth of this tree.
        :return: the depth
        """
        # I have written this method, but it is based on ColorTreeNode.get_depth(), which you will need to complete.
        #   Note that I am subtracting one from the returned value, so that the root will be at depth 0.
        if self.root is None:
            return -1
        else:
            return self.root.get_depth() - 1

    def contains(self, target: BSTColor) -> bool:
        """
        deterimines whether the "target" BSTColor object is contained in this tree.
        :param target: the BSTColor we are looking for.
        :return: whether the given target color is part of this tree.
        """
        # I have written this method for you, but it relies on ColorTreeNode.contains(), which you will need to complete.
        if self.root is None:
            return False
        return self.root.contains(target)

    def remove(self, target: BSTColor) -> bool:
        """
        Removes the given target BSTColor from this tree, if it is contained in it.
        :param target: the BSTColor object to remove.
        :return: whether we were able to remove the target color; if True, the number of items in this tree should have
                 decreased by one.
        """
        if self.root is None:
            return False
        # TODO (after all others): you need to write this method.

        # this is probably the hardest method to write - please see the GoogleDoc instructions for what needs to happen.

        return False  # replace this with your code.

    def size(self) -> int:
        """
        :return: the number of BSTColors in this tree.
        """
        #  I have written this method for you.
        if self.root is None:
            return 0
        return self.root.size()

    def clear_all_selections(self):
        """
        turns off "isSelected" for all nodes in this tree.
        """
        #  I have written this method for you.
        if self.root is None:
            return
        self.root.clear_all_selections()

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

    def add(self, color:BSTColor) -> None:
        """
        adds the given BSTColor to the (sub?)tree rooted by this node.
        :param color: the BSTColor object to add
        """

        if self.value is None:
            raise Exception("Something went wrong... this node has no color.")
        # TODO # 0: You need to write this!

        #  The assumption is that if you are here, this node already has a color, so you need to either tell a subtree
        #  to add this, or create a child with this color. To start with, you'll need one of the following, depending
        #  on what you want to sort by:

        # if color.hue < self.value.hue:  # Recommended
        # or
        # if color.letter < self.value.letter:
        # or
        # if color.brightness < self.value.brightness:
        # or
        # if color.saturation < self.value.saturation:

    def draw_self_in_box(self, canvas: np.ndarray, min_x: int, max_x: int, y: int) -> None:
        """
        draws the (sub?)tree rooted by this node in the canvas so that it fits in the specified range. (Note: this
        may overflow the max_x if the range is too skinny.
        :param canvas: the 2d x 3 color ndarray to draw into
        :param min_x: the left edge of where this subtree can be drawn
        :param max_x: the right edge (ideally) where this subtreen can be drawn
        :param y: the top edge of this particular node
        """
        # I've written this one for you.
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
        if self.isSelected:  # potentially highlight this node.
            cv2.rectangle(img=canvas,
                          pt1=(mid_x - BOX_SIZE // 2-1, y-1),
                          pt2=(mid_x + BOX_SIZE // 2+1, y + BOX_SIZE+1),
                          color=(255,255,255),
                          thickness=2)
            cv2.rectangle(img=canvas,
                          pt1=(mid_x - BOX_SIZE // 2 - 1, y - 1),
                          pt2=(mid_x + BOX_SIZE // 2 + 1, y + BOX_SIZE + 1),
                          color=(0, 0, 0),
                          thickness=1)
        # recursive calls to the left and right children....
        if self.leftNode is not None:
            left_mid = (min_x + mid_x)//2
            cv2.line(img=canvas,
                     pt1=(mid_x,y+BOX_SIZE),
                     pt2=(left_mid, y+VERTICAL_OFFSET),
                     color=(255,255,255),
                     thickness=1) # drawing connective line to left child
            self.leftNode.draw_self_in_box(canvas=canvas, min_x=min_x, max_x=mid_x, y =y + VERTICAL_OFFSET)
        if self.rightNode is not None:
            right_mid = (mid_x + max_x) // 2
            cv2.line(img=canvas,
                     pt1=(mid_x, y + BOX_SIZE),
                     pt2=(right_mid, y + VERTICAL_OFFSET),
                     color=(255, 255, 255),
                     thickness=1) # drawing connective line to right child
            self.rightNode.draw_self_in_box(canvas=canvas, min_x=mid_x, max_x=max_x, y=y + VERTICAL_OFFSET)

    def get_colors_in_order(self, list_of_colors:List[BSTColor]) -> None:
        """
        appends all the colors in the (sub?)tree rooted by this node into the list_of_colors given, in ascending order.
        :param list_of_colors: the (preexisting) list of colors to grow
        """
        if self.value is None:
            return
        # TODO - you write this. Hint: this is recursive.

    def get_colors_in_reverse_order(self, list_of_colors:List[BSTColor]) -> None:
        """
       appends all the colors in the (sub?)tree rooted by this node into the list_of_colors given, in descending order.
       :param list_of_colors: the (preexisting) list of colors to grow
       """
        if self.value is None:
            return
        # TODO - you write this. Hint: this is recursive.

    def get_depth(self) -> int:
        """
        finds the maximum depth of the (sub?)tree rooted by this node, plus one for this node.
        :return: the max depth + 1
        """
        # TODO - you write this. Hint: this is recursive.

        # return 1 for this node, plus the maximum depth of left and right.

        return 1  # replace this with your code.

    def contains(self, target: BSTColor) -> bool:
        """
        determines whether the given target BSTColor object is part of the (sub?)tree rooted by this node, including
        this node, itself.
        :param target: the BSTColor we are looking for.
        :return: whether the target is found.
        """
        # TODO - you write this. Hint: this is recursive.
        # If you're feeling fancy: if this is the matching node, set self.isSelected to True.

        return False

    def clear_all_selections(self) -> None:
        """
        turns off "isSelected" for all ColorNodes in the (sub?)tree rooted by this node.
        """
        self.isSelected = False;
        if self.leftNode is not None:
            self.leftNode.clear_all_selections()
        if self.rightNode is not None:
            self.rightNode.clear_all_selections()

    def size(self) -> int:
        """
        :return: the number of BSTColor objects in the subtree rooted by this node.
        """
        # I've written this one for you.
        result = 1
        if self.leftNode is not None:
            result += self.leftNode.size()
        if self.rightNode is not None:
            result += self.rightNode.size()
        return result


