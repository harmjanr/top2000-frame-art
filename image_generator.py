import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

# Constants
OUTPUT_DIR = "resources"
NPO_RADIO2_LOGO = os.path.join(OUTPUT_DIR, "npo_radio2_logo.png")
TOP2000_LOGO = os.path.join(OUTPUT_DIR, "top2000_logo.png")
BACKGROUND_IMAGE = os.path.join(OUTPUT_DIR, "background_cafe.jpg")
DEFAULT_OUTPUT = os.path.join(OUTPUT_DIR, "now_playing.jpg")


def create_now_playing_image(artist, title, cover_url, output_path=None):
    """
    Creates a composite image with album cover as background, logo on top right,
    and artist/title text at the bottom center.
    
    Args:
        artist (str): The artist name
        title (str): The song title
        cover_url (str): URL of the album cover image
        output_path (str): Path where to save the output image (defaults to resources/now_playing.jpg)
    
    Returns:
        str: Path to the saved image
    """
    if output_path is None:
        output_path = DEFAULT_OUTPUT
    
    # Image dimensions
    WIDTH = 3840
    HEIGHT = 2160
    
    # Load background image
    background = Image.open(BACKGROUND_IMAGE)
    
    # Convert RGBA to RGB if necessary (for JPEG compatibility)
    if background.mode == 'RGBA':
        background = background.convert('RGB')
    
    # Resize background to fill the canvas while maintaining aspect ratio
    bg_ratio = background.width / background.height
    target_ratio = WIDTH / HEIGHT
    
    if bg_ratio > target_ratio:
        # Background is wider, scale by height
        new_height = HEIGHT
        new_width = int(HEIGHT * bg_ratio)
    else:
        # Background is taller, scale by width
        new_width = WIDTH
        new_height = int(WIDTH / bg_ratio)
    
    background = background.resize((new_width, new_height), Image.LANCZOS)
    
    # Crop to exact dimensions (center crop)
    left = (new_width - WIDTH) // 2
    top = (new_height - HEIGHT) // 2
    right = left + WIDTH
    bottom = top + HEIGHT
    background = background.crop((left, top, right, bottom))
    
    # Create base image with background
    img = background.copy()
    
    # Download album cover
    response = requests.get(cover_url)
    album_cover = Image.open(BytesIO(response.content))
    
    # Convert RGBA to RGB if necessary
    if album_cover.mode == 'RGBA':
        # Create a white background for transparent images
        rgb_cover = Image.new('RGB', album_cover.size, (255, 255, 255))
        rgb_cover.paste(album_cover, mask=album_cover.split()[3] if len(album_cover.split()) == 4 else None)
        album_cover = rgb_cover
    
    # Scale album cover to full height while maintaining aspect ratio
    cover_height = HEIGHT
    cover_aspect_ratio = album_cover.width / album_cover.height
    cover_width = int(cover_height * cover_aspect_ratio)
    album_cover = album_cover.resize((cover_width, cover_height), Image.LANCZOS)
    
    # Position album cover horizontally centered
    cover_x = (WIDTH - cover_width) // 2
    cover_y = 0
    img.paste(album_cover, (cover_x, cover_y))
    draw = ImageDraw.Draw(img)
    
    # Load and place NPO Radio 2 logo in top right
    try:
        radio2_logo = Image.open(NPO_RADIO2_LOGO)
        # Resize logo to reasonable size (e.g., 320px wide, 20% smaller than before)
        radio2_logo_width = 320
        radio2_aspect_ratio = radio2_logo.height / radio2_logo.width
        radio2_logo_height = int(radio2_logo_width * radio2_aspect_ratio)
        radio2_logo = radio2_logo.resize((radio2_logo_width, radio2_logo_height), Image.LANCZOS)
        
        # Position in top right with more padding
        radio2_logo_x = WIDTH - radio2_logo_width - 80
        radio2_logo_y = 80
        img.paste(radio2_logo, (radio2_logo_x, radio2_logo_y), radio2_logo if radio2_logo.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Warning: Could not load NPO Radio 2 logo: {e}")
    
    # Load and place logo in bottom left (20% bigger)
    logo_width = 600  # Increased from 500 (20% bigger)
    logo_height = 0
    bottom_padding = 80  # Increased padding for more space
    logo_bar_gap = 60  # Space between logo and red bar
    try:
        logo = Image.open(TOP2000_LOGO)
        # Resize logo to reasonable size (e.g., 600px wide, maintaining aspect ratio)
        aspect_ratio = logo.height / logo.width
        logo_height = int(logo_width * aspect_ratio)
        logo = logo.resize((logo_width, logo_height), Image.LANCZOS)
        
        # Position in bottom left with more padding
        logo_x = 40
        logo_y = HEIGHT - logo_height - bottom_padding
        img.paste(logo, (logo_x, logo_y), logo if logo.mode == 'RGBA' else None)
    except Exception as e:
        print(f"Warning: Could not load logo: {e}")
    
    # Add text in the red bar
    text = f"{artist} - {title}"
    
    # Try to load a bold font to calculate text height
    try:
        # Try DejaVu Sans Bold (available in Alpine Linux)
        font = ImageFont.truetype("/usr/share/fonts/ttf-dejavu/DejaVuSans-Bold.ttf", 85)
    except Exception:
        try:
            # macOS Helvetica Bold
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 85, index=1)
        except Exception:
            try:
                # macOS Arial Bold
                font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 85)
            except Exception:
                try:
                    # macOS Helvetica regular
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 85)
                except Exception:
                    print("Warning: Could not load TrueType font, using default")
                    font = ImageFont.load_default()
    
    # Get text bounding box to calculate bar height
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_offset_y = bbox[1]  # Top offset of the text from baseline
    
    # Calculate red bar dimensions with minimal padding and center it on the logo
    text_vertical_padding = 15  # Small padding top and bottom
    bar_height = text_height + (text_vertical_padding * 2)
    bar_x_start = logo_x + logo_width + logo_bar_gap
    bar_y_start = logo_y + (logo_height - bar_height) // 2  # Center on logo
    bar_x_end = WIDTH
    bar_y_end = bar_y_start + bar_height
    
    # Draw red bar with NPO Radio 2 red color
    draw.rectangle([bar_x_start, bar_y_start, bar_x_end, bar_y_end], fill="#DA0D14")
    
    # Position text within the red bar, vertically centered accounting for text offset
    text_x = bar_x_start + 50  # Left padding
    text_y = bar_y_start + (bar_height - text_height) // 2 - text_offset_y
    
    # Draw white text (no outline needed on red background)
    draw.text((text_x, text_y), text, font=font, fill="white")
    
    # Save the image
    img.save(output_path, "JPEG", quality=100)
    
    return output_path