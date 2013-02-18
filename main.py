import pygame
import sys
from pygame.locals import KEYDOWN, KEYUP, K_LSUPER, K_RSUPER, QUIT
from pygame.locals import K_q, K_w, K_d, K_t
from pygame.locals import MOUSEBUTTONUP
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
            elif event.key == K_d:
                game.addCard()
            elif event.key == K_t:
                game.endTurn()
        elif event.type == MOUSEBUTTONUP:
            x, y = event.pos
            x -= Graphics.DRAW_OFFSET['x']
            y -= Graphics.DRAW_OFFSET['y']
            game.handleClick(x, y, event.button == 1)

while True:
    input()
    Graphics.window.fill(pygame.Color("white"))
    game.draw()
    pygame.display.update()
    clock.tick(60)
