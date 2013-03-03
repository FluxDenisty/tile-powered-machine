import pygame
import json
from random import shuffle
from graphics import Graphics
from tile import Tile
from menu import Menu
from sidebar import SideBar

DRAW_OFFSET = Graphics.DRAW_OFFSET
window = Graphics.window


class Game:

    TILE_SIZE = 50
    HAND_SIZE = 7

    def __init__(self, width, height):
        global window
        window = Graphics.window
        self.width = width
        self.height = height

        self.cardWidth = 75
        self.cardHeight = 100

        self.activePlayer = 0
        self.selectedCard = None

        self.hands = [None] * 2
        self.hands[0] = [None] * self.HAND_SIZE
        self.hands[1] = [None] * self.HAND_SIZE

        self.powerHandles = [None] * 2

        self.menu = Menu(self)
        self.sideBar = SideBar()
        self.sideBar.addItem("LClick cards to select them")
        self.sideBar.addItem("LClick placed tiles to rotate them")
        self.sideBar.addItem("RClick tile for tile menu")
        self.sideBar.addItem("RClick card for card menu")
        self.sideBar.addItem("D to draw")
        self.sideBar.addItem("T to end turn")
        self.sideBar.addItem("R to reload json data")
        self.sideBar.addItem("LClick board to place selected tile")
        self.sideBar.addItem("")

        self.cards = []
        self.deckSize = 0

        self.parseTiles()
        self.makeDeck()
        self.sideBar.addItem("")

        # Draw opening hands
        for player in xrange(0, 2):
            for i in xrange(0, 5):
                self.hands[player][i] = self.deck.pop()

        self.grid = [[None for y in range(self.height)] for x in range(self.width)]
        base0 = Tile(self.tileData[0], 0, self.width / 2, self.height - 1, 0)
        base1 = Tile(self.tileData[0], 0, self.width / 2, 0, 1)
        base0.active = base1.active = True
        self.grid[self.width / 2][0] = base1
        self.grid[self.width / 2][self.height - 1] = base0

        self.calculatePower(0)
        self.calculatePower(1)

    def makeDeck(self, firstRun=True):
        self.deck = [None] * self.deckSize
        i = 0
        index = 0
        for tile in self.tileData:
            letter = chr(ord('A') + i)
            if firstRun is True:
                self.sideBar.addItem(letter + " - " + tile['name'])
            for j in xrange(0, tile['number']):
                self.deck[index] = i
                index += 1
            i += 1
        shuffle(self.deck)

    def parseTiles(self):
        json_data = open('tiles.json')

        self.tileData = json.load(json_data)
        json_data.close()

        self.deckSize = 0
        for tile in self.tileData:
            self.deckSize += tile['number']

    def reloadData(self):
        self.parseTiles()
        self.makeDeck(False)
        for col in self.grid:
            for tile in col:
                if tile is not None:
                    tile.loadData(self.tileData[tile.mID])

    def calculatePower(self, player=None):
        if player is None:
            player = self.activePlayer

        x = self.width / 2
        # HACKHACKHACKHACKHACKHACKHACK Hack
        y = (self.height - 1) * (1 - player)
        base = self.grid[x][y]

        for col in self.grid:
            for tile in col:
                if tile is not None:
                    tile.checked = False

        power = self.powerBFS(base, player)

        output = "Player " + str(player + 1) + " power: " + str(power)
        if self.powerHandles[player] is None:
            self.powerHandles[player] = self.sideBar.addItem(output)
        else:
            self.sideBar.editItem(output, self.powerHandles[player])

    def powerBFS(self, tile, player):
        tile.checked = True
        power = 0
        if tile.active:
            power += tile.power
        con = tile.getConnections()

        adjacent = [None] * 4
        if tile.y != 0:
            adjacent[0] = self.grid[tile.x][tile.y - 1]
        if tile.x != self.width - 1:
            adjacent[1] = self.grid[tile.x + 1][tile.y]
        if tile.y != self.height - 1:
            adjacent[2] = self.grid[tile.x][tile.y + 1]
        if tile.x != 0:
            adjacent[3] = self.grid[tile.x - 1][tile.y]

        for i in xrange(0, 4):
            other = adjacent[i]
            if other is None or other.owner is not player or other.checked is True:
                continue
            if con[i] is True and other.getConnections()[(i + 2) % 4] is True:
                power += self.powerBFS(other, player)

        return power

    ## DRAW FUNCTIONS ##

    def draw(self):
        global DRAW_OFFSET, window
        self.drawBoard()
        DRAW_OFFSET['y'] += self.height * Tile.SIZE
        self.drawHand()
        DRAW_OFFSET['y'] -= self.height * Tile.SIZE
        DRAW_OFFSET['x'] += self.width * Tile.SIZE
        self.sideBar.draw(window)
        DRAW_OFFSET['x'] -= self.width * Tile.SIZE
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
        white = pygame.Color('white')
        black = pygame.Color('black')
        green = pygame.Color('green')
        blue = pygame.Color('blue')
        red = pygame.Color('red')

        box = list((DRAW_OFFSET['x'], DRAW_OFFSET['y'], 0, 0))
        box[2] = self.width * Tile.SIZE
        box[3] = 100
        window.fill(blue if self.activePlayer == 0 else red, box, 0)

        box = list((DRAW_OFFSET['x'] + 5, DRAW_OFFSET['y'] + 5, 70, 90))
        font = pygame.font.Font(None, 42)
        smallFont = pygame.font.Font(None, 24)
        for i in xrange(0, self.HAND_SIZE):
            card = self.getHand()[i]
            if card is not None:
                window.fill(white, box, 0)
                if (self.selectedCard == i):
                    pygame.draw.rect(window, green, box, 5)
                else:
                    pygame.draw.rect(window, black, box, 2)
                text = font.render(chr(ord('A') + card), 1, black)
                text_pos = list(box)
                text_pos[0] += 5
                text_pos[1] += 5
                window.blit(text, text_pos)

                text = smallFont.render(self.tileData[card]["conType"], 1, black)
                text_pos[1] += 50
                window.blit(text, text_pos)
            box[0] += 75

    ## EVENT HANDLERS ##

    def handleClick(self, x, y, left=True):
        if (self.menu.handleClick(x, y)):
            return 1
        if x > self.width * Tile.SIZE:
            return 0

        if y > self.height * Tile.SIZE:
            if (not left and self.selectedCard is not None):
                self.menu.activate(x, y)
            else:
                index = x / self.cardWidth
                self.cardClicked(index)
            return 1
        else:
            if (left):
                self.tileClicked(x / Tile.SIZE, y / Tile.SIZE)
            else:
                tile = self.grid[x / Tile.SIZE][y / Tile.SIZE]
                self.menu.activate(x, y, tile)
            return 1

    def cardClicked(self, index):
        if (index == self.selectedCard):
            self.selectedCard = None
        elif self.getHand()[index] is not None:
            self.selectedCard = index
        return 1

    def tileClicked(self, x, y):
        tile = self.grid[x][y]
        if tile is None:
            tileID = self.takeCard()
            if (tileID is not None):
                tile = Tile(self.tileData[tileID], tileID, x, y, self.activePlayer)
                self.grid[x][y] = tile
        else:
            tile.rotate()
        self.calculatePower()

    def flipTile(self, x, y):
        tile = self.grid[x][y]
        tile.flip()
        self.calculatePower(tile.owner)

    def destroyTile(self, x, y):
        self.grid[x][y] = None
        self.calculatePower()

    def addCard(self):
        hand = self.getHand()
        for i in xrange(0, self.HAND_SIZE):
            if hand[i] is None:
                hand[i] = self.deck.pop()
                return

    def takeCard(self):
        card = None
        if (self.selectedCard is not None):
            card = self.getHand()[self.selectedCard]
            self.getHand()[self.selectedCard] = None
            self.selectedCard = None
        return card

    def discardSelected(self):
        if (self.selectedCard is not None):
            self.getHand()[self.selectedCard] = None
            self.selectedCard = None

    def endTurn(self):
        self.calculatePower()
        self.activePlayer = 0 if self.activePlayer == 1 else 1
        self.selectedCard = None
        self.calculatePower()

    def getHand(self):
        return self.hands[self.activePlayer]
