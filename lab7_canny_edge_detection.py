# -*- coding: utf-8 -*-


import numpy as np
import cv2
from matplotlib import pyplot as plt

import os

def get_gradient_mag_phase(image):
    # Soblel kernels
    Sx = np.asarray([[-1, 0, 1 ],[-2, 0, 2],[-1, 0, 1]], dtype=float)
    Sy = np.asarray([[1, 2, 1 ],[0, 0, 0,],[-1, -2, -1]], dtype=float)

    Gx = cv2.filter2D(image,cv2.CV_32F,Sx)
    Gy = cv2.filter2D(image,cv2.CV_32F,Sy)
    # Magnitude
    G=np.sqrt(np.square(Gx)+np.square(Gy))
    # Phase
    Theta = np.degrees(np.arctan2(Gy,Gx)).astype(int)
    Theta = np.where(Theta < 0, Theta, Theta+180)
    ## Here I usse lambda functions but you can do in many other ways
    Theta = np.vectorize(lambda x: ((int((x+22.5)/45.))*45)%180)(Theta)

    return G, Theta

def non_maxima_suppression(G, Theta):

    edge_candidates=np.zeros(G.shape, dtype=np.uint8)

    for i in range(1,G.shape[0]-1):
        for j in range(1,G.shape[1]-1):
            if Theta[i,j] == 0:
                if np.max([G[i,j-1],G[i,j],G[i,j+1]]) == G[i,j]:
                    edge_candidates[i,j] = 1
            elif Theta[i,j] == 45:
                if np.max([G[i+1,j-1],G[i,j],G[i-1,j+1]]) == G[i,j]:
                    edge_candidates[i,j] = 1
            elif Theta[i,j] == 90:
                if np.max([G[i-1,j],G[i,j],G[i+1,j]]) == G[i,j]:
                    edge_candidates[i,j] = 1
            elif Theta[i,j] == 135:
                if np.max([G[i-1,j-1],G[i,j],G[i+1,j+1]]) == G[i,j]:
                    edge_candidates[i,j] = 1

    return edge_candidates


def hysteresis_thresholding(G, edge_candidates, th_low, th_high):

    # Set all pixel with G > th_high as edges
    edges=np.where(G > th_high, 1, 0)
    # Discard non local maxima
    edges=np.multiply(edges, edge_candidates)
    #Check weak edges 3x3
    for i in range(1,G.shape[0]-1):
        for j in range(1,G.shape[1]-1):
            if G[i,j]>th_low and edges[i,j]!=1 and edge_candidates[i,j]==1:
                # Look for strong edges in 3x3
                if np.max(edges[i-1:i+1,j-1:j+1])>0:
                    edges[i,j]=1
    edges=edges.astype(dtype=np.uint8)
    return edges

# Canny Edge
def canny_edge(image,th_low,th_high):
    #1 Gaussian low pass - remove noise
    gauss_image=cv2.GaussianBlur(image,ksize=(0,0),sigmaX=2.0,sigmaY=0, borderType=cv2.BORDER_DEFAULT)
    #2 Gradient estimation
    G, Theta = get_gradient_mag_phase(gauss_image)
    #3 Non maxima suppresion
    edge_candidates=non_maxima_suppression(G, Theta)
    #4 Hysteresis thresholding
    edge_map = hysteresis_thresholding(G, edge_candidates, th_low, th_high)
    return edge_map