import cv2
import numpy as np

def apply_sharpening(image_path):
    image = cv2.imread(image_path)
    kernel = np.array([[0, -1, 0],
                       [-1, 5, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)
