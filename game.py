import pygame
from config import intervals

# Holds the current state of the game and user settings
class GameState:
    def __init__(self):
        # Index of the selected interval in the intervals list
        self.idx_interval = 2

        # Milliseconds between automatic dice rolls
        self.TIMER_MS = intervals[self.idx_interval]

        # Result of the current dice roll
        self.current_roll = None

        # True if the game is automatically paused due to rolling a 7
        self.paused = False

        # True if the user manually paused the game
        self.manual_paused = False

        # Dark mode setting (True for dark mode, False for light)
        self.dark = False

        # Whether the info panel is currently shown
        self.show_info = False

        # Indicates if the game has started
        self.started = False

        # Number of players selected before starting the game
        self.num_players = 4

        # Stores the player selected to move the robber when a 7 is rolled
        self.robber_player = None

        # Timestamp for scheduling the next automatic roll
        self.next_tick = 0
