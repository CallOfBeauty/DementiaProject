# image_analysis.py
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input, decode_predictions
from PIL import Image, ImageFile
import numpy as np
import annotate_image

ImageFile.LOAD_TRUNCATED_IMAGES = True

def load_and_prep_image(image_path, target_size=(224, 224)):
    """Load and prepare an image for analysis."""
    img = Image.open(image_path).convert('RGB')
    img = img.resize(target_size)
    img = np.array(img)
    img = preprocess_input(img)
    img = np.expand_dims(img, axis=0)
    return img

def model_predict(image_path, model):
    """Use a pre-trained model to predict the contents of an image."""
    img = load_and_prep_image(image_path)
    preds = model.predict(img)
    return decode_predictions(preds, top=5)[0]

def integrate_user_descriptions(predictions, user_descriptions):
    """Integrate user descriptions with model predictions."""
    user_words = set(user_descriptions.lower().split())
    integrated_data = {}

    for _, label, score in predictions:
        label_words = set(label.lower().replace('_', ' ').split())
        common_words = user_words.intersection(label_words)
        if common_words:
            integrated_data[label] = {
                "Model Confidence": f"{score:.2f}",
                "Related User Words": list(common_words)
            }

    return integrated_data

# Load the pre-trained ResNet50 model
model = ResNet50(weights="imagenet")

# Replace 'your_image.jpg' with your image file
image_path = '/Users/dntentia/PycharmProjects/metadata_extraction/image/image.png'
predictions = model_predict(image_path, model)

# User input for additional descriptions
user_descriptions = input("Enter your descriptions of the image: ")

# Integrate model predictions with user descriptions
integrated_info = integrate_user_descriptions(predictions, user_descriptions)
print("Integrated Data:", integrated_info)

# Placeholder for bounding box data
# This needs to be replaced with actual object detection data
boxes_example = [(100, 100, 200, 200), (300, 300, 400, 400)]
labels_example = [label for _, label, _ in predictions]

# Call the function from annotate_image.py to draw bounding boxes
annotate_image.draw_boxes(image_path, boxes_example, labels_example)
