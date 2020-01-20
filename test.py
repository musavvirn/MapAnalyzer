
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os

class Map:
    id = 0
    name = ""
    size = ""
    players = 0
    imgSize = ""
    color = []

    def __init__(self, id, name, size, players):
        self.id = id
        self.name = name
        self.size = size
        self.players = players
        print("Map created: " + self.name)

    def getDetails(self):
        print(self.name + " " + self.size + " " + str(self.players))

    def setColors(self, color):
        if (len(color) == self.players):
            for c in color:
                self.color.append(c)
            print(self.color)
        else:
            print("Number of colors must match the player count!")

IMG = "d.png"

BLUE = "#0000FF"
RED = "#FF0000"
GREEN = "#00FF00"
YELLOW = "#FAFF11"
TEAL = "#0CFEF0"
PURPLE = "#F00AF1"
GREY = "#3F4243"
ORANGE = "#FB8200"

COLORS_HEX = [BLUE, RED, GREEN, YELLOW, TEAL, PURPLE, GREY, ORANGE]
IMG_RGB = []

image = cv2.imread(IMG)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


rgb_map = []
for i in range(0, image.shape[1]):
    for j in range(0, image.shape[0]):
        r = image[j, i, 0]
        g = image[j, i, 1]
        b = image[j, i, 2]
        rgb = [r, g, b]
        print(rgb)
        rgb_map.append(rgb)
pie = [0, 0, 0, 0, 0, 0, 0, 0]

def compare_rgb_2(c, i):
    DIFF = 20
    found = False
    if ((abs(c[0] - i[0]) < DIFF) and (abs(c[1] - i[1]) < DIFF) and (abs(c[2] - i[2]) < DIFF)):
        found = True
    return found           
    

for i in rgb_map:
    if (compare_rgb_2(i, [0, 0, 255])):
        pie[0] += 1
    if (compare_rgb_2(i, [255, 0, 0])):
        pie[1] += 1
    if (compare_rgb_2(i, [0, 255, 0])):
        pie[2] += 1
    if (compare_rgb_2(i, [255, 255, 0])):
        pie[3] += 1
    if (compare_rgb_2(i, [0, 255, 255])):
        pie[4] += 1
    if (compare_rgb_2(i, [255, 0, 255])):
        pie[5] += 1
    if (compare_rgb_2(i, [255, 200, 255])):
        pie[6] += 1
    if (compare_rgb_2(i, [255, 100, 255])):
        pie[7] += 1

print(pie)
plt.figure(figsize = (8, 6))
plt.pie(pie, labels = pie, colors = COLORS_HEX)
plt.show()

print("The type of this input is {}".format(type(image)))
print("Shape: {}".format(image.shape))

plt.imshow(image)
plt.show()


## Output
# The type of this input is <class 'numpy.ndarray'>
# Shape: image dimensions, 3 colors (RGB)
# convert to RGB since default in cv2 is BRG

def RGB2HEX(color):
    return "#{:02x}{:02x}{:02x}".format(int(color[0]), int(color[1]), int(color[2]))


def get_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

def hex_to_rgb(hex):
     hex = hex.lstrip('#')
     hlen = len(hex)
     h = tuple(int(hex[i:i+hlen//3], 16) for i in range(0, hlen, hlen//3))
     return h

def get_hex(ordered_colors, counts):
    hex = [RGB2HEX(ordered_colors[i]) for i in counts.keys()]
    rgb = []
    global IMG_RGB
    for c in hex: 
        rgb.append(hex_to_rgb(c))
    
    IMG_RGB = rgb
    return hex


COLORS_RGB = [
    hex_to_rgb(BLUE),
    hex_to_rgb(RED),
    hex_to_rgb(GREEN),
    hex_to_rgb(YELLOW),
    hex_to_rgb(TEAL),
    hex_to_rgb(PURPLE),
    hex_to_rgb(GREY),
    hex_to_rgb(ORANGE)
]

COLORS_RGB_2 = [
    (0,0,255),
    (255,0,0),
    (0,255,0),
    (255,255,0),
    (0,255,255),
    (255,0,255),
    hex_to_rgb(GREY),
    hex_to_rgb(ORANGE)
]

print(COLORS_RGB)
print(COLORS_RGB_2)

# COLORS_RGB = {
#     'BLUE': hex_to_rgb(BLUE),
#     'RED' : hex_to_rgb(RED),
#     'GREEN': hex_to_rgb(GREEN),
#     'YELLOW': hex_to_rgb(YELLOW),
#     'TEAL': hex_to_rgb(TEAL),
#     'PURPLE': hex_to_rgb(PURPLE),
#     'GREY': hex_to_rgb(GREY),
#     'ORANGE': hex_to_rgb(ORANGE)
# }

# print(COLORS_RGB)
def compare_rgb(IMG_RGB):
    print(IMG_RGB)
    for c in COLORS_RGB_2:
        for x in IMG_RGB:
            if (c>x):
                print(c)

def compare_rgb():
    DIFF = 6
    matched_rgb = []
    for c in COLORS_RGB_2:
        for i in IMG_RGB:
            if ((abs(c[0] - i[0]) < DIFF) and (abs(c[1] - i[1]) < DIFF) and (abs(c[2] - i[2]) < DIFF)):
                matched_rgb.append(i)
                # print(i)
    return matched_rgb

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
        matched_hex.append(RGB2HEX(r))
    
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
        plt.figure(figsize = (8, 6))
        plt.pie(counts2, labels = counts2, colors = matched_hex)
        plt.show()
    return rgb_colors

get_colors(get_image(IMG), 2, True)
print(IMG_RGB)

compare_rgb()












