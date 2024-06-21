import numpy as np
import cv2
import dip

class Phase0:
    def __init__(self):
        self.BEM = None
        self.Theta = None

    def Algo(self, im, show = False):
    ###  BINARY EDGE MAP
        BEM = im
        # BEM = cv2.Canny(
        #             image = cv2.GaussianBlur(
        #                         src = im,
        #                         ksize = (0, 0),
        #                         sigmaX = 1.5,
        #                         sigmaY = 0,
        #                         borderType = cv2.BORDER_DEFAULT),
        #             threshold1 = 20, 
        #             threshold2 = 40,
        #             apertureSize = 3,
        #             L2gradient = True)
        if show:
            dip.show_image(
                        image = BEM,
                        title = "Binary Edge Map")
    ### GRADIENT ORIENTATION
        Sx = cv2.Sobel(im, cv2.CV_64F, 1, 0)
        Sy = cv2.Sobel(im, cv2.CV_64F, 0, 1)
        Gradient_Theta = np.arctan2(Sy,Sx)
        Theta = Gradient_Theta * (180 / np.pi) % 180
        Theta_Quant = (np.floor((Theta + 22.5) / 45.0) * 45) % 180
        return BEM, Theta, Theta_Quant, Sx, Sy