import pygame
import random

LANES = 4
LANE_KEYS = [pygame.K_d, pygame.K_f, pygame.K_j, pygame.K_k]
LANE_LABELS = ['D', 'F', 'J', 'K']
LANE_COLORS = [(220, 80, 80), (80, 180, 220), (100, 220, 100), (220, 180, 60)]


class Note:
    WIDTH = 70
    HEIGHT = 20
    HOLD_DURATION = 1000  # 1 second in milliseconds

    def __init__(self, lane, y=-30, speed=4, is_hold=False):
        self.lane = lane
        self.y = y
        self.speed = speed
        self.is_hold = is_hold

        self.hit = False
        self.missed = False

        # Hold-note state
        self.holding = False
        self.hold_start_time = None
        self.hold_progress = 0

    def update(self):
        # Normal notes and unstarted hold notes continue falling.
        # Once a hold note is being held, keep its head at the hit line.
        if not self.holding:
            self.y += self.speed

    def start_hold(self):
        self.holding = True
        self.hold_start_time = pygame.time.get_ticks()

    def update_hold(self):
        if not self.holding or self.hold_start_time is None:
            return False

        elapsed = pygame.time.get_ticks() - self.hold_start_time
        self.hold_progress = min(
            1.0,
            elapsed / self.HOLD_DURATION
        )

        if elapsed >= self.HOLD_DURATION:
            self.holding = False
            self.hit = True
            self.hold_progress = 1.0
            return True

        return False

    def cancel_hold(self):
        self.holding = False
        self.hold_start_time = None
        self.hold_progress = 0

    def get_rect(self, lane_x):
        return pygame.Rect(
            lane_x - self.WIDTH // 2,
            int(self.y),
            self.WIDTH,
            self.HEIGHT
        )

    def get_hold_rect(self, lane_x):
        tail_height = 70

        return pygame.Rect(
            lane_x - self.WIDTH // 2 + 8,
            int(self.y + self.HEIGHT),
            self.WIDTH - 16,
            tail_height
        )