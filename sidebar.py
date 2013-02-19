import pygame
from graphics import Graphics


class SideBar:

    WIDTH = 400
    HEIGHT = 850

    def __init__(self):
        self.items = []
        self.font = pygame.font.Font(None, 28)

    def addItem(self, item):
        text = self.font.render(item, 1, pygame.Color('black'))
        self.items.append(text)

    def draw(self, window):
        DRAW_OFFSET = Graphics.DRAW_OFFSET
        x = DRAW_OFFSET['x'] + 5
        y = DRAW_OFFSET['y'] + 5
        for text in self.items:
            window.blit(text, (x, y))
            y += text.get_height() + 5
