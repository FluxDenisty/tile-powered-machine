import pygame
import json
from random import shuffle
from graphics import Graphics

DRAW_OFFSET = Graphics.DRAW_OFFSET
window = Graphics.window


class Game:

    def __init__(self, width, height):
        global window
        window = Graphics.window
        self.width = width
        self.height = height
        self.cards = []
        self.deckSize = 0

        self.parseTiles()
        self.makeDeck()

        self.grid = [[None] * self.height] * self.width

    def makeDeck(self):
        self.deck = [None] * self.deckSize
        i = 0
        index = 0
        for tile in self.tileData:
            for j in xrange(0, tile['number']):
                self.deck[index] = i
                index += 1
            i += 1
        shuffle(self.deck)

    def parseTiles(self):
        json_data = open('tiles.json')

        self.tileData = json.load(json_data)
        json_data.close()

        for tile in self.tileData:
            self.deckSize += tile['number']

    def draw(self):
        global DRAW_OFFSET
        self.drawBoard()
        DRAW_OFFSET['y'] += self.height * 50
        self.drawHand()
        DRAW_OFFSET['y'] -= self.height * 50

    def drawBoard(self):
        global DRAW_OFFSET, window
        box = list((DRAW_OFFSET['x'], DRAW_OFFSET['y'], self.width * 50, self.height * 50))
        window.fill(pygame.Color('grey'), box, 0)

        box[2] = 50
        box[3] = 50
        for x in xrange(0, len(self.grid)):
            box[1] = DRAW_OFFSET['y']
            for y in xrange(0, len(self.grid[x])):
                tile = self.grid[x][y]
                if tile is None:
                    pygame.draw.rect(window, pygame.Color('red'), box, 1)

                box[1] += 50
            box[0] += 50

    def drawHand(self):
        global DRAW_OFFSET, window
        box = (DRAW_OFFSET['x'], DRAW_OFFSET['y'], self.width * 50, 100)
        window.fill(pygame.Color('green'), box, 0)
