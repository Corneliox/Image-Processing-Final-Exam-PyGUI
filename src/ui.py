import PySimpleGUI as sg
from utils import load_image, save_image
from sharpening import apply_sharpening
from smoothing import apply_smoothing
from edge_detection import apply_sobel, apply_canny
from segmentation import apply_segmentation

def launch_ui():
    sg.theme("DarkBlue")

    layout = [
        [sg.Text("Image Processing Application", size=(30, 1), justification="center")],
        [sg.Image(key="image_display")],
        [sg.Text("Upload an Image:"), sg.Input(), sg.FileBrowse(key="image_path")],
        [sg.Button("Sharpen"), sg.Button("Smooth"), sg.Button("Edge Detection"), sg.Button("Segment")],
        [sg.Exit()]
    ]

    window = sg.Window("Image Processing Application", layout)

    image_path = None

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if event == "Sharpen":
            result = apply_sharpening(image_path)
            save_image(result, "output/sharpened_image.jpg")
        elif event == "Smooth":
            result = apply_smoothing(image_path)
            save_image(result, "output/smoothed_image.jpg")
        elif event == "Edge Detection":
            sobel_result = apply_sobel(image_path)
            canny_result = apply_canny(image_path)
            save_image(sobel_result, "output/sobel_edges.jpg")
            save_image(canny_result, "output/canny_edges.jpg")
        elif event == "Segment":
            result = apply_segmentation(image_path)
            save_image(result, "output/segmented_image.jpg")
    
    window.close()
