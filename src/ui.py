import PySimpleGUI as sg
import os
import cv2
from PIL import Image
from io import BytesIO
import numpy as np
from utils import save_image


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


# Image processing functions
def apply_sharpening(image_path, intensity=5):
    image = cv2.imread(image_path)
    kernel = np.array([[0, -1, 0],
                       [-1, intensity, -1],
                       [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)


def apply_smoothing(image_path, intensity=5):
    image = cv2.imread(image_path)
    # Larger kernel size for higher intensity smoothing
    return cv2.GaussianBlur(image, (intensity * 2 + 1, intensity * 2 + 1), 0)


def apply_sobel(image_path):
    image = cv2.imread(image_path, 0)
    return cv2.Sobel(image, cv2.CV_64F, 1, 1, ksize=5)


def apply_canny(image_path):
    image = cv2.imread(image_path, 0)
    return cv2.Canny(image, 100, 200)


def apply_segmentation(image_path, threshold=5):
    image = cv2.imread(image_path)
    data = image.reshape((-1, 3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(data, threshold, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]
    return segmented_image.reshape(image.shape)


# Function to navigate between pages
def switch_page(window, page):
    for p in ["Main", "Sharpening", "Smoothing", "Edge Detection", "Segmentation"]:
        window[f"-PAGE_{p}-"].update(visible=False)
    window[f"-PAGE_{page}-"].update(visible=True)


# Function to save the image
def save_image(image, filename):
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        # Save the image
        cv2.imwrite(filename, image)
    except Exception as e:
        sg.popup_error(f"Error saving image: {str(e)}")


# Function to launch the GUI
def launch_ui():
    sg.theme("DarkBlue")

    # Layouts for each page
    main_layout = [
        [sg.Text("Image Processing Final Exam GUI", size=(30, 1), justification="center")],
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

    window = sg.Window("Image Processing Final Exam GUI", layout, finalize=True)

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

        # Real-time update for Sharpening, Smoothing, and Segmentation sliders
        if event == "sharpen_intensity":
            intensity = values["sharpen_intensity"]
            processed_image = apply_sharpening(image_path, intensity=intensity)
            display_image(window, "sharpen_output", processed_image)

        elif event == "smooth_level":
            intensity = values["smooth_level"]
            processed_image = apply_smoothing(image_path, intensity=intensity)
            display_image(window, "smooth_output", processed_image)

        elif event == "segment_threshold":
            threshold = values["segment_threshold"]
            processed_image = apply_segmentation(image_path, threshold=threshold)
            display_image(window, "segment_output", processed_image)

        # Handling "Save" button event
        elif event == "Save":
            save_name = values["sharpen_save_name"] if 'sharpen' in event else values["smooth_save_name"]
            if save_name:
                save_image(processed_image, save_name)
                sg.popup(f"Image saved as {save_name}")
            else:
                sg.popup_error("Please provide a valid file name.")

        # Handling "Back" button event
        elif event == "Back":
            # Clear processed images and show the original image
            clear_page(window, ["sharpen_input", "sharpen_output", "smooth_input", "smooth_output",
                                "edge_input", "edge_sobel", "edge_canny", "segment_input", "segment_output"])
            switch_page(window, "Main")
            if image_path:
                display_image(window, "main_image_display", image_path)

    window.close()


if __name__ == "__main__":
    launch_ui()
