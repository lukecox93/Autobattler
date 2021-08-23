import random
import pygame

RED = (255, 0, 0)


class Enemy:
    def __init__(self, level, x, y):
        self.x = x
        self.y = y
        self.target = level.player
        self.delta_x = 0
        self.delta_y = 0
        self.bounce = None
        self.bounciness = None
        self.rect = None
        self.damage = 0
        self.hp = 0
        self.speed = 0

    def draw(self, level):
        pygame.draw.rect(level.window, RED, self.rect)
        level.targeting(self)
        if self.bounce >= 1:
            pygame.Rect.move_ip(self.rect, -self.delta_x, -self.delta_y)
            self.bounce += 1
            if self.bounce >= self.bounciness:
                self.bounce = 0
                self.speed /= 2
        else:
            pygame.Rect.move_ip(self.rect, self.delta_x, self.delta_y)

    def collision(self, level, enemies):
        level.player.hp -= self.damage
        self.hp -= level.player.body_damage

        if self.hp <= 0:
            enemies.remove(self)
        else:
            self.bounce = 1
            self.speed = -self.speed * 2

    def bullet_collision(self, level, bullet):
        self.hp -= bullet.damage
        if self.hp <= 0:
            self.killed(level, self)

    def killed(self, level, body):
        level.player.xp += self.given_xp
        level.enemies.remove(self)
