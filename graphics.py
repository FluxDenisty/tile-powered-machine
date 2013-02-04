import pygame


class Graphics:
    DRAW_OFFSET = {'x': 5, 'y': 5}
    window = None

    def __init__(self, width, height):
        Graphics.window = pygame.display.set_mode((width, height))
