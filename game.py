import pygame
import json
from random import shuffle
from graphics import Graphics
from tile import Tile
from menu import Menu

DRAW_OFFSET = Graphics.DRAW_OFFSET
window = Graphics.window


class Game:

    TILE_SIZE = 50

    def __init__(self, width, height):
        global window
        window = Graphics.window
        self.width = width
        self.height = height

        self.cardWidth = 80
        self.cardHeight = 100

        self.activePlayer = 0

        self.handSize = [[0] * 1] * 2
        self.hands = [[None] * 6] * 2

        self.menu = Menu(self)

        self.cards = []
        self.deckSize = 0

        self.parseTiles()
        self.makeDeck()

        self.grid = [[None for y in range(self.height)] for x in range(self.width)]

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
        global DRAW_OFFSET, window
        self.drawBoard()
        DRAW_OFFSET['y'] += self.height * Tile.SIZE
        self.drawHand()
        DRAW_OFFSET['y'] -= self.height * Tile.SIZE
        self.menu.draw(window)

    def drawBoard(self):
        global DRAW_OFFSET, window
        box = list((DRAW_OFFSET['x'], DRAW_OFFSET['y'], 0, 0))
        box[2] = self.width * Tile.SIZE
        box[3] = self.height * Tile.SIZE
        window.fill(pygame.Color('grey'), box, 0)

        box[2] = Tile.SIZE
        box[3] = Tile.SIZE
        for x in xrange(0, len(self.grid)):
            box[1] = DRAW_OFFSET['y']
            for y in xrange(0, len(self.grid[x])):
                tile = self.grid[x][y]
                if tile is None:
                    pygame.draw.rect(window, pygame.Color('red'), box, 1)
                else:
                    tile.draw(window, box[0], box[1])

                box[1] += Tile.SIZE
            box[0] += Tile.SIZE

    def drawHand(self):
        global DRAW_OFFSET, window

        box = list((DRAW_OFFSET['x'], DRAW_OFFSET['y'], 0, 0))
        box[2] = self.width * Tile.SIZE
        box[3] = 100
        window.fill(pygame.Color('blue'), box, 0)

    def handleClick(self, x, y, left=True):
        if (self.menu.handleClick(x, y)):
            return 1
        if x > self.width * Tile.SIZE:
            return 0

        if y > self.height * Tile.SIZE:
            index = y / self.cardWidth
            if index < self.getHandSize:
                self.cardClicked(index)
            return 1
        else:
            if (left):
                self.tileClicked(x / Tile.SIZE, y / Tile.SIZE)
            else:
                tile = self.grid[x / Tile.SIZE][y / Tile.SIZE]
                self.menu.activate(tile, x, y)
            return 1

    def cardClicked(self, index):
        return 0

    def tileClicked(self, x, y):
        tile = self.grid[x][y]
        if tile is None:
            tileID = self.deck.pop()
            self.grid[x][y] = Tile(self.tileData[tileID], tileID, x, y)
        else:
            tile.rotate()

    def destroyTile(self, x, y):
        self.grid[x][y] = None

    def getHand(self):
        return self.hands[self.activePlayer]

    def getHandSize(self):
        return self.handSizes[self.activePlayer]

    def drawCard(self):
        self.getHand()[self.getHandSize()] = self.deck.pop()
        self.handSizes[self.activePlayer] += 1
