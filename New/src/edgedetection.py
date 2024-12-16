# edgedetection.py
import cv2
import numpy as np
from PIL import Image, ImageTk
import PySimpleGUI as sg
import os

def edge_detection(image):
    return cv2.Canny(image, 100, 200) #Canny

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
        [sg.Image(key='-ORIGINAL-'), sg.Image(key='-EDGES-')],
        [sg.Button('Process'), sg.Button('Save'), sg.Button('Back'), sg.Button('Exit')]
    ]

    window = sg.Window('Edge Detection', layout, finalize=True)
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
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                    if image is not None:
                        original_tk = cv2_to_tk(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))
                        window['-ORIGINAL-'].update(data=original_tk)

                        edges = edge_detection(image)
                        processed_images.append(edges)

                        edges_tk = cv2_to_tk(cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR))
                        window['-EDGES-'].update(data=edges_tk)

                sg.popup('Processing completed!')

        if event == 'Save':
            if processed_images:
                save_path = sg.popup_get_folder('Select save folder:')
                if save_path:
                    for i, image in enumerate(processed_images):
                        filename = f"edges_{i+1}.png"
                        cv2.imwrite(os.path.join(save_path, filename), image)
                    sg.popup('Images saved successfully!')

        if event == 'Back':
            window.close()
            return

    window.close()