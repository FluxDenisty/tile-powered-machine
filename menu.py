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
        self.options = [None] * 4

    def activate(self, tile, x, y):
        if (tile is not None):
            self.active = True
            self.tile = tile
            self.x = x
            self.y = y
            self.options[0] = "Flip Tile"
            self.options[1] = "Destroy Tile"
            self.options[2] = "X_Move Tile_X"
            self.options[3] = "X_Create Tile_X"

    def handleClick(self, x, y):
        right = self.x + self.WIDTH
        bottom = self.y + self.HEIGHT
        if (not self.active):
            return 0
        if (x >= self.x and x <= right and y >= self.y and y <= bottom):
            option = (y - self.y) / self.OPTION_HEIGHT
            if option is 0:
                self.tile.flip()
            elif option is 1:
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
