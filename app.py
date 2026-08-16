# ============================================================
# app.py
# AI-Based Wall Color Recommendation & Virtual Painting System
# ============================================================

import os
import numpy as np
import streamlit as st
from PIL import Image

import segmentation

from recommendation import (
    analyze_room_image, 
    recommend_colors
)

from painting import paint_wall

from color_database import (
    ROOM_COLORS,
    ROOM_TYPES,
    INTENSITIES
)


# ============================================================
# YOUR PROJECT DETAILS
# ============================================================
# Replace the values below with your exact details.

PROGRAM_NAME = "Artificial Intelligence Career for Women (AICW)"

TEAM_MEMBERS = [
    {
        "Name": "D.Sowjanya",
        "Email": "dwarapudisowjanya027@gmail.com"
    },
    {
        "Name": "T.Sirisha",
        "Email": "sirishatillapudi@gmail.com"
    },
    {
        "Name": "M.Vijaya Triveni",
        "Email": "malliditriveni2007@gmail.com"
    },
    {
        "Name": "Ch.Himabindu",
        "Email": "ch.himabindu1000@gmail.com"
    }
]

GUIDE_NAME = "Abdul Aziz Md"

COLLEGE_NAME = "VSM College of Engineering"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI-Based Wall Color Recommendation and Virtual Painting System",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "show_application" not in st.session_state:
    st.session_state.show_application = False


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* -------------------------------------------------------
       MAIN PAGE MARGINS
    ------------------------------------------------------- */

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 4rem;
        padding-right: 4rem;
    }


    /* -------------------------------------------------------
       PROFESSIONAL SOFT BACKGROUND
    ------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(
                circle at 10% 10%,
                rgba(70, 100, 140, 0.10),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 20%,
                rgba(90, 130, 150, 0.08),
                transparent 30%
            ),
            linear-gradient(
                135deg,
                #f7f9fc 0%,
                #eef3f7 50%,
                #f8fafc 100%
            );
    }


    /* -------------------------------------------------------
       SIDEBAR
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #eef3f7 0%,
                #e7edf3 100%
            );
        border-right: 1px solid #d6dde5;
    }


    /* -------------------------------------------------------
       SIDEBAR TEXT
    ------------------------------------------------------- */

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #243447;
    }


    /* -------------------------------------------------------
       PROJECT TITLE
    ------------------------------------------------------- */

    .project-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 750;
        color: #203040;
        line-height: 1.2;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }


    .project-subtitle {
        text-align: center;
        font-size: 1.1rem;
        color: #526170;
        margin-bottom: 2rem;
    }


    /* -------------------------------------------------------
       HOME PAGE HERO
    ------------------------------------------------------- */

    .hero-box {
        padding: 2.2rem;
        border-radius: 22px;
        background:
            linear-gradient(
                135deg,
                rgba(255,255,255,0.94),
                rgba(239,244,248,0.94)
            );
        border: 1px solid #d8e0e8;
        box-shadow: 0 10px 30px rgba(30, 50, 70, 0.08);
        margin-bottom: 2rem;
    }


    /* -------------------------------------------------------
       INFORMATION BOX
    ------------------------------------------------------- */

    .info-box {
        padding: 1.3rem 1.5rem;
        border-radius: 16px;
        background: rgba(255,255,255,0.82);
        border: 1px solid #dce3ea;
        margin-bottom: 1.2rem;
    }


    /* -------------------------------------------------------
       FEATURE CARDS
    ------------------------------------------------------- */

    .feature-card {
        padding: 1.2rem;
        border-radius: 15px;
        background: rgba(255,255,255,0.9);
        border: 1px solid #dce3ea;
        min-height: 150px;
        box-shadow: 0 5px 18px rgba(30,50,70,0.05);
    }


    /* -------------------------------------------------------
       START BUTTON
    ------------------------------------------------------- */

    div.stButton > button {
        border-radius: 12px;
        font-weight: 650;
        min-height: 3rem;
    }


    /* -------------------------------------------------------
       RESULT CARDS
    ------------------------------------------------------- */

    .result-title {
        text-align: center;
        font-weight: 700;
        color: #263746;
        margin-bottom: 0.5rem;
    }


    /* -------------------------------------------------------
       SMALL TEXT
    ------------------------------------------------------- */

    .small-muted {
        color: #667585;
        font-size: 0.9rem;
    }


    /* -------------------------------------------------------
       GLOBAL TEXT VISIBILITY
    ------------------------------------------------------- */

    .stApp,
    .stApp p,
    .stApp span,
    .stApp label,
    .stApp div {
        color: #263746;
    }

    .stApp h1,
    .stApp h2,
    .stApp h3,
    .stApp h4,
    .stApp h5,
    .stApp h6 {
        color: #1f2937 !important;
    }

    /* Streamlit markdown text */
    [data-testid="stMarkdownContainer"] {
        color: #263746 !important;
    }

    [data-testid="stMarkdownContainer"] p {
        color: #263746 !important;
    }

    /* Captions */
    [data-testid="stCaptionContainer"] {
        color: #526170 !important;
    }

    /* Selectbox labels */
    [data-testid="stWidgetLabel"] {
        color: #263746 !important;
    }

    [data-testid="stWidgetLabel"] p {
        color: #263746 !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #1f2937 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #526170 !important;
    }

    /* Sidebar text */
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] label {
        color: #263746 !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## Artificial Intelligence Career for Women"
    )

    st.caption(
        "Project Program"
    )

    st.divider()

    st.markdown("### 👥 TEAM MEMBERS")

    for index, member in enumerate(TEAM_MEMBERS, start=1):

        st.markdown(
            f"""
            **{index}. {member["Name"]}**

            <span style="
                color:#667585;
                font-size:0.85rem;
            ">
            {member["Email"]}
            </span>
            """,
            unsafe_allow_html=True
        )

        if index != len(TEAM_MEMBERS):
            st.markdown("")

    st.divider()

    st.markdown("### 👨‍🏫 PROJECT GUIDE")

    st.write(GUIDE_NAME)

    st.divider()

    st.markdown("### 🏛️ COLLEGE")

    st.write(COLLEGE_NAME)

    st.divider()

    if st.session_state.show_application:

        if st.button(
            "← Back to Project Home",
            use_container_width=True
        ):
            st.session_state.show_application = False
            st.rerun()


