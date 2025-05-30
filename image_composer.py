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
        900×900 bundle photo.
        • Remove BGs.
        • Keep native size unless a bottle is wider than 430 px or taller than 850 px;
          then shrink proportionally so it fits.
        • Align bottles on the same baseline; no extra lines or shadows.
        """
        processed = []
        MAX_W, MAX_H = 430, 850   # per-bottle limits inside its 450-px half

        for path in image_paths:
            with open(path, "rb") as f:
                img = self.remove_background(f.read())

            ratio = min(1, MAX_W / img.width, MAX_H / img.height)  # ≤1 (never upsizes)
            if ratio < 1:
                new_size = (int(img.width * ratio), int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)

            processed.append(img)

        left, right = processed
        canvas = Image.new("RGBA", (900, 900), (255, 255, 255, 255))

        half_w   = 450
        baseline = 890                      # 10-px bottom margin
        x_left   = (half_w - left.width)  // 2
        x_right  = half_w + (half_w - right.width) // 2
        y_left   = baseline - left.height
        y_right  = baseline - right.height

        canvas.paste(left,  (x_left,  y_left),  left)
        canvas.paste(right, (x_right, y_right), right)

        canvas.convert("RGB").save(output_path, quality=90)
        return output_path
