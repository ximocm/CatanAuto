import sys, pygame, random, textwrap
from config import *
from game import GameState
from gui import draw_button, draw_info_panel
from utils import load_icon, tint, roll_dice

# ───────── DETECCIÓN DE PLATAFORMA ─────────
IS_ANDROID = hasattr(sys, "getandroidapilevel") or sys.platform.startswith("android")

# ───────── INICIALIZACIÓN ─────────
pygame.mixer.pre_init(44100, -16, 2, 2048) 
pygame.init()
from utils import resource_path

try:
    sound_ping = pygame.mixer.Sound(resource_path("ping.wav"))
except Exception as e:
    sound_ping = None
info = pygame.display.Info()
W, H = (info.current_w, info.current_h) if IS_ANDROID else (320, 480)
flags = pygame.FULLSCREEN if IS_ANDROID else pygame.RESIZABLE
screen = pygame.display.set_mode((W, H), flags)
pygame.display.set_caption("Catan Dice Roller")

# ───────── FUENTES ─────────
font_big = load_font(110, W, H)
font_small = load_font(36, W, H)

# ───────── ICONOS ─────────
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

# ───────── BOTONES ─────────
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
ROLL_EVT = pygame.USEREVENT + 1
state = GameState()
clock = pygame.time.Clock()
running = True

# ───────── LOOP PRINCIPAL ─────────
while running:
    FG = LIGHT if state.dark else (0, 0, 0)
    BG = DARK_BG if state.dark else LIGHT_BG
    screen.fill(BG)

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

        elif ev.type == pygame.VIDEORESIZE and not IS_ANDROID:
            W, H = ev.w, ev.h
            screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
            font_big = load_font(110, W, H)
            font_small = load_font(36, W, H)
            buttons = create_buttons()

        elif (IS_ANDROID and ev.type == pygame.FINGERDOWN) or (not IS_ANDROID and ev.type == pygame.MOUSEBUTTONDOWN):
            W, H = pygame.display.get_surface().get_size()
            if ev.type == pygame.FINGERDOWN:
                x, y = ev.x * W, ev.y * H
            else:
                x, y = ev.pos

            if state.show_info:
                state.show_info = False
                continue
            elif buttons["info"].collidepoint((x, y)):
                state.show_info = True
                continue
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

            if buttons["pause"].collidepoint((x, y)):
                state.manual_paused = not state.manual_paused
                pygame.time.set_timer(ROLL_EVT, 0 if state.manual_paused else state.TIMER_MS)
                if not state.manual_paused:
                    state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

            elif buttons["dark"].collidepoint((x, y)):
                state.dark = not state.dark

            elif buttons["minus"].collidepoint((x, y)):
                state.idx_interval = max(0, state.idx_interval - 1)
                state.TIMER_MS = intervals[state.idx_interval]
                pygame.time.set_timer(ROLL_EVT, state.TIMER_MS)
                state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

            elif buttons["plus"].collidepoint((x, y)):
                state.idx_interval = min(len(intervals) - 1, state.idx_interval + 1)
                state.TIMER_MS = intervals[state.idx_interval]
                pygame.time.set_timer(ROLL_EVT, state.TIMER_MS)
                state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

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
            state.current_roll = roll_dice()
            if sound_ping: sound_ping.play()
            if state.current_roll == 7:
                state.paused = True
                state.robber_player = random.randint(1, state.num_players)
                pygame.time.set_timer(ROLL_EVT, 0)
            else:
                state.next_tick = pygame.time.get_ticks() + state.TIMER_MS

    # ─────── DIBUJADO ───────
    if not state.started:
        t = font_small.render("Select number of players:", True, FG)
        screen.blit(t, t.get_rect(center=(W//2, int(H*0.2))))
        num = load_font(min(200, int(H*0.4)), W, H).render(str(state.num_players), True, FG)
        screen.blit(num, num.get_rect(center=(W//2, H//2)))
        draw_button(screen, font_small, buttons["minus"], text="–")
        draw_button(screen, font_small, buttons["plus"], text="+")
        draw_button(screen, font_small, buttons["now"], text="Start")
    else:
        roll_txt = font_big.render(str(state.current_roll), True, FG)
        screen.blit(roll_txt, roll_txt.get_rect(center=(W//2, H//2 - scale(30, W, H))))

        if state.paused:
            msg = f"7 rolled! Player {state.robber_player} moves the robber"
        elif state.manual_paused:
            msg = "Paused - press pause to resume"
        else:
            secs = max(0, (state.next_tick - pygame.time.get_ticks()) // 1000)
            msg = f"Next roll in {1 + secs:2d}s  Interval {state.TIMER_MS // 1000}s"

        wrap_width = (W - 20) // font_small.size("X")[0]
        y0 = H//2 + scale(50, W, H)
        for line in textwrap.wrap(msg, wrap_width):
            t = font_small.render(line, True, FG)
            screen.blit(t, t.get_rect(center=(W//2, y0)))
            y0 += t.get_height() + scale(4, W, H)

        # Iconos según modo
        moon = icons["moon_L"] if state.dark else icons["moon"]
        sun  = icons["sun_L"] if state.dark else icons["sun"]
        dice = icons["dice_L"] if state.dark else icons["dice"]
        info = icons["info_L"] if state.dark else icons["info"]
        pause = icons["pause_L"] if state.dark else icons["pause"]

        draw_button(screen, font_small, buttons["info"], icon=info)
        draw_button(screen, font_small, buttons["dark"], icon=(moon if not state.dark else sun))
        draw_button(screen, font_small, buttons["pause"], icon=pause)
        draw_button(screen, font_small, buttons["minus"], text="–")
        draw_button(screen, font_small, buttons["plus"], text="+")
        draw_button(screen, font_small, buttons["now"], icon=dice)

        if state.show_info:
            draw_info_panel(screen, W, H, font_small, INFO_LINES)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
