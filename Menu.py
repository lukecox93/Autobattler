import pygame
import sys
from Arrow import arrow


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

MAIN_FONT = pygame.font.SysFont("Verdana", 30)

class menu:
    width = 1920
    height = 1080

    def __init__(self):
        self.window = pygame.display.set_mode((menu.width, menu.height))
        self.difficulty_level = 1
        self.difficulty_rect = None
        self.run = True
        self.arrows = []

    def create_arrow(self, effect, position):
        obj = arrow(effect, position, self)
        self.arrows.append(obj)
        obj.draw()


    def event_handler(self):
        events = pygame.event.get()
        mouse = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.run = False
                    sys.exit()
            mouse_over = pygame.Rect.collidelist(mouse, self.arrows)
            if mouse_over >= 0:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if (10 > self.difficulty_level + self.arrows[mouse_over].effect > 0):
                        self.difficulty_level += self.arrows[mouse_over].effect
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)


    def draw_menu(self):
        difficulty_text = MAIN_FONT.render("Difficulty: " + str(self.difficulty_level), True, BLACK)
        self.window.fill(WHITE)
        self.difficulty_rect = pygame.rect.Rect(menu.width // 2 - difficulty_text.get_width() // 2 - 10,
                                               menu.height // (3 / 2) - difficulty_text.get_height() // 2 - 10,
                                               difficulty_text.get_width() + 20,
                                               difficulty_text.get_height() + 20)
        self.window.blit(difficulty_text, (
            (menu.width // 2 - difficulty_text.get_width() // 2), (menu.height // 2 - difficulty_text.get_height())))
        self.create_arrow(1, (menu.width // 2, menu.height // 2))
        self.create_arrow(-1, (menu.width // 2, menu.height // 2 + 40))
        pygame.display.update()