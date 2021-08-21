import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class arrow:
    width = 20
    height = 20

    def __init__(self, effect, position, screen):
        self.effect = effect
        self.rect = pygame.Rect(position, (arrow.width, arrow.height))
        self.screen = screen


    def draw(self):
        pygame.draw.rect(self.screen.window, BLACK, self.rect)
