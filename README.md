# Image Watermarking App

A simple Streamlit application to add text watermarks to images.

## Features

- Upload any image (JPG, PNG, JPEG, BMP, GIF)
- Add custom text watermark
- Choose watermark position (center, corners)
- Adjust font size, color, and opacity
- Preview original and watermarked images
- Download the watermarked image

## Requirements

- Python 3.7+
- Streamlit
- Pillow

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```
streamlit run app.py
```

Open the provided URL in your browser and start watermarking images!

## How to Use

1. Upload an image using the file uploader
2. Enter the text you want as watermark
3. Select the position for the watermark
4. Adjust font size, color, and opacity as needed
5. View the preview
6. Download the watermarked image

## Notes

- The app uses the default system font. For custom fonts, modify the `add_watermark` function in `app.py`
- Watermarks are added as semi-transparent text overlays