import pygame

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Player():
    xp_to_level_up = 3
    colour = BLACK

    def __init__(self, x, y, width, height, speed, att_speed, hp):
        self.speed = speed
        self.att_speed = att_speed
        self.rect = pygame.Rect(x, y, width, height)
        self.max_hp = hp
        self.hp = hp
        self.target = None
        self.body_damage = 1
        self.collided = 0
        self.level = 1
        self.base_bullet_damage = 1
        self.bullet_damage = self.base_bullet_damage * self.level
        self.base_bullet_size = 6
        self.bullet_size = 6
        self.xp = 0
        self.xp_to_level_up = (Player.xp_to_level_up * self.level)
        self.score = 0

    def move(self, keys_pressed, level):
        if (keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]) and self.rect[0] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, -self.speed, 0)
        if (keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]) and self.rect[0] + self.speed + self.rect[2] < level.width:
            pygame.Rect.move_ip(self.rect, self.speed, 0)
        if (keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]) and self.rect[1] - self.speed > 0:
            pygame.Rect.move_ip(self.rect, 0, -self.speed)
        if (keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]) and self.rect[1] + self.speed + self.rect[3] < level.height:
            pygame.Rect.move_ip(self.rect, 0, self.speed)

    def draw_health_bar(self, level):
        health_rect = (self.rect[0], self.rect[1] - 10, self.rect[2] * (self.hp/self.max_hp), 5)
        pygame.draw.rect(level.window, RED, (self.rect[0], self.rect[1] - 10, self.rect[2], 5))
        pygame.draw.rect(level.window, GREEN, health_rect)

    def draw_xp_bar(self, level):
        xp_rect = (5, 5, ((level.width - 10) * (self.xp / self.xp_to_level_up)), 5)
        pygame.draw.rect(level.window, BLACK, xp_rect)

    def player_collided(self):
        if self.collided > 0:
            self.collided += 1
            if self.collided >= 5:
                self.collided = 0
        else:
            self.colour = BLACK

    def check_hp(self):
        if self.hp <= 0:
            return True
        return False

    def check_level_up(self):
        if self.xp >= self.xp_to_level_up:
            self.level_up()


    def level_up(self):
        self.bullet_damage = round(self.bullet_damage * 1.1, 2)
        self.att_speed = round(self.att_speed * 1.1, 2)
        self.bullet_size = round(self.bullet_size * 1.2, 2)
        self.level += 1
        self.xp = 0
        self.xp_to_level_up = Player.xp_to_level_up * self.level
