# ============================================================
# recommendation.py
# AI-Based Wall Color Recommendation
# Improved Dynamic Color Scoring
# ============================================================

import cv2
import numpy as np

from color_database import ROOM_COLORS


# ============================================================
# 1. ANALYZE ROOM IMAGE
# ============================================================

def analyze_room_image(image):

    if image is None:
        raise ValueError("No image was provided.")

    image = np.asarray(image)

    if image.ndim != 3:
        raise ValueError("Image must be a color image.")

    if image.shape[2] == 4:
        image = image[:, :, :3]

    image = image.astype(np.uint8)

    # --------------------------------------------------------
    # Resize for faster analysis
    # --------------------------------------------------------

    small = cv2.resize(
        image,
        (300, 300)
    )

    # --------------------------------------------------------
    # RGB statistics
    # --------------------------------------------------------

    average_rgb = np.mean(
        small.reshape(-1, 3),
        axis=0
    )

    red = float(average_rgb[0])
    green = float(average_rgb[1])
    blue = float(average_rgb[2])

    # --------------------------------------------------------
    # Brightness
    # --------------------------------------------------------

    gray = cv2.cvtColor(
        small,
        cv2.COLOR_RGB2GRAY
    )

    brightness_value = float(
        np.mean(gray)
    )

    if brightness_value < 80:
        brightness = "Dark"

    elif brightness_value < 170:
        brightness = "Normal"

    else:
        brightness = "Bright"

    # --------------------------------------------------------
    # Image tone
    # --------------------------------------------------------

    if red > blue + 8:
        tone = "Warm"

    elif blue > red + 8:
        tone = "Cool"

    else:
        tone = "Neutral"

    # --------------------------------------------------------
    # Saturation
    # --------------------------------------------------------

    hsv = cv2.cvtColor(
        small,
        cv2.COLOR_RGB2HSV
    )

    saturation_value = float(
        np.mean(hsv[:, :, 1])
    )

    # --------------------------------------------------------
    # Contrast
    # --------------------------------------------------------

    contrast = float(
        np.std(gray)
    )

    return {
        "brightness": brightness,
        "brightness_value": brightness_value,
        "tone": tone,
        "average_rgb": average_rgb,
        "saturation": saturation_value,
        "contrast": contrast
    }


# ============================================================
# 2. COLOR DISTANCE
# ============================================================

def color_distance(room_rgb, color_rgb):

    room_rgb = np.array(
        room_rgb,
        dtype=np.float32
    )

    color_rgb = np.array(
        color_rgb,
        dtype=np.float32
    )

    return float(
        np.linalg.norm(
            room_rgb - color_rgb
        )
    )


# ============================================================
# 3. COLOR BRIGHTNESS
# ============================================================

def get_color_brightness(color_rgb):

    color = np.array(
        color_rgb,
        dtype=np.float32
    )

    return float(
        np.mean(color)
    )


# ============================================================
# 4. DETERMINE COLOR TONE
# ============================================================

def get_color_tone(color_rgb):

    color = np.array(
        color_rgb,
        dtype=np.float32
    )

    red = color[0]
    green = color[1]
    blue = color[2]

    if red > blue + 15:
        return "Warm"

    elif blue > red + 15:
        return "Cool"

    else:
        return "Neutral"


# ============================================================
# 5. GET COLORS FOR ROOM
# ============================================================

def get_room_colors(room_type):

    if room_type in ROOM_COLORS:
        return ROOM_COLORS[room_type]

    return ROOM_COLORS["Living Room"]


# ============================================================
# 6. CALCULATE DYNAMIC COLOR SCORE
# ============================================================

