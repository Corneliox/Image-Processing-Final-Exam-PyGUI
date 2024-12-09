import cv2

def apply_smoothing(image_path, intensity=5):
    image = cv2.imread(image_path)
    # Larger kernel size for higher intensity smoothing
    return cv2.GaussianBlur(image, (intensity * 2 + 1, intensity * 2 + 1), 0)
