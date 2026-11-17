from PIL import Image, ImageDraw, ImageFont
import os
import math

# Dimensions: 1200x1750 (Vertical Wedding Invitation Size)
WIDTH, HEIGHT = 1200, 1750

# Colors matching the luxury ivory and burgundy/gold palette
IVORY = (251, 246, 238)         # #FBF6EE
CHAMPAGNE_GOLD = (201, 166, 107)  # #C9A66B
DARK_BURGUNDY = (75, 20, 35)      # #4B1423
DARK_TEXT = (50, 40, 35)          # Deep charcoal-brown for high readability
GOLD_LIGHT = (230, 200, 140)
BLUSH_PINK = (220, 175, 175)
ROSE_DEEP = (140, 50, 70)

# Output path
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "assets", "wedding-invitation.png")
FONT_DIR = os.path.join(OUTPUT_DIR, "fonts")

def draw_luxury_frame(draw, margin, color, width=3):
    """Draw an elegant double rectangular frame with decorative corners."""
    draw.rectangle([margin, margin, WIDTH - margin, HEIGHT - margin], outline=color, width=width)
    inner_margin = margin + 12
    draw.rectangle([inner_margin, inner_margin, WIDTH - inner_margin, HEIGHT - inner_margin], outline=color, width=1)

def draw_floral_cluster(draw, cx, cy, scale, flip_h=False, flip_v=False):
    """Draws rich floral and vine cluster decorations in the corners and bottom."""
    hx = -1 if flip_h else 1
    hy = -1 if flip_v else 1

    # Curved background vines
    for offset_angle in range(0, 60, 10):
        vine_points = []
        for t in range(0, 61):
            frac = t / 60
            angle = math.radians(10 + offset_angle + frac * 50)
            r = scale * (0.4 + 0.6 * frac)
            x = cx + r * math.cos(angle) * hx
            y = cy + r * math.sin(angle) * hy
            vine_points.append((x, y))
        for i in range(len(vine_points) - 1):
            draw.line([vine_points[i], vine_points[i+1]], fill=CHAMPAGNE_GOLD, width=1)

    # Multi-layered roses and flower petals
    flower_centers = [
        (cx + 35 * hx, cy + 35 * hy),
        (cx + 70 * hx, cy + 25 * hy),
        (cx + 25 * hx, cy + 75 * hy),
        (cx + 60 * hx, cy + 70 * hy)
    ]
    
    for fx, fy in flower_centers:
        # Outer soft glow/petals
        draw.ellipse([fx - 18, fy - 18, fx + 18, fy + 18], fill=BLUSH_PINK)
        # Mid petals
        draw.ellipse([fx - 12, fy - 12, fx + 12, fy + 12], fill=ROSE_DEEP)
        # Deep center core
        draw.ellipse([fx - 6, fy - 6, fx + 6, fy + 6], fill=DARK_BURGUNDY)
        # Highlight specs
        draw.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=GOLD_LIGHT)

    # Leaves and foliage detail
    for t in range(20, 80, 15):
        frac = t / 100
        lx = cx + scale * frac * hx * 1.2
        ly = cy + scale * frac * hy * 0.8
        draw.polygon([
            (lx, ly), 
            (lx + 12 * hx, ly - 6 * hy), 
            (lx + 18 * hx, ly + 4 * hy)
        ], fill=CHAMPAGNE_GOLD)

