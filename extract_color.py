from sklearn.cluster import KMeans
import matplotlib.pyplot as plot
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
IMG_2 = "fullimg1.bmp"
image = cv2.imread(IMG)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# defines all RGB colors of img, populated by get_hex
IMG_RGB = []
rgb_map = []


# REQUIRES: single RGB color
# EFFECTS: converts RGB to HEX and returns it
def rgb_to_hex(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))

# REQUIRES: img file path
# EFFECTS: reads img, converts to RGB mode (cv2 default is BGR) and returns it
def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

# REQUIRES: single HEX color
# EFFECTS: returns RGB 
def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     r = tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
     return r

# REQUIRES: list of RGB colors, counts (counts of clusters)
# EFFECTSL list of HEX colors
def get_hex(ordered_colors, counts):
    hex = [rgb_to_hex(ordered_colors[i]) for i in counts.keys()]
    rgb = []
    global IMG_RGB
    for c in hex: 
        rgb.append(hex_to_rgb(c))
    
    IMG_RGB = rgb
    return hex

print(COLORS_RGB_2)

# REQUIRES: list of img RGB colors
# EFFECTS: compares RGB colors of img with COLORS_RGB_2; VOID
def compare_rgb(IMG_RGB):
    print(IMG_RGB)
    for c in COLORS_RGB_2:
        for x in IMG_RGB:
            if (c>x):
                print(c)

# REQUIRES: 
# EFFECTS: compares RGB colors of img with COLORS_RGB_2 and returns found colors
def compare_rgb():
    # tolerance level for comparison; applied to each of R,G,B
    DIFF = 6
    matched_rgb = []
    for c in COLORS_RGB_2:
        for i in IMG_RGB:
            if ((abs(c[0] - i[0]) < DIFF) and (abs(c[1] - i[1]) < DIFF) and (abs(c[2] - i[2]) < DIFF)):
                matched_rgb.append(i)
                # print(i)
    return matched_rgb

# REQUIRES: img, no of color clusters, true to show as chart
# EFFECTS: use KMeans to extract and group colors in clusters; displayes as pie chart if true
def get_colors(image, number_of_colors, show_chart):
    modified_image = image
    modified_image = modified_image.reshape(modified_image.shape[0] * modified_image.shape[1], 3)

    clf = KMeans(n_clusters = number_of_colors)
    labels = clf.fit_predict(modified_image)
    counts = Counter(labels)
    
    center_colors = clf.cluster_centers_
    # We get ordered colors by iterating through the keys
    ordered_colors = [center_colors[i] for i in counts.keys()]
    hex_colors = get_hex(ordered_colors, counts)
    rgb_colors = [ordered_colors[i] for i in counts.keys()]
    matched_rgb = compare_rgb()
    matched_hex = []

    for r in matched_rgb:
        matched_hex.append(rgb_to_hex(r))
    
    print(matched_rgb)

    counts2 = []
    for h in hex_colors:
        x = hex_to_rgb(h)
        for m in matched_rgb:
            if (x == m):
                print("Found!", m)
                i = hex_colors.index(h)
                counts2.append(counts.get(i))

    print(counts2)
    print(counts)
    if (show_chart):
        plot.figure(figsize = (8, 6))
        plot.pie(counts2, labels = counts2, colors = ordered_colors)
        plot.show()
    return rgb_colors

get_colors(get_image(IMG), 2, True)
compare_rgb()













