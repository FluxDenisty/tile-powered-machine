import pygame


class Tile:
    '''
    defaults for conTypes:
        O - only top
        I - top and bottom
        L - top and right
        T - bottom left and right
        X - all
    NOTE: rotation is clockwise
    Rotation order is top, right, bottom, left
    '''

    SIZE = 50

    def __init__(self, data):
        self.data = data
        self.conType = data['conType']
        self.rotation = 0
        self.setConnections()

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4
        self.setConnections()

    def getConnections(self):
        return self.connections

    def setConnections(self):
        ret = [False] * 4
        c = self.conType

        if (c is "O" or c is "I" or c is "L" or c is "X"):
            ret[(0 + self.rotation) % 4] = True
        if (c is "L" or c is "T" or c is "X"):
            ret[(1 + self.rotation) % 4] = True
        if (c is "I" or c is "T" or c is "X"):
            ret[(2 + self.rotation) % 4] = True
        if (c is "T" or c is "X"):
            ret[(3 + self.rotation) % 4] = True

        self.connections = ret

    def draw(self, window, x, y):
        window.fill(pygame.Color("white"), (x, y, self.SIZE, self.SIZE), 0)
        green = pygame.Color("green")
        off = self.SIZE / 2
        middle = (off + x, off + y)
        if (self.connections[0]):
            pygame.draw.line(window, green, (off + x, y), middle, 3)
        if (self.connections[1]):
            pygame.draw.line(window, green, (self.SIZE + x, y + off), middle, 3)
        if (self.connections[2]):
            pygame.draw.line(window, green, (off + x, self.SIZE + y), middle, 3)
        if (self.connections[3]):
            pygame.draw.line(window, green, (x, off + y), middle, 3)
