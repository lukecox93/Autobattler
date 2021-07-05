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
            self.bullet_targeting(bullet)
        if self.player.collided > 0:
            self.player.collided += 1
            if self.player.collided >= 5:
                self.player.collided = 0
        else:
            self.player.colour = BLACK
        pygame.draw.rect(self.window, self.player.colour, (self.player.rect))
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
                            // 2), 10, 4, 5, self.player.target, 1)
            self.bullets.append(bullet)

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
            if self.enemies[collision].hp <= 0:
                del self.enemies[collision]
            else:
                self.enemies[collision].speed = -self.enemies[collision].speed*2


    def move_enemies(self):
        for enemy in self.enemies:
            if enemy.speed < 0:
                if enemy.bounce >= enemy.bounciness:
                    enemy.speed = -enemy.speed//2
                    enemy.bounce = 0
                else:
                    enemy.bounce += 1
            if (enemy.rect[0] + enemy.rect[2]//2) < (self.player.rect[0] + self.player.rect[2]//2):
                pygame.Rect.move_ip(enemy.rect, enemy.speed, 0)
            elif (enemy.rect[0] + enemy.rect[2]//2) > (self.player.rect[0] + self.player.rect[2]//2):
                pygame.Rect.move_ip(enemy.rect, -enemy.speed, 0)
            if (enemy.rect[1] + enemy.rect[3]//2) < (self.player.rect[1] + self.player.rect[3]//2):
                pygame.Rect.move_ip(enemy.rect, 0, enemy.speed)
            elif (enemy.rect[1] + enemy.rect[3]//2) > (self.player.rect[1] + self.player.rect[3]//2):
                pygame.Rect.move_ip(enemy.rect, 0, -enemy.speed)

    def bullet_targeting(self, bullet):
        if bullet.target not in self.enemies:
            pygame.Rect.move_ip(bullet.rect, bullet.speed, 0)
        else:
            if (bullet.rect[0] + bullet.rect[2] // 2) < (bullet.target.rect[0] + bullet.target.rect[2] // 2):
                pygame.Rect.move_ip(bullet.rect, bullet.speed, 0)
            elif (bullet.rect[0] + bullet.rect[2] // 2) > (bullet.target.rect[0] + bullet.target.rect[2] // 2):
                pygame.Rect.move_ip(bullet.rect, -bullet.speed, 0)
            if (bullet.rect[1] + bullet.rect[3] // 2) < (bullet.target.rect[1] + bullet.target.rect[3] // 2):
                pygame.Rect.move_ip(bullet.rect, 0, bullet.speed)
            elif (bullet.rect[1] + bullet.rect[3] // 2) > (bullet.target.rect[1] + bullet.target.rect[3] // 2):
                pygame.Rect.move_ip(bullet.rect, 0, -bullet.speed)
    #TODO - need to use trig or vectors to pathfind properly


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
        self.target = None
        self.body_damage = 1
        self.collided = 0
        self.colour = BLACK

    def move(self, keys_pressed, level):
        if keys_pressed[pygame.K_LEFT] and self.rect[0] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, -self.speed, 0)
        if keys_pressed[pygame.K_RIGHT] and self.rect[0] + self.speed + self.rect[2] < level.width:
            pygame.Rect.move_ip(self.rect, self.speed, 0)
        if keys_pressed[pygame.K_UP] and self.rect[1] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, 0, -self.speed)
        if keys_pressed[pygame.K_DOWN] and self.rect[1] + self.speed + self.rect[3] < level.height:
            pygame.Rect.move_ip(self.rect, 0, self.speed)


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
        print(level_1.enemies)

        if player.hp <= 0:
            print("game over")
            level_1.window.fill(RED)
            pygame.display.update()
            pygame.time.wait(2000)
            main()

    pygame.quit()

if __name__ == "__main__":
    main()