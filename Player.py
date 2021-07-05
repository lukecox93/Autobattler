import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.init()

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
        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and self.rect[0] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, -self.speed, 0)
        if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and self.rect[0] + self.speed + self.rect[2] < level.width:
            pygame.Rect.move_ip(self.rect, self.speed, 0)
        if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and self.rect[1] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, 0, -self.speed)
        if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and self.rect[1] + self.speed + self.rect[3] < level.height:
            pygame.Rect.move_ip(self.rect, 0, self.speed)

    def check_hp(self, level):
        if level.player.hp <= 0:
            level.window.fill(RED)
            pygame.display.update()
            pygame.time.wait(2000)
            return True
        return False