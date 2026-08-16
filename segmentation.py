# ============================================================
# segmentation.py
# AI-Based Wall Color Recommendation & Virtual Painting System
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
# SEGMENTATION IMAGE SIZE
# ============================================================

# The original uploaded image is NOT changed.
# Only a smaller copy is used for AI segmentation.

MAX_SEGMENTATION_SIZE = 768


# ============================================================
# LOAD MODEL ONLY WHEN REQUIRED
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

def get_wall_class(model):

    id2label = model.config.id2label

    label2id = {
        str(label).lower(): int(index)
        for index, label in id2label.items()
    }

    wall_class = None

    for label, index in label2id.items():

        if label == "wall":
            wall_class = index
            break

    if wall_class is None:

        for label, index in label2id.items():

            if "wall" in label:
                wall_class = index
                break

    if wall_class is None:

        raise RuntimeError(
            "Wall class not found in SegFormer model."
        )

    return wall_class


# ============================================================
# IMAGE PREPARATION
# ============================================================

def prepare_image(image):

    if image is None:
        raise ValueError(
            "No image was provided."
        )

    if isinstance(image, Image.Image):

        return image.convert("RGB")

    image = np.asarray(image)

    if image.ndim != 3:

        raise ValueError(
            "Image must be a color image."
        )

    if image.shape[2] == 4:

        image = image[:, :, :3]

    return Image.fromarray(
        image.astype(np.uint8)
    ).convert("RGB")


# ============================================================
# RESIZE IMAGE FOR SEGMENTATION
# ============================================================

def resize_for_segmentation(image):

    image = image.copy()

    original_size = image.size

    width, height = image.size

    largest_dimension = max(
        width,
        height
    )

    if largest_dimension <= MAX_SEGMENTATION_SIZE:

        return image, original_size

    scale = (
        MAX_SEGMENTATION_SIZE /
        largest_dimension
    )

    new_width = int(
        width * scale
    )

    new_height = int(
        height * scale
    )

    resized = image.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS
    )

    return resized, original_size


# ============================================================
# AI SEGMENTATION
# ============================================================

def predict_segmentation(image):

    image = prepare_image(image)

    # --------------------------------------------------------
    # Load model only when required
    # --------------------------------------------------------

    processor, model = load_model()

    wall_class = get_wall_class(model)

    # --------------------------------------------------------
    # Keep original size
    # --------------------------------------------------------

    original_width, original_height = image.size

    # --------------------------------------------------------
    # Create smaller image ONLY for segmentation
    # --------------------------------------------------------

    segmentation_image, _ = resize_for_segmentation(
        image
    )

    segmentation_width, segmentation_height = (
        segmentation_image.size
    )

    # --------------------------------------------------------
    # Prepare model input
    # --------------------------------------------------------

    inputs = processor(
        images=segmentation_image,
        return_tensors="pt"
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    # --------------------------------------------------------
    # Run SegFormer
    # --------------------------------------------------------

    with torch.inference_mode():

        outputs = model(
            **inputs
        )

    logits = outputs.logits

    # --------------------------------------------------------
    # Resize segmentation to the SMALL image size
    # --------------------------------------------------------

    logits = torch.nn.functional.interpolate(
        logits,
        size=(
            segmentation_height,
            segmentation_width
        ),
        mode="bilinear",
        align_corners=False
    )

    segmentation = torch.argmax(
        logits,
        dim=1
    )[0].cpu().numpy()

    # --------------------------------------------------------
    # Create wall mask
    # --------------------------------------------------------

    mask = np.zeros(
        (
            segmentation_height,
            segmentation_width
        ),
        dtype=np.uint8
    )

    mask[
        segmentation == wall_class
    ] = 255

    # --------------------------------------------------------
    # Resize mask back to ORIGINAL image size
    # --------------------------------------------------------

    mask = cv2.resize(
        mask,
        (
            original_width,
            original_height
        ),
        interpolation=cv2.INTER_NEAREST
    )

    # --------------------------------------------------------
    # Free memory
    # --------------------------------------------------------

    del outputs
    del logits

    if torch.cuda.is_available():

        torch.cuda.empty_cache()

    return mask


# ============================================================
# CLEAN MASK
# ============================================================

def clean_mask(mask):

    kernel = np.ones(
        (5, 5),
        np.uint8
    )

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

    image_area = (
        mask.shape[0] *
        mask.shape[1]
    )

    minimum_area = (
        image_area * 0.01
    )

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

    mask = predict_segmentation(
        image
    )

    mask = clean_mask(
        mask
    )

    mask = remove_small_regions(
        mask
    )

    mask = smooth_mask(
        mask
    )

    return mask


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "----------------------------------------"
    )

    print(
        "Segmentation module loaded successfully."
    )

    print(
        "Model cache enabled."
    )

    print(
        "Automatic wall detection ready."
    )

    print(
        "----------------------------------------"
    )
