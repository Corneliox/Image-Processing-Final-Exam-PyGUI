import cv2
import numpy as np
from PIL import Image, ImageTk
import PySimpleGUI as sg

def sharpen_image(image, intensity):
    kernel = np.array([[0, -1, 0],
                       [-1, 5 + intensity, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def cv2_to_tk(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    return image

def load_image():
    filename = sg.popup_get_file('Choose an image', file_types=(("Image Files", "*.jpg;*.jpeg;*.png;*.bmp"),))
    if filename:
        return cv2.imread(filename)
    return None

layout = [
    [sg.Image(key='-IMAGE-')],
    [sg.Slider(range=(0, 10), resolution=0.1, orientation='h', size=(20, 20), key='-SLIDER-', default_value=1)],
    [sg.Button('Upload Image'), sg.Button('Exit')]
]

window = sg.Window('Image Sharpening', layout, finalize=True)

image = None

while True:
    event, values = window.read(timeout=10)

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Upload Image':
        image = load_image()
        if image is not None:
            sharpened_image = sharpen_image(image, values['-SLIDER-'])
            image_tk = cv2_to_tk(sharpened_image)
            window['-IMAGE-'].update(data=image_tk)

    if event == '-SLIDER-' and image is not None:
        sharpened_image = sharpen_image(image, values['-SLIDER-'])
        image_tk = cv2_to_tk(sharpened_image)
        window['-IMAGE-'].update(data=image_tk)

window.close()