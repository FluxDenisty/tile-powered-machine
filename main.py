import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP, K_LSUPER, K_RSUPER, K_q, K_w, QUIT
from game import Game
from graphics import Graphics

WIDTH = 11
HEIGHT = 15

pygame.init()
clock = pygame.time.Clock()

Graphics(WIDTH * 50 + 10, HEIGHT * 50 + 100 + 10)
pygame.display.set_caption('tile-powered-machine')

cmd = False

game = Game(WIDTH, HEIGHT)


def input():
    global cmd
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            if event.key == K_LSUPER or event.key == K_RSUPER:
                cmd = True
            elif event.key == K_w or event.key == K_q:
                pygame.quit()
                sys.exit()
        elif event.type == KEYUP:
            if event.key == K_LSUPER or event.key == K_RSUPER:
                cmd = False


while True:
    input()
    Graphics.window.fill(pygame.Color("white"))
    game.draw()
    pygame.display.update()
    clock.tick(60)
