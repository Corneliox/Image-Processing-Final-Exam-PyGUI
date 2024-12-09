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
    # Calculate maximum dimensions for 3/4 screen size
    max_width = 1920 * 3 // 4
    max_height = 1080 * 3 // 4

    # Resize the image to fit within the maximum dimensions
    height, width = image.shape[:2]
    aspect_ratio = width / height
    new_width = min(max_width, int(max_height * aspect_ratio))
    new_height = min(max_height, int(max_width / aspect_ratio))
    resized_image = cv2.resize(image, (new_width, new_height))

    image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    return image

layout = [
    [sg.Text('Select an image:'), sg.Input(), sg.FileBrowse()],
    [sg.Image(key='-IMAGE-')],
    [sg.Slider(range=(0, 10), resolution=0.1, orientation='h', size=(20, 20), key='-SLIDER-', default_value=1)],
    [sg.Button('Process'), sg.Button('Exit')]
]

window = sg.Window('Image Sharpening', layout)

image = None

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Process':
        filename = values[0]
        if filename:
            image = cv2.imread(filename, cv2.IMREAD_UNCHANGED)
            if image is not None:
                sharpened_image = sharpen_image(image, values['-SLIDER-'])
                image_tk = cv2_to_tk(sharpened_image)
                window['-IMAGE-'].update(data=image_tk)

window.close()