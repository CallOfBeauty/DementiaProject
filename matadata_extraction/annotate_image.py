# annotate_image.py
from PIL import Image, ImageDraw, ImageFont, ImageFile

# Allow loading of truncated/corrupted images if possible
ImageFile.LOAD_TRUNCATED_IMAGES = True


def draw_boxes(image_path, boxes, labels):
    """Draw bounding boxes and labels on the image."""
    with Image.open(image_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.load_default()

        for box, label in zip(boxes, labels):
            draw.rectangle(box, outline="red", width=2)
            draw.text((box[0], box[1]), label, fill="red", font=font)

        img.show()  # Or use img.save("annotated_image.jpg") to save the image
