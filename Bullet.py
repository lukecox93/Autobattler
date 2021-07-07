import pygame

pygame.init()

class Bullet():
    width = 6
    height = 6
    speed = 15
    def __init__(self, x, y, player):
        self.target = player.target
        self.damage = player.bullet_damage
        self.rect = pygame.Rect(x, y, Bullet.width, Bullet.height)
        self.delta_x = 0
        self.delta_y = 0
        self.direction = 0