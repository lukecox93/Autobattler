import pygame
import sys


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
        self.buttons = []

    def create_arrow(self, effect, position):
        button = arrow(effect, position, self)
        self.buttons.append(button)
        button.draw()

    def create_start_button(self):
        button = start_button(self)
        self.buttons.append(button)
        button.draw()

    def create_exit_button(self):
        button = exit_button(self)
        self.buttons.append(button)
        button.draw()


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
            mouse_over = pygame.Rect.collidelist(mouse, self.buttons)
            if mouse_over >= 0:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.buttons[mouse_over].event()
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
        self.create_start_button()
        self.create_exit_button()
        pygame.display.update()

class arrow:
    width = 20
    height = 20

    def __init__(self, effect, position, screen):
        self.effect = effect
        self.rect = pygame.Rect(position, (arrow.width, arrow.height))
        self.screen = screen


    def draw(self):
        pygame.draw.rect(self.screen.window, BLACK, self.rect)

    def event(self):
        if 0 < self.screen.difficulty_level + self.effect < 10:
            self.screen.difficulty_level += self.effect

class start_button:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Start Game", True, BLACK)
        self.rect = (screen.width // 2 - self.text.get_width() // 2, screen.height // 2 - self.text.get_height() + 120, self.text.get_width(), self.text.get_height())
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, ((self.screen.width // 2 - self.text.get_width() // 2), (self.screen.height // 2 - self.text.get_height() + 120)))

    def event(self):
        self.screen.run = False

class exit_button:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Exit Game", True, BLACK)
        self.screen = screen
        self.rect = pygame.rect.Rect(screen.width // 2 - self.text.get_width() // 2,
                                               screen.height // (3 / 2) - self.text.get_height() // 2,
                                               self.text.get_width(), self.text.get_height())

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, (self.rect))

    def event(self):
        sys.exit()