# ============================================================
# DISPLAY IMAGE WITHOUT DISTORTION
# ============================================================

def resize_display_image(
    image,
    max_width=420,
    max_height=320
):
    """
    Resize only for Streamlit display.

    Original image quality is preserved for
    processing and downloading.

    Aspect ratio is preserved.
    """

    if not isinstance(image, Image.Image):

        image = Image.fromarray(image)

    display_image = image.copy()

    display_image.thumbnail(
        (max_width, max_height),
        Image.Resampling.LANCZOS
    )

    return display_image


# ============================================================
# HOME PAGE
# ============================================================

def show_home_page():

    # --------------------------------------------------------
    # HERO SECTION
    # --------------------------------------------------------

    st.markdown(
       """
       <h1 style="
        font-size: 42px;
        font-weight: 700;
        line-height: 1.2;
        margin-bottom: 10px;
       ">
        🎨 AI-Based Wall Color Recommendation
        <br>
        & Virtual Painting System
        </h1>

       <p style="
        font-size: 18px;
        margin-top: 5px;
        margin-bottom: 25px;
       ">
        Intelligent color selection and realistic
        virtual wall visualization
         </p>
        """,
        unsafe_allow_html=True
    )

    # ========================================================
    # START APPLICATION BUTTON
    # ========================================================

    button_left, button_center, button_right = st.columns(
        [2, 2, 2]
    )

    with button_center:

        if st.button(
            "🚀 Start Application",
            type="primary",
            use_container_width=True
        ):

            st.session_state.show_application = True
            st.rerun()

    st.divider()
    # --------------------------------------------------------
    # PROJECT OVERVIEW
    # --------------------------------------------------------

    st.subheader("📖 Project Overview")

    st.markdown(
        """
        <div class="info-box" style="
            padding: 1.6rem 1.8rem;
            line-height: 1.65;
        ">

        <h3 style="
            margin-top: 0;
            margin-bottom: 0.8rem;
            color: #1f3b4d;
        ">
        🎨 Bringing Your Wall Color Ideas to Life
        </h3>

        <p>
        Choosing the perfect wall color is not always easy. A color
        that looks attractive on a small physical sample may appear
        completely different when applied to an entire room. Lighting,
        furniture, room layout, existing colors, shadows, and wall
        texture can all influence the final appearance. As a result,
        selecting the wrong color can lead to unnecessary repainting,
        additional expense, and wasted time.
        </p>

        <p>
        <b>AI-Based Wall Color Recommendation & Virtual Painting
        System</b> provides a smarter and more visual approach to
        wall-color selection. Instead of relying only on imagination,
        users can upload a photograph of their room or capture one
        directly using the device camera and preview suitable wall
        colors before making an actual painting decision.
        </p>

        <p>
        The system first analyzes the provided room image and
        automatically identifies the wall region using
        <b>semantic image segmentation</b>. It then examines visual
        characteristics such as room brightness and overall color
        tone. Along with the selected room type and preferred paint
        intensity, these characteristics are used to evaluate and
        rank suitable wall colors.
        </p>

        <p>
        The user can explore the recommended color options, select a
        preferred color, and instantly generate a <b>virtual painting
        preview</b>. The selected color is applied only to the detected
        wall region while the system attempts to preserve the original
        lighting, shadows, brightness variations, and wall texture,
        creating a more natural visualization.
        </p>

        <p style="
            margin-bottom: 0;
        ">
        By combining <b>image processing, semantic segmentation,
        visual analysis, color recommendation, suitability scoring,
        and virtual visualization</b>, this application transforms
        wall-color selection into an interactive and convenient
        experience. Users can compare the original room with the
        virtually painted result and make a more confident decision
        before physically painting their walls.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # PROBLEM / SOLUTION
    # --------------------------------------------------------

    st.subheader("🎯 What This System Solves")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
            <div class="feature-card">

            ### 🔍 Color Uncertainty

            Users often find it difficult to imagine how a
            selected wall color will look after painting.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="feature-card">

            ### 🤖 Intelligent Recommendation

            The system analyzes room characteristics and
            ranks suitable colors according to their
            calculated suitability.

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="feature-card">

            ### 🎨 Virtual Visualization

            Users can preview the selected color directly
            on the detected wall before physically painting.

            </div>
            """,
            unsafe_allow_html=True
        )


    st.divider()


    # --------------------------------------------------------
    # KEY FEATURES
    # --------------------------------------------------------

    st.subheader("✨ Key Features")

    features = [
        "📷 Room image upload",
        "📸 Camera image capture",
        "🏠 Room-type selection",
        "☀️ Room brightness analysis",
        "🧠 Automatic wall segmentation",
        "🎨 AI-assisted color recommendation",
        "⭐ Color suitability ranking",
        "🎯 Custom color selection",
        "🖌️ Virtual wall painting",
        "🔄 Original and painted-image comparison",
        "⬇️ Downloadable results"
    ]

    feature_columns = st.columns(3)

    for index, feature in enumerate(features):

        with feature_columns[index % 3]:

            st.markdown(
                f"""
                <div class="info-box">
                {feature}
                </div>
                """,
                unsafe_allow_html=True
            )



