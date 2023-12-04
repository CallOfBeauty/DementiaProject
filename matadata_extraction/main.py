from PIL import Image, PngImagePlugin
import exifread
import pandas as pd

def extract_exif_data(image_path):
    with open(image_path, 'rb') as img_file:
        tags = exifread.process_file(img_file, details=False)
        return {tag: tags[tag].values for tag in tags}

def extract_png_textual_info(image):
    """ Extract textual information from PNG files """
    info = {}
    if hasattr(image, 'text'):
        for key, value in image.text.items():
            info[f"PNG Text: {key}"] = value
    return info

def extract_basic_info(image_path):
    with Image.open(image_path) as img:
        info = {
            "File Format": img.format,
            "Image Size": img.size,
            "Color Mode": img.mode,
            "Width (pixels)": img.width,
            "Height (pixels)": img.height
        }

        # Add PNG textual information if available
        if img.format == "PNG":
            info.update(extract_png_textual_info(img))

        # Add other properties from the 'info' dictionary
        for key, value in img.info.items():
            if key not in ["icc_profile", "dpi"]:
                info[f"Image Property: {key}"] = value

    return info

def save_to_excel(info, filename):
    df = pd.DataFrame([info])
    df.to_excel(filename, index=False)

image_path = '/Users/dntentia/PycharmProjects/metadata_extraction/image/image.png'
basic_info = extract_basic_info(image_path)

# Attempt to extract EXIF data if it's a JPEG or TIFF
if basic_info["File Format"] in ["JPEG", "TIFF"]:
    exif_data = extract_exif_data(image_path)
    basic_info.update(exif_data)

save_to_excel(basic_info, 'image_info.xlsx')
