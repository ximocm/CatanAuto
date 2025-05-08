import pygame, textwrap
from config import LIGHT

# Draws a button either with an icon or with text, centered inside the given rectangle
def draw_button(screen, font, rect, *, icon=None, text=None, text_color=(0, 0, 0)):
    if icon:
        # Scale the icon to fit the button rectangle and draw it
        img = pygame.transform.smoothscale(icon, rect.size)
        screen.blit(img, rect)
    elif text:
        # Render the text and center it in the button rectangle
        label = font.render(text, True, text_color)
        screen.blit(label, label.get_rect(center=rect.center))

# Draws a semi-transparent overlay with wrapped info text and returns the clickable link area
def draw_info_panel(screen, W, H, font, lines):
    import textwrap

    # Create a translucent black overlay
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    # Calculate how many characters fit per line
    wrap_width = (W - 20) // font.size("X")[0]

    # Wrap all lines of text to fit the screen width
    rendered_lines = sum([textwrap.wrap(line, wrap_width) or [""] for line in lines], [])

    # Calculate dynamic font height based on available space
    font_h = int((H * 0.8) / (len(rendered_lines) * 1.2))
    f = pygame.font.Font(None, min(font_h, 36))

    # Vertical starting position for centered layout
    y = (H - len(rendered_lines) * font_h * 1.2) / 2
    clickable_rect = None

    for l in rendered_lines:
        # Render and draw each line centered horizontally
        t = f.render(l, True, (255, 255, 255))
        rect = t.get_rect(center=(W // 2, int(y)))
        screen.blit(t, rect)

        # Store the rect of the PayPal link for interaction
        if "https://paypal.me/ximocabanes" in l:
            clickable_rect = rect

        y += font_h * 1.2

    # Return the area that can be clicked to open the link
    return clickable_rect
