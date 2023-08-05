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

    def __init__(self,x,y,l,w,d):
        super().__init__(x,y,l,w)
        self.direction = d
        self.moving = False


class Snake(pygame.sprite.Sprite):

    def __init__(self, direction, x, y):
        super().__init__()
        self.length = 2 #snake will be just one body length long initially
        self.body = [] #will need a list of rectangles for when the snake changes positions
        self.body.append(Body(x*32+4,y*32-4,24,24,direction))
        self.body[0].moving = True

    def update(self):

        for i in range(len(self.body)):

            if i == 0 or i == len(self.body) - 1:

                if self.body[i].direction == 'W':

                    if i == 0:
                        self.body[i].height += speed
                        self.body[i].moving = True
                    else:
                        self.body[i].height -= speed

                    if self.body[i].height > self.length * 32-8:
                        self.body[i].moving = True
                        self.body[i].height = self.length * 32-8

                    if self.body[i].height < 24:
                        self.body.pop(i)
                        break

                if self.body[i].direction == 'A':

                    if i == 0:
                        self.body[i].width += speed
                        self.body[i].moving = True
                    else:
                        self.body[i].width -= speed

                    if self.body[i].width > self.length * 32 - 8:
                        self.body[i].moving = True
                        self.body[i].width = self.length * 32 - 8

                    if self.body[i].width < 24:
                        self.body.pop(i)
                        break

                if self.body[i].direction == 'S':

                    if i == 0:
                        self.body[i].height += speed
                    else:
                        self.body[i].height -= speed
                        self.body[i].moving = True

                    if self.body[i].height > self.length * 32 - 8:
                        self.body[i].moving = True
                        self.body[i].height = self.length * 32 - 8

                    if self.body[i].height < 24:
                        self.body.pop(i)
                        break

                if self.body[i].direction == 'D':

                    if i == 0:
                        self.body[i].width += speed
                    else:
                        self.body[i].width -= speed
                        self.body[i].moving = True

                    if self.body[i].width > self.length * 32 - 8:
                        self.body[i].moving = True
                        self.body[i].width = self.length * 32 - 8

                    if self.body[i].width < 24:
                        self.body.pop(i)
                        break

            if self.body[i].moving:

                if self.body[i].direction == 'W':
                    self.body[i].move_ip(0,-speed)

                if self.body[i].direction == 'A':
                    self.body[i].move_ip(-speed, 0)

                if self.body[i].direction == 'S':
                    self.body[i].move_ip(0, speed)

                if self.body[i].direction == 'D':
                    self.body[i].move_ip(speed, 0)

            pygame.draw.rect(Game, (255, 255, 255), self.body[i])

    # updates the direction for the head of the snake
    def updateDirection(self, direction):
        bodyDir = self.body[0].direction
        self.body[0].direction = direction

        # we are creating a copy of the previous rectangle for when the snake changes direction

        index = len(self.body) - 1
        x = self.body[index].left
        y = self.body[index].top
        width = self.body[index].width
        length = self.body[index].height
        self.body.append(Body(x, y, width, length, bodyDir))

        self.body[0].height = 24
        self.body[0].width = 24

        origX = self.body[0].left
        origY = self.body[0].top

        if direction == 'D':
            self.body.left = origX + 24


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
            if event.key == pygame.K_a:
                snake.updateDirection('A')
            if event.key == pygame.K_s:
                snake.updateDirection('S')
            if event.key == pygame.K_d:
                snake.updateDirection('D')
    drawBoard()
    snake.update()
    pygame.display.update()
    FPS.tick(30)  # sets a framerate limit to 30
