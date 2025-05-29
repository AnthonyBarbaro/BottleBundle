# image_composer.py

import os
import io
from rembg import remove
from PIL import Image

class ImageComposer:
    def __init__(self, output_size=(1200, 1200)):
        self.output_size = output_size

    def remove_background(self, image_bytes: bytes) -> Image.Image:
        output = remove(image_bytes)
        return Image.open(io.BytesIO(output)).convert("RGBA")

    def create_bundle_image(self, image_paths: list[str], output_path: str):
        """
        Takes a list of 2 image paths, removes backgrounds, places them side-by-side,
        and saves the final 1200×1200 image to output_path.
        """
        images_rgba = []
        for path in image_paths:
            with open(path, 'rb') as f:
                raw_bytes = f.read()
            img_no_bg = self.remove_background(raw_bytes)
            # Scale each bottle to half the width
            bottle = img_no_bg.resize((600, 1200), Image.LANCZOS)
            images_rgba.append(bottle)

        # Create blank white canvas
        combined = Image.new("RGBA", self.output_size, (255, 255, 255, 255))
        # Paste left bottle
        combined.paste(images_rgba[0], (0, 0), images_rgba[0])
        # Paste right bottle
        combined.paste(images_rgba[1], (600, 0), images_rgba[1])

        # Save as RGB (Shopify-friendly)
        final_img = combined.convert("RGB")
        final_img.save(output_path)
        return output_path
