import pygame
import sys

pygame.font.init()
MAIN_FONT = pygame.font.SysFont("Verdana", 30)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)


class GameOver:

    def __init__(self, level):
        self.run = True
        self.level = level
        self.new_game_text = MAIN_FONT.render("Try again", True, BLACK)
        self.exit_text = MAIN_FONT.render("Quit", True, BLACK)
        self.window = level.window
        self.game_over_rect = None
        self.exit_rect = None

    def start(self):
        while self.run:
            self.draw()
            self.event_handler()

    def get_high_score(self):
        with open("High score.txt", "r") as file:
            high_score = int(file.read())
            return high_score

    def create_rects(self):
        self.game_over_rect = pygame.rect.Rect(self.level.width // 2 - self.new_game_text.get_width() // 2 - 10,
                                               self.level.height // (3 / 2) - self.new_game_text.get_height() // 2 - 10,
                                               self.new_game_text.get_width() + 20,
                                               self.new_game_text.get_height() + 20)
        self.exit_rect = pygame.rect.Rect(self.level.width // 2 - self.exit_text.get_width() // 2 - 10,
                                          self.level.height // (3 / 2) - self.exit_text.get_height() // 2 + 50,
                                          self.exit_text.get_width() + 20, self.exit_text.get_height() + 20)

    def draw(self):
        game_over_text = MAIN_FONT.render("Game Over!", True, BLACK)
        self.create_rects()
        self.window.fill(RED)
        self.display_high_score()
        self.window.blit(game_over_text, (
            (self.level.width // 2 - game_over_text.get_width() // 2),
            (self.level.height // 2 - game_over_text.get_height())))
        pygame.draw.rect(self.window, WHITE, self.game_over_rect)
        pygame.draw.rect(self.window, WHITE, self.exit_rect)
        self.window.blit(self.new_game_text, (self.game_over_rect[0] + 10, self.game_over_rect[1] + 10))
        self.window.blit(self.exit_text, (self.exit_rect[0] + 10, self.exit_rect[1] + 10))
        pygame.display.update()

    def display_high_score(self):
        score_text = MAIN_FONT.render("You lasted " + str(self.level.player.score) + " seconds", True, BLACK)
        high_score = self.get_high_score()
        if self.level.player.score > high_score:
            high_score_text = MAIN_FONT.render(
                "New High Score! You lasted " + str(self.level.player.score) + " seconds",
                True, BLACK)
            self.window.blit(high_score_text,
                             (self.level.width // 2 - high_score_text.get_width() // 2, (self.level.height // 2)))
            self.record_new_high_score()
        else:
            high_score_text = MAIN_FONT.render("High Score: " + str(high_score) + " seconds", True, BLACK)
            self.window.blit(score_text,
                             (self.level.width // 2 - score_text.get_width() // 2, (self.level.height // 2)))
            self.window.blit(high_score_text, (
                (self.level.width // 2 - high_score_text.get_width() // 2),
                self.level.height // 2 + high_score_text.get_height()))

    def record_new_high_score(self):
        with open("High score.txt", "w") as file:
            file.write(str(self.level.player.score))

    def event_handler(self):
        for event in pygame.event.get():
            if pygame.Rect.collidepoint(self.game_over_rect, pygame.mouse.get_pos()):
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    self.run = False
                    self.level.menu.current_game = False
                    self.level.menu.run = True
                    self.level.menu.start()
            elif pygame.Rect.collidepoint(self.exit_rect, pygame.mouse.get_pos()):
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    sys.exit()
            else:
                pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)
