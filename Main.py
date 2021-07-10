import pygame
from Player import Player
from Level import Level
import os.path
from Drop import Drop
import random

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.display.set_caption("Autobattler")

def main():
    pygame.init()
    if not os.path.isfile("High score.txt"):
        with open("High score.txt", "w") as file:
            file.write("0")
    clock = pygame.time.Clock()
    player = Player(Level.width // 2 - 25, Level.height // 2 - 25, 50, 50, 5, 1000, 1)
    level_1 = Level(player)
    level_1.events()
    while level_1.run:
        clock.tick(level_1.fps)
        level_1.event_handler()
        if player.bullet_cooldown():
            level_1.target_finder()
        level_1.draw_game()
        level_1.player.player_collided()
        keys_pressed = pygame.key.get_pressed()
        player.move(keys_pressed, level_1)
        level_1.bullet_collision()
        level_1.drop_collision()
        if level_1.player_enemy_collision():
            level_1.game_over()
            main()
        level_1.player.check_level_up()

    pygame.quit()


if __name__ == "__main__":
    main()
