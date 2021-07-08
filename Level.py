import pygame
import math
import sys
from Enemy import Enemy
from Bullet import Bullet
from Player import Player

pygame.font.init()

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

MAIN_FONT = pygame.font.SysFont("Verdana", 30)

pygame.init()

class Level():
    width = 1920
    height = 1080
    def __init__(self, player):
        self.player = player
        self.window = pygame.display.set_mode((Level.width, Level.height))
        self.fps = 60
        self.enemies = []
        self.bullets = []
        self.targets = []
        self.run = True
        self.enemy_spawn_rate = 1
        self.gameover = False
        self.game_over_rect = None

    def draw_game(self):
        self.window.fill(WHITE)
        health_text = MAIN_FONT.render("HP: " + str(self.player.hp), True, BLACK)
        self.window.blit(health_text, (Level.width - health_text.get_width() - 10, 10))
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
        pygame.time.set_timer(self.enemy_type_1, 1000//self.enemy_spawn_rate)
        self.bullet_cooldown = pygame.USEREVENT + 2
        pygame.time.set_timer(self.bullet_cooldown, round(1000/player.att_speed))
        self.increase_spawn_rate = pygame.USEREVENT + 3
        pygame.time.set_timer(self.increase_spawn_rate, 2000)
        self.increase_score = pygame.USEREVENT + 4
        pygame.time.set_timer(self.increase_score, 1000)

    def pause_events(self):
        self.enemy_type_1 = pygame.USEREVENT + 1
        pygame.time.set_timer(self.enemy_type_1, 0)
        self.bullet_cooldown = pygame.USEREVENT + 2
        pygame.time.set_timer(self.bullet_cooldown, 0)
        self.increase_spawn_rate = pygame.USEREVENT + 3
        pygame.time.set_timer(self.increase_spawn_rate, 0)
        self.increase_score = pygame.USEREVENT + 4
        pygame.time.set_timer(self.increase_score, 0)

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
                enemy = Enemy(self)
                self.enemies.append(enemy)
            if event.type == pygame.USEREVENT + 2: #create bullet
                self.target_finder()
            if event.type == pygame.USEREVENT + 3:
                self.enemy_spawn_rate += 1
            if event.type == pygame.USEREVENT + 4:
                self.player.score += 1
            if self.gameover == True:
                if pygame.Rect.collidepoint(self.game_over_rect, pygame.mouse.get_pos()):
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                        self.gameover = False
                else:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

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
            self.create_bullet()


    def create_bullet(self):
        bullet = Bullet(self.player.rect[0] + (self.player.rect[2] // 2) - Bullet.width//2, self.player.rect[1] + (self.player.rect[3]
                                                                                                 // 2) - Bullet.height//2, self.player)
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
            elif bullet.rect[0] > Level.width or bullet.rect[0] < 0 or bullet.rect[1] > Level.height or bullet.rect[1] < 0:
                self.bullets.remove(bullet)

    def enemy_killed(self, enemy):
        self.player.xp += enemy.given_xp
        self.enemies.remove(enemy)

    def player_collision(self):
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
                self.enemies[collision].speed = -self.enemies[collision].speed*2
            return self.player.check_hp()

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
            self.event_handler()

    def draw_game_over_screen(self):
        score_text = MAIN_FONT.render("You lasted " + str(self.player.score) + " seconds", True, BLACK)
        game_over_text = MAIN_FONT.render("Game Over!", True, BLACK)
        self.new_game_text = MAIN_FONT.render("Try again", True, BLACK)
        self.game_over_rect = pygame.rect.Rect(Level.width // 2 - self.new_game_text.get_width() // 2 - 10,
                                               Level.height // (3/2) - self.new_game_text.get_height() // 2 - 10,
                                               self.new_game_text.get_width() + 20,
                                               self.new_game_text.get_height() + 20)
        high_score = self.get_high_score()
        self.window.fill(RED)
        if self.player.score > high_score:
            high_score_text = MAIN_FONT.render("New High Score! You lasted " + str(self.player.score) + " seconds", True, BLACK)
            self.window.blit(high_score_text, (Level.width//2 - high_score_text.get_width()//2, (Level.height // 2)))
            self.record_new_high_score()
        else:
            high_score_text = MAIN_FONT.render("High Score: " + str(high_score) + " seconds", True, BLACK)
            self.window.blit(score_text, (Level.width//2 - score_text.get_width()//2,  (Level.height//2)))
            self.window.blit(high_score_text, ((Level.width//2 - high_score_text.get_width()//2), Level.height//2 + high_score_text.get_height()))
        self.window.blit(game_over_text, (
        (Level.width // 2 - game_over_text.get_width() // 2), (Level.height // 2 - game_over_text.get_height())))
        pygame.draw.rect(self.window, WHITE, self.game_over_rect)
        self.window.blit(self.new_game_text, (self.game_over_rect[0] + 10, self.game_over_rect[1] + 10))
        pygame.display.update()

    def record_new_high_score(self):
        with open("High score.txt", "w") as file:
            file.write(str(self.player.score))