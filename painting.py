# ============================================================
# painting.py
# Realistic AI Wall Color Application
# ============================================================

import cv2
import numpy as np

from PIL import Image


# ============================================================
# 1. PREPARE IMAGE
# ============================================================

def prepare_image(image):

    if isinstance(image, Image.Image):

        return np.array(
            image.convert("RGB")
        )

    image = np.asarray(image)

    if image.ndim != 3:
        raise ValueError(
            "Image must be a color image."
        )

    if image.shape[2] == 4:

        image = image[:, :, :3]

    return image.astype(
        np.uint8
    )


# ============================================================
# 2. PREPARE MASK
# ============================================================

def prepare_mask(
    mask,
    image_shape
):

    mask = np.asarray(mask)

    if mask.ndim == 3:

        mask = cv2.cvtColor(
            mask,
            cv2.COLOR_RGB2GRAY
        )

    height, width = image_shape[:2]

    if mask.shape[:2] != (
        height,
        width
    ):

        mask = cv2.resize(
            mask,
            (width, height),
            interpolation=cv2.INTER_LINEAR
        )

    mask = np.clip(
        mask,
        0,
        255
    ).astype(
        np.uint8
    )

    return mask


# ============================================================
# 3. REALISTIC WALL PAINTING
# ============================================================

def paint_wall(
    image,
    mask,
    color,
    strength=0.70
):

    """
    Realistically recolor the detected wall.

    Original lighting, shadows and texture
    are preserved.
    """

    # --------------------------------------------------------
    # Prepare image
    # --------------------------------------------------------

    image = prepare_image(
        image
    )

    # --------------------------------------------------------
    # Prepare mask
    # --------------------------------------------------------

    mask = prepare_mask(
        mask,
        image.shape
    )

    # --------------------------------------------------------
    # Smooth mask
    # --------------------------------------------------------

    alpha = mask.astype(
        np.float32
    ) / 255.0

    alpha = cv2.GaussianBlur(
        alpha,
        (9, 9),
        0
    )

    alpha = np.clip(
        alpha,
        0,
        1
    )

    # --------------------------------------------------------
    # Color strength
    # --------------------------------------------------------

    alpha = alpha * strength

    # --------------------------------------------------------
    # Convert image to LAB
    #
    # LAB separates:
    # L = brightness
    # A/B = color
    #
    # This allows us to change color while
    # preserving original wall brightness.
    # --------------------------------------------------------

    lab = cv2.cvtColor(
        image,
        cv2.COLOR_RGB2LAB
    )

    original_l = (
        lab[:, :, 0]
        .astype(np.float32)
    )

    # --------------------------------------------------------
    # Target RGB color
    # --------------------------------------------------------

    target_rgb = np.array(
        color,
        dtype=np.uint8
    ).reshape(
        1,
        1,
        3
    )

    target_rgb = np.repeat(
        target_rgb,
        image.shape[0],
        axis=0
    )

    target_rgb = np.repeat(
        target_rgb,
        image.shape[1],
        axis=1
    )

    # --------------------------------------------------------
    # Convert target color to LAB
    # --------------------------------------------------------

    target_lab = cv2.cvtColor(
        target_rgb,
        cv2.COLOR_RGB2LAB
    ).astype(
        np.float32
    )

    target_l = target_lab[:, :, 0]

    target_a = target_lab[:, :, 1]

    target_b = target_lab[:, :, 2]

    # --------------------------------------------------------
    # Preserve original wall brightness
    # --------------------------------------------------------

    # Normalize brightness relative to target
    brightness_ratio = (
        original_l /
        np.maximum(
            target_l,
            1
        )
    )

    brightness_ratio = np.clip(
        brightness_ratio,
        0.55,
        1.45
    )

    # Keep original luminance structure
    new_l = (
        target_l *
        brightness_ratio
    )

    new_l = np.clip(
        new_l,
        0,
        255
    )

    # --------------------------------------------------------
    # Create recolored LAB image
    # --------------------------------------------------------

    recolored_lab = np.zeros_like(
        lab,
        dtype=np.float32
    )

    recolored_lab[:, :, 0] = new_l

    recolored_lab[:, :, 1] = target_a

    recolored_lab[:, :, 2] = target_b

    recolored_lab = np.clip(
        recolored_lab,
        0,
        255
    ).astype(
        np.uint8
    )

    # --------------------------------------------------------
    # Convert back to RGB
    # --------------------------------------------------------

    recolored = cv2.cvtColor(
        recolored_lab,
        cv2.COLOR_LAB2RGB
    )

    # --------------------------------------------------------
    # Blend with original
    # --------------------------------------------------------

    alpha_3 = alpha[:, :, np.newaxis]

    result = (
        image.astype(np.float32)
        * (1 - alpha_3)
        +
        recolored.astype(np.float32)
        * alpha_3
    )

    result = np.clip(
        result,
        0,
        255
    ).astype(
        np.uint8
    )

    return Image.fromarray(
        result
    )


# ============================================================
# 4. SAVE IMAGE
# ============================================================

def save_painted_image(
    image,
    output_path
):

    if isinstance(
        image,
        Image.Image
    ):

        image.save(
            output_path
        )

    else:

        Image.fromarray(
            image
        ).save(
            output_path
        )


# ============================================================
# 5. TEST
# ============================================================

if __name__ == "__main__":

    print("----------------------------------------")
    print("Realistic Painting Module")
    print("----------------------------------------")
    print("Wall lighting preservation: ON")
    print("Wall shadow preservation: ON")
    print("Wall texture preservation: ON")
    print("Realistic color blending: ON")
    print("----------------------------------------")