def calculate_color_score(
    color_name,
    color_rgb,
    analysis,
    room_type,
    intensity
):

    color = np.array(
        color_rgb,
        dtype=np.float32
    )

    score = 0.0

    # ========================================================
    # A. BASE ROOM SUITABILITY
    # ========================================================

    # Small base score instead of giving every color 25 points.
    score += 10


    # ========================================================
    # B. ROOM BRIGHTNESS COMPATIBILITY
    # ========================================================

    room_brightness = analysis["brightness_value"]

    color_brightness = get_color_brightness(
        color_rgb
    )

    # Difference between room brightness and color brightness
    brightness_difference = abs(
        room_brightness - color_brightness
    )

    # Continuous score.
    # Similar brightness gets a higher score.
    brightness_score = max(
        0,
        20 - (brightness_difference * 0.12)
    )

    score += brightness_score


    # ========================================================
    # C. BRIGHT ROOM / DARK ROOM BALANCE
    # ========================================================

    if analysis["brightness"] == "Dark":

        # Dark rooms benefit from lighter colors.
        if color_brightness > 200:
            score += 15

        elif color_brightness > 160:
            score += 10

        elif color_brightness > 120:
            score += 5

        else:
            score -= 5


    elif analysis["brightness"] == "Normal":

        # Medium-brightness colors are preferred.
        balance = 20 - abs(
            color_brightness - 175
        ) * 0.08

        score += max(
            0,
            balance
        )


    else:

        # Bright rooms can handle slightly deeper colors.
        balance = 20 - abs(
            color_brightness - 145
        ) * 0.08

        score += max(
            0,
            balance
        )


    # ========================================================
    # D. COLOR TONE HARMONY
    # ========================================================

    color_tone = get_color_tone(
        color_rgb
    )

    room_tone = analysis["tone"]

    if room_tone == "Warm":

        if color_tone == "Warm":
            score += 15

        elif color_tone == "Neutral":
            score += 10

        else:
            score += 5


    elif room_tone == "Cool":

        if color_tone == "Cool":
            score += 15

        elif color_tone == "Neutral":
            score += 10

        else:
            score += 5


    else:

        # Neutral rooms can work well with all tones,
        # but neutral colors get a slight advantage.
        if color_tone == "Neutral":
            score += 12

        else:
            score += 9


    # ========================================================
    # E. ROOM COLOR HARMONY
    # ========================================================

    distance = color_distance(
        analysis["average_rgb"],
        color_rgb
    )

    # Convert distance into a continuous harmony score.
    harmony_score = max(
        0,
        15 - (distance * 0.06)
    )

    score += harmony_score


    # ========================================================
    # F. INTENSITY PREFERENCE
    # ========================================================

    if intensity == "Very Light":

        target = 225

        intensity_score = max(
            0,
            15 - abs(color_brightness - target) * 0.12
        )

        score += intensity_score


    elif intensity == "Light":

        target = 195

        intensity_score = max(
            0,
            15 - abs(color_brightness - target) * 0.12
        )

        score += intensity_score


    elif intensity == "Medium":

        target = 160

        intensity_score = max(
            0,
            15 - abs(color_brightness - target) * 0.12
        )

        score += intensity_score


    elif intensity == "Dark":

        target = 110

        intensity_score = max(
            0,
            15 - abs(color_brightness - target) * 0.12
        )

        score += intensity_score


    elif intensity == "Very Dark":

        target = 75

        intensity_score = max(
            0,
            15 - abs(color_brightness - target) * 0.12
        )

        score += intensity_score


    # ========================================================
    # G. SATURATION COMPATIBILITY
    # ========================================================

    color_hsv = cv2.cvtColor(
        np.uint8([[color]]),
        cv2.COLOR_RGB2HSV
    )

    color_saturation = float(
        color_hsv[0, 0, 1]
    )

    room_saturation = analysis["saturation"]

    saturation_difference = abs(
        room_saturation -
        color_saturation
    )

    saturation_score = max(
        0,
        8 - (saturation_difference * 0.05)
    )

    score += saturation_score


    # ========================================================
    # H. CONTRAST CONSIDERATION
    # ========================================================

    room_contrast = analysis["contrast"]

    if room_contrast > 60:

        # Rooms with strong contrast can accept
        # slightly stronger wall colors.
        if 70 <= color_brightness <= 190:
            score += 5

    elif room_contrast < 30:

        # Low contrast rooms benefit from softer colors.
        if color_brightness > 130:
            score += 5


    # ========================================================
    # I. DARK ROOM LIGHT-COLOR BONUS
    # ========================================================

    if analysis["brightness"] == "Dark":

        if color_brightness > 200:
            score += 5

        elif color_brightness > 170:
            score += 3


    # ========================================================
    # J. FINAL SCORE
    # ========================================================

    score = max(
        0,
        min(
            100,
            score
        )
    )

    return round(
        score,
        2
    )


# ============================================================
# 7. RECOMMEND COLORS
# ============================================================

def recommend_colors(
    image,
    room_type="Living Room",
    intensity="Medium"
):

    # --------------------------------------------------------
    # Analyze uploaded image
    # --------------------------------------------------------

    analysis = analyze_room_image(
        image
    )

    # --------------------------------------------------------
    # Get room-specific colors
    # --------------------------------------------------------

    room_colors = get_room_colors(
        room_type
    )

    results = []

    # --------------------------------------------------------
    # Calculate score for every color
    # --------------------------------------------------------

    for color_name, color_rgb in room_colors:

        score = calculate_color_score(
            color_name,
            color_rgb,
            analysis,
            room_type,
            intensity
        )

        results.append({

            "name": color_name,

            "rgb": color_rgb,

            "description":
                f"{color_name} is evaluated based on "
                f"room brightness, existing color tone, "
                f"color harmony, saturation, contrast and "
                f"selected {intensity.lower()} intensity.",

            "score": score

        })

    # --------------------------------------------------------
    # Highest score first
    # --------------------------------------------------------

    results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return results


# ============================================================
# 8. GET BEST COLOR
# ============================================================

def get_best_color(
    image,
    room_type="Living Room",
    intensity="Medium"
):

    results = recommend_colors(
        image,
        room_type,
        intensity
    )

    return results[0]


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("----------------------------------------")
    print("AI Recommendation System")
    print("----------------------------------------")
    print("Dynamic image analysis: ON")
    print("Brightness analysis: ON")
    print("Warm/Cool tone analysis: ON")
    print("Color harmony scoring: ON")
    print("Saturation analysis: ON")
    print("Contrast analysis: ON")
    print("Intensity scoring: ON")
    print("----------------------------------------")