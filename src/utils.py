import cv2

def load_image(image_path):
    return cv2.imread(image_path)

def save_image(image, output_path):
    cv2.imwrite(output_path, image)
