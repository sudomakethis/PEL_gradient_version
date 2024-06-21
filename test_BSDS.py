from Evaluation import Evaluation
import cv2
import os
import dip
from Dataset import Dataset
import numpy as np

# load of the binary map obtained using the pel algorithm
parent_dir = os.path.dirname(__file__)
image_name = "208001"
algo_map_dir = "\\Data\\" + image_name + "\\"
file_name = image_name + "_BEMT.png"
folder_path = parent_dir + algo_map_dir
file_path = parent_dir + algo_map_dir + file_name

BEM_algo = cv2.imread(filename = file_path, flags = cv2.IMREAD_GRAYSCALE)
dip.show_image(image = BEM_algo, title = "Binary Edge Map Algo", info = False)

# loading of the ground truth taken from the segmentation file .seg of the BSDS Dataset
height, width = Dataset.get_img_info(image_name)
segmented = Dataset.seg2rgb(image_name, height, width)

BEM_human = cv2.Canny(segmented, 20, 40, apertureSize = 3, L2gradient = True)

# computation of the f_score metric for the pel algo
BEM_algo = np.where(BEM_algo == 14, 0, BEM_algo) # put 0 as background, because PEL background in greyscale is 14
print("PEL\n")
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

print("\nCanny\n")

# Canny edge detection
file_path = parent_dir + "\\Data\\" + image_name + ".jpg"
img = cv2.imread(filename = file_path, flags = cv2.IMREAD_GRAYSCALE)
img_filtered = cv2.GaussianBlur(src = img, ksize = (0, 0), sigmaX = 1.5, sigmaY = 0, borderType = cv2.BORDER_DEFAULT)
BEM_Canny = cv2.Canny(img_filtered, 20, 40, apertureSize = 3, L2gradient = True)
dip.show_image(image = BEM_Canny, title = "Binary Edge Map Canny", info = False)

# computation of the f_score metric for the Canny algo
f_Canny = Evaluation.f_score(BEM_Canny, BEM_human)
print("f_score: ", f_Canny)
mse_Canny = Evaluation.mse(BEM_Canny, BEM_human)
print("mse:", mse_Canny)
epe_Canny = Evaluation.epe(BEM_Canny, BEM_human)
print("epe:", epe_Canny)
acc_Canny = Evaluation.accuracy(BEM_Canny, BEM_human)
print("accuracy:", acc_Canny)
jac_Canny = Evaluation.jaccard(BEM_Canny, BEM_human)
print("jaccard:", jac_Canny)