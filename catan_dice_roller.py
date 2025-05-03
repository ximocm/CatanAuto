# ──────────────────────────────────────────────────────────────
#  Catan Dice Roller  v1.0
#  Author   : Ximo  (github.com/ximocm)
#  License  : Creative Commons BY-NC 4.0  – free for NON-commercial use
#
#  Features:
#    • Automatic roll of 2d6 every X s  (15 / 30 / 60 / 90)
#    • “Ping” sound   • Pauses on 7   • “Roll now” 🎲
#    • Dark / Light mode 🌙/☀️  • Info button ⓘ (credits panel)
#    • Responsive UI: resizable window on PC or fullscreen on Android
#    • Transparent buttons (icon / text only)
#
#  Required files in the SAME folder:
#     ping.wav   moon.png   sun.png   dice.png   info.png
#     (all with transparent background)
# ──────────────────────────────────────────────────────────────

import pygame, random, os, sys

# ───────────  PLATFORM DETECTION  ────────────
IS_ANDROID = hasattr(sys, "getandroidapilevel") or sys.platform.startswith("android")

# ─────────────  INITIAL WINDOW  ───────────────
pygame.init()
if IS_ANDROID:
    info = pygame.display.Info()
    W, H = info.current_w, info.current_h
    flags = pygame.FULLSCREEN
else:                               # PC → small resizable window
    W, H = 320, 480
    flags = pygame.RESIZABLE
screen = pygame.display.set_mode((W, H), flags)
pygame.display.set_caption("Catan Dice Roller")

# ─────────────  RELATIVE SCALING  ─────────────
BASE = 400
s = lambda x: int(x * W / BASE)

# ─────────────────  FONTS  ────────────────────
font_big   = pygame.font.Font(None, s(110))
font_small = pygame.font.Font(None, s(36))

# ───────────────  LOAD RESOURCES  ─────────────
root = sys.path[0]

# Sound
pygame.mixer.init()
ping = pygame.mixer.Sound(os.path.join(root, "ping.wav"))

# PNG icons (transparent background)
icon_moon = pygame.image.load(os.path.join(root, "moon.png")).convert_alpha()
icon_sun  = pygame.image.load(os.path.join(root, "sun.png")).convert_alpha()
icon_dice = pygame.image.load(os.path.join(root, "dice.png")).convert_alpha()
icon_info = pygame.image.load(os.path.join(root, "info.png")).convert_alpha()

def tint(icon: pygame.Surface, color: tuple[int, int, int]) -> pygame.Surface:
    """Return a copy of the icon tinted to the given color (keeps alpha)."""
    img = icon.copy()
    img.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT)   # remove original colour
    img.fill(color + (0,), None, pygame.BLEND_RGBA_ADD)      # add new colour
    return img

LIGHT = (230, 230, 230)           # light grey for dark mode
icon_moon_L  = tint(icon_moon,  LIGHT)
icon_sun_L   = tint(icon_sun,   LIGHT)
icon_dice_L  = tint(icon_dice,  LIGHT)
icon_info_L  = tint(icon_info,  LIGHT)

def scaled(img, rect):
    """Scale icon to exactly fit the button rect."""
    return pygame.transform.smoothscale(img, rect.size)

# ───────────────  GAME LOGIC  ────────────────
intervals    = [15_000, 30_000, 60_000, 90_000]   # ms
idx_interval = 2                                  # default 60 s
TIMER_MS     = intervals[idx_interval]

def roll() -> int:
    return random.randint(1, 6) + random.randint(1, 6)

current_roll = roll()
next_tick    = pygame.time.get_ticks() + TIMER_MS
paused, dark, show_info = False, False, False
ROLL_EVT = pygame.USEREVENT + 1
pygame.time.set_timer(ROLL_EVT, TIMER_MS)

# ─────────────────  BUTTONS  ──────────────────
def create_buttons():
    global btn_info, btn_dark, btn_minus, btn_plus, btn_now
    btn_info  = pygame.Rect(s(10),      s(10),      s(50),  s(50))  # ⓘ
    btn_dark  = pygame.Rect(W - s(60),  s(10),      s(50),  s(50))  # 🌙/☀️
    btn_minus = pygame.Rect(s(10),      H - s(80),  s(60),  s(60))  # –
    btn_plus  = pygame.Rect(s(90),      H - s(80),  s(60),  s(60))  # +
    btn_now   = pygame.Rect(W - s(160), H - s(80),  s(150), s(60))  # 🎲
create_buttons()

def draw_button(rect, *, icon=None, text=None):
    """Transparent button: draws only icon or text."""
    if icon:
        screen.blit(scaled(icon, rect), rect)
    elif text:
        lbl = font_small.render(text, True, FG)
        screen.blit(lbl, lbl.get_rect(center=rect.center))

