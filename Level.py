import pygame
import math
import sys
from Player import Player
from Basic_enemy import BasicEnemy
from Big_enemy import BigEnemy
from Drop import Drop

pygame.font.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

MAIN_FONT = pygame.font.SysFont("Verdana", 30)


class Level:
    width = 1920
    height = 1080

    def __init__(self, player):
        self.new_game_text = MAIN_FONT.render("Try again", True, BLACK)
        self.exit_text = MAIN_FONT.render("Quit", True, BLACK)
        self.spawn_basic_enemy = pygame.USEREVENT + 1
        self.spawn_big_enemy = pygame.USEREVENT + 2
        self.increase_spawn_rate = pygame.USEREVENT + 3
        self.increase_score = pygame.USEREVENT + 4
        self.spawn_drop = pygame.USEREVENT + 5
        self.player = player
        self.window = pygame.display.set_mode((Level.width, Level.height))
        self.fps = 60
        self.enemies = []
        self.bullets = []
        self.targets = []
        self.drops = []
        self.run = True
        self.enemy_spawn_rate = 1
        self.gameover = False
        self.game_over_rect = None

    def draw_game(self):
        self.window.fill(WHITE)
        for enemy in self.enemies:
            enemy.draw(self)
        for bullet in self.bullets:
            bullet.draw(self)
        for drop in self.drops:
            drop.draw(self)
        pygame.draw.rect(self.window, self.player.colour, self.player.rect)
        self.player.draw_health_bar(self)
        self.player.draw_xp_bar(self)
        pygame.display.update()

    def events(self):
        pygame.time.set_timer(self.spawn_basic_enemy, 1000 // self.enemy_spawn_rate)
        pygame.time.set_timer(self.spawn_big_enemy, 10000 // self.enemy_spawn_rate)
        pygame.time.set_timer(self.increase_spawn_rate, 2000)
        pygame.time.set_timer(self.increase_score, 1000)
        pygame.time.set_timer(self.spawn_drop, 500)

    def pause_events(self):
        pygame.time.set_timer(self.spawn_basic_enemy, 0)
        pygame.time.set_timer(self.spawn_big_enemy, 0)
        pygame.time.set_timer(self.increase_spawn_rate, 0)
        pygame.time.set_timer(self.increase_score, 0)
        pygame.time.set_timer(self.spawn_drop, 0)

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
                enemy = self.spawn(BasicEnemy)
                self.enemies.append(enemy)
            if event.type == pygame.USEREVENT + 2:
                enemy = self.spawn(BigEnemy)
                self.enemies.append(enemy)
            if event.type == pygame.USEREVENT + 3:
                self.enemy_spawn_rate += 1
            if event.type == pygame.USEREVENT + 4:
                self.player.score += 1
            if event.type == pygame.USEREVENT + 5:
                drop = self.spawn(Drop)
                self.drops.append(drop)

    def game_over_event_handler(self):
        for event in pygame.event.get():
            if pygame.Rect.collidepoint(self.game_over_rect, pygame.mouse.get_pos()):
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.gameover = False
            elif pygame.Rect.collidepoint(self.exit_rect, pygame.mouse.get_pos()):
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    sys.exit()
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def spawn(self, thing_to_spawn):
        drop = thing_to_spawn(self)
        drop = self.check_location(drop, thing_to_spawn)
        return drop

    def check_location(self, drop, thing_to_spawn):
        if pygame.Rect.colliderect(drop.rect, self.player.rect):
            drop = self.spawn(thing_to_spawn)
        return drop

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
            self.player.shoot(self)

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
            elif bullet.rect[0] > Level.width or bullet.rect[0] < 0 or bullet.rect[1] > Level.height or \
                    bullet.rect[1] < 0:
                self.bullets.remove(bullet)

    def enemy_killed(self, enemy):
        self.player.xp += enemy.given_xp
        self.enemies.remove(enemy)

    def player_enemy_collision(self):
        collision = pygame.Rect.collidelist(self.player.rect, self.enemies)
        if collision >= 0:
            self.player.hp -= self.enemies[collision].damage
            self.enemies[collision].hp -= self.player.body_damage
            Player.colour = RED
            self.player.collided = 1
            self.enemies[collision].bounce = 1
            if self.enemies[collision].hp <= 0:
                del self.enemies[collision]
            else:
                self.enemies[collision].speed = -self.enemies[collision].speed * 2
            return self.player.check_hp()

    def drop_collision(self):
        collision = pygame.Rect.collidelist(self.player.rect, self.drops)
        if collision >= 0:
            Player.colour = GREEN

    def get_high_score(self):
        with open("High score.txt", "r") as file:
            high_score = int(file.read())
            return high_score

    def game_over(self):
        self.pause_events()
        self.enemies = []
        self.bullets = []
        self.draw_game_over_screen()
        self.gameover = True
        while self.gameover:
            self.game_over_event_handler()

    def draw_game_over_screen(self):
        score_text = MAIN_FONT.render("You lasted " + str(self.player.score) + " seconds", True, BLACK)
        game_over_text = MAIN_FONT.render("Game Over!", True, BLACK)
        self.game_over_rect = pygame.rect.Rect(Level.width // 2 - self.new_game_text.get_width() // 2 - 10,
                                               Level.height // (3 / 2) - self.new_game_text.get_height() // 2 - 10,
                                               self.new_game_text.get_width() + 20,
                                               self.new_game_text.get_height() + 20)
        self.exit_rect = pygame.rect.Rect(Level.width // 2 - self.exit_text.get_width() // 2 - 10,
                                               Level.height // (3 / 2) - self.exit_text.get_height() // 2 + 50,
                                               self.exit_text.get_width() + 20, self.exit_text.get_height() + 20)
        high_score = self.get_high_score()
        self.window.fill(RED)
        if self.player.score > high_score:
            high_score_text = MAIN_FONT.render("New High Score! You lasted " + str(self.player.score) + " seconds",
                                               True, BLACK)
            self.window.blit(high_score_text,
                             (Level.width // 2 - high_score_text.get_width() // 2, (Level.height // 2)))
            self.record_new_high_score()
        else:
            high_score_text = MAIN_FONT.render("High Score: " + str(high_score) + " seconds", True, BLACK)
            self.window.blit(score_text, (Level.width // 2 - score_text.get_width() // 2, (Level.height // 2)))
            self.window.blit(high_score_text, (
                (Level.width // 2 - high_score_text.get_width() // 2),
                Level.height // 2 + high_score_text.get_height()))
        self.window.blit(game_over_text, (
            (Level.width // 2 - game_over_text.get_width() // 2), (Level.height // 2 - game_over_text.get_height())))
        pygame.draw.rect(self.window, WHITE, self.game_over_rect)
        pygame.draw.rect(self.window, WHITE, self.exit_rect)
        self.window.blit(self.new_game_text, (self.game_over_rect[0] + 10, self.game_over_rect[1] + 10))
        self.window.blit(self.exit_text, (self.exit_rect[0] + 10, self.exit_rect[1] + 10))
        pygame.display.update()

    def record_new_high_score(self):
        with open("High score.txt", "w") as file:
            file.write(str(self.player.score))
