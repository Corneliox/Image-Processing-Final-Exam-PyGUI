import PySimpleGUI as sg
import os
from PIL import Image, ImageTk
from io import BytesIO
from utils import load_image, save_image
from sharpening import apply_sharpening
from smoothing import apply_smoothing
from edge_detection import apply_sobel, apply_canny
from segmentation import apply_segmentation

def display_image(window, path):
    try:
        image = Image.open(path)
        image.thumbnail((400, 400))  # Resize for display
        bio = BytesIO()
        image.save(bio, format="PNG")
        window["image_display"].update(data=bio.getvalue())
    except Exception as e:
        sg.popup_error(f"Error displaying image: {str(e)}")

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

    # Ensure output directory exists
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, "Exit"):
            break

        if values["image_path"]:
            image_path = values["image_path"]
            display_image(window, image_path)

        if image_path:
            try:
                if event == "Sharpen":
                    result = apply_sharpening(image_path)
                    save_image(result, os.path.join(output_dir, "sharpened_image.jpg"))
                elif event == "Smooth":
                    result = apply_smoothing(image_path)
                    save_image(result, os.path.join(output_dir, "smoothed_image.jpg"))
                elif event == "Edge Detection":
                    sobel_result = apply_sobel(image_path)
                    canny_result = apply_canny(image_path)
                    save_image(sobel_result, os.path.join(output_dir, "sobel_edges.jpg"))
                    save_image(canny_result, os.path.join(output_dir, "canny_edges.jpg"))
                elif event == "Segment":
                    result = apply_segmentation(image_path)
                    save_image(result, os.path.join(output_dir, "segmented_image.jpg"))
                sg.popup("Processing completed successfully!")
            except Exception as e:
                sg.popup_error(f"Error: {str(e)}")
        else:
            sg.popup_error("Please upload an image first.")

    window.close()

if __name__ == "__main__":
    launch_ui()
