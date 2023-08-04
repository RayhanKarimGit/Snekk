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

Game = pygame.display.set_mode((32 * gridSize, 32 * gridSize))  # Width and Height of Window

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

def drawBoard():
    displayTile(darkCornerTile, 0, 0)  # top left corner
    displayTile(darkCornerTile, gridSize - 1, gridSize - 1)  # bottom right corner
    displayTile(darkCornerTile, 0, gridSize - 1)  # bottom left corner
    displayTile(darkCornerTile, gridSize - 1, 0)  # top right corner

    for i in range(gridSize - 2):
        displayTile(sideWall, i + 1, gridSize - 1)  # creates the front wall
        displayTile(sideWall, i + 1, 0)  # creates the back wall
        displayTile(sideWall, 0, i + 1)  # left side wall
        displayTile(sideWall, gridSize - 1, i + 1)  # right side wall

    for i in range(gridSize - 2):
        for j in range(gridSize - 2):
            displayTile(darkFloor, i + 1, j + 1)


# Body Class
class Body(pygame.Rect):

    def __init__(self,x,y,l,w):
        super().__init__(x,y,l,w)
        self.changing = True #boolean to keep track whether this body segment is increasing or decreasing in size


class Snake(pygame.sprite.Sprite):

    def __init__(self, direction, x, y):
        super().__init__()
        self.direction = direction
        self.length = 1 #snake will be just one body length long initially
        self.body = [] #will need a list of rectangles for when the snake changes positions
        self.body.append(Body(x*32+4,y*32-4,24,24))

    def update(self):

        for i in range(len(self.body)):

            if self.direction == 'W':

                if not self.body[i].changing:
                    self.body[i].move_ip(0, -speed)
                else:
                    self.body[i].height += 1

            if self.direction == 'A':

                if not self.body[i].changing:
                    self.body[i].move_ip(-speed, 0)
                else:
                    self.body[i].width += 1

            if self.direction == 'S':

                if not self.body[i].changing:
                    self.body[i].move_ip(0, speed)
                else:
                    self.body[i].height += 1

            if self.direction == 'D':

                if not self.body[i].changing:
                    self.body[0].move_ip(speed, 0)
                else:
                    self.body[i].width += 1

            pygame.draw.rect(Game, (255, 255, 255), self.body[i])

    def updateDirection(self, direction):
        self.direction = direction


pygame.init()

snake = Snake('W',10,10)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.updateDirection('W')
                snake.body[0].changing = True
            if event.key == pygame.K_a:
                snake.updateDirection('A')
                snake.body[0].changing = True
            if event.key == pygame.K_s:
                snake.updateDirection('S')
                snake.body[0].changing = True
            if event.key == pygame.K_d:
                snake.updateDirection('D')
                snake.body[0].changing = True
    drawBoard()
    snake.update()
    pygame.display.update()
    FPS.tick(60)  # sets a framerate limit to 30
