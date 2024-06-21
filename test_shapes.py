from Evaluation import Evaluation
import cv2
import os
import dip
import numpy as np

# test with simple shapes, ground truth computed using Canny

# load of the binary map obtained using the pel algorithm
parent_dir = os.path.dirname(__file__)
image_name = "rhombus"
algo_map_dir = "\\Data\\" + image_name + "\\"
file_name = image_name + "_BEMT.png"
folder_path = parent_dir + algo_map_dir
file_path = parent_dir + algo_map_dir + file_name

BEM_algo = cv2.imread(filename = file_path, flags = cv2.IMREAD_GRAYSCALE)
BEM_algo = np.where(BEM_algo == 14, 0, BEM_algo) # put 0 as background, because PEL background in greyscale is 14
dip.show_image(image = BEM_algo, title = "Binary Edge Map Algo", info = False)

file_path = parent_dir + "\\Data\\rhombus.png"
img = cv2.imread(filename = file_path, flags = cv2.IMREAD_GRAYSCALE)
print(img.shape)

# computation of the ground truth using Canny
# img_filtered = cv2.GaussianBlur(src = img, ksize = (0, 0), sigmaX = 2.0, sigmaY = 0, borderType = cv2.BORDER_DEFAULT)
# BEM_human = cv2.Canny(img_filtered, 20, 40, apertureSize = 3, L2gradient = True)

# computation of the ground truth using Morphological operators
k = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
], np.uint8)
e = np.zeros((img.shape))
d = np.zeros((img.shape))

e = cv2.erode(img, k)
d = cv2.dilate(img, k)

BEM_human = d - e

dip.show_image(image = BEM_human, title = "Binary Edge Map Human", info = False)

f_algo = Evaluation.f_score(BEM_algo, BEM_human)
print("f_score:", f_algo)
mse_algo = Evaluation.mse(BEM_algo, BEM_human)
print("mse:", mse_algo)
epe_algo = Evaluation.epe(BEM_algo, BEM_human)
print("epe:", epe_algo)
acc_algo = Evaluation.accuracy(BEM_algo, BEM_human)
print("accuracy:", acc_algo)
jac_algo = Evaluation.jaccard(BEM_algo, BEM_human)
print("jaccard:", jac_algo)