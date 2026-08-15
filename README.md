# AI-Based Wall Colour Recommendation and Virtual Painting System

## Project Overview

The **AI-Based Wall Colour Recommendation and Virtual Painting System** is a computer-vision-based application that helps users visualize suitable wall colours before physically painting a room.

The system accepts a room photograph, identifies the wall region, analyses visual characteristics such as brightness, dominant colours, and room context, and recommends multiple suitable wall-colour options. After a colour is selected, the virtual painting module applies the colour to the detected wall region while attempting to preserve important visual details such as wall texture, shadows, furniture, doors, and windows.

The project combines **image preprocessing, wall segmentation, colour analysis, recommendation, and virtual painting** into one workflow.

## Problem Statement

Choosing a wall colour from a physical catalogue can be difficult because the perceived colour changes depending on room lighting, furniture, floor colour, camera exposure, and surrounding surfaces.

Users also want to see how different colours will look on their actual wall before making a painting decision. This project provides an interactive way to explore colour choices using the user's own room image.

## Objectives

- Accept a room image from the user.
- Preprocess the image for consistent processing.
- Identify or segment the wall region.
- Analyse visual features related to colour selection.
- Recommend multiple suitable wall colours.
- Generate a virtual-painted preview for selected colours.
- Allow users to compare different colour options.
- Provide a modular architecture that can be extended in the future.

## Main Features

### 1. Image Upload
The user uploads a photograph of the room.

### 2. Image Preprocessing
The image is prepared for further processing through resizing, normalization, colour-space conversion, and optional noise/contrast adjustment.

### 3. Wall Segmentation
The system identifies the wall region and creates a wall mask. The project architecture includes a segmentation module for detecting the wall and reducing unwanted regions.

### 4. AI-Based Colour Recommendation
The recommendation module analyses room appearance and ranks suitable colour options. Candidate colours can be evaluated using factors such as:

- Brightness
- Contrast
- Existing room colours
- Colour harmony
- User preference

### 5. Virtual Painting
The selected colour is applied only to the wall region. Blending is used so that the preview can retain texture and shading instead of simply replacing the wall with a flat colour.

### 6. Interactive Output
The application displays the original room image, recommended colours, and virtual-painted result so that the user can compare alternatives.

## System Workflow

```text
User
  |
  v
Upload Room Image
  |
  v
Image Preprocessing
  |
  v
Wall Segmentation
  |
  v
Feature Extraction
  |
  v
Colour Recommendation
  |
  v
User Selects Colour
  |
  v
Virtual Painting
  |
  v
Final Preview
```

## Project Modules

| File | Purpose |
|---|---|
| `app.py` | Main application and user interface |
| `recommendation.py` | Analyses the image and recommends suitable colours |
| `segmentation.py` | Detects the wall region and creates the wall mask |
| `painting.py` | Applies the selected colour to the wall and blends the result |
| `color_database.py` | Stores/handles the colour information used by the recommendation system |
| `requirements.txt` | Contains the Python libraries required to run the project |

## Technologies Used

- **Python 3.10** – Core programming language
- **OpenCV** – Image processing and image manipulation
- **NumPy** – Numerical and image-array operations
- **Pillow (PIL)** – Image loading, resizing, and saving
- **scikit-learn** – Optional machine-learning support
- **scikit-image / segmentation models** – Segmentation support
- **Matplotlib** – Visualization and testing
- **Streamlit** – User interface/web application
- **Segmentation model** – Used in the wall-detection architecture

## Colour Recommendation Examples

The system can recommend colours such as:

- Warm White
- Soft Beige
- Dove Grey
- Powder Blue
- Light Grey
- Ivory
- Cream
- Beige
- Soft Grey
- Sky Blue
- Sage Green
- Mint Green
- Peach
- Light Yellow
- Lavender

The recommendation is intended to provide a ranked list rather than a single fixed colour.

## Virtual Painting Method

The virtual painting process uses the detected wall mask. Instead of completely replacing the original pixels, colour blending can be used to preserve texture and shading.

Conceptually:

```text
Output = α × Target Colour + (1 − α) × Original Pixel
```

