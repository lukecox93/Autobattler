import pygame

pygame.init()

class Bullet():
    def __init__(self, x, y, width, height, speed, target, damage):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.target = target
        self.damage = damage
        self.rect = pygame.Rect(x, y, width, height)
        self.delta_x = 0
        self.delta_y = 0
        self.direction = 0