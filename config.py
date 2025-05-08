import pygame

intervals = [5_000, 15_000, 30_000, 45_000, 60_000,90_000]
LIGHT = (230, 230, 230)
DARK_BG = (20, 20, 20)
LIGHT_BG = (255, 255, 255)

INFO_LINES = [
    "Catan Dice Roller v1.2",
    "Author: Ximo (github.com/ximocm)",
    "License: CC BY-NC-4.0 (non-commercial)",
    "",
    "Enjoying my projects?",
    "Buy me a coffee: https://paypal.me/ximocabanes",
    "",
    "Icons by Flaticon (Good Ware, Xinh Studio, Freepik)",
    "Sound Effect by u_qpfzpydtro from Pixabay"
    "",
    "© 2025 Ximo"
]

def scale(base_size, w, h):
    return int(base_size * min(w, h) / 400)

def load_font(size, w, h):
    return pygame.font.Font(None, scale(size, w, h))
