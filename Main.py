import random

import pygame

BLACK = (0,0,0)
RED = (255, 0, 0)

run = True

class level():
    def __init__(self, player):
        self.player = player
        self.width = 900
        self.height = 500
        self.window = pygame.display.set_mode((self.width, self.height))
        self.fps = 60
        self.enemies = []

    def draw_game(self):
        self.window.fill((255, 255, 255))
        pygame.draw.rect(self.window, BLACK, (self.player.x, self.player.y, self.player.width, self.player.height))
        for enemy in self.enemies:
            pygame.draw.rect(self.window, RED, enemy)
        pygame.display.update()

    def init_enemies(self):
        self.enemy_type_1 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_type_1, 1000)

    def events(self):
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



class Player():
    def __init__(self, width, height, speed):
        self.x = 400
        self.y = 200
        self.width = width
        self.height = height
        self.speed = speed

    def move(self, keys_pressed, level):
        if keys_pressed[pygame.K_a] and self.x - self.speed > 0:
            self.x -= self.speed
        if keys_pressed[pygame.K_d] and self.x + self.speed + self.width < level.width:
            self.x += self.speed
        if keys_pressed[pygame.K_w] and self.y - self.speed > 0:
            self.y -= self.speed
        if keys_pressed[pygame.K_s] and self.y + self.speed + self.height < level.height:
            self.y += self.speed



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
    player = Player(50, 50, 5)
    level_1 = level(player)
    level_1.init_enemies()
    while run:
        clock.tick(level_1.fps)
        level_1.events()
        level_1.draw_game()
        keys_pressed = pygame.key.get_pressed()
        player.move(keys_pressed, level_1)


    pygame.quit()

if __name__ == "__main__":
    main()