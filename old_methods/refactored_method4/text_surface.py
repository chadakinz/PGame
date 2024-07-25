import pygame
class Text:
    def __init__(self, msg, size = 100):
        pygame.font.init()
        self.font = pygame.font.SysFont('chalkduster.ttf', size)
        self.text = self.font.render(msg, True, (0, 0, 0))

