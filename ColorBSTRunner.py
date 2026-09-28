from typing import List
import cv2

from BSTColor import BSTColor
from ColorBSTDisplay import ColorBSTDisplay
from ColorTree import ColorTree

colorList:List[BSTColor] = []
tree = ColorTree()

display = ColorBSTDisplay(tree)
display.colorList = colorList


for i in range(32):
    col = BSTColor()
    colorList.append(col)
    tree.add(col)
    display.display(wait_for_key=False)
    cv2.waitKey(200)

cv2.waitKey()
cv2.destroyAllWindows()

