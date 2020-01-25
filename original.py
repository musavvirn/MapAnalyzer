from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from color_constants import COLORS_RGB_2
from color_constants import COLORS_HEX
from template_match import map_match

# img to be read
IMG = "img0.bmp"
IMG_2 = "fullimg7.bmp"

# defines all RGB colors of img, populated by extract_rgb
IMG_RGB = []

# REQUIRES: 
# EFFECTS: extracts RGB colors of img for each pixel and popluates IMG_RGB
def extract_rgb(img):
    global IMG_RGB
    IMG_RGB = []
    
    image = cv2.imread(img)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image)
    plt.show()

    for i in range(0, image.shape[1]):
        for j in range(0, image.shape[0]):
            r = image[j, i, 0]
            g = image[j, i, 1]
            b = image[j, i, 2]
            rgb = [r, g, b]
            # print(rgb)
            IMG_RGB.append(rgb)
    return i



# REQUIRES: 2 RGB colors
# EFFECTS: matches the RGBs with a tolerance and returns TRUE if matched
def compare_rgb_2(c, i):
    DIFF = 20
    found = False
    if (i == [67, 67, 67]):
        if ((abs(c[0] - i[0]) < 1) and (abs(c[1] - i[1]) < 1) and (abs(c[2] - i[2]) < 1)):
            print(c)
            found = True
    elif ((abs(c[0] - i[0]) < DIFF) and (abs(c[1] - i[1]) < DIFF) and (abs(c[2] - i[2]) < DIFF)):
        print(c)
        found = True
    return found           
    
# defines coutns of player colors found in IMG_RGB, populated by player_color_match and used for pie plot
PLAYER_COLOR_PIE = [0, 0, 0, 0, 0, 0, 0, 0]

# REQUIRES: 
# EFFECTS: counts each player color in img rgb and adds it to PLAYER_COLOR_PIE
def player_color_match():
    global PLAYER_COLOR_PIE
    PLAYER_COLOR_PIE = [0, 0, 0, 0, 0, 0, 0, 0]

    for i in IMG_RGB:
        if (compare_rgb_2(i, [0, 0, 255])):
            PLAYER_COLOR_PIE[0] += 1
        if (compare_rgb_2(i, [255, 0, 0])):
            PLAYER_COLOR_PIE[1] += 1
        if (compare_rgb_2(i, [0, 255, 0])):
            PLAYER_COLOR_PIE[2] += 1
        if (compare_rgb_2(i, [255, 255, 0])):
            PLAYER_COLOR_PIE[3] += 1
        if (compare_rgb_2(i, [10, 240, 240])):
            PLAYER_COLOR_PIE[4] += 1
        if (compare_rgb_2(i, [255, 0, 255])):
            PLAYER_COLOR_PIE[5] += 1
        if (compare_rgb_2(i, [67,67,67])):
            PLAYER_COLOR_PIE[6] += 1
        if (compare_rgb_2(i, [255,130,0])):
            PLAYER_COLOR_PIE[7] += 1
        
    adjust_color()
    
# adjust for RED, ORANGE & GREY - interference from other map elements    
def adjust_color():
    print("Adjusting...")
    # PLAYER_COLOR_PIE[1] += -25
    # PLAYER_COLOR_PIE[7] += -40
    # for j in range(7):
    #     if (PLAYER_COLOR_PIE[j] < 0):
    #         PLAYER_COLOR_PIE[j] = 0


# REQUIRES: 
# EFFECTS: creates pie plot using PLAYER_COLOR_PIE
def create_plot(img):
    extract_rgb(img)
    player_color_match()
    print(PLAYER_COLOR_PIE)
    plt.figure(figsize = (8, 6))
    plt.pie(PLAYER_COLOR_PIE, labels = PLAYER_COLOR_PIE, colors = COLORS_HEX)
    plt.show()

# REQUIRES: 
# EFFECTS: matches map, crops it out, matches player color & creates pie plot using PLAYER_COLOR_PIE
def map_match_save(img):
    xy = map_match(img)
    print(xy)
    crop_img = cv2.imread("crop_bottom.bmp")[xy[1]:xy[1]+xy[3], xy[0]:xy[0]+xy[2]]
    cv2.imshow("cropped", crop_img)
    cv2.imwrite("cropped.bmp", crop_img)
    cv2.waitKey(0)


map_match_save(IMG_2)
create_plot("cropped.bmp")












