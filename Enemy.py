import pygame

pygame.init()

class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 1
        self.damage = 1
        self.hp = 2
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.bounce = 0
        self.bounciness = 10