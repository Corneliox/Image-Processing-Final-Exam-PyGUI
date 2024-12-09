# **Image Processing Project**

## **Overview**
This project is a comprehensive image processing application that performs the following tasks:
- Image sharpening
- Smoothing
- Edge detection (using Sobel and Canny methods)
- Image segmentation (using K-means clustering)

The application provides a user-friendly GUI to upload images, adjust parameters, and view the processed results in real-time.

---

## **Features**
1. **Sharpening**
   - Enhances image details using a Laplacian filter.
   - Adjustable sharpening intensity.

2. **Smoothing**
   - Reduces noise in the image using Gaussian blur.
   - Adjustable smoothing intensity.

3. **Edge Detection**
   - Implements both Sobel and Canny methods.
   - Compares results of both methods side by side.

4. **Image Segmentation**
   - Clusters the image into distinct regions using K-means clustering.
   - Adjustable parameters for fine-tuned segmentation.

---

## **Installation**

### **Requirements**
- Python 3.8+
- Libraries: OpenCV, NumPy, PySimpleGUI

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/image-processing-project.git
   cd image-processing-project
2. Install the required dependencies: 
    ```bash
    pip install -r requirements.txt
3. Ensure that your input images are placed in the `data/input/` folder

---
## **Usage**

1. Run the application using Python: 
   ``` bash
   python main.py
2. Use the GUI to: 
   - **Upload an image** from your computer
   - **Select the desired processing step & Adjust parameters** for sharpening, smoothing, edge detection, and image segmentation
   - **View Result**
3. Processed image will be saved automatically in the `data/output/` folder.

---
## **Folder Structure**

The project follows a well-organized folder structure:

```plaintext
Final-Exam-PyGUI/
├── data/
│   ├── input/                # Folder for raw input images
│   └── output/               # Folder for processed images
├── src/
│   ├── main.py               # Main entry point for the application
│   ├── ui.py                 # Handles the user interface logic
│   ├── sharpening.py         # Module for sharpening functionality
│   ├── smoothing.py          # Module for smoothing functionality
│   ├── edge_detection.py     # Module for edge detection
│   ├── segmentation.py       # Module for segmentation
│   └── utils.py              # Utility functions (e.g., image loaders, saving results)
├── tests/                    # Unit tests for each feature
├── requirements.txt          # List of dependencies
└── README.md                 # Project documentation
```
--- 
## **Preview**
- **Original and Processed Images:** View side-by-side comparisons of original and processed images.
- **GUI Features**:
  - Simple, intuitive design for uploading and processing images.
  - Real-time parameter adjustments.

---
## **Algorithm Used**
1. **Sharpening:** 
   - Unsharp masking algorithm to enhance image details.
2. **Smoothing**
   - Gaussian blur for noise reduction while preserving image features.
3. **Edge Detection**
   - **Sobel** : Gradient-based edge detection.
   - **Canny** : Multi-stage edge detection for precise results.
4. **Image Segmentation**
   - K-means clustering to separate the image into distinct regions.

---
## **Testing**

- **Unit Tests:** Ensure each feature works as expected using Python's built-in `unittest` module
- Unit test are provided for each features. To run all tests : 
  ```
  bash
  pytest tests/

--- 
## **License**

-None-