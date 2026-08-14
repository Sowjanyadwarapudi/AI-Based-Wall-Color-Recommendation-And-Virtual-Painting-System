# ============================================================
# segmentation.py
# AI Based Smart Room Wall Color Recommendation
# Automatic Wall Detection using SegFormer
# ============================================================

import cv2
import numpy as np
import torch
import streamlit as st

from PIL import Image
from transformers import (
    AutoImageProcessor,
    SegformerForSemanticSegmentation
)

# ============================================================
# DEVICE
# ============================================================

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"

# ============================================================
# LOAD MODEL ONLY ONCE
# ============================================================

@st.cache_resource(show_spinner=False)
def load_model():

    print("Loading AI segmentation model...")

    processor = AutoImageProcessor.from_pretrained(
        MODEL_NAME
    )

    model = SegformerForSemanticSegmentation.from_pretrained(
        MODEL_NAME
    )

    model.to(DEVICE)
    model.eval()

    print("Model loaded successfully.")

    return processor, model


# ============================================================
# FIND WALL CLASS
# ============================================================

processor, model = load_model()

id2label = model.config.id2label

label2id = {
    str(label).lower(): int(index)
    for index, label in id2label.items()
}

WALL_CLASS = None

for label, index in label2id.items():

    if label == "wall":
        WALL_CLASS = index
        break

if WALL_CLASS is None:

    for label, index in label2id.items():

        if "wall" in label:

            WALL_CLASS = index
            break

if WALL_CLASS is None:

    raise RuntimeError(
        "Wall class not found in SegFormer model."
    )

print("Wall Class ID:", WALL_CLASS)
# ============================================================
# IMAGE PREPARATION
# ============================================================

def prepare_image(image):
    """
    Convert input image into PIL RGB format.
    """

    if image is None:
        raise ValueError("No image was provided.")

    if isinstance(image, Image.Image):
        return image.convert("RGB")

    image = np.asarray(image)

    if image.ndim != 3:
        raise ValueError("Image must be a color image.")

    if image.shape[2] == 4:
        image = image[:, :, :3]

    return Image.fromarray(
        image.astype(np.uint8)
    ).convert("RGB")


# ============================================================
# AI SEGMENTATION
# ============================================================

def predict_segmentation(image):
    """
    Run SegFormer model and return segmentation map.
    """

    image = prepare_image(image)

    # Load cached model
    processor, model = load_model()

    original_width, original_height = image.size

    inputs = processor(
        images=image,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.inference_mode():

        outputs = model(**inputs)

    logits = outputs.logits

    logits = torch.nn.functional.interpolate(
        logits,
        size=(original_height, original_width),
        mode="bilinear",
        align_corners=False
    )

    segmentation = torch.argmax(
        logits,
        dim=1
    )[0].cpu().numpy()

    # Free memory
    del outputs
    del logits

    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return segmentation
# ============================================================
# CREATE WALL MASK
# ============================================================

def create_wall_mask(segmentation):
    """
    Extract wall pixels from segmentation map.
    """

    mask = np.zeros(
        segmentation.shape,
        dtype=np.uint8
    )

    mask[segmentation == WALL_CLASS] = 255

    return mask


# ============================================================
# CLEAN MASK
# ============================================================

def clean_mask(mask):

    kernel = np.ones((5, 5), np.uint8)

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )

    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    return mask


# ============================================================
# REMOVE SMALL OBJECTS
# ============================================================

def remove_small_regions(mask):

    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cleaned = np.zeros_like(mask)

    image_area = mask.shape[0] * mask.shape[1]

    minimum_area = image_area * 0.01

    for contour in contours:

        if cv2.contourArea(contour) >= minimum_area:

            cv2.drawContours(
                cleaned,
                [contour],
                -1,
                255,
                cv2.FILLED
            )

    return cleaned


# ============================================================
# SMOOTH MASK
# ============================================================

def smooth_mask(mask):

    mask = cv2.GaussianBlur(
        mask,
        (9, 9),
        0
    )

    _, mask = cv2.threshold(
        mask,
        100,
        255,
        cv2.THRESH_BINARY
    )

    return mask


# ============================================================
# MAIN FUNCTION
# ============================================================

def segment_wall(image):

    image = prepare_image(image)

    segmentation = predict_segmentation(image)

    mask = create_wall_mask(segmentation)

    mask = clean_mask(mask)

    mask = remove_small_regions(mask)

    mask = smooth_mask(mask)

    return mask


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("----------------------------------------")
    print("Segmentation module loaded successfully.")
    print("Model cache enabled.")
    print("Automatic wall detection ready.")
    print("----------------------------------------")