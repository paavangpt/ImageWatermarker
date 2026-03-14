import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io

# Custom CSS for modern UI
st.markdown("""
<style>
    .main .block-container {
        max-width: 95%;
        padding-left: 0.5rem;
        padding-right: 0.5rem;
    }
    .stSidebar {
        background-color: #f8f9fa;
        border-right: 2px solid #e9ecef;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    h1, h2, h3 {
        color: #343a40;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def hex_to_rgba(hex_color, alpha):
    """Convert hex color to RGBA tuple."""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return rgb + (alpha,)

def add_watermark(img, text, position, font_size, color, opacity, pattern=False, rotation=0, h_gap=20, v_gap=20):
    """Add watermark text to image."""
    img = img.convert("RGBA")
    txt = Image.new("RGBA", img.size, (255, 255, 255, 0))
    
    # Try to load a system font with specified size
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
    except OSError:
        try:
            font = ImageFont.truetype("/Library/Fonts/Arial.ttf", font_size)
        except OSError:
            font = ImageFont.load_default()  # Fallback, but size won't change
    
    fill_color = hex_to_rgba(color, opacity)
    
    # Create base text image
    bbox = ImageDraw.Draw(Image.new("RGBA", (1,1))).textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    if pattern:
        # Repeat watermark as pattern
        spacing_x = text_width + h_gap
        spacing_y = text_height + v_gap
        for x in range(0, img.width, spacing_x):
            for y in range(0, img.height, spacing_y):
                text_img = Image.new("RGBA", (text_width, text_height), (0,0,0,0))
                text_draw = ImageDraw.Draw(text_img)
                text_draw.text((0, 0), text, font=font, fill=fill_color)
                if rotation != 0:
                    text_img = text_img.rotate(rotation, expand=True)
                txt.paste(text_img, (x, y), text_img)
    else:
        # Single watermark at specified position
        text_img = Image.new("RGBA", (text_width, text_height), (0,0,0,0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), text, font=font, fill=fill_color)
        if rotation != 0:
            text_img = text_img.rotate(rotation, expand=True)
        
        new_width, new_height = text_img.size
        
        if position == "center":
            x = (img.width - new_width) // 2
            y = (img.height - new_height) // 2
        elif position == "top-left":
            x, y = 10, 10
        elif position == "top-right":
            x = img.width - new_width - 10
            y = 10
        elif position == "bottom-left":
            x = 10
            y = img.height - new_height - 10
        elif position == "bottom-right":
            x = img.width - new_width - 10
            y = img.height - new_height - 10
        
        txt.paste(text_img, (x, y), text_img)
    
    watermarked = Image.alpha_composite(img, txt)
    return watermarked

# Streamlit UI
st.title("Image Watermarking App")

# Sidebar for configuration
with st.sidebar:
    st.header("📝 Configuration")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "png", "jpeg", "bmp", "gif"])
    watermark_text = st.text_input("Watermark text", "Sample Watermark")
    
    st.subheader("Position & Style")
    position = st.selectbox("Position", ["center", "top-left", "top-right", "bottom-left", "bottom-right"])
    font_size = st.slider("Font size", 10, 100, 50)
    color = st.color_picker("Text color", "#ffffff")
    opacity = st.slider("Opacity", 0, 255, 128)
    rotation = st.slider("Rotation (degrees)", 0, 360, 0)
    
    st.subheader("Pattern Options")
    pattern = st.checkbox("Repeat watermark as pattern")
    h_gap = st.slider("Horizontal gap", 0, 200, 20)
    v_gap = st.slider("Vertical gap", 0, 200, 20)

# Main area for preview
st.header("Preview")
if uploaded_file is not None and watermark_text:
    image = Image.open(uploaded_file)
    
    watermarked_image = add_watermark(image, watermark_text, position, font_size, color, opacity, pattern, rotation, h_gap, v_gap)
    
    st.image(watermarked_image, caption="Watermarked Image", width=800)
    
    # Prepare download
    buf = io.BytesIO()
    watermarked_image.save(buf, format="PNG")
    byte_im = buf.getvalue()
    
    st.download_button(
        label="📥 Download Watermarked Image",
        data=byte_im,
        file_name="watermarked.png",
        mime="image/png"
    )
else:
    st.info("👆 Upload an image and enter watermark text to see the preview.")