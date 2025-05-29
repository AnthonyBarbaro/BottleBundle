from rembg import remove
from PIL import Image
import numpy as np
import io
import os

class BackgroundCleaner:
    def __init__(self, colors_to_remove=None):
        self.colors_to_remove = colors_to_remove or []

    def remove_background(self, image_path):
        with open(image_path, 'rb') as i:
            input_image = i.read()
        output_image = remove(input_image)
        image = Image.open(io.BytesIO(output_image)).convert("RGBA")
        return image

    def remove_specific_colors(self, image):
        if not self.colors_to_remove:
            return image

        data = np.array(image)
        mask = np.zeros(data.shape[:2], dtype=bool)

        for color in self.colors_to_remove:
            mask |= np.all(data[:, :, :3] == color, axis=-1)

        data[mask] = [255, 255, 255, 0]
        return Image.fromarray(data, 'RGBA')

    def add_white_background(self, image):
        white_bg = Image.new('RGBA', image.size, (255, 255, 255, 255))
        white_bg.paste(image, (0, 0), image)
        return white_bg.convert('RGB')  # RGB for Shopify compatibility

# Directories
input_dir = 'cleam'  # Update path if needed
output_dir = 'cleaned'  # Output path

# Ensure output folder exists
os.makedirs(output_dir, exist_ok=True)

# Colors to be made transparent (optional)
colors_to_remove = [(243, 244, 238), (236, 235, 235)]

# Initialize cleaner
cleaner = BackgroundCleaner(colors_to_remove=colors_to_remove)

# Process images
for filename in os.listdir(input_dir):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        try:
            image = cleaner.remove_background(input_path)
            image = cleaner.remove_specific_colors(image)
            image = cleaner.add_white_background(image)
            image.save(output_path)
            print(f"✅ Saved cleaned image: {output_path}")
        except Exception as e:
            print(f"❌ Failed on {filename}: {e}")

print("🎉 Background cleaning complete.")
