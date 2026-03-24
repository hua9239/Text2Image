import hashlib
import os
from pathlib import Path
from io import BytesIO

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import StreamingResponse
from PIL import Image, ImageDraw, ImageFont

# Initialize FastAPI application
app = FastAPI(title="Text2Image API")

# Directory for caching generated images
GENERATED_IMAGES_DIR = Path("./generated_images")
GENERATED_IMAGES_DIR.mkdir(exist_ok=True)

# Font paths for different systems (Linux, macOS, Windows)
FONT_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
    "/System/Library/Fonts/PingFang.ttc",
    "C:\\Windows\\Fonts\\msjh.ttc",
]

# Image generation configuration
FONT_SIZE = 72
IMAGE_HEIGHT = 100
PADDING = 20
TEXT_COLOR = "#FFFFFF"      # White text
STROKE_COLOR = "#000000"    # Black outline
STROKE_WIDTH = 3


def get_system_font():
    """Load CJK-compatible font from system paths"""
    for font_path in FONT_PATHS:
        if os.path.exists(font_path):
            try:
                font = ImageFont.truetype(font_path, FONT_SIZE)
                print(f"[+] Font loaded: {font_path}")
                return font
            except Exception as e:
                print(f"[-] Font load failed ({font_path}): {e}")
                continue
    
    print("[*] Warning: CJK font not found, using default font")
    print("[*] Please ensure font package is installed: apt-get install fonts-noto-cjk")
    return ImageFont.load_default()


try:
    FONT = get_system_font()
except Exception as e:
    print(f"[-] Critical font loading error: {e}")
    FONT = ImageFont.load_default()


def calculate_text_hash(text: str) -> str:
    """Generate SHA256 hash for text caching"""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_text_bbox(font, text):
    """Calculate text bounding box for proper sizing"""
    temp_img = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    draw = ImageDraw.Draw(temp_img)
    bbox = draw.textbbox((0, 0), text, font=font, stroke_width=STROKE_WIDTH)
    return bbox


def generate_image(text: str) -> BytesIO:
    """Generate PNG image with text and stroke outline"""
    bbox = get_text_bbox(FONT, text)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    canvas_width = text_width + (PADDING * 2)
    
    # Create transparent background image
    img = Image.new("RGBA", (canvas_width, IMAGE_HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Center text horizontally and vertically
    x = (canvas_width - text_width) / 2 - bbox[0]
    y = (IMAGE_HEIGHT - text_height) / 2 - bbox[1]
    
    # Draw text with stroke outline
    draw.text(
        (x, y),
        text,
        font=FONT,
        fill=TEXT_COLOR,
        stroke_width=STROKE_WIDTH,
        stroke_fill=STROKE_COLOR
    )
    
    img_io = BytesIO()
    img.save(img_io, format="PNG")
    img_io.seek(0)
    
    return img_io


@app.get("/")
async def root():
    return {
        "service": "Text2Image API",
        "version": "1.0.0",
        "usage": "GET /image?text=your_text"
    }


@app.get("/image")
async def create_image(text: str = Query(..., max_length=100)):
    """Main endpoint: Generate or return cached text image"""
    try:
        text_hash = calculate_text_hash(text)
        cache_path = GENERATED_IMAGES_DIR / f"{text_hash}.png"
        
        # Return cached image if exists
        if cache_path.exists():
            print(f"[+] Cache hit: {text_hash}.png")
            with open(cache_path, "rb") as f:
                img_io = BytesIO(f.read())
        else:
            print(f"[*] Generating new image: {text[:20]}... (hash: {text_hash})")
            img_io = generate_image(text)
            
            with open(cache_path, "wb") as f:
                f.write(img_io.getvalue())
            
            img_io.seek(0)
        
        return StreamingResponse(
            img_io,
            media_type="image/png",
            headers={
                "Content-Disposition": f'inline; filename="{text_hash}.png"',
            }
        )
    
    except Exception as e:
        print(f"[-] Image generation error: {e}")
        raise HTTPException(status_code=500, detail=f"Image generation failed: {str(e)}")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)
