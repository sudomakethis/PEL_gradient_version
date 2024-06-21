import numpy as np
# import cv2
import os
import dip
import random as rnd

class Dataset:
    def seg2rgb(file_name, height, width):
        parent_dir = os.path.dirname(__file__)
        file_dir = "\\Data\\"
        file = parent_dir + file_dir + file_name + ".seg"

        f = open(file,'r')
        text = f.readlines()

        img = np.ones((height,width), dtype = int)*255

        line = 0
        for line in text[11:]:  # data starts at index 11
            line_text = line.split()
            label = int(line_text[0])
            row = int(line_text[1])
            start_col = int(line_text[2])
            end_col = int(line_text[3])
            img[row, start_col:end_col+1] = label

        RGB_img = np.zeros((img.shape[0], img.shape[1], 3))

        n_labels_line = text[6].split()
        n_labels = int(n_labels_line[1])
        for i in range(0, n_labels):
            index_list = np.argwhere(img == i)
            red = rnd.uniform(0, 1)
            green = rnd.uniform(0, 1)
            blue = rnd.uniform(0, 1)
            for index in index_list:
                RGB_img[index[0], index[1], 0] = red
                RGB_img[index[0], index[1], 1] = green
                RGB_img[index[0], index[1], 2] = blue

        # dip.show_image(image = RGB_img, title = "Segmented image")
        return (RGB_img*255.0).astype(np.uint8)
    
    def get_img_info(file_name):
        parent_dir = os.path.dirname(__file__)
        file_dir = "\\Data\\"
        file = parent_dir + file_dir + file_name + ".seg"

        f = open(file,'r')
        text = f.readlines()

        width_line = text[4].split()
        width = int(width_line[1])
        height_line = text[5].split()
        height = int(height_line[1])

        return height, width
