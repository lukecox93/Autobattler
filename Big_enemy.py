import pygame
from Enemy import Enemy
import random


class BigEnemy(Enemy):
    def __init__(self, level):
        super().__init__(level)
        self.width = 40
        self.height = 40
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.speed = 2
        self.damage = 4
        self.hp = 10
        self.bounce = 0
        self.bounciness = 10
        self.given_xp = 15
