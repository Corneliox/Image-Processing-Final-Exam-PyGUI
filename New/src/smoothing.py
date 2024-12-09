import cv2
import numpy as np
from PIL import Image, ImageTk
import PySimpleGUI as sg
import os

def smooth_image(image, sigmaX):
    return cv2.GaussianBlur(image, (0, 0), sigmaX)

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
    [sg.Text('Select image folder:'), sg.Input(), sg.FolderBrowse()],
    [sg.Image(key='-IMAGE-')],
    [sg.Slider(range=(0, 10), resolution=0.1, orientation='h', size=(20, 20), key='-SLIDER-', default_value=1)],
    [sg.Button('Process'), sg.Button('Save'), sg.Button('Exit')]
]

window = sg.Window('Image Smoothing', layout)

image_folder = None
processed_image = None

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Process':
        image_folder = values[0]
        if image_folder:
            image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
            for image_file in image_files:
                image_path = os.path.join(image_folder, image_file)
                image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                if image is not None:
                    smoothed_image = smooth_image(image, values['-SLIDER-'])
                    processed_image = smoothed_image.copy()  # Store the processed image
                    image_tk = cv2_to_tk(smoothed_image)
                    window['-IMAGE-'].update(data=image_tk)

    if event == 'Save' and processed_image is not None:
        save_path = sg.popup_get_folder('Select save folder:')
        if save_path:
            filename = f"smoothed_{values['-SLIDER-']}_{image_file}"
            save_path = os.path.join(save_path, filename)
            cv2.imwrite(save_path, processed_image)
            sg.popup('Image saved successfully!')

window.close()