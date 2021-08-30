import pygame
from Player import Player
from Level import Level
from Menu import Menu
from Game_Over import GameOver
import os.path

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

pygame.display.set_caption("Autobattler")

def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    info = pygame.display.Info()
    screen_width, screen_height = info.current_w, info.current_h
    Menu.width, Menu.height = screen_width, screen_height
    Level.width, Level.height = Menu.width, Menu.height

    # TODO - change things to be sized relatively to the size of the screen.
    if not os.path.isfile("High score.txt"):
        with open("High score.txt", "w") as file:
            file.write("0")
    clock = pygame.time.Clock()
    menu_1 = Menu()
    fps = 60
    while True:
        while menu_1.run:
            clock.tick(fps)
            menu_1.draw_menu()
            menu_1.event_handler()
        player = Player(Level.width // 2 - 25, Level.height // 2 - 25, 50, 50, 5, 1, 10)
        level_1 = Level(player, menu_1)
        level_1.events()
        while level_1.run:
            clock.tick(level_1.fps)
            level_1.event_handler()
            if player.bullet_cooldown():
                if level_1.target_finder(level_1.player, level_1.enemies) >= 1:
                    level_1.player.shoot(level_1)
            level_1.draw_game()
            level_1.player.player_collided()
            keys_pressed = pygame.key.get_pressed()
            player.move(keys_pressed, level_1)
            level_1.bullet_collision()
            level_1.buff_collision()
            level_1.buff_handler()
            if level_1.player_enemy_collision():
                game_over = GameOver(level_1)
                while game_over.run:
                    game_over.event_handler()
                    game_over.draw()
                main()
            level_1.player.check_level_up()


if __name__ == "__main__":
    main()
