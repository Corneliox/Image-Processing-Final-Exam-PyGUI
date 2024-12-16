# smoothing.py
import cv2
import numpy as np
from PIL import Image, ImageTk
import PySimpleGUI as sg
import os

def smooth_image(image, intensity): #Smooting using Gausian Blur
    return cv2.GaussianBlur(image, (intensity, intensity), 0)

def cv2_to_tk(image):
    max_width = 1920 * 3 // 4
    max_height = 1080 * 3 // 4
    height, width = image.shape[:2]
    aspect_ratio = width / height
    new_width = min(max_width, int(max_height * aspect_ratio))
    new_height = min(max_height, int(max_width / aspect_ratio))
    resized_image = cv2.resize(image, (new_width, new_height))
    image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)
    return ImageTk.PhotoImage(image)

def main():
    layout = [
        [sg.Text('Select image folder:'), sg.Input(), sg.FolderBrowse()],
        [sg.Image(key='-IMAGE-')],
        [sg.Slider(range=(1, 31), resolution=2, orientation='h', size=(20, 20), key='-SLIDER-', default_value=5)],
        [sg.Button('Process'), sg.Button('Save'), sg.Button('Back'), sg.Button('Exit')]
    ]

    window = sg.Window('Image Smoothing', layout, finalize=True)
    image_folder = None
    processed_images = []

    while True:
        event, values = window.read()

        if event in (sg.WIN_CLOSED, 'Exit'):
            break

        if event == 'Process':
            image_folder = values[0]
            if image_folder:
                image_files = [f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
                processed_images = []
                for image_file in image_files:
                    image_path = os.path.join(image_folder, image_file)
                    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
                    if image is not None:
                        smoothed = smooth_image(image, int(values['-SLIDER-']))
                        processed_images.append(smoothed)
                sg.popup('Processing completed!')

        if event == 'Save':
            if processed_images:
                save_path = sg.popup_get_folder('Select save folder:')
                if save_path:
                    for i, image in enumerate(processed_images):
                        filename = f"smoothed_{i+1}.png"
                        cv2.imwrite(os.path.join(save_path, filename), image)
                    sg.popup('Images saved successfully!')

        if event == 'Back':
            window.close()
            return

    window.close()