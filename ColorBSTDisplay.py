from typing import List, Optional, Any

import cv2
import numpy as np
from numpy import dtype, float64, ndarray

from BSTColor import BSTColor
from ColorTree import ColorTree, ColorTreeNode

BUTTON_HEIGHT = 50

TOP_OF_BUTTONS = 700

WINDOW_WIDTH = 1000

HEIGHT_OF_BOXES_IN_ROWS = 20
TOP_OF_REVERSE_LIST = 660
TOP_OF_FORWARD_LIST = 600
TOP_OF_ADDED_LIST = 90
TOP_OF_POTENTIAL_LIST = 30


class ColorBSTDisplay:
    def __init__(self, t: ColorTree):
        self.added_colors: List[BSTColor]  = []
        self.potential_colors: List[BSTColor] = []
        self.sorted_colors: List[BSTColor] = []
        self.reversed_colors: List[BSTColor] = []
        self.dimensions = (800, WINDOW_WIDTH, 3)
        self.tree = t
        self.selected_color = None
        self.message: Optional[str] = None
        cv2.namedWindow("Display")
        cv2.setMouseCallback("Display", self.handle_mouse_click)


    def display(self, wait_for_key:int = 0, destroy_windows:bool = True):
        canvas = np.zeros(shape=self.dimensions, dtype=np.uint8)

        if self.selected_color is None and len(self.potential_colors)>0:
            self.selected_color = self.potential_colors[0]

        cv2.putText(img=canvas,
                    text="Potential:",
                    org=(10,20),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale= 1.0,
                    color=(255,255,0))
        self.draw_row_of_boxes_for_list(canvas, self.potential_colors, TOP_OF_POTENTIAL_LIST)

        cv2.putText(img=canvas,
                    text="Added:",
                    org=(10, 80),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(255, 255, 0))
        self.draw_row_of_boxes_for_list(canvas, self.added_colors, TOP_OF_ADDED_LIST)

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
        self.tree.draw_self(canvas)

        self.draw_depth(canvas)

        self.draw_message(canvas)


        self.showListInOrder(canvas)

        self.show_list_in_reverse_order(canvas)

        self.draw_buttons(canvas)

        cv2.imshow("Display", canvas)
        if wait_for_key >= 0:
            cv2.waitKey(wait_for_key)
        if destroy_windows:
            cv2.destroyAllWindows()

    def draw_message(self, canvas: Any):
        if self.message is not None:
            (w, h), bsln = cv2.getTextSize(text=self.message, fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75,
                                           thickness=1)
            cv2.putText(img=canvas, text=self.message, org=(WINDOW_WIDTH - 10 - w, TOP_OF_FORWARD_LIST - 5),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75, color=(255, 255, 255))

    def draw_depth(self, canvas: Any):
        depth = self.tree.get_depth()
        if depth != -1:
            cv2.putText(img=canvas, text=f"Depth: {depth}", org=(10, 150),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.75, color=(255, 128, 255))

    def draw_buttons(self, canvas: Any):
        cv2.rectangle(img=canvas,
                      pt1=(0, TOP_OF_BUTTONS),
                      pt2=(canvas.shape[1] // 3, TOP_OF_BUTTONS + BUTTON_HEIGHT),
                      color=(128, 235, 250),
                      thickness=-1)
        (w, h), base = cv2.getTextSize(text="Add", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, thickness=1);
        cv2.putText(img=canvas, text="Add", org=(canvas.shape[1] // 6 - w // 2, 725 + h // 2),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 0))

        cv2.rectangle(img=canvas,
                      pt1=(canvas.shape[1] // 3, TOP_OF_BUTTONS),
                      pt2=(2 * canvas.shape[1] // 3, TOP_OF_BUTTONS + BUTTON_HEIGHT),
                      color=(255, 128, 230),
                      thickness=-1)
        (w, h), base = cv2.getTextSize(text="Find", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, thickness=1);
        cv2.putText(img=canvas, text="Find", org=(canvas.shape[1] // 2 - w // 2, 725 + h // 2),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 0))

        cv2.rectangle(img=canvas,
                      pt1=(2 * canvas.shape[1] // 3, TOP_OF_BUTTONS),
                      pt2=(canvas.shape[1], TOP_OF_BUTTONS + BUTTON_HEIGHT),
                      color=(128, 235, 250),
                      thickness=-1)
        (w, h), base = cv2.getTextSize(text="Remove", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, thickness=1);
        cv2.putText(img=canvas, text="Remove", org=(5 * canvas.shape[1] // 6 - w // 2, 725 + h // 2),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 0))

    def show_list_in_reverse_order(self, canvas: Any):
        self.reversed_colors = []
        self.tree.put_colors_in_list_reversed(self.reversed_colors)

        if len(self.reversed_colors) > 0:
            cv2.putText(img=canvas,
                        text="ReverseOrder:",
                        org=(10, 650),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 0))
            self.draw_row_of_boxes_for_list(canvas, self.reversed_colors, TOP_OF_REVERSE_LIST)

    def showListInOrder(self, canvas: Any):
        self.sorted_colors = []
        self.tree.put_colors_in_list_forward(self.sorted_colors)
        if len(self.sorted_colors) > 0:
            cv2.putText(img=canvas,
                        text="InOrder:",
                        org=(10, 590),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 0))
            self.draw_row_of_boxes_for_list(canvas, self.sorted_colors, TOP_OF_FORWARD_LIST)

    def draw_row_of_boxes_for_list(self, canvas: np.ndarray, list_to_draw: List[BSTColor], y:int):
        if len(list_to_draw) > 0:
            width_per_box = self.dimensions[1]/len(list_to_draw)
            for i in range(len(list_to_draw)):
                cv2.rectangle(img=canvas,
                              pt1=(int(i*width_per_box),y),
                              pt2=(int((i+1)*width_per_box), y + HEIGHT_OF_BOXES_IN_ROWS),
                              color=list_to_draw[i].BGR_color,
                              thickness=-1)
                if list_to_draw[i] == self.selected_color:
                    cv2.rectangle(img=canvas,
                                  pt1=(int(i * width_per_box)+1, y+1),
                                  pt2=(int((i + 1) * width_per_box) - 1, y + HEIGHT_OF_BOXES_IN_ROWS - 1),
                                  color=(255,255,255),
                                  thickness=2)
                cv2.putText(img=canvas,
                            text=list_to_draw[i].letter,
                            org=(int((i+0.5) * width_per_box - 5), y+15),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.33,
                            color=(0, 0, 0))

    def handle_add_button(self):
        if self.selected_color is not None:
            self.tree.add(self.selected_color)
            self.added_colors.append(self.selected_color)
            self.potential_colors.remove(self.selected_color)
            if len(self.potential_colors) == 0:
                for _ in range(32):
                    self.potential_colors.append(BSTColor())
            self.selected_color = None
            self.display(wait_for_key=-1, destroy_windows=False)

    def handle_find_button(self):
        if self.selected_color is None or self.tree.root is None:
            return
        result:bool = self.tree.find(self.selected_color)
        if result:
            self.message = "Found the color in the tree!"
        else:
            self.message = "The color is not in the tree!"
        self.display(wait_for_key=-1, destroy_windows=False)

    def handle_remove_button(self):
        if self.selected_color is None or self.tree.root is None:
            return
        succeeded:bool = self.tree.remove(self.selected_color)
        if succeeded:
            self.added_colors.remove(self.selected_color)
            self.display(wait_for_key=-1, destroy_windows=False)
            self.message = "Removed color from the tree!"
        else:
            self.message = "Could not remove: The color was not in the tree!"
        self.display(wait_for_key=-1, destroy_windows=False)



    def handle_mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            print(f"Mouse clicked at ({x}, {y}).")
            if TOP_OF_POTENTIAL_LIST <= y <= TOP_OF_POTENTIAL_LIST+HEIGHT_OF_BOXES_IN_ROWS:
                box_width = WINDOW_WIDTH / len(self.potential_colors)
                self.selected_color=self.potential_colors[int(x/box_width)]
                self.display(wait_for_key=-1,destroy_windows=False)
            elif TOP_OF_ADDED_LIST <= y <= TOP_OF_ADDED_LIST+HEIGHT_OF_BOXES_IN_ROWS:
                box_width = WINDOW_WIDTH / len(self.added_colors)
                self.selected_color = self.added_colors[int(x / box_width)]
                self.display(wait_for_key=-1, destroy_windows=False)
            elif TOP_OF_FORWARD_LIST <= y <= TOP_OF_FORWARD_LIST + HEIGHT_OF_BOXES_IN_ROWS:
                box_width = WINDOW_WIDTH / len(self.sorted_colors)
                self.selected_color = self.sorted_colors[int(x / box_width)]
                self.display(wait_for_key=-1, destroy_windows=False)
            elif TOP_OF_REVERSE_LIST <= y <= TOP_OF_REVERSE_LIST + HEIGHT_OF_BOXES_IN_ROWS:
                box_width = WINDOW_WIDTH / len(self.reversed_colors)
                self.selected_color = self.reversed_colors[int(x / box_width)]
                self.display(wait_for_key=-1, destroy_windows=False)
            elif TOP_OF_BUTTONS <= y <= TOP_OF_BUTTONS + BUTTON_HEIGHT:
                if x < WINDOW_WIDTH/3:
                    self.handle_add_button()
                elif x > 2*WINDOW_WIDTH/3:
                    self.handle_remove_button()
                else:
                    self.handle_find_button()