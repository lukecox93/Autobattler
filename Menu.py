import pygame
import sys
from Level import Level
from Player import Player


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

MAIN_FONT = pygame.font.SysFont("Verdana", 30)

class Menu:
    width = 1920
    height = 1080
    control_type = 0
    fps = 0
    clock = pygame.time.Clock()

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
        self.FPS_choices = [60, 144, 240]
        self.current_game = False
        self.carry_on = False
        self.button_types = [StartButton, ContinueButton, ExitButton, ControlsButton, FPSButton]

    def start(self):
        while self.run:
            self.clock.tick(self.FPS_choices[self.fps])
            self.buttons.clear()
            self.create_menu_objects()
            self.draw_menu()
            self.event_handler()

    def create_arrow(self, effect, position, orientation):
        button = Arrow(effect, position, self, orientation)
        self.buttons.append(button)

    def create_button(self, button_type):
        self.buttons.append(button_type(self))

    def event_handler(self):
        events = pygame.event.get()
        mouse = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        for event in events:
            if event.type == pygame.QUIT:
                self.run = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.current_game:
                        ContinueButton(self).event()
            mouse_over = pygame.Rect.collidelist(mouse, self.buttons)
            if mouse_over >= 0:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.buttons[mouse_over].event()
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def create_menu_objects(self):
        self.difficulty_text = MAIN_FONT.render("Difficulty: " + str(self.difficulty_level), True, BLACK)
        self.difficulty_rect = pygame.rect.Rect(Menu.width // 2 - ((self.difficulty_text.get_width() + Arrow.width + self.gap) // 2), Menu.height // 2, self.difficulty_text.get_width() + Arrow.width + self.gap, self.difficulty_text.get_height())
        for button in self.button_types:
            if button != ContinueButton or self.current_game:
                self.create_button(button)


        self.create_arrow(1, (self.difficulty_rect[0] + self.difficulty_text.get_width() + self.gap, self.difficulty_rect[1]), False)
        self.create_arrow(-1, (self.difficulty_rect[0] + self.difficulty_text.get_width() + self.gap, self.difficulty_rect[1] + self.gap + Arrow.height), True)


    def draw_menu(self):
        self.window.fill(WHITE)
        self.window.blit(self.difficulty_text, (self.difficulty_rect[0], self.difficulty_rect[1]))
        [button.draw() for button in self.buttons]
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
        self.text = MAIN_FONT.render("New Game", True, BLACK)
        self.rect = pygame.rect.Rect(screen.width // 2 - self.text.get_width() // 2, screen.height // 2 - self.text.get_height() + 120, self.text.get_width(), self.text.get_height())
        self.screen = screen

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, ((self.screen.width // 2 - self.text.get_width() // 2), (self.screen.height // 2 - self.text.get_height() + 120)))

    def event(self):
        self.screen.current_game = True
        player = Player(Level.width // 2 - 25, Level.height // 2 - 25, 50, 50, 5, 1, 10)
        level_1 = Level(player, self.screen)
        level_1.start()


class ContinueButton:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Continue", True, BLACK)
        self.screen = screen
        self.rect = pygame.rect.Rect(screen.width // 2 - self.text.get_width() // 2, self.screen.buttons[0].rect[1] - self.text.get_height() - self.screen.gap, self.text.get_width(), self.text.get_height())

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, self.rect)

    def event(self):
        self.screen.run = False
        self.screen.carry_on = True


class ExitButton:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Exit Game", True, BLACK)
        self.screen = screen
        self.rect = pygame.rect.Rect(screen.width // 2 - self.text.get_width() // 2,
                                               screen.height // (4 / 3),
                                               self.text.get_width(), self.text.get_height())

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, self.rect)

    def event(self):
        sys.exit()

class ControlsButton:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("Control type: " + str(screen.control_types[Menu.control_type]), True, BLACK)
        self.screen = screen
        self.rect = pygame.rect.Rect((screen.width - self.text.get_width()) // 2, screen.buttons[0].rect[1] + self.text.get_height() + self.screen.gap, self.text.get_width(), self.text.get_height())

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, self.rect)

    def event(self):
        Menu.control_type += 1
        Menu.control_type %= 3
        self.screen.create_button(ControlsButton)
        self.screen.buttons.remove(self)

class FPSButton:
    def __init__(self, screen):
        self.text = MAIN_FONT.render("FPS: " + str(screen.FPS_choices[Menu.fps]), True, BLACK)
        self.screen = screen
        self.rect = pygame.rect.Rect((screen.width - self.text.get_width()) // 2, screen.buttons[0].rect[1] + (self.text.get_height() + self.screen.gap) * 2, self.text.get_width(), self.text.get_height())

    def draw(self):
        pygame.draw.rect(self.screen.window, RED, self.rect)
        self.screen.window.blit(self.text, self.rect)

    def event(self):
        Menu.fps += 1
        Menu.fps %= 3
        self.screen.create_button(FPSButton)
        self.screen.buttons.remove(self)