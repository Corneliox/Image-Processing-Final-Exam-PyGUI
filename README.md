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
- Python 3.12+
- Libraries: OpenCV, NumPy, PySimpleGUI, Pillow

### **Setup**
1. Clone the repository:
   ```bash
   git clone https://github.com/Corneliox/Image-Processing-Final-Exam-PyGUI.git
   cd Image-Processing-Final-Exam-PyGUI
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
3. Processed image will be saved if you click the `save` button.

---
## **Folder Structure**

The project follows a well-organized folder structure:

```plaintext
Final-Exam-PyGUI/New
├── Image/                    # 
├── src/
│   ├── __pycache__           # Somehow it just Appear??
│   ├── main.py               # Main entry point for the application
│   ├── sharpening.py         # Module for sharpening functionality
│   ├── smoothing.py          # Module for smoothing functionality
│   ├── edgedetection.py      # Module for edge detection
│   ├── imagesegmentation.py  # Module for segmentation
├── .gitignore                # List of ignored files on my local laptop
├── requirements.txt          # List of dependencies
└── README.md                 # Project documentation
```
--- 
## **Preview**
- **Processed Images:** Simply put the parameters and **Click** process to see the differences
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
## **Creator License**
This Project was created by Cornelio Abdimash Christiono | 23.K4.0005, Soegijapranata Satholic University

**Purpose:** Final Examination of Semester 3