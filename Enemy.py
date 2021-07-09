import random
import pygame

class Enemy():
    def __init__(self, level):
        self.x = random.randint(0, level.width)
        self.y = random.randint(0, level.height)
        self.width = 20
        self.height = 20
        self.speed = 4
        self.damage = 1
        self.hp = 2
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bounce = 0
        self.bounciness = 10
        self.target = level.player
        self.delta_x = 0
        self.delta_y = 0
        self.given_xp = random.randint(1, 3)