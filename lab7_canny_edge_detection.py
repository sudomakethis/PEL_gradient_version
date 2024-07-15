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
    edge_candidates = np.zeros(G.shape, dtype=np.uint8)

    # Slicing gli indici delle celle adiacenti per ogni direzione
    I, J = np.arange(1, G.shape[0]-1), np.arange(1, G.shape[1]-1)

    # Direzione 0 gradi (orizzontale)
    mask_0 = (Theta[1:-1, 1:-1] == 0) & (G[1:-1, 1:-1] >= G[1:-1, :-2]) & (G[1:-1, 1:-1] >= G[1:-1, 2:])
    edge_candidates[1:-1, 1:-1][mask_0] = 1

    # Direzione 45 gradi (diagonale - alto a sinistra a basso a destra)
    mask_45 = (Theta[1:-1, 1:-1] == 45) & (G[1:-1, 1:-1] >= G[2:, :-2]) & (G[1:-1, 1:-1] >= G[:-2, 2:])
    edge_candidates[1:-1, 1:-1][mask_45] = 1

    # Direzione 90 gradi (verticale)
    mask_90 = (Theta[1:-1, 1:-1] == 90) & (G[1:-1, 1:-1] >= G[:-2, 1:-1]) & (G[1:-1, 1:-1] >= G[2:, 1:-1])
    edge_candidates[1:-1, 1:-1][mask_90] = 1

    # Direzione 135 gradi (diagonale - alto a destra a basso a sinistra)
    mask_135 = (Theta[1:-1, 1:-1] == 135) & (G[1:-1, 1:-1] >= G[:-2, :-2]) & (G[1:-1, 1:-1] >= G[2:, 2:])
    edge_candidates[1:-1, 1:-1][mask_135] = 1

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