import PySimpleGUI as sg
import os
from PIL import Image
from io import BytesIO
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


# Function to clear processed images on a page
def clear_page(window, keys):
    for key in keys:
        window[key].update(data=None)


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
        [sg.Text("Save As:"), sg.Input(default_text="sharpened_image.jpg", key="sharpen_save_name")],
        [sg.Button("Save"), sg.Button("Back")]
    ]

    smoothing_layout = [
        [sg.Text("Smoothing", size=(30, 1), justification="center")],
        [sg.Image(key="smooth_input"), sg.Image(key="smooth_output")],
        [sg.Slider(range=(1, 20), default_value=5, size=(40, 15), orientation="horizontal", key="smooth_level")],
        [sg.Text("Save As:"), sg.Input(default_text="smoothed_image.jpg", key="smooth_save_name")],
        [sg.Button("Save"), sg.Button("Back")]
    ]

    edge_detection_layout = [
        [sg.Text("Edge Detection", size=(30, 1), justification="center")],
        [sg.Image(key="edge_input"), sg.Image(key="edge_sobel"), sg.Image(key="edge_canny")],
        [sg.Text("Save Sobel As:"), sg.Input(default_text="sobel_edges.jpg", key="sobel_save_name")],
        [sg.Text("Save Canny As:"), sg.Input(default_text="canny_edges.jpg", key="canny_save_name")],
        [sg.Button("Save Sobel"), sg.Button("Save Canny"), sg.Button("Back")]
    ]

    segmentation_layout = [
        [sg.Text("Segmentation", size=(30, 1), justification="center")],
        [sg.Image(key="segment_input"), sg.Image(key="segment_output")],
        [sg.Slider(range=(1, 10), default_value=5, size=(40, 15), orientation="horizontal", key="segment_threshold")],
        [sg.Text("Save As:"), sg.Input(default_text="segmented_image.jpg", key="segment_save_name")],
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
    processed_image = None  # For saving the last processed image

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        # Handle image upload
        if event == "Load Image":
            if values["image_path"]:
                image_path = values["image_path"]
                try:
                    # Validate and display the uploaded image
                    display_image(window, "main_image_display", image_path)
                    sg.popup("Image loaded successfully!")
                except Exception as e:
                    sg.popup_error(f"Error loading image: {str(e)}")
            else:
                sg.popup_error("Please select an image to load.")

        # Handle navigation to other pages
        if image_path:
            if event == "Sharpening":
                switch_page(window, "Sharpening")
                display_image(window, "sharpen_input", image_path)
            elif event == "Smoothing":
                switch_page(window, "Smoothing")
                display_image(window, "smooth_input", image_path)
            elif event == "Edge Detection":
                switch_page(window, "Edge Detection")
                display_image(window, "edge_input", image_path)
                sobel_result = apply_sobel(image_path)
                canny_result = apply_canny(image_path)
                display_image(window, "edge_sobel", sobel_result)
                display_image(window, "edge_canny", canny_result)
            elif event == "Segmentation":
                switch_page(window, "Segmentation")
                display_image(window, "segment_input", image_path)
        else:
            sg.popup_error("Please upload an image before proceeding.")

        # Sharpening Logic
        if event == "sharpen_intensity":
            intensity = values["sharpen_intensity"]
            processed_image = apply_sharpening(image_path, intensity=intensity)
            display_image(window, "sharpen_output", processed_image)
        elif event == "Save" and "sharpen_save_name" in values:
            save_image(processed_image, values["sharpen_save_name"])
            sg.popup("Sharpened image saved.")

        # Back button logic: clear images and return to Main
        if event == "Back":
            current_page = [key for key in window.AllKeysDict.keys() if window[key].Visible][0]
            page_name = current_page.replace("-PAGE_", "")
            clear_page(window, [f"{page_name.lower()}_input", f"{page_name.lower()}_output"])
            switch_page(window, "Main")

    window.close()


if __name__ == "__main__":
    launch_ui()
