import cv2
import numpy as np
from PIL import Image, ImageTk
import PySimpleGUI as sg
import os

def sharpen_image(image, intensity):
    kernel = np.array([[0, -1, 0],
                       [-1, 4, -1],
                       [0, -1, 0]]) * intensity
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

def display_images(images):
    num_images = len(images)
    num_cols = 5  # Adjust the number of columns as needed
    num_rows = (num_images + num_cols - 1) // num_cols

    layout = [[sg.Image(key=f'-IMAGE_{i}-') for i in range(j*num_cols, min((j+1)*num_cols, num_images))] for j in range(num_rows)]
    window = sg.Window('Processed Images', layout, finalize=True)

    for i, image in enumerate(images):
        image_tk = ImageTk.PhotoImage(Image.fromarray(image))
        window[f'-IMAGE_{i}-'].update(data=image_tk)

    window.read(close=True)

layout = [
    [sg.Text('Select image folder:'), sg.Input(), sg.FolderBrowse()],
    [sg.Image(key='-IMAGE-')],
    [sg.Slider(range=(0, 10), resolution=0.1, orientation='h', size=(20, 20), key='-SLIDER-', default_value=1)],
    [sg.Button('Process'), sg.Button('Save'), sg.Button('Exit')]
]

window = sg.Window('Image Sharpening', layout, finalize=True)  # Add finalize=True

image_folder = None
processed_images = []

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Process':
        image_folder = values[0]
        if image_folder:
            image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
            processed_images = []
            for image_file in image_files:
                image_path = os.path.join(image_folder, image_file)
                image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
                if image is not None:
                    sharpened_image = sharpen_image(image, values['-SLIDER-'])
                    processed_images.append(sharpened_image)

            display_images(processed_images)

    if event == 'Save':
        if processed_images:
            save_path = sg.popup_get_folder('Select save folder:')
            if save_path:
                for i, image in enumerate(processed_images):
                    filename = f"sharpened_{i+1}_{image_files[i]}"
                    save_path = os.path.join(save_path, filename)
                    cv2.imwrite(save_path, image)
                sg.popup('Images saved successfully!')

window.close()