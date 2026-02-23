from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Load the original image
img_path = "/mnt/kimi/upload/Berceuse m27-30.png"
img = Image.open(img_path)

# Convert to RGBA to support transparency
img_rgba = img.convert("RGBA")
width, height = img_rgba.size

# Create a transparent overlay for text
overlay = Image.new("RGBA", (width, height), (255, 255, 255, 0))
draw = ImageDraw.Draw(overlay)

# Load fonts
try:
    font_note = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 13
    )
    font_small = ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 11
    )
except Exception:
    font_note = ImageFont.load_default()
    font_small = ImageFont.load_default()

# Define colors with transparency
rh_color = (200, 0, 0, 220)  # Red for RH
lh_color = (0, 0, 180, 220)  # Blue for LH
bg_rh = (255, 220, 220, 150)  # Light red background
bg_lh = (220, 220, 255, 150)  # Light blue background


# Helper function to draw text with background
def draw_note_with_bg(draw_obj, x, y, text, color, bg_color, font):
    # Get text size
    bbox = draw_obj.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Draw background rectangle
    padding = 2
    draw_obj.rectangle(
        [x - padding, y - padding, x + text_width + padding, y + text_height + padding],
        fill=bg_color,
    )

    # Draw text
    draw_obj.text((x, y), text, fill=color, font=font)

    return text_width, text_height


# Measure 27 - Top system positions
m27_rh_notes = [
    (180, "Ab4", 90),
    (240, "C5", 90),
    (300, "Db5", 90),
    (360, "C5", 90),
    (420, "Ab4", 90),
    (480, "C5", 90),
    (540, "Bb4", 90),
    (600, "C5", 90),
    (660, "Ab4", 90),
    (720, "C5", 90),
    (780, "Gb4", 90),
    (840, "C5", 90),
    (900, "F4", 90),
    (960, "Ab4", 90),
    (1020, "Eb4", 90),
    (1080, "Ab4", 90),
]

m27_rh_upper = [
    (180, "F5", 70),
    (240, "F5", 70),
    (300, "F5", 70),
    (360, "F5", 70),
    (420, "F5", 70),
    (480, "F5", 70),
    (540, "Eb5", 70),
    (600, "Eb5", 70),
    (660, "F5", 70),
    (720, "F5", 70),
    (780, "F5", 70),
    (840, "F5", 70),
    (900, "F5", 70),
    (960, "F5", 70),
    (1020, "Gb5", 70),
    (1080, "Gb5", 70),
]

m27_lh_notes = [
    (200, "Db2", 320),
    (380, "Db3", 320),
    (560, "Ab3", 320),
    (740, "Db4", 320),
    (920, "Ab3", 320),
    (1100, "Db3", 320),
]

# Measure 28 - Middle system
m28_rh_notes = [
    (180, "F4", 540),
    (240, "Ab4", 540),
    (300, "Db5", 540),
    (360, "Ab4", 540),
    (420, "F4", 540),
    (480, "Ab4", 540),
    (540, "Eb5", 540),
    (600, "Ab4", 540),
    (660, "F4", 540),
    (720, "Ab4", 540),
    (780, "C5", 540),
    (840, "Ab4", 540),
    (900, "Db5", 540),
    (960, "Ab4", 540),
    (1020, "C5", 540),
    (1080, "Ab4", 540),
]

m28_rh_upper = [
    (180, "Ab5", 520),
    (240, "Ab5", 520),
    (300, "Ab5", 520),
    (360, "Ab5", 520),
    (420, "Ab5", 520),
    (480, "Ab5", 520),
    (540, "Ab5", 520),
    (600, "Ab5", 520),
    (660, "Ab5", 520),
    (720, "Ab5", 520),
    (780, "Ab5", 520),
    (840, "Ab5", 520),
    (900, "Ab5", 520),
    (960, "Ab5", 520),
    (1020, "Ab5", 520),
    (1080, "Ab5", 520),
]

m28_lh_notes = [
    (200, "Db2", 770),
    (380, "Db3", 770),
    (560, "Ab3", 770),
    (740, "Db4", 770),
    (920, "Ab3", 770),
    (1100, "Db3", 770),
]

# Measure 29 - Bottom system (first half)
m29_rh_notes = [
    (180, "Db5", 940),
    (240, "Ab4", 940),
    (300, "C5", 940),
    (360, "Ab4", 940),
    (420, "Db5", 940),
    (480, "Ab4", 940),
    (540, "Eb5", 940),
    (600, "Ab4", 940),
    (660, "Db5", 940),
    (720, "Ab4", 940),
    (780, "C5", 940),
    (840, "Ab4", 940),
    (900, "Bb4", 940),
    (960, "Db5", 940),
    (1020, "Ab4", 940),
    (1080, "Db5", 940),
]

m29_rh_upper = [
    (180, "Ab5", 920),
    (240, "Ab5", 920),
    (300, "Ab5", 920),
    (360, "Ab5", 920),
    (420, "Ab5", 920),
    (480, "Ab5", 920),
    (540, "Gb5", 920),
    (600, "Gb5", 920),
    (660, "F5", 920),
    (720, "F5", 920),
    (780, "F5", 920),
    (840, "F5", 920),
    (900, "F5", 920),
    (960, "F5", 920),
    (1020, "F5", 920),
    (1080, "F5", 920),
]

m29_lh_notes = [
    (200, "Db2", 1170),
    (380, "Db3", 1170),
    (560, "Ab3", 1170),
    (740, "Db4", 1170),
    (920, "Ab3", 1170),
    (1100, "Db3", 1170),
]

# Optional: keep script runnable with a quick preview of the base image
plt.figure(figsize=(12, 8))
plt.imshow(img_rgba)
plt.axis("off")
plt.show()
