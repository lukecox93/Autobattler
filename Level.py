import pygame
import random
import math
import sys
from Enemy import Enemy
from Bullet import Bullet
pygame.font.init()



BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

HEALTH_FONT = pygame.font.SysFont("Verdana", 30)

pygame.init()

class Level():
    def __init__(self, player):
        self.player = player
        self.width = 1920
        self.height = 1080
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.enemies = []
        self.bullets = []
        self.targets = []
        self.run = True

    def draw_game(self):
        self.window.fill(WHITE)
        health_text = HEALTH_FONT.render("HP: " + str(self.player.hp), True, BLACK)
        self.window.blit(health_text, (self.width - health_text.get_width() - 10, 10))
        for enemy in self.enemies:
            pygame.draw.rect(self.window, RED, (enemy.rect))
            self.targeting(enemy)
            if enemy.bounce >= 1:
                pygame.Rect.move_ip(enemy.rect, -enemy.delta_x, -enemy.delta_y)
                enemy.bounce += 1
                if enemy.bounce >= enemy.bounciness:
                    enemy.bounce = 0
            else:
                pygame.Rect.move_ip(enemy.rect, enemy.delta_x, enemy.delta_y)
        for bullet in self.bullets:
            pygame.draw.rect(self.window, BLUE, (bullet.rect))
            pygame.Rect.move_ip(bullet.rect, bullet.delta_x, bullet.delta_y)

        pygame.draw.rect(self.window, self.player.colour, (self.player.rect))
        self.player.draw_health_bar(self)
        self.player.draw_xp_bar(self)

        pygame.display.update()

    def events(self,player):
        self.enemy_type_1 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_type_1, 1000)
        self.create_bullet = pygame.USEREVENT + 2
        pygame.time.set_timer(self.create_bullet, round(1000/player.att_speed))

    def event_handler(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                    sys.exit()
            if event.type == pygame.USEREVENT + 1:
                enemy = Enemy(random.randint(0, self.width), random.randint(0, self.height), self.player)
                self.enemies.append(enemy)
            if event.type == pygame.USEREVENT + 2: #create bullet
                self.target_finder()

    def target_finder(self):
        targets = []
        for enemy in self.enemies:  # find closest enemy
            targets.append(math.sqrt(
                (abs((enemy.rect[0] + enemy.rect[2] // 2) - (self.player.rect[0] + self.player.rect[2] // 2)) ** 2) + (
                            abs((enemy.rect[1] + enemy.rect[3] // 2) - (self.player.rect[1] + self.player.rect[3] // 2))
                            ** 2)))
        if targets:
            closest_enemy_index = targets.index(min(targets))
            self.player.target = self.enemies[closest_enemy_index]
            #TODO = bullets spawn based on their top left coordinates rather than their centre, only becomes an issue with larger bullet sizes but worth changing
            bullet = Bullet(self.player.rect[0] + (self.player.rect[2] // 2), self.player.rect[1] + (self.player.rect[3]
                            // 2), round(self.player.bullet_size), round(self.player.bullet_size), 15, self.player.target, self.player.bullet_damage)
            self.bullets.append(bullet)
            self.targeting(bullet)

    def targeting(self, sprite):
        x_dist = ((sprite.target.rect[0] + (sprite.target.rect[2] // 2)) - (sprite.rect[0] + (sprite.rect[2] // 2)))
        y_dist = (sprite.target.rect[1] + (sprite.target.rect[3] // 2) - (sprite.rect[1] + (sprite.rect[2] // 2)))

        sprite.delta_x = round((x_dist * sprite.speed) / (max(abs(x_dist), abs(y_dist))))
        sprite.delta_y = round((y_dist * sprite.speed) / (max(abs(x_dist), abs(y_dist))))

    def bullet_collision(self):
        for bullet in self.bullets:
            collision = pygame.Rect.collidelist(bullet.rect, self.enemies)
            if collision >= 0:
                self.enemies[collision].hp -= bullet.damage
                if self.enemies[collision].hp <= 0:
                    self.enemy_killed(self.enemies[collision])
                self.bullets.remove(bullet)
            elif bullet.x > self.width or bullet.x < 0 or bullet.y > self.height or bullet.y < 0:
                self.bullets.remove(bullet)

    def enemy_killed(self, enemy):
        self.player.xp += enemy.given_xp
        self.enemies.remove(enemy)

    def player_collision(self):
        collision = pygame.Rect.collidelist(self.player.rect, self.enemies)
        if collision >= 0:
            self.player.hp -= self.enemies[collision].damage
            self.enemies[collision].hp -= self.player.body_damage
            self.player.colour = RED
            self.player.collided = 1
            self.enemies[collision].bounce = 1
            if self.enemies[collision].hp <= 0:
                del self.enemies[collision]
            else:
                self.enemies[collision].speed = -self.enemies[collision].speed*2

