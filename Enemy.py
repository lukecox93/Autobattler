import random

import pygame

pygame.init()

class Enemy():
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 4
        self.damage = 1
        self.hp = 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.bounce = 0
        self.bounciness = 10
        self.target = target
        self.delta_x = 0
        self.delta_y = 0
        self.given_xp = random.randint(1, 3)