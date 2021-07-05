import pygame
import random
import math

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

run = True

class level():
    def __init__(self, player):
        self.player = player
        self.width = 900
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.enemies = []
        self.bullets = []
        self.targets = []

    def draw_game(self):
        self.window.fill(WHITE)
        for enemy in self.enemies:
            pygame.draw.rect(self.window, RED, (enemy.rect))
        for bullet in self.bullets:
            pygame.draw.rect(self.window, BLUE, (bullet.rect))
            pygame.Rect.move_ip(bullet.rect, bullet.speed, 0)
        pygame.draw.rect(self.window, BLACK, (self.player.rect))
        pygame.display.update()

    def events(self,player):
        self.enemy_type_1 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_type_1, 1000)
        self.create_bullet = pygame.USEREVENT + 2
        pygame.time.set_timer(self.create_bullet, 1000//player.att_speed)

    def event_handler(self):
        global run
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.USEREVENT + 1:
                enemy = Enemy(random.randint(0, self.width), random.randint(0, self.height))
                self.enemies.append(enemy)
            if event.type == pygame.USEREVENT + 2: #create bullet
                self.target_finder()

    def target_finder(self):
        for enemy in self.enemies:  # find closest enemy
            self.targets.append(math.sqrt(
                (abs((enemy.rect[0] + enemy.rect[2] // 2) - (self.player.rect[0] + self.player.rect[2] // 2)) ** 2) + (
                            abs((enemy.rect[1] + enemy.rect[3] // 2) - (self.player.rect[1] + self.player.rect[3] // 2)) ** 2)))
        if self.targets:
            closest_enemy_index = self.targets.index(min(self.targets))
            target = self.enemies[closest_enemy_index]
            bullet = Bullet(self.player.rect[0] + (self.player.rect[2] // 2), self.player.rect[1] + (self.player.rect[3] // 2), 10, 4,
                            5, target)
            self.bullets.append(bullet)
        self.targets = []

    def bullet_collision(self):
        for bullet in self.bullets:
            collision = pygame.Rect.collidelist(bullet.rect, self.enemies)
            if collision >= 0:
                del self.enemies[collision]
                self.bullets.remove(bullet)
            elif bullet.x > self.width or bullet.x < 0 or bullet.y > self.height or bullet.y < 0:
                self.bullets.remove(bullet)

    def player_collision(self):
        collision = pygame.Rect.collidelist(self.player.rect, self.enemies)
        if collision >= 0:
            del self.enemies[collision]
            self.player.hp -= 1

    def move_enemies(self):
        for enemy in self.enemies:
            if (enemy.rect[0] + enemy.rect[2]//2) < (self.player.rect[0] + self.player.rect[2]//2):
                pygame.Rect.move_ip(enemy.rect, enemy.speed, 0)
            elif (enemy.rect[0] + enemy.rect[2]//2) > (self.player.rect[0] + self.player.rect[2]//2):
                pygame.Rect.move_ip(enemy.rect, -enemy.speed, 0)
            if (enemy.rect[1] + enemy.rect[3]//2) < (self.player.rect[1] + self.player.rect[3]//2):
                pygame.Rect.move_ip(enemy.rect, 0, enemy.speed)
            elif (enemy.rect[1] + enemy.rect[3]//2) > (self.player.rect[1] + self.player.rect[3]//2):
                pygame.Rect.move_ip(enemy.rect, 0, -enemy.speed)


class Player():
    def __init__(self, x, y, width, height, speed, att_speed, hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.att_speed = att_speed
        self.rect = pygame.Rect(x, y, width, height)
        self.hp = hp

    def move(self, keys_pressed, level):
        if keys_pressed[pygame.K_a] and self.rect[0] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, -self.speed, 0)
        if keys_pressed[pygame.K_d] and self.rect[0] + self.speed + self.rect[2] < level.width:
            pygame.Rect.move_ip(self.rect, self.speed, 0)
        if keys_pressed[pygame.K_w] and self.rect[1] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, 0, -self.speed)
        if keys_pressed[pygame.K_s] and self.rect[1] + self.speed + self.rect[3] < level.height:
            pygame.Rect.move_ip(self.rect, 0, self.speed)


class Bullet():
    def __init__(self, x, y, width, height, speed, target):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.target = target
        self.rect = pygame.Rect(x, y, width, height)


class Enemy():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.speed = 1
        self.rect = pygame.Rect(x, y, self.width, self.height)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    player = Player(400, 200, 50, 50, 5, 5, 5)
    level_1 = level(player)
    level_1.events(player)
    while run:
        clock.tick(level_1.fps)
        level_1.event_handler()
        level_1.draw_game()
        keys_pressed = pygame.key.get_pressed()
        player.move(keys_pressed, level_1)
        level_1.bullet_collision()
        level_1.player_collision()
        level_1.move_enemies()

        if player.hp <= 0:
            print("game over")
            level_1.window.fill(RED)
            pygame.display.update()
            pygame.time.wait(2000)
            main()

    pygame.quit()

if __name__ == "__main__":
    main()