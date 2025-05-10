# ──────────────────────────────────────────────────────────────
#  Catan Dice Roller — v1.3
# 
#  Author  : Ximo (https://github.com/ximocm)
#  License : Creative Commons BY-NC 4.0 – Free for NON-commercial use
#
#  New in v1.3.1:
#    • Updated code comments for production readability
#    • Changed the file structure
#    • Fix darkmode +/- button text color
#
#  New in v1.2:
#    • Added manual Pause/Resume button (pause.png)
#    • Fixed-size buttons (do not scale with window)
#    • Improved text margins and wrapping in info panel
#
#  Features:
#    • Automatic 2d6 roll every X seconds (15 / 30 / 60 / 90)
#    • "Ping" sound effect on roll
#    • Auto-pause on 7, with robber player selected
#    • Manual Pause/Resume ⏸▶
#    • "Roll Now" button 🎲
#    • Dark/Light mode toggle 🌙/☀️
#    • Info panel with credits (ⓘ)
#    • Responsive UI: resizable on PC, fullscreen on Android
#    • Transparent, fixed-size buttons (icon/text only)
#
#  Required files (in same folder or assets):
#    • ping.wav, moon.png, sun.png, dice.png, info.png, pause.png
#    • All with transparent background
# ──────────────────────────────────────────────────────────────

import sys, pygame, random, textwrap
from config import *
from game import GameState
from gui import draw_button, draw_info_panel
from utils import load_icon, tint, roll_dice, resource_path

# Detect if running on Android (via pyjnius / buildozer)
IS_ANDROID = hasattr(sys, "getandroidapilevel") or sys.platform.startswith("android")

# Initialize Pygame audio and video systems
pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.init()

# Try to load ping sound, fallback to None if unavailable
try:
    sound_ping = pygame.mixer.Sound(resource_path("ping.wav"))
except Exception:
    sound_ping = None

# Determine screen size depending on platform
info = pygame.display.Info()
W, H = (info.current_w, info.current_h) if IS_ANDROID else (320, 480)
flags = pygame.FULLSCREEN if IS_ANDROID else pygame.RESIZABLE
screen = pygame.display.set_mode((W, H), flags)
pygame.display.set_caption("Catan Dice Roller")

# Load fonts with size scaled to screen resolution
font_big = load_font(110, W, H)
font_small = load_font(36, W, H)

# Load icon assets and their tinted light-mode versions
def get_icons():
    moon = load_icon("moon.png")
    sun = load_icon("sun.png")
    dice = load_icon("dice.png")
    info = load_icon("info.png")
    pause = load_icon("pause.png")
    return {
        "moon": moon, "sun": sun, "dice": dice, "info": info, "pause": pause,
        "moon_L": tint(moon, LIGHT), "sun_L": tint(sun, LIGHT),
        "dice_L": tint(dice, LIGHT), "info_L": tint(info, LIGHT),
        "pause_L": tint(pause, LIGHT)
    }

icons = get_icons()

