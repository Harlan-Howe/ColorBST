from typing import List
import cv2

from BSTColor import BSTColor
from ColorBSTDisplay import ColorBSTDisplay
from ColorTree import ColorTree, ColorTreeNode

def start():
    tree = ColorTree()

    display = ColorBSTDisplay(tree)
    ColorTreeNode.display = display

    display.potential_colors = []
    for i in range(64):
        display.potential_colors.append(BSTColor())

    display.added_colors = []

    display.display(wait_for_key=-1, destroy_windows= False)

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start()