def create_invitation_image():
    # Create base image with ivory background
    img = Image.new("RGB", (WIDTH, HEIGHT), IVORY)
    draw = ImageDraw.Draw(img)

    # Ensure font directory exists
    os.makedirs(FONT_DIR, exist_ok=True)

    # Fallback or load truetype fonts (Make sure font files are placed in your 'fonts' folder)
    try:
        script_font = ImageFont.truetype(os.path.join(FONT_DIR, "GreatVibes.ttf"), 95)
        serif_title = ImageFont.truetype(os.path.join(FONT_DIR, "CormorantGaramond-Bold.ttf"), 52)
        serif_bold = ImageFont.truetype(os.path.join(FONT_DIR, "CormorantGaramond-Bold.ttf"), 36)
        serif_regular = ImageFont.truetype(os.path.join(FONT_DIR, "CormorantGaramond-Regular.ttf"), 30)
        serif_italic = ImageFont.truetype(os.path.join(FONT_DIR, "CormorantGaramond-Regular.ttf"), 32)
    except IOError:
        # Fallback to default if custom font files aren't pre-loaded locally
        script_font = serif_bold = serif_regular = serif_italic = serif_title = ImageFont.load_default()

    # --- Outer Frames & Borders ---
    draw_luxury_frame(draw, 50, CHAMPAGNE_GOLD, width=3)

    # --- Rich Floral Corners (Top & Bottom) ---
    draw_floral_cluster(draw, 50, 50, scale=90)                             # Top-Left
    draw_floral_cluster(draw, WIDTH - 50, 50, scale=90, flip_h=True)        # Top-Right
    draw_floral_cluster(draw, 50, HEIGHT - 50, scale=90, flip_v=True)       # Bottom-Left
    draw_floral_cluster(draw, WIDTH - 50, HEIGHT - 50, scale=90, flip_h=True, flip_v=True) # Bottom-Right

    # --- Top Monogram ---
    mono_cx = WIDTH // 2
    mono_cy = 140
    draw.ellipse([mono_cx - 45, mono_cy - 45, mono_cx + 45, mono_cy + 45], fill=DARK_BURGUNDY, outline=CHAMPAGNE_GOLD, width=2)
    
    mono_text = "M & M"
    bbox = draw.textbbox((0, 0), mono_text, font=serif_bold)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((mono_cx - tw // 2, mono_cy - th // 2 - 2), mono_text, fill=CHAMPAGNE_GOLD, font=serif_bold)

    # --- Couple Names (Centered) ---
    names_text = "Muhsin & Murshida"
    bbox = draw.textbbox((0, 0), names_text, font=script_font)
    tw = bbox[2] - bbox[0]
    # Drop shadow for luxury depth
    draw.text(((WIDTH - tw) // 2 + 2, 230 + 2), names_text, fill=GOLD_LIGHT, font=script_font)
    draw.text(((WIDTH - tw) // 2, 230), names_text, fill=DARK_BURGUNDY, font=script_font)

    # --- Invitation Hook / Tagline ---
    tagline_text = "Together with their families,\nrequest the honour of your presence"
    # Render multi-line centered text manually or via multiline
    for i, line in enumerate(tagline_text.split('\n')):
        bbox = draw.textbbox((0, 0), line, font=serif_italic)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, 360 + (i * 40)), line, fill=DARK_TEXT, font=serif_italic)

    # --- Gold Ornamental Divider ---
    div_y = 470
    div_width = 350
    x1 = (WIDTH - div_width) // 2
    x2 = (WIDTH + div_width) // 2
    cx = WIDTH // 2
    draw.line([(x1, div_y), (cx - 20, div_y)], fill=CHAMPAGNE_GOLD, width=2)
    draw.line([(cx + 20, div_y), (x2, div_y)], fill=CHAMPAGNE_GOLD, width=2)
    # Center diamond
    ds = 6
    draw.polygon([(cx, div_y - ds), (cx + ds, div_y), (cx, div_y + ds), (cx - ds, div_y)], fill=CHAMPAGNE_GOLD)

    # --- Event Title (No Walima, Centered) ---
    event_title = "Wedding Ceremony"
    bbox = draw.textbbox((0, 0), event_title, font=serif_title)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 520), event_title, fill=DARK_BURGUNDY, font=serif_title)

    # --- Date & Time ---
    date_text = "Sunday, 28 March 2027"
    bbox = draw.textbbox((0, 0), date_text, font=serif_bold)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 610), date_text, fill=DARK_TEXT, font=serif_bold)

    time_text = "at 11:00 AM"
    bbox = draw.textbbox((0, 0), time_text, font=serif_regular)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 660), time_text, fill=CHAMPAGNE_GOLD, font=serif_regular)

    # --- Venue Details ---
    venue_block = [
        "Vista Convention Centre",
        "Vengad",
    ]
    
    start_y = 750
    for i, line in enumerate(venue_block):
        if not line: 
            continue
        font_to_use = serif_bold if i == 0 else serif_regular
        color_to_use = DARK_BURGUNDY if i == 0 else DARK_TEXT
        bbox = draw.textbbox((0, 0), line, font=font_to_use)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, start_y + (i * 42)), line, fill=color_to_use, font=font_to_use)

    # --- Family Parents Lines ---
    parents_block = [
        "Daughter of Mr. Muhammed & Mrs. Sakeena",
        "Son of Mr. Abdul Majeed & Mrs. Misriyya"
    ]
    
    parent_y = 980
    for i, line in enumerate(parents_block):
        bbox = draw.textbbox((0, 0), line, font=serif_regular)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, parent_y + (i * 40)), line, fill=DARK_TEXT, font=serif_regular)

    forever_text = "With joyful hearts, we invite you to share in the beginning of our forever.\nWith love and gratitude, we begin our forever."
    for i, line in enumerate(forever_text.split('\n')):
        bbox = draw.textbbox((0, 0), line, font=serif_regular)
        tw = bbox[2] - bbox[0]
        draw.text(((WIDTH - tw) // 2, 1210 + (i * 38)), line, fill=DARK_TEXT, font=serif_regular)

    # --- Hashtag ---
    hashtag = "#MuhsinAndMurshida"
    bbox = draw.textbbox((0, 0), hashtag, font=serif_bold)
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 1370), hashtag, fill=CHAMPAGNE_GOLD, font=serif_bold)

    # --- Save Image ---
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    img.save(OUTPUT_PATH, "PNG")
    print(f"Luxury wedding invitation saved successfully to: {OUTPUT_PATH}")

def create_og_image():
    """Convert the Gemini-generated image to an optimized OG sharing thumbnail (1200x630 JPEG, <300KB)."""
    src = os.path.join(OUTPUT_DIR, "vercel", "assets", "Gemini_Generated_Image_r4ojdcr4ojdcr4oj.png")
    dst = os.path.join(OUTPUT_DIR, "assets", "og-image.jpg")
    dst_vercel = os.path.join(OUTPUT_DIR, "vercel", "assets", "og-image.jpg")

    img = Image.open(src).convert("RGB")
    resized = img.resize((1200, 630), Image.LANCZOS)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    resized.save(dst, "JPEG", quality=85, optimize=True)
    size = os.path.getsize(dst)
    print(f"OG image saved to: {dst} ({size} bytes, {resized.size})")

    # Also save to vercel deployment directory
    os.makedirs(os.path.dirname(dst_vercel), exist_ok=True)
    resized.save(dst_vercel, "JPEG", quality=85, optimize=True)
    print(f"OG image saved to: {dst_vercel} ({os.path.getsize(dst_vercel)} bytes)")


if __name__ == "__main__":
    create_invitation_image()
    create_og_image()