# Define buttons' positions and sizes relative to screen dimensions
def create_buttons():
    BTN_W, BTN_H = scale(80, W, H), scale(60, W, H)
    bottom_y, top_y, gap = int(H * 0.82), int(H * 0.04), scale(20, W, H)
    return {
        "now":   pygame.Rect((W - BTN_W)//2, bottom_y, BTN_W, BTN_H),
        "minus": pygame.Rect(gap, bottom_y, BTN_W, BTN_H),
        "plus":  pygame.Rect(W - BTN_W - gap, bottom_y, BTN_W, BTN_H),
        "info":  pygame.Rect(gap, top_y, BTN_H, BTN_H),
        "pause": pygame.Rect(W - gap*2 - BTN_H*2, top_y, BTN_H, BTN_H),
        "dark":  pygame.Rect(W - gap - BTN_H, top_y, BTN_H, BTN_H)
    }

buttons = create_buttons()
ROLL_EVT = pygame.USEREVENT + 1  # Custom event ID for auto-roll
state = GameState()
clock = pygame.time.Clock()
running = True
link_rect = None  # Rect for the clickable PayPal link in the info panel

# ───── Main application loop ─────
while running:
    # Set colors depending on dark/light mode
    FG = LIGHT if state.dark else (0, 0, 0)
    BG = DARK_BG if state.dark else LIGHT_BG
    screen.fill(BG)

    # Handle system and user events
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.VIDEORESIZE and not IS_ANDROID:
            # Handle window resize (PC only)
            W, H = ev.w, ev.h
            screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            font_big = load_font(110, W, H)
            font_small = load_font(36, W, H)
            buttons = create_buttons()

        elif (IS_ANDROID and ev.type == pygame.FINGERDOWN) or (not IS_ANDROID and ev.type == pygame.MOUSEBUTTONDOWN):
            # Get input coordinates from touch or mouse
            W, H = pygame.display.get_surface().get_size()
            if ev.type == pygame.FINGERDOWN:
                x, y = ev.x * W, ev.y * H
            else:
                x, y = ev.pos

            # Info panel: check for link click or close
            if state.show_info:
                if link_rect and link_rect.collidepoint((x, y)):
                    import webbrowser
                    webbrowser.open("https://paypal.me/ximocabanes")
                state.show_info = False
                continue

            # Show info panel
            elif buttons["info"].collidepoint((x, y)):
                state.show_info = True
                continue

            # Before game starts: player number selection and start
            if not state.started:
                if buttons["minus"].collidepoint((x, y)):
                    state.num_players = max(2, state.num_players - 1)
                elif buttons["plus"].collidepoint((x, y)):
                    state.num_players = min(6, state.num_players + 1)
                elif buttons["now"].collidepoint((x, y)):
                    state.started = True
                    state.current_roll = roll_dice()
                    if sound_ping: sound_ping.play()
                    pygame.time.set_timer(ROLL_EVT, state.TIMER_MS)
                    state.next_tick = pygame.time.get_ticks() + state.TIMER_MS
                continue

            # Toggle pause/resume
            if buttons["pause"].collidepoint((x, y)):
                state.manual_paused = not state.manual_paused
                pygame.time.set_timer(ROLL_EVT, 0 if state.manual_paused else state.TIMER_MS)
                if not state.manual_paused:
                    state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

            # Toggle dark/light mode
            elif buttons["dark"].collidepoint((x, y)):
                state.dark = not state.dark

            # Decrease interval time
            elif buttons["minus"].collidepoint((x, y)):
                state.idx_interval = max(0, state.idx_interval - 1)
                state.TIMER_MS = intervals[state.idx_interval]
                pygame.time.set_timer(ROLL_EVT, state.TIMER_MS)
                state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

            # Increase interval time
            elif buttons["plus"].collidepoint((x, y)):
                state.idx_interval = min(len(intervals) - 1, state.idx_interval + 1)
                state.TIMER_MS = intervals[state.idx_interval]
                pygame.time.set_timer(ROLL_EVT, state.TIMER_MS)
                state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

            # Manual dice roll
            elif buttons["now"].collidepoint((x, y)):
                state.current_roll = roll_dice()
                if sound_ping: sound_ping.play()
                state.paused = state.current_roll == 7
                if state.paused:
                    state.robber_player = random.randint(1, state.num_players)
                    pygame.time.set_timer(ROLL_EVT, 0)
                else:
                    pygame.time.set_timer(ROLL_EVT, state.TIMER_MS)
                    state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

        elif ev.type == ROLL_EVT and state.started and not state.paused and not state.manual_paused:
            # Handle automatic dice roll
            state.current_roll = roll_dice()
            if sound_ping: sound_ping.play()
            if state.current_roll == 7:
                state.paused = True
                state.robber_player = random.randint(1, state.num_players)
                pygame.time.set_timer(ROLL_EVT, 0)
            else:
                state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

    # ───── Render UI elements ─────
    if not state.started:
        # Display player selection screen
        t = font_small.render("Select number of players:", True, FG)
        screen.blit(t, t.get_rect(center=(W//2, int(H*0.2))))
        num = load_font(min(200, int(H*0.4)), W, H).render(str(state.num_players), True, FG)
        screen.blit(num, num.get_rect(center=(W//2, H//2)))
        draw_button(screen, font_small, buttons["minus"], text="–")
        draw_button(screen, font_small, buttons["plus"], text="+")
        draw_button(screen, font_small, buttons["now"], text="Start")
    else:
        # Display current roll and status
        roll_txt = font_big.render(str(state.current_roll), True, FG)
        screen.blit(roll_txt, roll_txt.get_rect(center=(W//2, H//2 - scale(30, W, H))))

        if state.paused:
            msg = f"7 rolled! Player {state.robber_player} moves the robber"
        elif state.manual_paused:
            msg = "Paused - press pause to resume"
        else:
            secs = max(0, (state.next_tick - pygame.time.get_ticks()) // 1000)
            msg = f"Next roll in {1 + secs:2d}s  Interval {state.TIMER_MS // 1000}s"

        # Render wrapped status message
        wrap_width = (W - 20) // font_small.size("X")[0]
        y0 = H//2 + scale(50, W, H)
        for line in textwrap.wrap(msg, wrap_width):
            t = font_small.render(line, True, FG)
            screen.blit(t, t.get_rect(center=(W//2, y0)))
            y0 += t.get_height() + scale(4, W, H)

        # Render buttons with appropriate icons and mode
        moon = icons["moon_L"] if state.dark else icons["moon"]
        sun  = icons["sun_L"] if state.dark else icons["sun"]
        dice = icons["dice_L"] if state.dark else icons["dice"]
        info = icons["info_L"] if state.dark else icons["info"]
        pause = icons["pause_L"] if state.dark else icons["pause"]

        draw_button(screen, font_small, buttons["info"], icon=info)
        draw_button(screen, font_small, buttons["dark"], icon=(moon if not state.dark else sun))
        draw_button(screen, font_small, buttons["pause"], icon=pause)
        draw_button(screen, font_small, buttons["minus"], text="–", text_color=LIGHT if state.dark else (0, 0, 0))
        draw_button(screen, font_small, buttons["plus"], text="+", text_color=LIGHT if state.dark else (0, 0, 0))
        draw_button(screen, font_small, buttons["now"], icon=dice)

        # Show info panel if active
        if state.show_info:
            link_rect = draw_info_panel(screen, W, H, font_small, INFO_LINES)
        else:
            link_rect = None

    pygame.display.flip()
    clock.tick(30)

# Cleanup on exit
pygame.quit()