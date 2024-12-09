import cv2

def apply_sobel(image_path):
    image = cv2.imread(image_path, 0)
    return cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=5)

def apply_canny(image_path):
    image = cv2.imread(image_path, 0)
    return cv2.Canny(image, 100, 200)
