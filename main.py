# ──────────────────────────────────────────────────────────────
#  Catan Dice Roller  v1.2
#  Author   : Ximo  (github.com/ximocm)
#  License  : Creative Commons BY-NC 4.0  – free for NON-commercial use
#
#  New in v1.2:
#    • Added manual Pause/Resume button (pause.png)
#    • Fixed-size buttons (do not scale with window)
#    • Text margins and wrapping in info panel
#
#  Features:
#    • Automatic roll of 2d6 every X s  (15 / 30 / 60 / 90)
#    • “Ping” sound   • Pauses on 7   • “Roll now” 🎲
#    • Manual Pause/Resume ⏸▶
#    • Dark / Light mode 🌙/☀️  • Info button ⓘ (credits panel)
#    • Responsive UI: window on PC or fullscreen on Android
#    • Transparent, fixed-size buttons (icon / text only)
#
#  Required files in the SAME folder:
#     ping.wav   moon.png   sun.png   dice.png   info.png   pause.png
#     (all with transparent background)
# ──────────────────────────────────────────────────────────────
print("✅ pygame initialized")
# ──────────────────────────────────────────────────────────────
import sys, traceback
# ──────────────────────────────────────────────────────────────
import pygame, random, os, textwrap
from kivy.utils import platform

# ───────────  PLATFORM DETECTION  ────────────
IS_ANDROID = hasattr(sys, "getandroidapilevel") or sys.platform.startswith("android")

