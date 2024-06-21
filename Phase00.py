import cv2
import dip

class Phase0:
    def Algo(self, path, show_im = False, show_BEM = False):
        im = cv2.imread(
            filename = path,
            flags = cv2.IMREAD_GRAYSCALE)
        if show_im:
            dip.show_image(
                image = im,
                title = "Original Image",
                info = True)
    ### BINARY EDGE MAP
        image = cv2.GaussianBlur(
                                src = im,
                                ksize = (0, 0),
                                sigmaX = 2.0,
                                sigmaY = 0,
                                borderType = cv2.BORDER_DEFAULT)
        
        BEM = cv2.Canny(
                    image = image,
                    threshold1 = 20, 
                    threshold2 = 40,
                    apertureSize = 3,
                    L2gradient = True)
        
        Gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        Gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        G = cv2.magnitude(Gx, Gy)
        theta = cv2.phase(Gx, Gy)
        
        if show_BEM:
            dip.show_image(
                        image = BEM,
                        title = "Binary Edge Map",
                        info = False)
        return im, BEM

dip.WizardFamiliar("Phase 0!")

class Phase0Gradient:
    def Algo(self, path, show_im = False, show_BEM = False):
        im = cv2.imread(
            filename = path,
            flags = cv2.IMREAD_GRAYSCALE)
        if show_im:
            dip.show_image(
                image = im,
                title = "Original Image",
                info = True)
        ### BINARY EDGE MAP
        image = cv2.GaussianBlur(
                                src = im,
                                ksize = (0, 0),
                                sigmaX = 2.0,
                                sigmaY = 0,
                                borderType = cv2.BORDER_DEFAULT)
        
        BEM = cv2.Canny(
                    image = image,
                    threshold1 = 20, 
                    threshold2 = 40,
                    apertureSize = 3,
                    L2gradient = True)
        
        Gx = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
        Gy = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
        G = cv2.magnitude(Gx, Gy)
        theta = cv2.phase(Gx, Gy)


        if show_BEM:
            dip.show_image(
                        image = BEM,
                        title = "Binary Edge Map",
                        info = False)
        return im, BEM, G, theta