The operation is applied only to pixels belonging to the wall region.

## Requirements

The project report specifies the following software environment:

- Python 3.10
- OpenCV
- NumPy
- Pillow
- scikit-image / segmentation support
- scikit-learn (optional)
- Matplotlib
- Streamlit

The recommended hardware includes 16 GB RAM and sufficient storage for project libraries and models. A GPU is optional for classical image-processing methods but recommended for deep-learning-based segmentation.

## Installation

1. Clone or download this repository.

2. Open a terminal/Command Prompt in the project folder.

3. Create and activate a Python environment using Python 3.10.

4. Install the required packages:

```bash
pip install -r requirements.txt
```

5. Run the Streamlit application:

```bash
streamlit run app.py
```

6. Upload a room image and follow the application interface to view colour recommendations and virtual-painted previews.

## Expected Output

The application is designed to provide:

1. Original room image
2. Detected wall region
3. Recommended wall colours
4. Virtual-painted previews
5. User-selected colour preview
6. Downloadable/usable preview images where implemented

## Evaluation

The project report proposes evaluating the system using:

| Metric | What it Measures |
|---|---|
| Segmentation Quality | Correctness of the wall mask |
| Colour Recommendation | User preference agreement |
| Visual Quality | Realistic appearance of recolouring |
| Processing Time | Average time required per image |
| Robustness | Performance across different lighting and room layouts |

Possible evaluation measures include IoU/Dice for segmentation, Top-1/Top-3 preference rate for recommendations, user/expert ratings for visual quality, and average processing time.

> **Note:** Final quantitative accuracy and performance values should be added after testing the actual implementation and test images.

## Advantages

- Reduces trial-and-error in wall-colour selection.
- Uses the user's own room photograph.
- Combines colour recommendation and virtual painting in one application.
- Provides quick visual feedback.
- Uses a modular architecture that can be improved or extended.
- Can be developed further as a web, desktop, or mobile application.

## Limitations

- Wall segmentation may be less accurate when walls are partially hidden.
- Similar-looking walls, ceilings, and floors can make segmentation difficult.
- Lighting and camera white balance can change perceived colours.
- 2D recolouring cannot perfectly reproduce real paint behaviour under every lighting and reflection condition.
- Recommendation quality depends on the selected rules, training data, or user feedback.
- Exact matching with commercial paint shade codes requires a calibrated colour reference and verified paint database.

## Future Enhancements

- Improve automatic wall segmentation using modern semantic-segmentation models.
- Add room-type classification such as bedroom, living room, study room, or office.
- Estimate lighting direction and intensity.
- Add controls for brightness, saturation, warmth, and colour families.
- Connect recommended colours with verified paint-brand shade codes.
- Add side-by-side before/after comparison.
- Extend the system to a mobile application with camera-based live preview or AR.
- Collect user feedback for a personalized colour recommendation model.

## Project Team

**VSM College of Engineering**  
**Department of Electronics and Communication Engineering**  
**AICW – Engineer Spoke Project**  
**Academic Year: 2026**

### Team Members

- D. Sowjanya – Team Lead
- Ch.V.V. Himabindu – Team Member
- T. Sirisha – Team Member
- M. Triveni – Team Member

### Project Guide

**Mr. Abdul Aziz MD**

## Conclusion

The AI-Based Wall Colour Recommendation and Virtual Painting System combines computer vision, image processing, colour recommendation, wall segmentation, and virtual painting to help users make better wall-colour decisions.

The system provides an interactive way to preview different colours on a real room image. Its modular design also provides a foundation for future improvements such as stronger segmentation models, lighting analysis, personalized recommendations, paint-brand colour matching, and mobile/AR deployment.

## Repository Structure

```text
AI-Based-Room-Wall-Color-Recommendation-And-Virtual-Painting/
│
├── app.py
├── color_database.py
├── painting.py
├── recommendation.py
├── requirements.txt
├── segmentation.py
└── README.md
```

## Project Status

**Prototype / Academic Project – 2026**

The project documentation describes the architecture, workflow, implementation plan, and evaluation approach. Final performance values should be updated with measurements from the team's actual implementation and test set.
