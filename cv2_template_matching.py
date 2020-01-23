import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('fullimg1.bmp',0)
# img = cv2.resize(cv2.imread('fullimg1.bmp',0), (683, 384))
img2 = img.copy()
template = cv2.imread('img0.bmp',0)

w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
# methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

methods = ['cv2.TM_CCOEFF']


def map_match(img2):
    for meth in methods:
        img = cv2.imread(img2, 0).copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        map_width = bottom_right[0] - top_left[0]
        map_height = bottom_right[1] - top_left[1]
        cv2.rectangle(img,top_left, bottom_right, 255, 2)
        map_coord = (top_left[0], top_left[1], map_width, map_height)
        print("MINIMAP match rectangle (x,y) (TOP LEFT & BOTTOM RIGHT): ", top_left, " ", bottom_right)
        print("SIZE: ", map_width, " x ", map_height)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()
    return map_coord

# map_match(img2)