# ============================================================
# ACTUAL APPLICATION
# ============================================================

def show_application():

    # --------------------------------------------------------
    # APPLICATION TITLE
    # --------------------------------------------------------

    st.markdown(
        """
        <div class="project-title">
            AI-Based Wall Color Recommendation
            & Virtual Painting System
        </div>

        <div class="project-subtitle">
            Upload or capture a room image and visualize
            suitable wall colors before painting.
        </div>
        """,
        unsafe_allow_html=True
    )


    st.divider()



    # ========================================================
    # IMAGE INPUT
    # ========================================================

    st.subheader("📷 Upload or Capture Room Image")

    upload_tab, camera_tab = st.tabs(
        [
            "📁 Upload Image",
            "📸 Camera"
        ]
    )

    uploaded_file = None

    with upload_tab:

        uploaded_file = st.file_uploader(
            "Choose a room image",
            type=[
                "jpg",
                "jpeg",
                "png"
            ],
            help="Upload a clear image of your room."
        )


    with camera_tab:

        camera_file = st.camera_input(
            "Take a picture of your room"
        )

        if camera_file is not None:

            uploaded_file = camera_file

    # ========================================================
    # ROOM SETTINGS
    # ========================================================

    st.subheader("🏠 Room Settings")

    left, right = st.columns(2)

    with left:

        room_type = st.selectbox(
            "Room Type",
            ROOM_TYPES
        )

    with right:

        intensity = st.selectbox(
            "Paint Intensity",
            INTENSITIES,
            index=2
        )


    st.divider()
        


    # ========================================================
    # NO IMAGE
    # ========================================================

    if uploaded_file is None:

        st.info(
            "💡 Upload a room image or use the camera "
            "to begin the analysis."
        )

        st.divider()

        st.subheader("🔄 Application Workflow")

        workflow = [
            ("1️⃣", "Provide Room Image"),
            ("2️⃣", "Analyze Room"),
            ("3️⃣", "Detect Wall"),
            ("4️⃣", "Recommend Colors"),
            ("5️⃣", "Choose Color"),
            ("6️⃣", "Virtually Paint Wall"),
            ("7️⃣", "Compare Results")
        ]

        workflow_columns = st.columns(4)

        for index, item in enumerate(workflow):

            with workflow_columns[index % 4]:

                st.markdown(
                    f"""
                    <div class="info-box">
                    <h3>{item[0]}</h3>
                    <b>{item[1]}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        return


    # ========================================================
    # LOAD IMAGE
    # ========================================================

    try:

        image = Image.open(
            uploaded_file
        ).convert("RGB")

    except Exception as error:

        st.error(
            f"❌ Unable to read the image: {error}"
        )

        return


    image_array = np.array(image)
    st.success("✅ Step 1: Image uploaded successfully.")


    # ========================================================
    # ORIGINAL IMAGE
    # ========================================================

    st.subheader("🖼️ Original Room Image")

    original_display = resize_display_image(
        image,
        max_width=500,
        max_height=350
    )

    image_left, image_center, image_right = st.columns(
        [1, 2, 1]
    )

    with image_center:

        st.image(
            original_display,
            caption="Uploaded / Captured Room",
            width="stretch"
        )


    st.divider()


    # ========================================================
    # AI ROOM ANALYSIS
    # ========================================================

    with st.spinner(
        "🔍 AI is analyzing your room..."
    ):

        try:

            analysis = analyze_room_image(
                image_array
            )
            st.success("✅ Step 2: Room analysis completed.")

        except Exception as error:

            st.error(
                f"❌ Room analysis failed: {error}"
            )

            return


    st.subheader("📊 AI Room Analysis")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🏠 Room Type",
            room_type
        )

    with c2:

        st.metric(
            "☀️ Brightness",
            analysis["brightness"]
        )

    with c3:

        st.metric(
            "🎨 Room Tone",
            analysis["tone"]
        )


    st.divider()


    # ========================================================
    # WALL DETECTION
    # ========================================================

    with st.spinner(
        "🧠 AI is detecting the wall..."
    ):

        try:

            wall_mask = segmentation.segment_wall(
                image
            )
            st.success("✅ Step 2: Room analysis completed.")

        except Exception as error:

            st.error(
                f"❌ Wall segmentation failed: {error}"
            )

            return


    wall_pixels = np.sum(
        wall_mask > 0
    )

    total_pixels = wall_mask.size

    wall_percentage = (
        wall_pixels /
        total_pixels
    ) * 100


    if wall_pixels == 0:

        st.error(
            "❌ AI could not detect a wall. "
            "Please upload another room image."
        )

        return


    st.success(
        f"✅ Wall detected successfully "
        f"({wall_percentage:.1f}% of image)"
    )

    st.progress(
        min(int(wall_percentage), 100)
    )


    st.divider()


    # ========================================================
    # WALL SEGMENTATION PREVIEW
    # ========================================================

    st.subheader("🧠 Wall Segmentation Result")

    mask_image = Image.fromarray(
        wall_mask
    )

    mask_display = resize_display_image(
        mask_image,
        max_width=500,
        max_height=350
    )

    mask_left, mask_center, mask_right = st.columns(
        [1, 2, 1]
    )

    with mask_center:

        st.image(
            mask_display,
            caption="Detected Wall Region",
            width="stretch"
        )


    st.divider()


    # ========================================================
    # AI COLOR RECOMMENDATION
    # ========================================================

    with st.spinner(
        "🎨 AI is recommending suitable colors..."
    ):

        try:

            recommendations = recommend_colors(
                image_array,
                room_type,
                intensity
            )
            st.success("✅ Step 4: Color recommendation completed.")

        except Exception as error:

            st.error(
                f"❌ Color recommendation failed: {error}"
            )

            return


    if not recommendations:

        st.error(
            "❌ No color recommendations were generated."
        )

        return


    best_color = recommendations[0]

    best_name = best_color["name"]

    best_rgb = best_color["rgb"]

    best_score = best_color["score"]


    # ========================================================
    # BEST COLOR
    # ========================================================

    st.subheader("🤖 AI Recommended Color")

    left, right = st.columns(
        [1, 3]
    )

    with left:

        r, g, b = best_rgb

        st.markdown(
            f"""
            <div style="
                width:120px;
                height:120px;
                background-color:rgb({r},{g},{b});
                border-radius:15px;
                border:2px solid #777;
                margin:auto;
            ">
            </div>
            """,
            unsafe_allow_html=True
        )


    with right:

        st.markdown(
            f"### {best_name}")

        st.write(
            best_color["description"]
        )

        st.success(
            f"Suitability Score: "
            f"{best_score:.1f}/100"
        )


    st.divider()


    # ========================================================
    # ALL COLOR RECOMMENDATIONS
    # ========================================================

    st.subheader("🎨 AI Color Rankings")

    for rank, item in enumerate(
        recommendations,
        start=1
    ):

        col1, col2, col3, col4 = st.columns(
            [0.6, 2, 3, 1]
        )

        with col1:

            st.write(
                f"**{rank}**"
            )

        with col2:

            st.write(
                f"**{item['name']}**"
            )

        with col3:

            r, g, b = item["rgb"]

            st.markdown(
                f"""
                <div style="
                    width:100%;
                    height:28px;
                    background-color:
                        rgb({r},{g},{b});
                    border-radius:6px;
                    border:1px solid #888;
                ">
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:

            st.write(
                f"{item['score']:.1f}/100"
            )


    st.divider()

    # ========================================================
    # COLOR SELECTION
    # ========================================================

    st.subheader(
        "🎨 Choose Your Wall Color"
    )

    st.write(
        "Select one of the AI-recommended colors below "
        "to visualize it on your wall."
    )

    # --------------------------------------------------------
    # RECOMMENDED COLORS ONLY
    # --------------------------------------------------------

    room_color_list = ROOM_COLORS[
        room_type
    ]

    color_names = [
        color[0]
        for color in room_color_list
    ]

    # Find AI recommended color
    if best_name in color_names:

        default_index = color_names.index(
            best_name
        )

    else:

        default_index = 0

    # User selects recommended color
    selected_color_name = st.selectbox(
        "Select a recommended color",
        color_names,
        index=default_index
    )

    # Get RGB of selected color
    selected_color_rgb = next(
        color[1]
        for color in room_color_list
        if color[0] == selected_color_name
    )

    selected_label = selected_color_name

    st.success(
        f"Selected color: {selected_color_name}"
    )

    st.divider()


    # ========================================================
    # PAINT WALL
    # ========================================================

    if st.button(
        "🎨 Paint Wall",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "🎨 Creating realistic virtual painting..."
        ):

            try:

                # AI recommended color
                ai_image = paint_wall(
                    image,
                    wall_mask,
                    best_rgb,
                    strength=0.70
                )

                # User selected recommended color
                selected_image = paint_wall(
                    image,
                    wall_mask,
                    selected_color_rgb,
                    strength=0.70
                )
                st.success("✅ Step 5: Virtual painting completed.")

            except Exception as error:

                st.error(
                    f"❌ Painting failed: {error}"
                )

                return


        # ====================================================
        # SAVE OUTPUTS
        # ====================================================

        os.makedirs(
            "outputs",
            exist_ok=True
        )

        ai_path = os.path.join(
            "outputs",
            "AI_Recommended.jpg"
        )

        selected_path = os.path.join(
            "outputs",
            "Selected_Color.jpg"
        )


        ai_image.save(
            ai_path,
            quality=95
        )

        selected_image.save(
            selected_path,
            quality=95
        )


        st.success(
            "✅ Wall painted successfully!"
        )

        st.divider()


        # ====================================================
        # FINAL RESULTS
        # ====================================================

        st.header(
            "✨ Final Results"
        )

        col1, col2, col3 = st.columns(
            [1, 1, 1],
            gap="large"
        )


        # ----------------------------------------------------
        # ORIGINAL IMAGE
        # ----------------------------------------------------

        with col1:

            st.markdown(
                """
                <div class="result-title">
                🖼️ Original
                </div>
                """,
                unsafe_allow_html=True
            )

            display_original = resize_display_image(
                image,
                max_width=350,
                max_height=280
            )

            st.image(
                display_original,
                width="stretch"
            )


        # ----------------------------------------------------
        # AI RECOMMENDED IMAGE
        # ----------------------------------------------------

        with col2:

            st.markdown(
                """
                <div class="result-title">
                🤖 AI Recommended
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                best_name
            )

            display_ai = resize_display_image(
                ai_image,
                max_width=350,
                max_height=280
            )

            st.image(
                display_ai,
                width="stretch"
            )

            with open(
                ai_path,
                "rb"
            ) as file:

                st.download_button(
                    "⬇️ Download AI Image",
                    file,
                    file_name="AI_Recommended.jpg",
                    mime="image/jpeg",
                    width="stretch"
                )


        # ----------------------------------------------------
        # USER SELECTED IMAGE
        # ----------------------------------------------------

        with col3:

            st.markdown(
                """
                <div class="result-title">
                🎨 Your Selection
                </div>
                """,
                unsafe_allow_html=True
            )

            st.caption(
                selected_label
            )

            display_selected = resize_display_image(
                selected_image,
                max_width=350,
                max_height=280
            )

            st.image(
                display_selected,
                width="stretch"
            )

            with open(
                selected_path,
                "rb"
            ) as file:

                st.download_button(
                    "⬇️ Download Selected Image",
                    file,
                    file_name="Selected_Color.jpg",
                    mime="image/jpeg",
                    width="stretch"
                )

        st.balloons()


# ============================================================
# MAIN CONTROLLER
# ============================================================

if st.session_state.show_application:

    show_application()

else:

    show_home_page()
