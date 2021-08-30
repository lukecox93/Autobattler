import pygame
import sys


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

MAIN_FONT = pygame.font.SysFont("Verdana", 30)

class Menu:
    width = 1920
    height = 1080


    def __init__(self):
        self.window = pygame.display.set_mode((Menu.width, Menu.height), pygame. FULLSCREEN)
        self.difficulty_level = 1
        self.difficulty_rect = None
        self.difficulty_text = None
        self.run = True
        self.buttons = []
        self.gap = 2
        self.control_types = ["WASD", "Arrow Keys", "Mouse"]
        self.control_type = 0

    def create_arrow(self, effect, position, orientation):
        button = Arrow(effect, position, self, orientation)
        self.buttons.append(button)

    def create_start_button(self):
        button = StartButton(self)
        self.buttons.append(button)

    def create_exit_button(self):
        button = ExitButton(self)
        self.buttons.append(button)

    def create_controls_button(self):
        button = ControlsButton(self)
        self.buttons.append(button)

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

    def create_menu_objects(self):
        self.difficulty_text = MAIN_FONT.render("Difficulty: " + str(self.difficulty_level), True, BLACK)
        self.difficulty_rect = pygame.rect.Rect(Menu.width // 2 - ((self.difficulty_text.get_width() + Arrow.width + self.gap) // 2), Menu.height // 2, self.difficulty_text.get_width() + Arrow.width + self.gap, self.difficulty_text.get_height())
        self.create_start_button()
        self.create_exit_button()
        self.create_controls_button()
        self.create_arrow(1, (self.difficulty_rect[0] + self.difficulty_text.get_width() + self.gap, self.difficulty_rect[1]), False)
        self.create_arrow(-1, (self.difficulty_rect[0] + self.difficulty_text.get_width() + self.gap, self.difficulty_rect[1] + self.gap + Arrow.height), True)


    def draw_menu(self):
        self.window.fill(WHITE)
        self.window.blit(self.difficulty_text, (self.difficulty_rect[0], self.difficulty_rect[1]))
        for button in self.buttons:
            button.draw()
        pygame.display.update()

class Arrow:
    width = 20
    height = 20

    def __init__(self, effect, position, screen, orientation):
        self.effect = effect
        self.rect = pygame.Rect(position, (Arrow.width, Arrow.height))
        self.screen = screen
        self.orientation = orientation
        self.image = pygame.transform.flip(pygame.transform.scale(pygame.image.load("Arrow.png"), (Arrow.width, Arrow.height)), False, orientation)

    def draw(self):
        self.screen.window.blit(self.image, self.rect)

    def event(self):
        if 0 < self.screen.difficulty_level + self.effect < 10:
            self.screen.difficulty_level += self.effect

class StartButton:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Start Game", True, BLACK)
        self.rect = pygame.rect.Rect(screen.width // 2 - self.text.get_width() // 2, screen.height // 2 - self.text.get_height() + 120, self.text.get_width(), self.text.get_height())
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, ((self.screen.width // 2 - self.text.get_width() // 2), (self.screen.height // 2 - self.text.get_height() + 120)))

    def event(self):
        self.screen.run = False

class ExitButton:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Exit Game", True, BLACK)
        self.screen = screen
        self.rect = pygame.rect.Rect(screen.width // 2 - self.text.get_width() // 2,
                                               screen.height // (3 / 2) - self.text.get_height() // 2,
                                               self.text.get_width(), self.text.get_height())

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, self.rect)

    def event(self):
        sys.exit()

class ControlsButton:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Control type: " + str(screen.control_types[screen.control_type]), True, BLACK)
        # TODO - make it so that the program remembers the previous selection for control type
        self.screen = screen
        self.rect = pygame.rect.Rect((screen.width - self.text.get_width()) // 2, screen.buttons[0].rect[1] + self.text.get_height() + self.screen.gap, self.text.get_width(), self.text.get_height())

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, self.rect)

    def event(self):
        self.screen.control_type += 1
        self.screen.control_type %= 3
        self.screen.create_controls_button()
        self.screen.buttons.remove(self)