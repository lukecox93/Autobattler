import pygame
import random

GREEN = (0, 255, 0)


class Buff:
    def __init__(self, level, x, y):
        self.colour = (0, 0, 0)
        self.width = 10
        self.height = 10
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.time_left = 10000000000000000000000

    def draw(self, level):
        pygame.draw.rect(level.window, self.colour, self.rect)


class HealthPack(Buff):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.colour = (255, 0, 0)
        self.hp_given = 5

    def effect(self, level):
        if level.player.hp + self.hp_given >= level.player.max_hp:
            level.player.hp = level.player.max_hp
        else:
            level.player.hp += self.hp_given


class AttackSpeedBuff(Buff):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.colour = (0, 0, 255)

    def effect(self, level):
        level.player.att_speed *= 1.2


class AttackDamageBuff(Buff):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.colour = (0, 255, 0)

    def effect(self, level):
        level.player.bullet_damage += 1
        # TODO - doesn't seem to have an effect


class TempAttackSpeedBuff(Buff):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.colour = (255, 165, 0)
        self.time_left = 5

    def effect(self, level):
        level.player.att_speed *= 3

    def remove_effect(self, level):
        level.player.att_speed /= 3


class TempAttackDamageBuff(Buff):
    def __init__(self, level, x, y):
        super().__init__(level, x, y)
        self.colour = (255, 255, 0)
        self.time_left = 5

    def effect(self, level):
        level.player.bullet_damage *= 3

    def remove_effect(self, level):
        level.player.bullet_damage /= 3
