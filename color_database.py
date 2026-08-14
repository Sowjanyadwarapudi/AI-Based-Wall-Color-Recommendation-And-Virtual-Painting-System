# ============================================================
# color_database.py
# AI-Based Wall Color Recommendation & Virtual Painting System
# ============================================================


# ============================================================
# ROOM COLORS
# ============================================================

ROOM_COLORS = {

    # --------------------------------------------------------
    # LIVING ROOM
    # --------------------------------------------------------

    "Living Room": [

        # 5 DECENT / LIGHT COLORS
        ("Ivory", (255, 255, 240)),
        ("Cream", (255, 253, 208)),
        ("Warm White", (250, 245, 230)),
        ("Light Beige", (245, 235, 210)),
        ("Soft Grey", (211, 211, 211)),

        # 5 MODERATE COLORS
        ("Sage Green", (156, 175, 136)),
        ("Dusty Blue", (126, 153, 173)),
        ("Terracotta", (203, 126, 94)),
        ("Muted Peach", (230, 170, 150)),
        ("Olive Green", (128, 128, 70)),

        # 5 DARK COLORS
        ("Navy Blue", (35, 55, 90)),
        ("Forest Green", (34, 80, 50)),
        ("Chocolate Brown", (90, 55, 35)),
        ("Charcoal Grey", (55, 60, 65)),
        ("Deep Teal", (20, 80, 85)),
    ],


    # --------------------------------------------------------
    # BEDROOM
    # --------------------------------------------------------

    "Bedroom": [

        # 5 DECENT / LIGHT
        ("Pearl White", (245, 245, 240)),
        ("Blush Pink", (245, 210, 215)),
        ("Lavender Mist", (220, 210, 235)),
        ("Light Blue", (190, 220, 235)),
        ("Pale Green", (200, 225, 200)),

        # 5 MODERATE
        ("Dusty Rose", (180, 120, 130)),
        ("Mauve", (170, 130, 155)),
        ("Sage Green", (156, 175, 136)),
        ("Muted Blue", (100, 140, 170)),
        ("Warm Taupe", (170, 145, 120)),

        # 5 DARK
        ("Deep Plum", (75, 35, 70)),
        ("Midnight Blue", (25, 40, 75)),
        ("Dark Forest Green", (25, 65, 40)),
        ("Burgundy", (100, 30, 45)),
        ("Espresso Brown", (65, 40, 30)),
    ],


    # --------------------------------------------------------
    # KITCHEN
    # --------------------------------------------------------

    "Kitchen": [

        # 5 DECENT / LIGHT
        ("Pure White", (255, 255, 255)),
        ("Cream", (255, 253, 208)),
        ("Light Beige", (245, 235, 210)),
        ("Pale Yellow", (250, 240, 170)),
        ("Light Grey", (220, 220, 220)),

        # 5 MODERATE
        ("Mint Green", (170, 220, 190)),
        ("Soft Yellow", (235, 210, 120)),
        ("Sky Blue", (135, 200, 225)),
        ("Warm Beige", (210, 185, 145)),
        ("Olive Green", (128, 128, 70)),

        # 5 DARK
        ("Dark Teal", (20, 80, 85)),
        ("Deep Green", (30, 85, 45)),
        ("Navy Blue", (35, 55, 90)),
        ("Burnt Orange", (150, 70, 35)),
        ("Dark Brown", (75, 45, 30)),
    ],


    # --------------------------------------------------------
    # DINING ROOM
    # --------------------------------------------------------

    "Dining Room": [

        # 5 DECENT / LIGHT
        ("Warm White", (250, 245, 230)),
        ("Cream", (255, 253, 208)),
        ("Ivory", (255, 255, 240)),
        ("Light Beige", (245, 235, 210)),
        ("Soft Peach", (245, 210, 190)),

        # 5 MODERATE
        ("Terracotta", (203, 126, 94)),
        ("Warm Taupe", (170, 145, 120)),
        ("Muted Orange", (210, 140, 80)),
        ("Sage Green", (156, 175, 136)),
        ("Dusty Rose", (180, 120, 130)),

        # 5 DARK
        ("Deep Burgundy", (100, 30, 45)),
        ("Chocolate Brown", (90, 55, 35)),
        ("Deep Teal", (20, 80, 85)),
        ("Forest Green", (34, 80, 50)),
        ("Charcoal Grey", (55, 60, 65)),
    ],


    # --------------------------------------------------------
    # BATHROOM
    # --------------------------------------------------------

    "Bathroom": [

        # 5 DECENT / LIGHT
        ("Pure White", (255, 255, 255)),
        ("Ice Blue", (215, 235, 245)),
        ("Mint White", (225, 245, 230)),
        ("Light Grey", (220, 220, 220)),
        ("Pale Aqua", (190, 230, 225)),

        # 5 MODERATE
        ("Sea Green", (100, 170, 150)),
        ("Aqua Blue", (100, 190, 200)),
        ("Dusty Blue", (126, 153, 173)),
        ("Sage Green", (156, 175, 136)),
        ("Soft Teal", (90, 160, 160)),

        # 5 DARK
        ("Deep Teal", (20, 80, 85)),
        ("Navy Blue", (35, 55, 90)),
        ("Dark Green", (25, 75, 45)),
        ("Slate Grey", (65, 80, 90)),
        ("Deep Blue", (30, 60, 110)),
    ],


    # --------------------------------------------------------
    # OFFICE
    # --------------------------------------------------------

    "Office": [

        # 5 DECENT / LIGHT
        ("Warm White", (250, 245, 230)),
        ("Light Beige", (245, 235, 210)),
        ("Soft Grey", (211, 211, 211)),
        ("Ivory", (255, 255, 240)),
        ("Pale Blue", (200, 220, 235)),

        # 5 MODERATE
        ("Sage Green", (156, 175, 136)),
        ("Muted Blue", (100, 140, 170)),
        ("Taupe", (170, 145, 120)),
        ("Dusty Blue", (126, 153, 173)),
        ("Olive Green", (128, 128, 70)),

        # 5 DARK
        ("Navy Blue", (35, 55, 90)),
        ("Charcoal Grey", (55, 60, 65)),
        ("Forest Green", (34, 80, 50)),
        ("Dark Brown", (75, 45, 30)),
        ("Deep Teal", (20, 80, 85)),
    ],


    # --------------------------------------------------------
    # KIDS ROOM
    # --------------------------------------------------------

    "Kids Room": [

        # 5 DECENT / LIGHT
        ("Baby Blue", (190, 220, 240)),
        ("Light Pink", (245, 205, 215)),
        ("Mint Green", (200, 230, 210)),
        ("Pale Yellow", (250, 240, 170)),
        ("Lavender", (215, 200, 230)),

        # 5 MODERATE
        ("Coral", (230, 120, 100)),
        ("Sky Blue", (135, 200, 225)),
        ("Peach", (235, 170, 140)),
        ("Mint Green", (150, 205, 170)),
        ("Lilac", (175, 140, 190)),

        # 5 DARK
        ("Royal Blue", (45, 70, 130)),
        ("Deep Purple", (70, 40, 100)),
        ("Forest Green", (34, 80, 50)),
        ("Deep Coral", (160, 60, 55)),
        ("Dark Teal", (20, 80, 85)),
    ],
}


