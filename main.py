import pygame, sys
from pygame.locals import QUIT
from pygame.locals import *
from pygame import *
import random

pygame.display.set_caption("            SNEKK")  # caption at the top of the window
FPS = pygame.time.Clock()
gridSize = 20
speed = 2

snakeColour = (196, 255, 14)

bodyWidth = 24
bodyLength = 24

darkMode = True

Game = pygame.display.set_mode((32 * gridSize, 32 * gridSize))  # Width and Height of Window

pygame.init()
snakeMove = pygame.mixer.Sound('Sounds/snakeMove.wav')
eatApple = pygame.mixer.Sound('Sounds/eatApple.wav')
collision = pygame.mixer.Sound('Sounds/collision.mp3')

# these are the walls the snake can collide with
walls = (pygame.rect.Rect(0, 0, 32 * gridSize, 32), pygame.rect.Rect(32 * gridSize - 32, 0, 32, 32 * gridSize),
         pygame.rect.Rect(0, 0, 32, 32 * gridSize), pygame.rect.Rect(0, 32 * gridSize - 32, 32 * gridSize, 32))

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

    apple.draw()

#Objects Class
class Object(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load('assets/'+img)
        self.rect = self.image.get_rect()

    def spawn(self, x, y):
        self.rect.x = x * 32 + 4
        self.rect.y = y * 32 + 4

    def draw(self):
        Game.blit(self.image, self.rect)

# Body Class
class Body(pygame.Rect):

    def __init__(self,x,y,d):
        super().__init__(x ,y ,bodyWidth , bodyLength)
        self.direction = d

apple = Object('apple.png')

class Snake(pygame.sprite.Sprite):

    def __init__(self, direction, x, y):
        super().__init__()
        self.body = [] #will need a list of rectangles for when the snake changes positions
        self.body.append(Body(x*32+4,y*32-4, direction))
        self.body.append(Body(x * 32 + 4, y * 32 + 20, direction))
        self.body.append(Body(x * 32 + 4, y * 32 + 44, direction))
        self.speed = 2 #snake will initially move at 2 pixels per frame

    def update(self):

        for i in range(len(self.body)):

            if self.body[i].direction == 'W':
                self.body[i].move_ip(0,-self.speed)

            if self.body[i].direction == 'A':
                self.body[i].move_ip(-self.speed, 0)

            if self.body[i].direction == 'S':
                self.body[i].move_ip(0, self.speed)

            if self.body[i].direction == 'D':
                self.body[i].move_ip(self.speed, 0)

            if not i == 0:

                if self.body[i - 1].direction == 'W' or self.body[i - 1].direction == 'S':

                    if self.body[i].direction == 'A':

                        if self.body[i].left < self.body[i - 1].left:
                            self.body[i].direction = self.body[i - 1].direction
                            self.body[i].left = self.body[i - 1].left
                            fixVertPos()

                    elif self.body[i].direction == 'D':

                        if self.body[i].right > self.body[i - 1].right:
                            self.body[i].direction = self.body[i - 1].direction
                            self.body[i].right = self.body[i - 1].right
                            fixVertPos()

                if self.body[i - 1].direction == 'A' or self.body[i - 1].direction == 'D':

                    if self.body[i].direction == 'S':

                        if self.body[i].bottom > self.body[i - 1].bottom:
                            self.body[i].direction = self.body[i - 1].direction
                            self.body[i].bottom = self.body[i - 1].bottom
                            fixHorizPos()

                    elif self.body[i].direction == 'W':

                        if self.body[i].top < self.body[i - 1].top:
                            self.body[i].direction = self.body[i - 1].direction
                            self.body[i].top = self.body[i - 1].top
                            fixHorizPos()

            pygame.draw.rect(Game, snakeColour, self.body[i])

            def fixVertPos():
                if self.body[i - 1].direction == 'W':
                    self.body[i].top = self.body[i - 1].top + 24

                if self.body[i - 1].direction == 'S':
                    self.body[i].bottom = self.body[i - 1].bottom - 24

            def fixHorizPos():
                if self.body[i - 1].direction == 'A':
                    self.body[i].left = self.body[i - 1].left + 24
                if self.body[i - 1].direction == 'D':
                    self.body[i].right = self.body[i - 1].right - 24


    # updates the direction for the head of the snake
    def updateDirection(self, direction):
        currentDirection = self.body[0].direction

        if currentDirection == 'W' or currentDirection == 'S':
            if direction != 'W' and direction != 'S':
                self.body[0].direction = direction
                pygame.mixer.Sound.play(snakeMove)

        if currentDirection == 'A' or currentDirection == 'D':
            if direction != 'A' and direction != 'D':
                self.body[0].direction = direction
                pygame.mixer.Sound.play(snakeMove)

    def checkCollisions(self):

        if self.body[0].colliderect(apple.rect):

            maxSpeed = 10
            index = len(self.body) - 1
            x = self.body[index].x
            y = self.body[index].y
            pygame.mixer.Sound.play(eatApple)
            if self.speed < maxSpeed:
                self.speed += 1

            if self.body[index].direction == 'W':
                self.body.append(Body(x, y + 24, 'W'))

            if self.body[index].direction == 'A':
                self.body.append(Body(x + 24, y, 'A'))

            if self.body[index].direction == 'S':
                self.body.append(Body(x, y - 24, 'S'))

            if self.body[index].direction == 'D':
                self.body.append(Body(x - 24, y, 'D'))
            spawnApple()

        for i in range(len(walls)):

            if snake.body[0].colliderect(walls[i]):
                pygame.mixer.Sound.play(collision)
                sys.exit()

        for i in range(len(self.body)):

            if i != 1 and i != 0 and self.body[0].colliderect(self.body[i]):
                pygame.mixer.Sound.play(collision)
                sys.exit()
def spawnApple():
    x = random.randint(1,18)
    y = random.randint(1,18)
    apple.spawn(x, y)


snake = Snake('W',10,10)
spawnApple()

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
    snake.checkCollisions()
    pygame.display.update()
    FPS.tick(30)  # sets a framerate limit to 30
