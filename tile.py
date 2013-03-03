import pygame


class Tile:
    '''
    defaults for conTypes:
        O - only top
        I - top and bottom
        L - top and right
        T - bottom left and right
        X - all
    Rotation is clockwise
    Rotation order is top, right, bottom, left
    '''

    SIZE = 50

    def __init__(self, data, mID, x, y, owner):
        self.data = data
        self.rotation = 0
        self.loadData(self.data)
        self.mID = mID
        self.x = x
        self.y = y
        self.owner = owner
        self.active = False
        self.checked = False

    def loadData(self, data):
        self.conType = data['conType']
        self.power = data['power']
        self.cost = data['cost']
        self.setConnections()

    def flip(self):
        self.active = not(self.active)
        return self.active

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.setConnections()

    def getConnections(self):
        return self.connections

    def setConnections(self):
        ret = [False] * 4
        c = self.conType

        if (c == "O" or c == "I" or c == "L" or c == "X"):
            ret[(0 + self.rotation) % 4] = True
        if (c == "L" or c == "T" or c == "X"):
            ret[(1 + self.rotation) % 4] = True
        if (c == "I" or c == "T" or c == "X"):
            ret[(2 + self.rotation) % 4] = True
        if (c == "T" or c == "X"):
            ret[(3 + self.rotation) % 4] = True

        self.connections = ret

    def draw(self, window, x, y):
        bg = pygame.Color('blue') if self.owner == 0 else pygame.Color('red')
        window.fill(bg, (x, y, self.SIZE, self.SIZE), 0)
        green = pygame.Color("green")
        black = pygame.Color("black")
        grey = pygame.Color("grey")
        off = self.SIZE / 2
        middle = (off + x, off + y)

        # Draw Connections
        if (self.connections[0]):
            pygame.draw.line(window, green, (off + x, y), middle, 3)
        if (self.connections[1]):
            pygame.draw.line(window, green, (self.SIZE + x, y + off), middle, 3)
        if (self.connections[2]):
            pygame.draw.line(window, green, (off + x, self.SIZE + y), middle, 3)
        if (self.connections[3]):
            pygame.draw.line(window, green, (x, off + y), middle, 3)

        font = pygame.font.Font(None, 36)
        text = font.render(chr(ord('A') + self.mID), 1, black)
        text_pos = (middle[0] - text.get_width() / 2, middle[1] - text.get_height() / 2)
        radius = (text.get_height() / 2) + 3
        pygame.draw.circle(window, green if self.active else grey, middle, radius)
        pygame.draw.circle(window, black, middle, radius, 2)
        window.blit(text, text_pos)