# ────────────────  RESOURCE PATH  ─────────────────
def resource_path(rel):
    """Get absolute path to a resource."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)

# ─────────────  INITIAL WINDOW SETUP  ───────────────
pygame.init()
if IS_ANDROID:
    info   = pygame.display.Info()
    W, H   = info.current_w, info.current_h
    flags  = pygame.FULLSCREEN
else:
    W, H, flags = 320, 480, pygame.RESIZABLE
screen = pygame.display.set_mode((W, H), flags)
pygame.display.set_caption("Catan Dice Roller")

# ─────────────  RELATIVE SCALING HELPER  ─────────────
BASE = 400
s = lambda x: int(x * W / BASE)

# ───────────────────  FONTS  ────────────────────────
font_big   = pygame.font.Font(None, s(110))
font_small = pygame.font.Font(None, s(36))

# ───────────────  LOAD AUDIO & ICONS  ───────────────
try:
    pygame.mixer.init()
    print("✅ Mixer initialized")
except Exception as e:
    print(f"❌ Error initializing mixer: {e}")

moon_path  = os.path.abspath("moon.png")
sun_path   = os.path.abspath("sun.png")
dice_path  = os.path.abspath("dice.png")
info_path  = os.path.abspath("info.png")
pause_path = os.path.abspath("pause.png")

try:
    icon_moon  = pygame.image.load(moon_path).convert_alpha()
    icon_sun   = pygame.image.load(sun_path).convert_alpha()
    icon_dice  = pygame.image.load(dice_path).convert_alpha()
    icon_info  = pygame.image.load(info_path).convert_alpha()
    icon_pause = pygame.image.load(pause_path).convert_alpha()
    print("✅ Icons loaded successfully")
except Exception as e:
    print(f"❌ Error loading icons: {e}")
    # Imágenes vacías por defecto
    icon_moon = icon_sun = icon_dice = icon_info = icon_pause = pygame.Surface((50, 50), pygame.SRCALPHA)

# ───────────────  TINT ICONS FOR DARK MODE  ─────────────
def tint(icon, color):
    img = icon.copy()
    img.fill((0,0,0,255), None, pygame.BLEND_RGBA_MULT)
    img.fill(color + (0,), None, pygame.BLEND_RGBA_ADD)
    return img

LIGHT       = (230,230,230)
icon_moon_L = tint(icon_moon, LIGHT)
icon_sun_L  = tint(icon_sun,  LIGHT)
icon_dice_L = tint(icon_dice, LIGHT)
icon_info_L = tint(icon_info, LIGHT)
icon_pause_L= tint(icon_pause, LIGHT)

# ───────────────  ICON SCALING HELPER  ───────────────
def scaled(img, rect):
    return pygame.transform.smoothscale(img, rect.size)

# ───────────────  GAME LOGIC SETUP  ───────────────
intervals    = [15_000, 30_000, 60_000, 90_000]
idx_interval = 2
TIMER_MS     = intervals[idx_interval]

def roll():
    return random.randint(1,6) + random.randint(1,6)

# ───────────────  INITIAL STATE  ───────────────
current_roll   = None
paused         = False
manual_paused  = False
dark           = False
show_info      = False
started        = False
num_players    = 4
robber_player  = None

ROLL_EVT = pygame.USEREVENT + 1

# ─────────────  BUTTON DIMENSIONS & MARGINS  ─────────────
BTN_SMALL = 50
MARGIN    = 10

# ───────────  BUTTON RECTS CREATION  ───────────
def create_buttons():
    global btn_info, btn_dark, btn_pause, btn_minus, btn_plus, btn_now
    # top row: info, pause, dark-mode
    btn_info  = pygame.Rect(MARGIN, MARGIN, BTN_SMALL, BTN_SMALL)
    btn_pause = pygame.Rect(W - MARGIN*2 - BTN_SMALL*2, MARGIN, BTN_SMALL, BTN_SMALL)
    btn_dark  = pygame.Rect(W - MARGIN - BTN_SMALL, MARGIN, BTN_SMALL, BTN_SMALL)
    # bottom row: minus, plus, roll-now
    y_bot     = H - MARGIN - BTN_SMALL
    gap       = max(MARGIN, W // 20)
    btn_minus = pygame.Rect(gap, y_bot, BTN_SMALL, BTN_SMALL)
    btn_plus  = pygame.Rect(gap*2 + BTN_SMALL, y_bot, BTN_SMALL, BTN_SMALL)
    btn_now   = pygame.Rect(W - MARGIN - BTN_SMALL, H - MARGIN - BTN_SMALL, BTN_SMALL, BTN_SMALL)

create_buttons()

# ───────────────  GENERIC BUTTON DRAWER  ───────────────
def draw_button(rect, *, icon=None, text=None):
    if icon:
        screen.blit(scaled(icon, rect), rect)
    elif text:
        lbl = font_small.render(text, True, FG)
        screen.blit(lbl, lbl.get_rect(center=rect.center))

# ───────────────  INFO PANEL CONTENT  ───────────────
INFO_LINES = [
    "Catan Dice Roller v1.2",
    "Author: Ximo (github.com/ximocm)",
    "License: CC BY-NC-4.0 (non-commercial)",
    "",
    "Enjoying my projects?",
    "Buy me a coffee: https://paypal.me/ximocm",
    "",
    "Icons:",
    "• Sun & Moon – Good Ware (Flaticon)",
    "• Dice – Xinh Studio (Flaticon)",
    "• Info – Freepik (Flaticon)",
    "• Pause – Freepik (Flaticon)",
    "",
    "© 2025 Ximo"
]

# ───────────────  DRAW INFO PANEL  ───────────────
def draw_info_panel():
    overlay = pygame.Surface((W, H), pygame.SRCALPHA)
    overlay.fill((0,0,0,200))
    screen.blit(overlay, (0,0))

    # wrap to ~80% width
    max_w = W
    char_w = font_small.size("X")[0] or 8
    max_chars = int(max_w // char_w)
    wrapped = []
    for line in INFO_LINES:
        wrapped += textwrap.wrap(line, max_chars) or [""]

    # dynamic font sizing for <80% height
    max_h = H * 0.8
    n = len(wrapped)
    font_h = int(max_h / (n * 1.2))
    info_font = pygame.font.Font(None, min(s(36), font_h))

    y = (H - n*font_h*1.2) / 2
    for sub in wrapped:
        txt = info_font.render(sub, True, (255,255,255))
        screen.blit(txt, txt.get_rect(center=(W//2, int(y))))
        y += font_h * 1.2

# ───────────  PRE-GAME PLAYER SELECTION  ───────────
def draw_player_selection():
    screen.fill(BG)
    title = font_small.render("Select number of players:", True, FG)
    screen.blit(title, title.get_rect(center=(W//2, int(H*0.2))))

    # number with max 40% of height
    size = min(s(200), int(H * 0.4))
    num_font = pygame.font.Font(None, size)
    count_surf = num_font.render(str(num_players), True, FG)
    screen.blit(count_surf, count_surf.get_rect(center=(W//2, H//2)))

    draw_button(btn_minus, text="–")
    draw_button(btn_plus,  text="+")
    draw_button(btn_now,   text="Start")

# ───────────────  MAIN LOOP  ───────────────
clock = pygame.time.Clock()
running = True

while running:
    FG = LIGHT if dark else (0,0,0)
    BG = (20,20,20) if dark else (255,255,255)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        # resize handling
        elif ev.type == pygame.VIDEORESIZE and not IS_ANDROID:
            W, H = ev.w, ev.h
            screen = pygame.display.set_mode((W,H), pygame.RESIZABLE)
            font_big   = pygame.font.Font(None, s(110))
            font_small = pygame.font.Font(None, s(36))
            create_buttons()

        # fullscreen toggle (PC)
        elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_f and not IS_ANDROID:
            flags ^= pygame.FULLSCREEN
            screen = pygame.display.set_mode((0,0), flags) \
                    if flags & pygame.FULLSCREEN \
                    else pygame.display.set_mode((320,480), pygame.RESIZABLE)
            W, H = screen.get_size()
            font_big   = pygame.font.Font(None, s(110))
            font_small = pygame.font.Font(None, s(36))
            create_buttons()

        # touch / click
        elif ev.type in (pygame.FINGERDOWN, pygame.MOUSEBUTTONDOWN):
            x,y = (ev.x*W, ev.y*H) if ev.type==pygame.FINGERDOWN else ev.pos

            # toggle info
            if btn_info.collidepoint((x,y)):
                show_info = not show_info
                continue
            if show_info:
                continue

            # pre-game selection
            if not started:
                if btn_minus.collidepoint((x,y)):
                    num_players = max(2, num_players-1)
                elif btn_plus.collidepoint((x,y)):
                    num_players = min(6, num_players+1)
                elif btn_now.collidepoint((x,y)):
                    started = True
                    current_roll = roll()
                    pygame.time.set_timer(ROLL_EVT, TIMER_MS)
                    next_tick = pygame.time.get_ticks() + TIMER_MS
                continue

            # manual pause/resume
            if btn_pause.collidepoint((x,y)):
                manual_paused = not manual_paused
                pygame.time.set_timer(ROLL_EVT, 0 if manual_paused else TIMER_MS)
                if not manual_paused:
                    next_tick = pygame.time.get_ticks() + TIMER_MS
                continue

            # dark mode toggle
            if btn_dark.collidepoint((x,y)):
                dark = not dark

            # adjust interval
            if btn_minus.collidepoint((x,y)):
                idx_interval = max(0, idx_interval-1)
                TIMER_MS = intervals[idx_interval]
                pygame.time.set_timer(ROLL_EVT, TIMER_MS)
                next_tick = pygame.time.get_ticks() + TIMER_MS
            elif btn_plus.collidepoint((x,y)):
                idx_interval = min(len(intervals)-1, idx_interval+1)
                TIMER_MS = intervals[idx_interval]
                pygame.time.set_timer(ROLL_EVT, TIMER_MS)
                next_tick = pygame.time.get_ticks() + TIMER_MS

            # roll now
            elif btn_now.collidepoint((x,y)):
                current_roll = roll()
                paused = (current_roll==7)
                if paused:
                    robber_player = random.randint(1, num_players)
                    pygame.time.set_timer(ROLL_EVT, 0)
                else:
                    pygame.time.set_timer(ROLL_EVT, TIMER_MS)
                    next_tick = pygame.time.get_ticks() + TIMER_MS

        # automatic roll event
        elif ev.type == ROLL_EVT and started and not paused and not manual_paused:
            current_roll = roll()
            if current_roll == 7:
                paused = True
                robber_player = random.randint(1, num_players)
                pygame.time.set_timer(ROLL_EVT, 0)
            else:
                next_tick = pygame.time.get_ticks() + TIMER_MS

    # ─────────────  DRAW PHASE  ─────────────
    screen.fill(BG)

    if not started:
        draw_player_selection()
    else:
        # show current roll
        num_surf = font_big.render(str(current_roll), True, FG)
        screen.blit(num_surf, num_surf.get_rect(center=(W//2, H//2 - s(30))))

        # main message
        if paused:
            msg = f"7 rolled! Player {robber_player} moves the robber"
        elif manual_paused:
            msg = "Paused - press pause to resume"
        else:
            secs = max(0, (next_tick - pygame.time.get_ticks())//1000)
            msg = f"Next roll in {1 + secs:2d}s  Interval {TIMER_MS//1000}s"

        wrap_width = (W - MARGIN) // font_small.size("X")[0]
        y0 = H//2 + s(50)
        for ln in textwrap.wrap(msg, wrap_width):
            txt = font_small.render(ln, True, FG)
            screen.blit(txt, txt.get_rect(center=(W//2, y0)))
            y0 += txt.get_height() + s(4)

        # prepare icons
        moon   = icon_moon_L if dark else icon_moon
        sun    = icon_sun_L  if dark else icon_sun
        dice   = icon_dice_L if dark else icon_dice
        infoI  = icon_info_L if dark else icon_info
        pauseI = icon_pause_L if dark else icon_pause

        # draw buttons
        draw_button(btn_info, icon=infoI)
        draw_button(btn_dark, icon=(moon if not dark else sun))
        draw_button(btn_pause, icon=pauseI)
        draw_button(btn_minus, text="–")
        draw_button(btn_plus,  text="+")
        draw_button(btn_now,   icon=dice)

        if show_info:
            draw_info_panel()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()