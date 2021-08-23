import pygame
from Enemy import Enemy
import random
import math


class BigEnemy(Enemy):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.width = 40
        self.height = 40
        self.x = random.randint(0, level.width - self.width)
        self.y = random.randint(0, level.height - self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 2
        self.damage = 4 * math.ceil(level.modifier / 2)
        self.hp = 10 * level.modifier
        self.bounce = 0
        self.bounciness = 10
        self.given_xp = 15
