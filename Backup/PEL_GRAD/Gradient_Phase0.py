from copy import deepcopy
import numpy as np
import cv2

# ------------------------- EDGE DETECTION -------------------------
class Phase0:
    def get_gradient_mag_phase(self,image):
        # Soblel kernels
        Sx = np.asarray([[-1, 0, 1 ],[-2, 0, 2],[-1, 0, 1]], dtype='float')
        Sy = np.asarray([[1, 2, 1 ],[0, 0, 0,],[-1, -2, -1]], dtype='float')
    
        Gx = cv2.filter2D(image,cv2.CV_32F,Sx)
        Gy = cv2.filter2D(image,cv2.CV_32F,Sy) 
        # Magnitude
        G=np.sqrt(np.square(Gx)+np.square(Gy))
        # Phase
        Theta = np.degrees(np.arctan2(Gy,Gx)).astype('int')
        print(Theta)
        Theta_original = deepcopy(Theta)
        print(Theta_original)
        for i in range(Theta.shape[0]):
            for j in range(Theta.shape[1]):
                print(Theta_original[i,j])
                if Theta_original[i,j] < 0:
                    Theta[i,j] += 180
                elif Theta_original[i,j] == 180:
                    Theta[i,j] = 0
                    continue
                if Theta[i,j] < 22.5:
                    Theta[i,j] = 0
                elif Theta[i,j] < 67.5:
                    Theta[i,j] = 45
                elif Theta[i,j] < 112.5:
                    Theta[i,j] = 90
                elif Theta[i,j] < 157.5:
                    Theta[i,j] = 135
                else:
                    Theta[i,j] = 0
        return G, Theta, Theta_original


    # Canny Edge
    def Canny(self,image,th_low,th_high):
        #1 Gaussian low pass - remove noise 
        gauss_image=cv2.GaussianBlur(image,(5,5),0) 
        #2 Gradient estimation
        G, Theta, Theta_original = self.get_gradient_mag_phase(gauss_image)
        edge_map = cv2.Canny(image,th_low,th_high)
        return edge_map, Theta, Theta_original