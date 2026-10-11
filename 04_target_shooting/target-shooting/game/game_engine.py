"""
GameEngine: owns the targets and handles player clicks.

Targets move and bounce (see Target.update). Score and combo are
tracked here too, and the round is timed.

Scoring rule: each hit is worth BASE_POINTS x multiplier. The multiplier
is 1 + (streak // HITS_PER_COMBO_LEVEL), capped at MAX_MULTIPLIER, where
streak = consecutive hits since the last miss. The multiplier is read
BEFORE the streak goes up, so the combo shown on screen is what the next
hit is worth. A miss resets the streak (and so the multiplier) to x1.

Round rule: the round lasts ROUND_SECONDS of accumulated real frame time.
When it runs out, game_over is set: the timer and targets freeze and
clicks no longer change anything except the Restart button.
"""

import math
import random

from game.target import Target
from game.hit_detection import check_hit
from game.renderer import WIDTH, HEIGHT, RESTART_BUTTON_RECT

NUM_TARGETS = 3
TARGET_RADIUS = 28
MAX_DT = 0.05  # cap frame time for MOVEMENT so a lag spike can't teleport targets
ROUND_SECONDS = 30

BASE_POINTS = 10
HITS_PER_COMBO_LEVEL = 3
MAX_MULTIPLIER = 5

# (pattern, speed in pixels/second) - slow, fast and medium speeds
MOVE_PATTERNS = [
    ("horizontal", 90),
    ("diagonal", 220),
    ("vertical", 150),
]


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Start a fresh round. Used at startup and for every restart."""
        # One of each pattern to start, so the mix of speeds is guaranteed
        self.targets = [
            self._random_target(MOVE_PATTERNS[i % len(MOVE_PATTERNS)])
            for i in range(NUM_TARGETS)
        ]
        self.hits = 0
        self.misses = 0
        self.score = 0
        self.streak = 0      # consecutive hits since the last miss
        self.elapsed = 0.0   # seconds of the round used so far
        self.game_over = False

    @property
    def multiplier(self):
        """Current combo multiplier: +1 every HITS_PER_COMBO_LEVEL hits, capped."""
        return min(1 + self.streak // HITS_PER_COMBO_LEVEL, MAX_MULTIPLIER)

    @property
    def time_left(self):
        return max(0.0, ROUND_SECONDS - self.elapsed)

    def _random_target(self, pattern=None):
        x = random.randint(TARGET_RADIUS + 10, WIDTH - TARGET_RADIUS - 10)
        y = random.randint(TARGET_RADIUS + 10, HEIGHT - TARGET_RADIUS - 10)

        kind, speed = pattern or random.choice(MOVE_PATTERNS)
        sign_x = random.choice((-1, 1))
        sign_y = random.choice((-1, 1))
        if kind == "horizontal":
            vx, vy = sign_x * speed, 0
        elif kind == "vertical":
            vx, vy = 0, sign_y * speed
        else:  # diagonal: total speed stays `speed`
            part = speed / math.sqrt(2)
            vx, vy = sign_x * part, sign_y * part

        return Target(x, y, radius=TARGET_RADIUS, vx=vx, vy=vy)

    def handle_click(self, pos):
        if self.game_over:
            # Only the Restart button does anything; no hits/misses/score.
            if RESTART_BUTTON_RECT.collidepoint(pos):
                self.reset()
            return

        target = check_hit(self.targets, pos)
        if target is not None:
            self.score += BASE_POINTS * self.multiplier  # multiplier BEFORE streak++
            self.streak += 1
            self.hits += 1
            self.targets.remove(target)
            self.targets.append(self._random_target())
        else:
            self.misses += 1
            self.streak = 0

    def update(self, dt):
        if self.game_over:
            return  # timer and targets stay frozen on the game-over screen

        # The timer uses the real (uncapped) dt so the round is 30 real seconds.
        self.elapsed += dt
        if self.elapsed >= ROUND_SECONDS:
            self.elapsed = ROUND_SECONDS
            self.game_over = True
            return

        # Only movement uses the capped dt.
        move_dt = min(dt, MAX_DT)
        for target in self.targets:
            target.update(move_dt, WIDTH, HEIGHT)

    def draw(self, surface, font, big_font):
        from game import renderer
        renderer.draw_scene(surface, self.targets)
        if self.game_over:
            renderer.draw_game_over(surface, font, big_font,
                                    self.score, self.hits, self.misses)
        else:
            renderer.draw_hud(surface, font, self.score, self.multiplier,
                              self.hits, self.misses, self.time_left)