# ───────────────  INFO PANEL  ────────────────
INFO_LINES = [
    "Catan Dice Roller  v1.0",
    "Author: Ximo"
    "(github.com/ximocm)",
    "License: CC BY-NC-4.0  (non-commercial)",
    "",
    "Enjoying my projects?",
    "Buy me a coffee https://paypal.me/ximocabanes/3",
    "Thanks for supporting open-source software!",
    "",
    "Icons:",
    "  • Sun & Moon - Good Ware (Flaticon)",
    "  • Dice - Xinh Studio (Flaticon)",
    "  • Info - Freepik (Flaticon)",
    "",
    "Not affiliated with Catan GmbH.",
    "© 2025 Ximo"
]

def draw_info_panel():
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))                 # 80 % black overlay
    screen.blit(overlay, (0, 0))
    y = s(40)
    for line in INFO_LINES:
        txt = font_small.render(line, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(W // 2, y)))
        y += txt.get_height() + s(6)

# ───────────────  MAIN LOOP  ────────────────
clock = pygame.time.Clock()
running = True
while running:
    for ev in pygame.event.get():

        # —— Quit ——
        if ev.type == pygame.QUIT:
            running = False

        # —— Resize window (PC) ——
        elif ev.type == pygame.VIDEORESIZE and not IS_ANDROID:
            W, H = ev.w, ev.h
            screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            font_big   = pygame.font.Font(None, s(110))
            font_small = pygame.font.Font(None, s(36))
            create_buttons()

        # —— Toggle fullscreen (key F) ——
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_f and not IS_ANDROID:
            flags ^= pygame.FULLSCREEN
            screen = pygame.display.set_mode((0, 0), flags) if flags & pygame.FULLSCREEN else \
                     pygame.display.set_mode((320, 480), pygame.RESIZABLE)
            W, H = screen.get_size()
            font_big   = pygame.font.Font(None, s(110))
            font_small = pygame.font.Font(None, s(36))
            create_buttons()

        # —— Automatic roll ——
        elif ev.type == ROLL_EVT and not paused:
            current_roll = roll()
            ping.play()
            if current_roll == 7:
                paused = True
                pygame.time.set_timer(ROLL_EVT, 0)     # stop timer
            else:
                next_tick = pygame.time.get_ticks() + TIMER_MS

        # —— Touch / mouse input ——
        elif ev.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
            x, y = (ev.x * W, ev.y * H) if ev.type == pygame.FINGERDOWN else ev.pos

            # Info panel toggle
            if btn_info.collidepoint((x, y)):
                show_info = not show_info
                continue

            # Ignore other controls if Info is open
            if show_info:
                continue

            # Dark mode toggle
            if btn_dark.collidepoint((x, y)):
                dark = not dark

            # Interval –
            if btn_minus.collidepoint((x, y)):
                idx_interval = max(0, idx_interval - 1)
                TIMER_MS = intervals[idx_interval]
                next_tick = pygame.time.get_ticks() + TIMER_MS
                pygame.time.set_timer(ROLL_EVT, TIMER_MS)

            # Interval +
            if btn_plus.collidepoint((x, y)):
                idx_interval = min(len(intervals) - 1, idx_interval + 1)
                TIMER_MS = intervals[idx_interval]
                next_tick = pygame.time.get_ticks() + TIMER_MS
                pygame.time.set_timer(ROLL_EVT, TIMER_MS)

            # Roll now
            if btn_now.collidepoint((x, y)):
                current_roll = roll()
                ping.play()
                next_tick = pygame.time.get_ticks() + TIMER_MS
                pygame.time.set_timer(ROLL_EVT, TIMER_MS)
                paused = current_roll == 7
                if paused:
                    pygame.time.set_timer(ROLL_EVT, 0)

            # Resume after 7
            if paused and not btn_dark.collidepoint((x, y)):
                paused = False
                next_tick = pygame.time.get_ticks() + TIMER_MS
                pygame.time.set_timer(ROLL_EVT, TIMER_MS)

    # ───────────────── DRAW ─────────────────
    BG = (20, 20, 20) if dark else (255, 255, 255)
    FG = LIGHT          if dark else (0, 0, 0)
    screen.fill(BG)

    # Current roll
    num_surf = font_big.render(str(current_roll), True, FG)
    screen.blit(num_surf, num_surf.get_rect(center=(W / 2, H / 2 - s(30))))

    # Countdown / message
    if paused:
        msg = "7 rolled! Tap to continue"
    else:
        secs = max(0, (next_tick - pygame.time.get_ticks()) // 1000)
        msg = f"Next roll: {secs:2d}s · {TIMER_MS // 1000}s"
    txt = font_small.render(msg, True, FG)
    screen.blit(txt, txt.get_rect(center=(W / 2, H / 2 + s(50))))

    # Pick light/dark icons
    moon  = icon_moon_L  if dark else icon_moon
    sun   = icon_sun_L   if dark else icon_sun
    dice  = icon_dice_L  if dark else icon_dice
    infoI = icon_info_L  if dark else icon_info

    # Buttons
    draw_button(btn_info, icon=infoI)
    draw_button(btn_dark, icon=moon if not dark else sun)
    draw_button(btn_minus, text="–")
    draw_button(btn_plus,  text="+")
    draw_button(btn_now,   icon=dice)

    # Info overlay
    if show_info:
        draw_info_panel()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
