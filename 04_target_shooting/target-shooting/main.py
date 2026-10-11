"""
Target Shooting (Lab Starter)

Run with:  python3 main.py

Click on targets to hit them. When the 30-second round ends, press R or
click Restart to play again.
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Target Shooting")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 22)
    big_font = pygame.font.SysFont("consolas", 56, bold=True)

    engine = GameEngine()
    clock.tick()  # discard setup time (font loading etc.) so round 1 gets a full 30 s
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # seconds since the previous frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                engine.handle_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and engine.game_over:
                    engine.reset()

        engine.update(dt)
        engine.draw(screen, font, big_font)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()