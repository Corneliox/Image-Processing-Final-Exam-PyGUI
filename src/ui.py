import PySimpleGUI as sg
import os
from PIL import Image
from io import BytesIO
import cv2
import numpy as np
from utils import save_image
from sharpening import apply_sharpening
from smoothing import apply_smoothing
from edge_detection import apply_sobel, apply_canny
from segmentation import apply_segmentation

# Function to display images in the GUI
def display_image(window, key, image_data):
    try:
        if isinstance(image_data, str):  # File path
            image = Image.open(image_data)
        else:  # Processed numpy array
            image = Image.fromarray(np.uint8(image_data))
        image.thumbnail((400, 400))  # Resize for display
        bio = BytesIO()
        image.save(bio, format="PNG")
        window[key].update(data=bio.getvalue())
    except Exception as e:
        sg.popup_error(f"Error displaying image: {str(e)}")

# Function to navigate between pages
def switch_page(window, page):
    for p in ["Main", "Sharpening", "Smoothing", "Edge Detection", "Segmentation"]:
        window[f"-PAGE_{p}-"].update(visible=False)
    window[f"-PAGE_{page}-"].update(visible=True)

def launch_ui():
    sg.theme("DarkBlue")
    
    # Layouts for each page
    main_layout = [
        [sg.Text("Image Processing Application", size=(30, 1), justification="center")],
        [sg.Text("Upload an Image:"), sg.Input(), sg.FileBrowse(key="image_path"), sg.Button("Load Image")],
        [sg.Image(key="main_image_display")],
        [sg.Button("Sharpening"), sg.Button("Smoothing"), sg.Button("Edge Detection"), sg.Button("Segmentation")],
        [sg.Exit()]
    ]
    
    sharpening_layout = [
        [sg.Text("Sharpening", size=(30, 1), justification="center")],
        [sg.Image(key="sharpen_input"), sg.Image(key="sharpen_output")],
        [sg.Slider(range=(1, 10), default_value=5, size=(40, 15), orientation="horizontal", key="sharpen_intensity")],
        [sg.Button("Save"), sg.Button("Back")]
    ]
    
    smoothing_layout = [
        [sg.Text("Smoothing", size=(30, 1), justification="center")],
        [sg.Image(key="smooth_input"), sg.Image(key="smooth_output")],
        [sg.Slider(range=(1, 20), default_value=5, size=(40, 15), orientation="horizontal", key="smooth_level")],
        [sg.Button("Save"), sg.Button("Back")]
    ]
    
    edge_detection_layout = [
        [sg.Text("Edge Detection", size=(30, 1), justification="center")],
        [sg.Image(key="edge_input"), sg.Image(key="edge_sobel"), sg.Image(key="edge_canny")],
        [sg.Button("Save Sobel"), sg.Button("Save Canny"), sg.Button("Back")]
    ]
    
    segmentation_layout = [
        [sg.Text("Segmentation", size=(30, 1), justification="center")],
        [sg.Image(key="segment_input"), sg.Image(key="segment_output")],
        [sg.Slider(range=(1, 10), default_value=5, size=(40, 15), orientation="horizontal", key="segment_threshold")],
        [sg.Button("Save"), sg.Button("Back")]
    ]
    
    # Combine all layouts into a single window
    layout = [
        [sg.Column(main_layout, key="-PAGE_Main-", visible=True),
         sg.Column(sharpening_layout, key="-PAGE_Sharpening-", visible=False),
         sg.Column(smoothing_layout, key="-PAGE_Smoothing-", visible=False),
         sg.Column(edge_detection_layout, key="-PAGE_Edge Detection-", visible=False),
         sg.Column(segmentation_layout, key="-PAGE_Segmentation-", visible=False)]
    ]
    
    window = sg.Window("Image Processing Application", layout, finalize=True)
    
    # Image path for processing
    image_path = None

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break
        
        # Navigation
        if event == "Sharpening":
            switch_page(window, "Sharpening")
        elif event == "Smoothing":
            switch_page(window, "Smoothing")
        elif event == "Edge Detection":
            switch_page(window, "Edge Detection")
        elif event == "Segmentation":
            switch_page(window, "Segmentation")
        elif event == "Back":
            switch_page(window, "Main")
        
        # Sharpening Page Logic
        if event == "sharpen_intensity":
            intensity = values["sharpen_intensity"]
            result = apply_sharpening(image_path, intensity=intensity)
            display_image(window, "sharpen_output", result)
        elif event == "Save":
            save_image(result, "output/sharpened_image.jpg")
            sg.popup("Sharpened image saved.")
        
        # Add logic for other pages here...
    
    window.close()

if __name__ == "__main__":
    launch_ui()
