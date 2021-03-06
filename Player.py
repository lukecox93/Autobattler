import pygame
from Bullet import Bullet

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Player:
    xp_to_level_up = 3
    colour = BLACK

    def __init__(self, x, y, width, height, speed, att_speed, hp):
        self.speed = speed
        self.att_speed = att_speed
        self.bullet_cd = att_speed
        self.rect = pygame.Rect(x, y, width, height)
        self.max_hp = hp
        self.hp = hp
        self.target = None
        self.body_damage = 1
        self.collided = 0
        self.level = 1
        self.bullet_damage = 1
        self.base_bullet_size = 6
        self.bullet_size = 6
        self.xp = 0
        self.xp_to_level_up = (Player.xp_to_level_up * self.level)
        self.score = 0
        self.colour = Player.colour
        self.bullet_chain = 0
        self.move_target = None
        self.delta_x = None
        self.delta_y = None

    def move(self, keys_pressed, level, control_type):
        if control_type == 0:
            self.wasd_move(keys_pressed, level)
        elif control_type == 1:
            self.arrow_key_move(keys_pressed, level)
        else:
            self.mouse_move(level)

    def wasd_move(self, keys_pressed, level):
        if keys_pressed[pygame.K_a] and self.rect[0] - self.speed >= 0:
            pygame.Rect.move_ip(self.rect, -self.speed, 0)
        if keys_pressed[pygame.K_d] and self.rect[0] + self.speed + self.rect[2] <= level.width:
            pygame.Rect.move_ip(self.rect, self.speed, 0)
        if keys_pressed[pygame.K_w] and self.rect[1] - self.speed >= 0:
            pygame.Rect.move_ip(self.rect, 0, -self.speed)
        if keys_pressed[pygame.K_s] and self.rect[1] + self.speed + self.rect[3] <= level.height:
            pygame.Rect.move_ip(self.rect, 0, self.speed)

    def arrow_key_move(self, keys_pressed, level):
        if keys_pressed[pygame.K_LEFT] and self.rect[0] - self.speed >= 0:
            pygame.Rect.move_ip(self.rect, -self.speed, 0)
        if keys_pressed[pygame.K_RIGHT] and self.rect[0] + self.speed + self.rect[2] <= level.width:
            pygame.Rect.move_ip(self.rect, self.speed, 0)
        if keys_pressed[pygame.K_UP] and self.rect[1] - self.speed >= 0:
            pygame.Rect.move_ip(self.rect, 0, -self.speed)
        if keys_pressed[pygame.K_DOWN] and self.rect[1] + self.speed + self.rect[3] <= level.height:
            pygame.Rect.move_ip(self.rect, 0, self.speed)

    def mouse_move(self, level):
        pygame.event.set_grab(True)
        self.movement_targeting()
        if self.rect[0] + self.delta_x <= 0 or self.rect[0] + self.delta_x + self.rect[2] >= level.width:
            self.delta_x = 0
        if self.rect[1] + self.delta_y <= 0 or self.rect[1] + self.delta_y + self.rect[3] >= level.height:
            self.delta_y = 0
        pygame.Rect.move_ip(self.rect, self.delta_x, self.delta_y)

    def movement_targeting(self):
        self.move_target = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        x_dist = ((self.move_target[0] + (self.move_target[2] // 2)) - (self.rect[0] + (self.rect[2] // 2)))
        y_dist = ((self.move_target[1] + (self.move_target[3] // 2)) - (self.rect[1] + (self.rect[2] // 2)))
        if max(abs(x_dist), abs(y_dist)) <= self.speed:
            self.delta_x, self.delta_y = 0, 0
        else:
            self.delta_x = round((x_dist * self.speed) / (max(abs(x_dist), abs(y_dist))))
            self.delta_y = round((y_dist * self.speed) / (max(abs(x_dist), abs(y_dist))))

    def draw_health_bar(self, level):
        health_rect = (self.rect[0], self.rect[1] - 10, self.rect[2] * (self.hp / self.max_hp), 5)
        pygame.draw.rect(level.window, RED, (self.rect[0], self.rect[1] - 10, self.rect[2], 5))
        pygame.draw.rect(level.window, GREEN, health_rect)

    def draw_xp_bar(self, level):
        xp_rect = (5, 5, ((level.width - 10) * (self.xp / self.xp_to_level_up)), 5)
        pygame.draw.rect(level.window, BLACK, xp_rect)

    def bullet_cooldown(self):
        if pygame.time.get_ticks() - self.bullet_cd >= 1000/self.att_speed:
            self.bullet_cd = pygame.time.get_ticks()
            return True
        return False

    def shoot(self, level):
        bullet = Bullet(self.rect[0] + (self.rect[2] // 2) - Bullet.width // 2,
                    self.rect[1] + (self.rect[3]// 2) - Bullet.height // 2, self)
        level.bullets.append(bullet)
        level.targeting(bullet)
        level.player.cd = 0

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
