import pygame
import random

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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
        self.bull = 10

    def draw_game(self):
        self.window.fill(WHITE)
        pygame.draw.rect(self.window, BLACK, (self.player.x, self.player.y, self.player.width, self.player.height))
        for enemy in self.enemies:
            pygame.draw.rect(self.window, RED, enemy)
        for bullet in self.bullets:
            pygame.draw.rect(self.window, BLUE, bullet)
            bullet[0] += 10
        pygame.display.update()

    def init_enemies(self):
        self.enemy_type_1 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_type_1, 1000)

    def init_bullets(self, player):
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
                enemy = Enemy(self)
                self.enemies.append(enemy.pos)
            if event.type == pygame.USEREVENT + 2:
                bullet = Bullet(self.player.x + (self.player.width//2), self.player.y + (self.player.height//2))
                self.bullets.append([bullet.x, bullet.y, bullet.width, bullet.height])


class Player():
    def __init__(self, width, height, speed, att_speed):
        self.x = 400
        self.y = 200
        self.width = width
        self.height = height
        self.speed = speed
        self.att_speed = att_speed

    def move(self, keys_pressed, level):
        if keys_pressed[pygame.K_a] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys_pressed[pygame.K_d] and self.x + self.speed + self.width < level.width:
            self.x += self.speed
        if keys_pressed[pygame.K_w] and self.y - self.speed > 0:
            self.y -= self.speed
        if keys_pressed[pygame.K_s] and self.y + self.speed + self.height < level.height:
            self.y += self.speed


class Bullet():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 4
        self.height = 4
        self.speed = 5
        self.target = (20,20)


class Enemy():
    def __init__(self, level):
        self.x = random.randint(0, level.width)
        self.y = random.randint(0, level.height)
        self.width = 20
        self.height = 20
        self.velocity = 5
        self.pos = pygame.Rect(self.x, self.y, self.width, self.height)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    player = Player(50, 50, 5, 5)
    level_1 = level(player)
    level_1.init_enemies()
    level_1.init_bullets(player)
    while run:
        clock.tick(level_1.fps)
        level_1.event_handler()
        level_1.draw_game()
        keys_pressed = pygame.key.get_pressed()
        player.move(keys_pressed, level_1)

    pygame.quit()

if __name__ == "__main__":
    main()