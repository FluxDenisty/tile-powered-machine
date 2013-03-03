import pygame


class Menu:

    WIDTH = 150
    HEIGHT = 120
    OPTION_HEIGHT = 30

    def __init__(self, game):
        self.game = game
        self.active = False
        self.tile = None
        self.x = 0
        self.y = 0
        self.options = [None] * 2

    def activate(self, x, y, tile=None):
        self.active = True
        self.x = x
        self.y = y
        self.tile = tile
        if (tile is not None):
            self.options[0] = "Flip Tile"
            self.options[1] = "Destroy Tile"
        else:
            self.options[0] = "Discard Selected"
            self.options[1] = "X_Scavenge VP_X"

    def handleClick(self, x, y):
        right = self.x + self.WIDTH
        bottom = self.y + self.HEIGHT
        if (not self.active):
            return 0
        if (x >= self.x and x <= right and y >= self.y and y <= bottom):
            option = (y - self.y) / self.OPTION_HEIGHT
            if option is 0:
                if (self.tile is None):
                    self.game.discardSelected()
                else:
                    self.game.flipTile(self.tile.x, self.tile.y)
            elif option is 1:
                if (self.tile is None):
                    self.game.scavenge(True)
                else:
                    self.game.destroyTile(self.tile.x, self.tile.y)
        self.active = False
        return 1

    def draw(self, window):
        if (not self.active):
            return 0
        black = pygame.Color("black")
        grey = pygame.Color("grey")
        box = (self.x, self.y, self.WIDTH, self.HEIGHT)
        window.fill(grey, box, 0)
        pygame.draw.rect(window, black, box, 1)

        # Draw individual options
        font = pygame.font.Font(None, 24)
        for i in xrange(0, len(self.options)):
            box = (self.x, self.y + (self.OPTION_HEIGHT * i), self.WIDTH, self.OPTION_HEIGHT)
            pygame.draw.rect(window, black, box, 1)
            text = font.render(self.options[i], 1, black)
            window.blit(text, (box[0] + 1, box[1] + 1))
