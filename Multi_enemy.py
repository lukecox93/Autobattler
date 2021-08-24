import pygame
from Enemy import Enemy
from Basic_enemy import BasicEnemy
import random
import math

RED = (255, 0, 0)
GREEN = (0, 255, 0)

class MultiEnemy(Enemy):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.bodies = []
        self.width = 20
        self.height = 20
        self.bodies.append(BasicEnemy(level, self.x, self.y))
        self.bodies.append(BasicEnemy(level, self.x - self.width - 2, self.y + self.height + 2))
        self.bodies.append(BasicEnemy(level, self.x, self.y + self.height + 2))
        self.bodies.append(BasicEnemy(level, self.x + self.width + 2, self.y + self.height + 2))
        self.bodies.append(BasicEnemy(level, self.x, self.y + (self.height*2 + 4)))
        self.rect = pygame.Rect(x - self.width - 2, y, self.width * 3 + 4, self.height * 3 + 4)
        self.bounce = 0
        self.bounciness = 2
        self.hp = 1
        self.given_xp = random.randint(1, 3)
        self.original_speed = 4
        self.speed = 4
        self.damage = 1 * math.ceil(level.modifier / 2)


    def draw(self, level):
        level.targeting(self)
        for body in self.bodies:
            pygame.draw.rect(level.window, RED, body.rect)
        self.move(level)

    def move(self, level):
        if self.bounce >= 1:
            pygame.Rect.move_ip(self.rect, -self.delta_x, -self.delta_y)
            if self.enemy_collision(level, -self.delta_x, -self.delta_y) < 0:
                for body in self.bodies:
                    pygame.Rect.move_ip(body.rect, -self.delta_x, -self.delta_y)
            self.bounce += 1
            if self.bounce >= 10:
                self.bounce = 0
                self.speed = self.original_speed
        else:
            pygame.Rect.move_ip(self.rect, self.delta_x, self.delta_y)
            if self.enemy_collision(level, self.delta_x, self.delta_y) < 0:
                for body in self.bodies:
                    pygame.Rect.move_ip(body.rect, self.delta_x, self.delta_y)

    def player_collision(self, level, enemies):
        collision = pygame.Rect.collidelist(level.player.rect, self.bodies)
        if collision >= 0:
            self.bodies[collision].player_collision(level, self.bodies)
            self.bounce = 1
            self.speed = self.original_speed * self.bounciness
            level.player.colour = RED
            level.player.collided = 1
            return level.player.check_hp()

    def bullet_collision(self, level, bullet):
        collision = pygame.Rect.collidelist(bullet.rect, self.bodies)
        if collision >= 0:
            self.bodies[collision].hp -= bullet.damage
            level.bullets.remove(bullet)
            if self.bodies[collision].hp <= 0:
                self.killed(level, collision)
            if len(self.bodies) == 0:
                level.enemies.remove(self)

    def killed(self, level, body):
        level.player.xp += self.given_xp
        del self.bodies[body]

    def enemy_collision(self, level, x, y):
        collision = pygame.Rect.collidelist(self.rect, level.enemies)
        if collision >= 0 and collision != level.enemies.index(self):
            pygame.Rect.move_ip(self.rect, -x, -y)
            return collision
        return -1

