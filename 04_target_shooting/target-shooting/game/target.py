"""
Target: a circular target the player clicks on. (x, y) is the CENTER
of the circle - this matters for how it's drawn vs. how it's hit-tested.

vx, vy are the velocity in pixels per second.
"""

import pygame


class Target:
    def __init__(self, x, y, radius=28, color=(230, 90, 70), vx=0.0, vy=0.0):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = vx
        self.vy = vy

    def update(self, dt, width, height):
        """Move by velocity * dt, then bounce off the play-area edges.
        This is where all the bounce logic lives. The whole circle must
        stay inside, so edges are tested using the radius."""
        self.x += self.vx * dt
        self.y += self.vy * dt

        r = self.radius
        if self.x - r < 0:
            self.x = r
            self.vx = abs(self.vx)
        elif self.x + r > width:
            self.x = width - r
            self.vx = -abs(self.vx)

        if self.y - r < 0:
            self.y = r
            self.vy = abs(self.vy)
        elif self.y + r > height:
            self.y = height - r
            self.vy = -abs(self.vy)

    def get_bounding_rect(self):
        """A square bounding box around the circle (top-left is the
        center minus the radius). Not used for hit testing - that is a
        true circle check in hit_detection.check_hit."""
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )