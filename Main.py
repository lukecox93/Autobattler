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
    menu_1 = Menu()
    while True:
        menu_1.start()
        if not menu_1.carry_on:
            player = Player(Level.width // 2 - 25, Level.height // 2 - 25, 50, 50, 5, 1, 10)
            level_1 = Level(player, menu_1)
            level_1.start()


if __name__ == "__main__":
    main()
