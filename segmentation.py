# ============================================================
# segmentation.py
# AI-Based Wall Color Recommendation & Virtual Painting System
# Automatic Wall Detection using SegFormer
# Streamlit Cloud Optimized Version
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

# Streamlit Cloud normally runs without a GPU.
# CPU is safer and more predictable for deployment.
DEVICE = "cpu"

MODEL_NAME = "nvidia/segformer-b0-finetuned-ade-512-512"


# ============================================================
# CPU SETTINGS
# ============================================================

# Prevent excessive CPU thread usage when multiple users
# access the application.

torch.set_num_threads(2)

try:
    torch.set_num_interop_threads(1)
except RuntimeError:
    pass


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


# First try exact "wall"
for label, index in label2id.items():

    if label == "wall":

        WALL_CLASS = index
        break


# If exact match is not found, search for labels
# containing the word "wall"

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
# AI SEGMENTATION
# ============================================================

def predict_segmentation(image):
    """
    Run SegFormer model and return segmentation map.
    """

    image = prepare_image(image)

    processor, model = load_model()


    # --------------------------------------------------------
    # LIMIT IMAGE SIZE FOR CLOUD PERFORMANCE
    # --------------------------------------------------------

    original_width, original_height = image.size

    MAX_SIZE = 1024

    if max(
        original_width,
        original_height
    ) > MAX_SIZE:

        scale = MAX_SIZE / max(
            original_width,
            original_height
        )

        new_width = int(
            original_width * scale
        )

        new_height = int(
            original_height * scale
        )

        image = image.resize(
            (new_width, new_height),
            Image.Resampling.LANCZOS
        )


    # --------------------------------------------------------
    # PREPARE MODEL INPUT
    # --------------------------------------------------------

    inputs = processor(
        images=image,
        return_tensors="pt"
    )


    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }


    # --------------------------------------------------------
    # MODEL INFERENCE
    # --------------------------------------------------------

    with torch.inference_mode():

        outputs = model(**inputs)


    logits = outputs.logits


    # --------------------------------------------------------
    # RESTORE MASK TO ORIGINAL IMAGE SIZE
    # --------------------------------------------------------

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


    # --------------------------------------------------------
    # RELEASE TEMPORARY MEMORY
    # --------------------------------------------------------

    del outputs
    del logits
    del inputs


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


    mask[
        segmentation == WALL_CLASS
    ] = 255


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


    minimum_area = image_area * 0.01


    for contour in contours:

        if cv2.contourArea(
            contour
        ) >= minimum_area:

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


    segmentation = predict_segmentation(
        image
    )


    mask = create_wall_mask(
        segmentation
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
        "Streamlit Cloud optimized version."
    )

    print(
        "Automatic wall detection ready."
    )

    print(
        "----------------------------------------"
    )
