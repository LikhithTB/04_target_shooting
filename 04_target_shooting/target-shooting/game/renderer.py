"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import math

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 25, 35)
COLOR_TEXT = (255, 255, 255)
COLOR_COMBO = (255, 220, 80)  # combo line turns gold once a combo is active
COLOR_WARN = (255, 90, 90)    # timer turns red in the last seconds
COLOR_BUTTON = (60, 110, 190)

WARN_SECONDS = 5

# Clickable Restart button on the game-over screen (also used by the engine)
RESTART_BUTTON_RECT = pygame.Rect(WIDTH // 2 - 110, 335, 220, 50)


def draw_scene(surface, targets):
    surface.fill(COLOR_BG)
    for target in targets:
        pygame.draw.circle(surface, target.color, (int(target.x), int(target.y)), target.radius)
        pygame.draw.circle(surface, (255, 255, 255), (int(target.x), int(target.y)), target.radius, 2)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_text_centered(surface, font, text, center, color=COLOR_TEXT):
    surf = font.render(text, True, color)
    surface.blit(surf, surf.get_rect(center=center))


def draw_hud(surface, font, score, multiplier, hits, misses, time_left):
    """Score, combo and hit/miss counter stacked top-left; countdown top-right."""
    draw_text(surface, font, f"Score: {score}", (10, 10))
    combo_color = COLOR_COMBO if multiplier > 1 else COLOR_TEXT
    draw_text(surface, font, f"Combo: x{multiplier}", (10, 36), combo_color)
    draw_text(surface, font, f"Hits: {hits}  Misses: {misses}", (10, 62))

    seconds = math.ceil(time_left)  # shows 30 at the start, 0 only at game over
    timer_color = COLOR_WARN if seconds <= WARN_SECONDS else COLOR_TEXT
    timer_surf = font.render(f"Time: {seconds}", True, timer_color)
    surface.blit(timer_surf, timer_surf.get_rect(topright=(WIDTH - 10, 10)))


def draw_game_over(surface, font, big_font, score, hits, misses):
    """Dim the frozen scene and show the final results and Restart button."""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    cx = WIDTH // 2
    draw_text_centered(surface, big_font, "GAME OVER", (cx, 150), COLOR_COMBO)
    draw_text_centered(surface, font, f"Final score: {score}", (cx, 230))
    draw_text_centered(surface, font, f"Hits: {hits}  Misses: {misses}", (cx, 265))

    pygame.draw.rect(surface, COLOR_BUTTON, RESTART_BUTTON_RECT, border_radius=8)
    pygame.draw.rect(surface, COLOR_TEXT, RESTART_BUTTON_RECT, 2, border_radius=8)
    draw_text_centered(surface, font, "Restart (R)", RESTART_BUTTON_RECT.center)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)