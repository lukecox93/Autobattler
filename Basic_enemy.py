import pygame
from Enemy import Enemy
import random
import math


class BasicEnemy(Enemy):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.width = 20
        self.height = 20
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.original_speed = 4
        self.speed = 4
        self.damage = 1 * math.ceil(level.modifier / 2)
        self.hp = 2 * level.modifier
        self.bounce = 0
        self.bounciness = 2
        self.given_xp = random.randint(1, 3)
