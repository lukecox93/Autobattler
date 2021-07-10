import pygame
import random

GREEN = (0, 255, 0)


class Drop:
    def __init__(self, level):
        self.width = 10
        self.height = 10
        self.x = random.randint(0, level.width - self.width)
        self.y = random.randint(0, level.height - self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.effect = None

    def draw(self, level):
        pygame.draw.rect(level.window, GREEN, self.rect)
