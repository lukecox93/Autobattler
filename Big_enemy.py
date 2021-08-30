import pygame
from Enemy import Enemy
import math

BLUE = (0, 0, 255)

class BigEnemy(Enemy):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_speed = 2
        self.speed = 2
        self.damage = 4 * math.ceil(level.modifier / 2)
        self.hp = 10 * level.modifier
        self.bounce = 0
        self.bounciness = 4
        self.given_xp = 15
        self.colour = BLUE
