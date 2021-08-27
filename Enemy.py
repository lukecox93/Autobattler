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
        self.original_speed = 0
        self.speed = 0
        self.given_xp = 0

    def draw(self, level):
        pygame.draw.rect(level.window, RED, self.rect)
        level.targeting(self)
        self.move(level)

    def move(self, level):
        if self.bounce >= 1:
            pygame.Rect.move_ip(self.rect, -self.delta_x, -self.delta_y)
            self.enemy_collision(level, -self.delta_x, -self.delta_y)
            self.bounce += 1
            if self.bounce >= 10:
                print(self.speed)
                self.bounce = 0
                self.speed = self.original_speed
                print(self.speed)
        else:
            pygame.Rect.move_ip(self.rect, self.delta_x, self.delta_y)
            self.enemy_collision(level, self.delta_x, self.delta_y)

    def player_collision(self, level, enemies):
        level.player.hp -= self.damage
        self.hp -= level.player.body_damage

        if self.hp <= 0:
            enemies.remove(self)
        else:
            self.bounce = 1
            self.speed = self.original_speed * self.bounciness

    def bullet_collision(self, level, bullet):
        self.hp -= bullet.damage
        if self.hp <= 0:
            self.killed(level, self)
        bullet.collision(level)

    def killed(self, level, body):
        level.player.xp += self.given_xp
        level.enemies.remove(self)

    def enemy_collision(self, level, x, y):
        collision = pygame.Rect.collidelist(self.rect, level.enemies)
        if collision >= 0 and collision != level.enemies.index(self):
            pygame.Rect.move_ip(self.rect, -x, -y)
