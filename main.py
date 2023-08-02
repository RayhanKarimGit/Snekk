import pygame, sys
from pygame.locals import QUIT
from pygame.locals import *
from pygame import *
import random

pygame.display.set_caption("            SNAKE")  # caption at the top of the window
FPS = pygame.time.Clock()
gridSize = 20
speed = 1

snakeColour = (255, 255, 255)
appleColour = (210, 43, 43)

bodyWidth = 40
bodyLength = 40;

darkMode = True


# method to load a png file based on its name
def loadImg(fileName):
    return pygame.image.load("assets/" + str(fileName) + ".png")


# displays an image with given coordinates, takes a coordinate based on the grid size of the square
def displayTile(image, x, y):
    Game.blit(image, (x * 32, y * 32))  # multiplies by 32 to ensure each 32x32 tile is placed next to each other


darkCornerTile = loadImg('darkcornerstone')
frontWall = loadImg('frontwall')
backWall = loadImg('brickwall')
sideWall = loadImg('wallblock')
darkFloor = loadImg('darktile')

# snake body parts
headDown = loadImg('snakeheadDown')
headLeft = loadImg('snakeheadLeft')
headRight = loadImg('snakeheadRight')
headUp = loadImg('snakeheadUp')
tailDown = loadImg('tailDown')
tailLeft = loadImg('tailLeft')
tailRight = loadImg('tailRight')
tailUp = loadImg('tailUp')
horizBody = loadImg('horizontalBody')
vertBody = loadImg('verticalBody')


def drawBoard():
    displayTile(darkCornerTile, 0, 0)  # top left corner
    displayTile(darkCornerTile, gridSize - 1, gridSize - 1)  # bottom right corner
    displayTile(darkCornerTile, 0, gridSize - 1)  # bottom left corner
    displayTile(darkCornerTile, gridSize - 1, 0)  # top right corner

    for i in range(gridSize - 2):
        displayTile(frontWall, i + 1, gridSize - 1)  # creates the front wall
        displayTile(backWall, i + 1, 0)  # creates the back wall
        displayTile(sideWall, 0, i + 1)  # left side wall
        displayTile(sideWall, gridSize - 1, i + 1)  # right side wall

    for i in range(gridSize - 2):
        for j in range(gridSize - 2):
            displayTile(darkFloor, i + 1, j + 1)


# Body Class
class Body(pygame.sprite.Sprite):

    def giveImage(self):

        if self.direction == 'W' or self.direction == 'S':
            return vertBody
        if self.direction == 'A' or self.direction == 'D':
            return horizBody

    def __init__(self, direction, x, y):
        super().__init__()
        self.direction = direction
        self.image = self.giveImage()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * 32, y * 32)

    def update(self):

        if self.direction == 'W':
            self.rect.move_ip(0, -speed)

        if self.direction == 'A':
            self.rect.move_ip(-speed, 0)

        if self.direction == 'S':
            self.rect.move_ip(0, speed)

        if self.direction == 'D':
            self.rect.move_ip(speed, 0)

        Game.blit(self.image, self.rect)

    def updateDirection(self, direction):
        self.direction = direction
        self.image = self.giveImage()

class Head(Body):

    def giveImage(self):
        if self.direction == 'W':
            return headUp

        if self.direction == 'A':
            return headLeft

        if self.direction == 'S':
            return headDown

        if self.direction == 'D':
            return headRight


class Tail(Body):

    def giveImage(self):
        if self.direction == 'W':
            return tailUp

        if self.direction == 'A':
            return tailLeft

        if self.direction == 'S':
            return tailDown

        if self.direction == 'D':
            return tailRight


pygame.init()

snake = (Head('D', 10, 9), Body('W', 10, 10), Tail('W', 10, 11))


def updateSnake():

    for i in range(len(snake)):
        snake[i].update()

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                snake[0].updateDirection('W')
            if event.key == pygame.K_a:
                snake[0].updateDirection('A')
            if event.key == pygame.K_s:
                snake[0].updateDirection('S')
            if event.key == pygame.K_d:
                snake[0].updateDirection('D')


Game = pygame.display.set_mode((32 * gridSize, 32 * gridSize))  # Width and Height of Window

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    drawBoard()
    updateSnake()
    pygame.display.update()
    FPS.tick(60)  # sets a framerate limit to 30
