"""Generate a luxury wedding invitation OG (Open Graph) image for social media sharing."""

from PIL import Image, ImageDraw, ImageFont
import os

# Dimensions: 1200x630 (standard OG image size)
WIDTH, HEIGHT = 1200, 630

# Colors matching the invitation palette
IVORY = (251, 246, 238)        # #FBF6EE
CHAMPAGNE_GOLD = (201, 166, 107)  # #C9A66B
DARK_EMERALD = (31, 77, 63)     # #1F4D3F
BLUSH = (242, 221, 214)         # #F2DDD6
WHITE = (255, 255, 255)
DARK_GOLD = (160, 120, 60)

# Output path
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "assets", "og-image.png")

def create_og_image():
    # Create base image with ivory background
    img = Image.new("RGB", (WIDTH, HEIGHT), IVORY)
    draw = ImageDraw.Draw(img)

    # Draw a subtle blush gradient border
    border_margin = 40
    draw.rectangle(
        [border_margin, border_margin, WIDTH - border_margin, HEIGHT - border_margin],
        outline=CHAMPAGNE_GOLD,
        width=3
    )

    # Inner border
    inner_margin = 50
    draw.rectangle(
        [inner_margin, inner_margin, WIDTH - inner_margin, HEIGHT - inner_margin],
        outline=CHAMPAGNE_GOLD,
        width=1
    )

    # Corner ornaments (L-shaped gold corners)
    corner_size = 60
    corner_offset = 55
    corner_width = 3

    # Top-left corner
    draw.line([(corner_offset, corner_offset + corner_size), (corner_offset, corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)
    draw.line([(corner_offset, corner_offset), (corner_offset + corner_size, corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)

    # Top-right corner
    draw.line([(WIDTH - corner_offset, corner_offset + corner_size), (WIDTH - corner_offset, corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)
    draw.line([(WIDTH - corner_offset, corner_offset), (WIDTH - corner_offset - corner_size, corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)

    # Bottom-left corner
    draw.line([(corner_offset, HEIGHT - corner_offset - corner_size), (corner_offset, HEIGHT - corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)
    draw.line([(corner_offset, HEIGHT - corner_offset), (corner_offset + corner_size, HEIGHT - corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)

    # Bottom-right corner
    draw.line([(WIDTH - corner_offset, HEIGHT - corner_offset - corner_size), (WIDTH - corner_offset, HEIGHT - corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)
    draw.line([(WIDTH - corner_offset, HEIGHT - corner_offset), (WIDTH - corner_offset - corner_size, HEIGHT - corner_offset)], fill=CHAMPAGNE_GOLD, width=corner_width)

    # Load fonts
    try:
        script_font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-RI.ttf", 72)
    except:
        script_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 72)

    try:
        serif_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 36)
    except:
        serif_font = ImageFont.load_default(size=36)

    try:
        serif_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf", 28)
    except:
        serif_small = ImageFont.load_default(size=28)

    try:
        sans_font = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf", 24)
    except:
        sans_font = ImageFont.load_default(size=24)

    try:
        sans_bold = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-B.ttf", 28)
    except:
        sans_bold = ImageFont.load_default(size=28)

    # "Together with their families" - top text
    top_text = "Together with their families"
    bbox = draw.textbbox((0, 0), top_text, font=sans_font)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 100), top_text, fill=DARK_EMERALD, font=sans_font)

    # Gold divider line above names
    line_y = 155
    line_width = 200
    x1 = (WIDTH - line_width) // 2
    x2 = (WIDTH + line_width) // 2
    draw.line([(x1, line_y), (x2, line_y)], fill=CHAMPAGNE_GOLD, width=2)

    # Small diamond at center of line
    diamond_size = 6
    cx = WIDTH // 2
    draw.polygon([
        (cx, line_y - diamond_size),
        (cx + diamond_size, line_y),
        (cx, line_y + diamond_size),
        (cx - diamond_size, line_y)
    ], fill=CHAMPAGNE_GOLD)

    # Couple names - "Murshida & Muhsin" in script font
    names = "Murshida & Muhsin"
    bbox = draw.textbbox((0, 0), names, font=script_font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text(((WIDTH - tw) // 2, 175), names, fill=DARK_EMERALD, font=script_font)

    # "are getting married" subtitle
    subtitle = "are getting married"
    bbox = draw.textbbox((0, 0), subtitle, font=serif_font)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 300), subtitle, fill=CHAMPAGNE_GOLD, font=serif_font)

    # Gold divider line below names
    line_y2 = 360
    draw.line([(x1, line_y2), (x2, line_y2)], fill=CHAMPAGNE_GOLD, width=2)
    draw.polygon([
        (cx, line_y2 - diamond_size),
        (cx + diamond_size, line_y2),
        (cx, line_y2 + diamond_size),
        (cx - diamond_size, line_y2)
    ], fill=CHAMPAGNE_GOLD)

    # Date
    date_text = "Sunday, 28 March 2027"
    bbox = draw.textbbox((0, 0), date_text, font=sans_bold)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 390), date_text, fill=DARK_EMERALD, font=sans_bold)

    # Time
    time_text = "11:00 AM – 3:00 PM"
    bbox = draw.textbbox((0, 0), time_text, font=serif_small)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 435), time_text, fill=CHAMPAGNE_GOLD, font=serif_small)

    # Venue
    venue_text = "Vista Convention Centre, Malappuram, Kerala"
    bbox = draw.textbbox((0, 0), venue_text, font=serif_small)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 480), venue_text, fill=DARK_EMERALD, font=serif_small)

    # Hashtag at bottom
    hashtag = "#MuhsinAndMurshida"
    bbox = draw.textbbox((0, 0), hashtag, font=sans_font)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 560), hashtag, fill=CHAMPAGNE_GOLD, font=sans_font)

    # Save image
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG", quality=95)
    print(f"OG image saved to: {OUTPUT_PATH}")
    print(f"Image size: {os.path.getsize(OUTPUT_PATH)} bytes")

if __name__ == "__main__":
    create_og_image()
