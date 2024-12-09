import cv2
import numpy as np
import PySimpleGUI as sg
import os 
from PIL import Image, ImageTk

def kmeans_segmentation(image, num_clusters):
    pixels = image.reshape((-1, 3))
    kmeans = cv2.kmeans(pixels, num_clusters, None, criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0), attempts=10, flags=cv2.KMEANS_RANDOM_CENTERS)
    centers = kmeans[0].round().astype(int)
    labels = kmeans[1].flatten()
    segmented_image = centers[labels].reshape(image.shape)
    return segmented_image

def threshold_segmentation(image, threshold):
    _, thresholded_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY)
    return thresholded_image

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
    [sg.Text('Choose a segmentation method:'),
     sg.Radio('K-Means Clustering', "RADIO1", default=True, key='-KMEANS-'),
     sg.Radio('Thresholding', "RADIO1", key='-THRESHOLD-')],
    [sg.Text('K-Means Clusters (for K-Means):'), sg.Slider(range=(2, 10), default_value=3, orientation='h', key='-KMEANS_CLUSTERS-')],
    [sg.Text('Threshold Value (for Thresholding):'), sg.Slider(range=(0, 255), orientation='h', key='-THRESHOLD_VALUE-')],
    [sg.Image(key='-IMAGE-')],
    [sg.Button('Process'), sg.Button('Save'), sg.Button('Exit')]
]

window = sg.Window('Image Segmentation', layout)

image = None
segmented_image = None

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Exit':
        break

    if event == 'Process':
        filename = values[0]
        if filename:
            image = cv2.imread(filename, cv2.IMREAD_COLOR)
            if image is not None:
                if values['-KMEANS-']:
                    num_clusters = int(values['-KMEANS_CLUSTERS-'])
                    segmented_image = kmeans_segmentation(image, num_clusters)
                else:
                    threshold_value = int(values['-THRESHOLD_VALUE-'])
                    segmented_image = threshold_segmentation(image, threshold_value)

                image_tk = cv2_to_tk(segmented_image)
                window['-IMAGE-'].update(data=image_tk)

    if event == 'Save' and segmented_image is not None:
        save_path = sg.popup_get_folder('Select save folder:')
        if save_path:
            method = 'kmeans' if values['-KMEANS-'] else 'threshold'
            filename = f"{method}_{values[method + '_CLUSTERS' if method == 'kmeans' else '_VALUE']}_{os.path.basename(filename)}"
            save_path = os.path.join(save_path, filename)
            cv2.imwrite(save_path, segmented_image)
            sg.popup('Image saved successfully!')

window.close()