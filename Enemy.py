import random

import pygame

pygame.init()

class Enemy():
    speed = 4
    width = 20
    height = 20
    def __init__(self, level):
        self.x = random.randint(0, level.width)
        self.y = random.randint(0, level.height)
        self.speed = Enemy.speed
        self.damage = 1
        self.hp = 2
        self.rect = pygame.Rect(self.x, self.y, Enemy.width, Enemy.height)
        self.bounce = 0
        self.bounciness = 10
        self.target = level.player
        self.delta_x = 0
        self.delta_y = 0
        self.given_xp = random.randint(1, 3)