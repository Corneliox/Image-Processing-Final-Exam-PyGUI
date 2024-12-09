import cv2

def apply_smoothing(image_path):
    image = cv2.imread(image_path)
    return cv2.GaussianBlur(image, (5, 5), 0)
