import pygame

# List of available time intervals (in milliseconds) for auto-rolling
intervals = [5_000, 15_000, 30_000, 45_000, 60_000, 90_000]

# Color constants for UI themes
LIGHT = (230, 230, 230)       # Text color for dark mode
DARK_BG = (20, 20, 20)        # Background color for dark mode
LIGHT_BG = (255, 255, 255)    # Background color for light mode

# Lines displayed in the info panel
INFO_LINES = [
    "Catan Dice Roller v1.3",
    "Author: Ximo  (github.com/ximocm)",
    "License: Creative Commons BY-NC 4.0",
    "",
    "100% fan-made project.",
    "Not affiliated with Catan GmbH or any publisher.",
    "",
    "If you enjoy this tool, consider supporting:",
    "https://paypal.me/ximocabanes",
    "to help create future tools and content.",
    "",
    "Assets used:",
    "- Icons by Flaticon:",
    "  Good Ware, Xinh Studio, Freepik",
    "- Sound effect by u_qpfzpydtro (Pixabay)",
    "",
    "© 2025 Ximo. All rights reserved."
]

def scale(base_size, w, h):
    # Scales a size based on current screen resolution.
    # Useful for consistent UI sizing across different devices.
    return int(base_size * min(w, h) / 400)

def load_font(size, w, h):
    # Loads a default font scaled to the current resolution.
    return pygame.font.Font(None, scale(size, w, h))
