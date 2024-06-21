#######     ########   ##
##     ##   ##         ##
##     ##   ##         ##
#######     ########   ##
##          ##         ##
##          ##         ##
##          ########   #########

import numpy as np
import cv2
import os
import time
import dip
import pickle
import time
from Gradient_Phase0 import Phase0
from Gradient_Phase1 import Phase1
from Gradient_Phase2 import Phase2_Algorithm
from Phase4 import Phase4
from copy import deepcopy

### SETUP TIME CONTROL

t = list()
t.append(time.time())

### GET IMAGE FROM DIRECTORY PATH

im = cv2.imread(
            filename = os.path.join(
                        os.path.dirname(__file__),
                        "Images\\Lena.png"),
            flags = cv2.IMREAD_GRAYSCALE)
dip.show_image(
            image = im,
            title = "Original Image",
            info = True,
            BGR2RGB = True)
t.append(round((time.time() - t[0]) * 1000, 2)) # Time Flag

###  BINARY EDGE MAP

BEM = cv2.Canny(
            image = cv2.GaussianBlur(
                        src = im,
                        ksize = (0, 0),
                        sigmaX = 1.5,
                        sigmaY = 0,
                        borderType = cv2.BORDER_DEFAULT),
            threshold1 = 20, 
            threshold2 = 40,
            apertureSize = 3,
            L2gradient = True)
dip.show_image(
            image = BEM,
            title = "Binary Edge Map")
t.append(round((time.time() - t[0]) * 1000, 2)) # Time Flag

### FILL GAPS

#BEM2 = dip.FillGaps(
#            edges = BEM)

## COPY FROM PAGANI

# Set the Canny edge detection parameters
low_threshold = 150
high_threshold = 200
# --------------- PHASE 0 : EDGE DETECTION ---------------
algophase1 = Phase0()
imgwedges, Theta, Theta_original = algophase1.Canny(im,low_threshold,high_threshold)
# --------------- PHASE 1 : FILL EDGE GAPS ---------------
algophase1 = Phase1()
filled_edges = algophase1.PEL_1_FillGaps(np.copy(imgwedges),Theta)
# --------------- PHASE 2 : CREATE SEGMENTS ---------------
algophase2 = Phase2_Algorithm(np.copy(filled_edges))
segments = algophase2.start_algorithm(Theta_original)

segments_list = []

for i in range(len(segments)):
    segments_list.append(segments[i].nodes)
    
print(segments_list[0])
print(segments_list[1])
print(segments_list[2])
print(segments_list[3])

pickle.dump(segments_list, open('segments.dump', 'wb'))

# algophase4 = Phase4(deepcopy(segments))
# algophase4.thin_segments(20)
# thinned_segments = algophase4.get_segments()

### END

t.append(round((time.time() - t[0]) * 1000, 2)) # Time Flag
#print("Elapsed time: ", t[-1], "ms")
print(t)

# print(segments[0].nodes)
# print(type(segments[0].nodes))
# print(segments[0].nodes[0])
# print(type(segments[0].nodes[0]))
# print(segments[0].nodes[0][0])
# print(type(segments[0].nodes[0][0]))

# for index in length(segments):
#   seg = segments[i].nodes
