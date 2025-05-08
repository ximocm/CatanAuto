import pygame
from config import intervals

class GameState:
    def __init__(self):
        self.idx_interval = 2
        self.TIMER_MS = intervals[self.idx_interval]
        self.current_roll = None
        self.paused = False
        self.manual_paused = False
        self.dark = False
        self.show_info = False
        self.started = False
        self.num_players = 4
        self.robber_player = None
        self.next_tick = 0
