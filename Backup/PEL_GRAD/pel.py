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
from Timer import Timer
from Phase0 import Phase0
import dip
import pickle

### TIME CONTROL - SETUP

timer = Timer()

### INPUT IMAGE - GET AND SHOW

# im = cv2.imread(
#             filename = os.path.join(
#                         os.path.dirname(__file__),
#                         "Data\\Lena.png"),
#             flags = cv2.IMREAD_GRAYSCALE)
# dip.show_image(
#             image = im,
#             title = "Original Image",
#             info = True,
#             BGR2RGB = True)
# timer.flag(name = 'Input Image')

im = np.array([[ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [255,255,255,255,255,255,255,255,255,255,255,255,255,255,255],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               [ 0 , 0 , 0 ,255, 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 , 0 ],
               ], np.uint8)

### PHASE 0 - BINARY EDGE MAP AND GRADIENT ORIENTATION

phase0 = Phase0()
BEM, Theta, Theta_Quant, Sx, Sy = phase0.Algo(im, show = False);
timer.flag(name = 'Phase 0')

dip.show_image(BEM)
dip.show_image(Theta)
dip.show_image(Theta_Quant)
dip.show_image(Sx)
dip.show_image(Sy)


### TIME CONTROL - RESULTS

timer.table()