import cv2
import numpy as np
from matplotlib import pyplot as plt

# IMG = image to analyze; TEMPLATE = template img that will be searched for
IMG = "fullimg4.bmp"
TEMPLATE = "btn.bmp"
template = cv2.imread(TEMPLATE,0)

# img = cv2.imread(IMG,0)
# img = cv2.resize(cv2.imread('fullimg1.bmp',0), (683, 384))
# img_copy = img.copy()


# extract template width and height
w, h = template.shape[::-1]

# 6 methods for template matching in a list; each method has varying params: colors/saturation etc
# METHODS = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
#             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

METHODS = ['cv2.TM_CCOEFF_NORMED']

# REQUIRES: img file to match
# EFFECTS: crops the bottom panel of img & matches for map only there, returns (x, y, width, height) of match
def map_match(img2):
    for meth in METHODS:
        # crop the bottom panel of img to since map will be there
        crop_img = cv2.imread(img2)[600:900, 0:1500]
        cv2.imwrite("crop_bottom.bmp", crop_img)
        img = cv2.imread("crop_bottom.bmp", 0).copy()
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
        print(top_left, bottom_right)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)

        # find map by using stats button as template
        top_left, bottom_right = find_map(top_left, bottom_right, img)


        map_width = bottom_right[0] - top_left[0]
        map_height = bottom_right[1] - top_left[1]
        map_coord = (top_left[0], top_left[1], map_width, map_height)
        print("MINIMAP match rectangle (x,y) (TOP LEFT & BOTTOM RIGHT): ", top_left, " ", bottom_right)
        print("SIZE: ", map_width, " x ", map_height)
        print(map_coord)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()
    return map_coord

# REQUIRES: top_left, bottom_right of stats button match and the img
# EFFECTS: finds & returns top_left, bottom_right of map by using stats button as template
def find_map(top_left, bottom_right, img):
    top_left = (top_left[0]-275, top_left[1]-30)
    bottom_right = (bottom_right[0]+25, bottom_right[1]+100)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    return top_left, bottom_right


# map_match(IMG)