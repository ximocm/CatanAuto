import os
import pygame
import sys
import random

# Returns the absolute path to a resource in the 'assets' folder
def resource_path(rel):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "assets", rel)

# Loads an image with alpha transparency from the assets folder
# Returns a fallback empty surface if loading fails
def load_icon(name):
    path = resource_path(name)
    try:
        return pygame.image.load(path).convert_alpha()
    except Exception as e:
        return pygame.Surface((50, 50), pygame.SRCALPHA)

# Applies a color tint to an icon image (used for light/dark variants)
def tint(icon, color):
    img = icon.copy()
    img.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)
    img.fill(color + (0,), None, pygame.BLEND_RGBA_ADD)
    return img

# Simulates rolling two six-sided dice (returns value from 2 to 12)
def roll_dice():
    return random.randint(1, 6) + random.randint(1, 6)
