from typing import List, Optional, Any

import cv2
import numpy as np
from numpy import dtype, float64, ndarray

from BSTColor import BSTColor
from ColorTree import ColorTree, ColorTreeNode


class ColorBSTDisplay:
    def __init__(self, t: ColorTree):
        self.added_colors  = []
        self.potential_colors = []
        self.dimensions = (800,1000,3)
        self.tree = t
        self.selected_color = None
        cv2.namedWindow("Display")
        cv2.setMouseCallback("Display", self.handle_mouse_click)


    def display(self, wait_for_key:int = 0, destroy_windows:bool = True):
        canvas = np.zeros(shape=self.dimensions, dtype=np.uint8)

        cv2.putText(img=canvas,
                    text="Potential:",
                    org=(10,20),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale= 1.0,
                    color=(255,255,0))
        self.draw_row_of_boxes_for_list(canvas, self.potential_colors, 30)

        cv2.putText(img=canvas,
                    text="Added:",
                    org=(10, 80),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                    fontScale=1.0,
                    color=(255, 255, 0))
        self.draw_row_of_boxes_for_list(canvas, self.added_colors, 90)

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





        self.showListInOrder(canvas)

        self.show_list_in_reverse_order(canvas)

        self.draw_buttons(canvas)

        cv2.imshow("Display", canvas)
        if wait_for_key >= 0:
            cv2.waitKey(wait_for_key)
        if destroy_windows:
            cv2.destroyAllWindows()

    def draw_buttons(self, canvas: Any):
        cv2.rectangle(img=canvas,
                      pt1=(0, 700),
                      pt2=(canvas.shape[1] // 3, 750),
                      color=(128, 235, 250),
                      thickness=-1)
        (w, h), base = cv2.getTextSize(text="Add", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, thickness=1);
        cv2.putText(img=canvas, text="Add", org=(canvas.shape[1] // 6 - w // 2, 725 + h // 2),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 0))

        cv2.rectangle(img=canvas,
                      pt1=(canvas.shape[1] // 3, 700),
                      pt2=(2 * canvas.shape[1] // 3, 750),
                      color=(255, 128, 230),
                      thickness=-1)
        (w, h), base = cv2.getTextSize(text="Find", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, thickness=1);
        cv2.putText(img=canvas, text="Find", org=(canvas.shape[1] // 2 - w // 2, 725 + h // 2),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 0))

        cv2.rectangle(img=canvas,
                      pt1=(2 * canvas.shape[1] // 3, 700),
                      pt2=(canvas.shape[1], 750),
                      color=(128, 235, 250),
                      thickness=-1)
        (w, h), base = cv2.getTextSize(text="Remove", fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, thickness=1);
        cv2.putText(img=canvas, text="Remove", org=(5 * canvas.shape[1] // 6 - w // 2, 725 + h // 2),
                    fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1.5, color=(0, 0, 0))

    def show_list_in_reverse_order(self, canvas: Any):
        inverted_colors = []
        self.tree.put_colors_in_list_reversed(inverted_colors)

        if len(inverted_colors) > 0:
            cv2.putText(img=canvas,
                        text="ReverseOrder:",
                        org=(10, 650),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 0))
            self.draw_row_of_boxes_for_list(canvas, inverted_colors, 660)

    def showListInOrder(self, canvas: Any):
        sorted_colors = []
        self.tree.put_colors_in_list_forward(sorted_colors)
        if len(sorted_colors) > 0:
            cv2.putText(img=canvas,
                        text="InOrder:",
                        org=(10, 590),
                        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1,
                        color=(255, 255, 0))
            self.draw_row_of_boxes_for_list(canvas, sorted_colors, 600)

    def draw_row_of_boxes_for_list(self, canvas: np.ndarray, list_to_draw: List[BSTColor], y:int):
        if len(list_to_draw) > 0:
            width_per_box = self.dimensions[1]/len(list_to_draw)
            for i in range(len(list_to_draw)):
                cv2.rectangle(img=canvas,
                              pt1=(int(i*width_per_box),y),
                              pt2=(int((i+1)*width_per_box),y+20),
                              color=list_to_draw[i].BGR_color,
                              thickness=-1)
                cv2.putText(img=canvas,
                            text=list_to_draw[i].letter,
                            org=(int((i+0.5) * width_per_box - 5), y+15),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.33,
                            color=(0, 0, 0))

    def handle_mouse_click(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONUP:
            print(f"Mouse clicked at ({x}, {y}).")