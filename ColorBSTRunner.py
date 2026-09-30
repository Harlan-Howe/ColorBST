from typing import List
import cv2

from BSTColor import BSTColor
from ColorBSTDisplay import ColorBSTDisplay
from ColorTree import ColorTree, ColorTreeNode

def start():

    color_List:List[BSTColor] = []
    potential_colors:List[BSTColor] = []

    for i in range(64):
        potential_colors.append(BSTColor())

    tree = ColorTree()

    display = ColorBSTDisplay(tree)
    ColorTreeNode.display = display


    display.added_colors = color_List
    display.potential_colors = potential_colors


    # for i in range(32):
    #     col = potential_colors.pop(0)
    #     color_List.append(col)
    #     tree.add(col)
    #     display.selected_color = None
    display.display(wait_for_key=-1, destroy_windows= False)

    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start()
