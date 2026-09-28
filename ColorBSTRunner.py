from typing import List

from BSTColor import BSTColor
from ColorBSTDisplay import ColorBSTDisplay
from ColorTree import ColorTree

colorList:List[BSTColor] = []
tree = ColorTree()

for i in range(20):
    col = BSTColor()
    colorList.append(col)
    tree.add(col)



display = ColorBSTDisplay(tree)
display.colorList = colorList

display.display()