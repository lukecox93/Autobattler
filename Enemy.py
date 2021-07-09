import random
import pygame

RED = (255, 0, 0)


class Enemy:
    def __init__(self, level):
        self.x = random.randint(0, level.width)
        self.y = random.randint(0, level.height)
        self.target = level.player
        self.delta_x = 0
        self.delta_y = 0
        self.bounce = None
        self.bounciness = None
        self.rect = None

    def draw(self, level):
        pygame.draw.rect(level.window, RED, self.rect)
        level.targeting(self)
        if self.bounce >= 1:
            pygame.Rect.move_ip(self.rect, -self.delta_x, -self.delta_y)
            self.bounce += 1
            if self.bounce >= self.bounciness:
                self.bounce = 0
        else:
            pygame.Rect.move_ip(self.rect, self.delta_x, self.delta_y)
