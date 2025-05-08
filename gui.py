import pygame, textwrap
from config import LIGHT

def draw_button(screen, font, rect, *, icon=None, text=None, text_color=(0, 0, 0)):
    if icon:
        img = pygame.transform.smoothscale(icon, rect.size)
        screen.blit(img, rect)
    elif text:
        label = font.render(text, True, text_color)
        screen.blit(label, label.get_rect(center=rect.center))



def draw_info_panel(screen, W, H, font, lines):
    import textwrap

    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    screen.blit(overlay, (0, 0))

    wrap_width = (W - 20) // font.size("X")[0]
    rendered_lines = sum([textwrap.wrap(line, wrap_width) or [""] for line in lines], [])
    font_h = int((H * 0.8) / (len(rendered_lines) * 1.2))
    f = pygame.font.Font(None, min(font_h, 36))

    y = (H - len(rendered_lines) * font_h * 1.2) / 2
    clickable_rect = None

    for l in rendered_lines:
        t = f.render(l, True, (255, 255, 255))
        rect = t.get_rect(center=(W // 2, int(y)))
        screen.blit(t, rect)

        if "https://paypal.me/ximocabanes" in l:
            clickable_rect = rect  # Guardamos la posición del enlace

        y += font_h * 1.2

    return clickable_rect
