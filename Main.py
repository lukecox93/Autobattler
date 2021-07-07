import pygame
from Player import Player
from Level import Level
from Enemy import Enemy

BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.display.set_caption("Autobattler")

def main():
    pygame.init()
    clock = pygame.time.Clock()
    player = Player(900, 500, 50, 50, 5, 4, 5)
    level_1 = Level(player)
    level_1.events(player)
    while level_1.run:
        clock.tick(level_1.fps)
        level_1.event_handler()
        level_1.draw_game()
        level_1.player.player_collided()
        keys_pressed = pygame.key.get_pressed()
        player.move(keys_pressed, level_1)
        level_1.bullet_collision()
        level_1.player_collision()
        if level_1.player.check_hp():
            level_1.window.fill(RED)
            pygame.display.update()
            pygame.time.wait(2000)
            main()
        level_1.player.check_level_up()

    pygame.quit()

if __name__ == "__main__":
    main()