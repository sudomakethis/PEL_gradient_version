#######     ##   #######
##    ##    ##   ##     ##
##     ##   ##   ##     ##
##     ##   ##   #######
##     ##   ##   ##
##    ##    ##   ##
#######     ##   ##

import numpy as np
from matplotlib import pyplot as plt
import cv2

WizardsFamiliar = ("""    

           ^...^
          / o,o \\
          |):::(|
        ====w=w===

""")
# +3 Spot (dark)

def show_image(image, title = "", info = False, BGR2RGB = False):
    if image is not None:
        if len(image.shape) == 2:
            if info:
                print("Image type Grayscale "+str(image.shape))
            plt.imshow(image, cmap = 'gray', vmin=0, vmax=255)
            plt.title(title)
            plt.xticks([]), plt.yticks([])
            plt.show()
        elif (len(image.shape) == 3 and (
            image.shape[2] == 3 or image.shape[2] == 4)):
            if info:
                print("Image type Colored",str(image.shape),
                "\nNumber of Channels",image.shape[2],
                "\nNumber of Rows",image.shape[0],
                "\nNumber of Columns",image.shape[1])
            if BGR2RGB:
                image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            plt.imshow(image)
            plt.title(title)
            plt.xticks([]), plt.yticks([])
            plt.show()
        else:
            print("Error. Dimension Check.")
    else:
        print("Error. Unable to load the Image.")
    return image

def FillGaps(edges):
    BEMF = edges
    return BEMF

print(WizardsFamiliar)