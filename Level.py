import math
import sys
import random
from Basic_enemy import BasicEnemy
from Big_enemy import BigEnemy
from Multi_enemy import MultiEnemy
from Buffs import *
from Game_Over import GameOver

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

    def __init__(self, player, menu):
        self.spawn_basic_enemy = pygame.USEREVENT + 1
        self.spawn_big_enemy = pygame.USEREVENT + 2
        self.increase_spawn_rate = pygame.USEREVENT + 3
        self.increase_score = pygame.USEREVENT + 4
        self.spawn_drop = pygame.USEREVENT + 5
        self.spawn_multi_enemy = pygame.USEREVENT + 6
        self.player = player
        self.window = pygame.display.set_mode((Level.width, Level.height), pygame.FULLSCREEN)
        self.fps = menu.FPS_choices[menu.fps]
        # TODO - change speeds so they are calculated according to the fps
        self.enemies = []
        self.bullets = []
        self.targets = []
        self.buffs = []
        self.taken_buffs = []
        self.available_buffs = (HealthPack, AttackSpeedBuff, AttackDamageBuff, TempAttackSpeedBuff, TempAttackDamageBuff, MoveSpeedBuff, TempMoveSpeedBuff, BulletChaining)
        self.run = True
        self.enemy_spawn_rate = 1
        self.menu = menu
        self.modifier = menu.difficulty_level
        self.clock = menu.clock
        self.damage_dealt = 0
        self.damage_taken = 0

    def start(self):
        self.events()
        while self.run:
            self.clock.tick(self.fps)
            self.event_handler()
            if self.player.bullet_cooldown():
                if self.target_finder(self.player, self.enemies) >= 1:
                    self.player.shoot(self)
            self.draw_game()
            self.player.player_collided()
            self.player.move(pygame.key.get_pressed(), self, self.menu.control_type)
            self.bullet_collision()
            self.buff_collision()
            self.buff_handler()
            self.player.check_level_up()
            if self.player_enemy_collision():
                self.pause_events()
                self.run = False
                game_over = GameOver(self)
                game_over.start()


    def draw_game(self):
        self.window.fill(WHITE)
        for enemy in self.enemies:
            enemy.draw(self)
        for bullet in self.bullets:
            bullet.draw(self)
        for buff in self.buffs:
            buff.draw(self)
        pygame.draw.rect(self.window, self.player.colour, self.player.rect)
        self.player.draw_health_bar(self)
        self.player.draw_xp_bar(self)
        pygame.display.update()

    def events(self):
        pygame.time.set_timer(self.spawn_basic_enemy, 1000 // self.enemy_spawn_rate)
        pygame.time.set_timer(self.spawn_big_enemy, 5000 // self.enemy_spawn_rate)
        pygame.time.set_timer(self.spawn_multi_enemy, 2000 // self.enemy_spawn_rate)
        pygame.time.set_timer(self.increase_spawn_rate, 2000)
        pygame.time.set_timer(self.increase_score, 1000)
        pygame.time.set_timer(self.spawn_drop, 5000)

    def pause_events(self):
        pygame.time.set_timer(self.spawn_basic_enemy, 0)
        pygame.time.set_timer(self.spawn_big_enemy, 0)
        pygame.time.set_timer(self.spawn_multi_enemy, 0)
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
                    self.pause_events()
                    self.menu.run = True
                    self.menu.start()
                    if self.menu.carry_on:
                        self.start()
                    else:
                        self.run = False
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
                drop = self.spawn(random.choice(self.available_buffs))
                self.buffs.append(drop)
            if event.type == pygame.USEREVENT + 6:
                enemy = self.spawn(MultiEnemy)
                self.enemies.append(enemy)

    def spawn(self, thing_to_spawn):
        drop = thing_to_spawn(self, random.randint(0, Level.width), random.randint(0, Level.height))
        drop = self.check_location(drop, thing_to_spawn)
        return drop

    def check_location(self, drop, thing_to_spawn):
        if pygame.Rect.colliderect(drop.rect, self.player.rect):
            drop = self.spawn(thing_to_spawn)
        return drop

    def target_finder(self, sprite, list_of_targets):
        targets = []
        for target in list_of_targets:
            targets.append(math.sqrt(
                (abs((target.rect[0] + target.rect[2] // 2) - (sprite.rect[0] + sprite.rect[2] // 2)) ** 2) + (
                        abs((target.rect[1] + target.rect[3] // 2) - (sprite.rect[1] + sprite.rect[3] // 2))
                        ** 2)))
        if targets:
            sprite.target = list_of_targets[targets.index(min(targets))]
            return 1
        return 0

    def targeting(self, sprite):
        x_dist = ((sprite.target.rect[0] + (sprite.target.rect[2] // 2)) - (sprite.rect[0] + (sprite.rect[2] // 2)))
        y_dist = ((sprite.target.rect[1] + (sprite.target.rect[3] // 2)) - (sprite.rect[1] + (sprite.rect[2] // 2)))

        sprite.delta_x = round((x_dist * sprite.speed) / (max(abs(x_dist), abs(y_dist))))
        sprite.delta_y = round((y_dist * sprite.speed) / (max(abs(x_dist), abs(y_dist))))

    def bullet_collision(self):
        for bullet in self.bullets:
            collision = pygame.Rect.collidelist(bullet.rect, self.enemies)
            if collision >= 0:
                self.enemies[collision].bullet_collision(self, bullet)
            elif bullet.rect[0] > Level.width or bullet.rect[0] < 0 or bullet.rect[1] > Level.height or \
                    bullet.rect[1] < 0:
                self.bullets.remove(bullet)

    def player_enemy_collision(self):
        collision = pygame.Rect.collidelist(self.player.rect, self.enemies)
        if collision >= 0:
            self.enemies[collision].player_collision(self, self.enemies)
            self.player.colour = RED
            self.player.collided = 1
            return self.player.check_hp()

    def buff_collision(self):
        collision = pygame.Rect.collidelist(self.player.rect, self.buffs)
        if collision >= 0:
            self.buffs[collision].effect(self)
            self.taken_buffs.append(self.buffs[collision])
            del self.buffs[collision]

    def buff_handler(self):
        for buff in self.taken_buffs:
            buff.time_left -= 1/self.fps
            if (buff.time_left) <= 0:
                buff.remove_effect(self)
                self.taken_buffs.remove(buff)





