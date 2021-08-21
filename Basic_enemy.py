import pygame
from Enemy import Enemy
import random


class BasicEnemy(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.width = 20
        self.height = 20
        self.x = random.randint(0, level.width - self.width)
        self.y = random.randint(0, level.height - self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 4
        self.damage = 1 * round(level.modifier / 2)
        self.hp = 2 * level.modifier
        self.bounce = 0
        self.bounciness = 10
        self.given_xp = random.randint(1, 3)
