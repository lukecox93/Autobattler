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
        if self.player.collided > 0:
            self.player.collided += 1
            if self.player.collided >= 5:
                self.player.collided = 0
        else:
            self.player.colour = BLACK
        pygame.draw.rect(self.window, self.player.colour, (self.player.rect))
        health_rect = (self.player.rect[0], self.player.rect[1] - 10, self.player.rect[2] * (self.player.hp/self.player.max_hp), 5)
        pygame.draw.rect(self.window, GREEN, health_rect)
        if self.player.hp < self.player.max_hp:
            pygame.draw.rect(self.window, RED, (health_rect[0] + health_rect[2], health_rect[1], self.player.rect[2] - health_rect[2], 5))
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
            bullet = Bullet(self.player.rect[0] + (self.player.rect[2] // 2), self.player.rect[1] + (self.player.rect[3]
                            // 2), 4, 4, 15, self.player.target, 1)
            self.bullets.append(bullet)
            self.targeting(bullet)

    def targeting(self, bullet):
        x_dist = ((bullet.target.rect[0] + (bullet.target.rect[2] // 2)) - (bullet.rect[0] + (bullet.rect[2] // 2)))
        y_dist = (bullet.target.rect[1] + (bullet.target.rect[3] // 2) - (bullet.rect[1] + (bullet.rect[2] // 2)))
        if x_dist == 0:
            if y_dist != 0:
                bullet.delta_x = 0
                bullet.delta_y = round((y_dist * bullet.speed) / (abs(y_dist)))
        elif y_dist == 0:
            if x_dist != 0:
                bullet.delta_y = 0
                bullet.delta_x = round((x_dist * bullet.speed) / (abs(x_dist)))
        elif y_dist == 0 and x_dist == 0:
            bullet.delta_x, bullet.delta_y = bullet.speed, 0
        else:
            bullet.delta_x = round((x_dist * bullet.speed) / (min(abs(x_dist), abs(y_dist))))
            bullet.delta_y = round((y_dist * bullet.speed) / (min(abs(x_dist), abs(y_dist))))

        if bullet.delta_x > bullet.speed:
            bullet.delta_y = abs(bullet.speed / bullet.delta_x) * bullet.delta_y
            bullet.delta_x = bullet.speed
        if bullet.delta_x < -bullet.speed:
            bullet.delta_y = abs(bullet.speed / bullet.delta_x) * bullet.delta_y
            bullet.delta_x = -bullet.speed
        if bullet.delta_y > bullet.speed:
            bullet.delta_x = abs(bullet.speed / bullet.delta_y) * bullet.delta_x
            bullet.delta_y = bullet.speed
        if bullet.delta_y < -bullet.speed:
            bullet.delta_x = abs(bullet.speed / bullet.delta_y) * bullet.delta_x
            bullet.delta_y = -bullet.speed

    def bullet_collision(self):
        for bullet in self.bullets:
            collision = pygame.Rect.collidelist(bullet.rect, self.enemies)
            if collision >= 0:
                self.enemies[collision].hp -= bullet.damage
                if self.enemies[collision].hp <= 0:
                    del self.enemies[collision]
                self.bullets.remove(bullet)
            elif bullet.x > self.width or bullet.x < 0 or bullet.y > self.height or bullet.y < 0:
                self.bullets.remove(bullet)

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
            return self.player.check_hp(self)

