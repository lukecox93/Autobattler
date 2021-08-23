import pygame
from Enemy import Enemy
from Basic_enemy import BasicEnemy
import random
import math

RED = (255, 0, 0)

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
        self.rect = pygame.Rect(x - self.width, y - self.height, self.width * 3 + 4, self.height * 3 + 4)
        self.bounce = 0
        self.bounciness = 10
        self.hp = 1
        self.given_xp = random.randint(1, 3)
        self.speed = 4
        self.damage = 1 * math.ceil(level.modifier / 2)


    def draw(self, level):
        level.targeting(self)
        for body in self.bodies:
            pygame.draw.rect(level.window, RED, body.rect)
            body.delta_x = self.delta_x
            body.delta_y = self.delta_y
        if self.bounce >= 1:
            pygame.Rect.move_ip(self.rect, -self.delta_x, -self.delta_y)
            self.bounce += 1
            if self.bounce >= self.bounciness:
                self.bounce = 0
                self.speed /= 2
        else:
            for body in self.bodies:
                pygame.Rect.move_ip(body.rect, body.delta_x, body.delta_y)
            pygame.Rect.move_ip(self.rect, self.delta_x, self.delta_y)

    def collision(self, level, enemies):
        collision = pygame.Rect.collidelist(level.player.rect, self.bodies)
        if collision >= 0:
            self.bodies[collision].collision(level, self.bodies)
            level.player.colour = RED
            level.player.collided = 1
            return level.player.check_hp()

    def bullet_collision(self, level, bullet):
        collision = pygame.Rect.collidelist(bullet.rect, self.bodies)
        # TODO - need to change collision detection - seems to be detecting that it hits the overall shape, but not individual parts.
        print(collision)
        if collision >= 0:
            self.bodies[collision].hp -= bullet.damage
            if self.bodies[collision].hp <= 0:
                self.killed(level, collision)
            if len(self.bodies) == 0:
                level.enemies.remove(self)


    def killed(self, level, body):
        level.player.xp += self.given_xp
        del self.bodies[body]
