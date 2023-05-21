import pygame
import random

# GLOBAL VARIABLES
COLOR = (255, 100, 98)
SURFACE_COLOR = (167, 255, 100)
WIDTH = 500
HEIGHT = 500


class NN:
    def __init__(self, nodes):
        self.nodes = nodes

    def feedForeward(self):
        return self.nodes.activate()


class moveF:
    def __init__(self, hidden):
        self.hidden = hidden

    def activate(self):
        return self.hidden.activate() * 0.7 + .2


class hidden:
    def __init__(self, firstNode):
        self.firstNode = firstNode

    def activate(self):
        return self.firstNode.activate() * 0.8 + 0.02


class inputNode:
    def __init__(self):
        self.weights = 0.2
        self.bias = 0.1

    def activate(self):
        return self.weights * self.weights + self.bias

# Object class


class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width, cellid):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(SURFACE_COLOR)
        self.image.set_colorkey(COLOR)
        self.cellid = cellid

        pygame.draw.rect(self.image, color, pygame.Rect(0, 0, width, height))

        self.rect = self.image.get_rect()


pygame.init()

RED = (255, 0, 0)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Creating Sprite")

all_sprites_list = pygame.sprite.Group()


for i in range(10):
    object_ = Sprite((random.randint(0, 255), random.randint(
        0, 255), random.randint(0, 255)), 10, 10, i + 1)
    object_.rect.x = random.randint(10, 490)
    object_.rect.y = random.randint(10, 490)
    # if object_.cellid == 2:
    #     object_.rect.x = 100
    # else:
    #     object_.rect.x = 400
    all_sprites_list.add(object_)


cell1NN = NN(moveF(hidden(inputNode())))


exit = True
clock = pygame.time.Clock()

while exit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = False

    print(cell1NN.feedForeward())
    nextToUse = []
    for i in all_sprites_list:

        cellIDToXY = [(i.cellid) for i in all_sprites_list]
        XandYs = [(i.rect.x, i.rect.y) for i in all_sprites_list]
        del XandYs[cellIDToXY.index(i.cellid)]
        if cell1NN.feedForeward() >= 0.24:
            # stop at edge commands (might need to ajust)
            for h in XandYs:
                print("hi")
                print(XandYs)
                print([(i.rect.x, i.rect.y)])
                if ((i.rect.x == h[0]) and (i.rect.y == h[1])):
                    # i.rect.y -= 20
                    nextToUse.append((i, i.cellid))
                    print("why")
                    
                elif (((i.rect.x + 10 <= h[0]) and (i.rect.y + 10 <= h[1])) or ((i.rect.x + 10 <= h[0]) and (i.rect.y - 10 >= h[1])) or ((i.rect.x - 10 >= h[0]) and (i.rect.y + 10 <= h[1])) or ((i.rect.x - 10 >= h[0]) and (i.rect.y - 10 >= h[1]))):
                    # i.rect.y -= 20
                    nextToUse.append((i, i.cellid))
                    print("whyt")
            for h in nextToUse:
                if h[1] == 1:
                    h[0].rect.x += 10
                else: 
                    h[0].rect.x -= 10
            if (i.rect.x >= (WIDTH)):
                i.rect.x -= 10
            elif (i.rect.x <= 0):
                i.rect.x += 10
            elif (i.rect.y <= 0):
                i.rect.y += 10
            elif (i.rect.y >= (HEIGHT)):
                i.rect.y -= 20
                i.rect.x -= 20
            else:
                if i.cellid == 1:
                    i.rect.x -= 1
                if i.cellid == 2:
                    i.rect.x += 1
    all_sprites_list.update()
    screen.fill(SURFACE_COLOR)
    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(90)