# ============================================================
# ROOM TYPES
# ============================================================

ROOM_TYPES = list(ROOM_COLORS.keys())


# ============================================================
# PAINT INTENSITIES
# ============================================================

INTENSITIES = [
    "Very Light",
    "Light",
    "Medium",
    "Dark",
    "Very Dark"
]


# ============================================================
# COLOR CATEGORIES
# ============================================================

COLOR_CATEGORIES = {

    "Decent / Light": [
        "Ivory",
        "Cream",
        "Warm White",
        "Pure White",
        "Light Beige",
        "Soft Grey",
        "Pearl White",
        "Light Blue",
        "Pale Green",
        "Pale Yellow",
        "Light Grey"
    ],

    "Moderate": [
        "Sage Green",
        "Dusty Blue",
        "Terracotta",
        "Muted Peach",
        "Olive Green",
        "Dusty Rose",
        "Mauve",
        "Muted Blue",
        "Warm Taupe",
        "Mint Green",
        "Sky Blue",
        "Warm Beige"
    ],

    "Dark": [
        "Navy Blue",
        "Forest Green",
        "Chocolate Brown",
        "Charcoal Grey",
        "Deep Teal",
        "Deep Plum",
        "Midnight Blue",
        "Dark Forest Green",
        "Burgundy",
        "Espresso Brown",
        "Dark Brown",
        "Deep Burgundy",
        "Dark Green",
        "Slate Grey",
        "Deep Blue",
        "Royal Blue",
        "Deep Purple"
    ]
}


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print("----------------------------------------")
    print("Color Database Loaded Successfully")
    print("----------------------------------------")

    for room, colors in ROOM_COLORS.items():

        print(
            f"{room}: {len(colors)} colors"
        )

    print("----------------------------------------")
    print("Total color intensity levels:")
    print("5 Decent / Light")
    print("5 Moderate")
    print("5 Dark")
    print("----------------------------------------")