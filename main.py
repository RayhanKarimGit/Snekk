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
buttonColour = (117, 204, 32)

bodyWidth = 24
bodyLength = 24

gameState = 0 #0 is the main menu screen

Game = pygame.display.set_mode((32 * gridSize, 32 * gridSize))  # Width and Height of Window

mouseClick = False

pygame.init()
snakeMove = pygame.mixer.Sound('Sounds/snakeMove.wav')
eatApple = pygame.mixer.Sound('Sounds/eatApple.wav')
collision = pygame.mixer.Sound('Sounds/collision.mp3')
click = pygame.mixer.Sound('Sounds/buttonClick.mp3')

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
brickWall = loadImg('brickwall')
sideWall = loadImg('wallblock')
darkFloor = loadImg('darktile')
backgroundTile = loadImg('back3')

title = loadImg('Snekk')
deathMessage = loadImg('deathMessage')
pauseTitle = loadImg('GamePaused')

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

class Button():

    def __init__(self, x, y , width, height, img, borderColour):
        self.rect = pygame.rect.Rect(x, y, width, height) # the border colour of the button
        self.fillRect = pygame.rect.Rect(x + 4, y + 4, width - 8, height - 8) #the rectangle of the main button body itself
        self.borderColour = borderColour
        self.img = loadImg(img) #main image of the button
        self.fillColour = (0, 0, 0) #main body of button will be filled in with black
        self.imgRect = self.img.get_rect()
        self.imgRect.center = (x + width / 2, y + height / 2)

    def draw(self):
        pygame.draw.rect(Game, self.borderColour,  self.rect) #draws the border rectangle
        pygame.draw.rect(Game, self.fillColour, self.fillRect) #draws the body colour of rectangle
        Game.blit(self.img, self.imgRect)

    def click(self, nextState):
        global gameState
        global mouseClick
        x, y = pygame.mouse.get_pos()
        if self.rect.collidepoint(x, y):
            self.fillColour = (255, 255, 255)
            if mouseClick:
                pygame.mixer.Sound.play(click)
                gameState = nextState
                return True  # returns true to also use as a boolean to determine whether the button has been clicked
        else:
            self.fillColour = (0, 0, 0)

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
        self.body.append(Body(x * 32 + 4,y * 32 + 4, direction))
        self.body.append(Body(x * 32 + 4, y * 32 + 20, direction))
        self.body.append(Body(x * 32 + 4, y * 32 + 44, direction))
        self.speed = 2 #snake will initially move at 2 pixels per frame
        self.nextDirection = direction #the direction for the snake to update to
        self.lastPosX = x * 32 + 4 #last known x coordinate of snake head
        self.lastPosY = y * 32 + 4 #last known y coordinate of snake head

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

        currentDirection = self.body[0].direction
        y = self.body[0].y
        x = self.body[0].x
        if currentDirection == 'W':
            if self.nextDirection != 'W' and self.nextDirection != 'S' and y < self.lastPosY:
                self.body[0].direction = self.nextDirection
                self.body[0].y = self.lastPosY #corrects y position
                pygame.mixer.Sound.play(snakeMove)

        if currentDirection == 'A':
            if self.nextDirection != 'A' and self.nextDirection != 'D' and x < self.lastPosX:
                self.body[0].direction = self.nextDirection
                self.body[0].x = self.lastPosX #corrects x position
                pygame.mixer.Sound.play(snakeMove)

        if currentDirection == 'S':
            if self.nextDirection != 'W' and self.nextDirection != 'S' and y > self.lastPosY + 32:
                self.body[0].direction = self.nextDirection
                self.body[0].y = self.lastPosY + 32  # corrects y positionself.body[0].y = self.lastPosY #corrects y position
                pygame.mixer.Sound.play(snakeMove)

        if currentDirection == 'D':
            if self.nextDirection != 'A' and self.nextDirection != 'D' and x > self.lastPosX + 32:
                self.body[0].direction = self.nextDirection
                self.body[0].x = self.lastPosX + 32  # corrects y position
                pygame.mixer.Sound.play(snakeMove)


    # updates the direction for the head of the snake
    def updateDirection(self, direction):
        self.nextDirection = direction
        self.lastPosX = int((self.body[0].x - 4) / 32) * 32 + 4
        self.lastPosY = int((self.body[0].y - 4) / 32) * 32 + 4

    def checkCollisions(self):

        global gameState

        if self.body[0].colliderect(apple.rect):

            maxSpeed = 7
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

            x = random.randint(1, 18)
            y = random.randint(1, 18)

            keepSpawning = True

            while keepSpawning:

                for i in range(len(self.body)):
                    if not self.body[i].collidepoint((x, y)):
                        apple.spawn(x, y)
                        keepSpawning = False
                    else:
                        x = randomint(1, 18)
                        y = randomint(1, 18)

        for i in range(len(walls)):

            if snake.body[0].colliderect(walls[i]):
                pygame.mixer.Sound.play(collision)
                resetGame()
                gameState = 2

        for i in range(len(self.body)):

            if i != 2 and i != 1 and i != 0 and self.body[0].colliderect(self.body[i]):
                pygame.mixer.Sound.play(collision)
                resetGame()
                gameState = 2

snake = Snake('W',10,10)
x = random.randint(1,18)
y = random.randint(1,18)
apple.spawn(x, y)

def resetGame():
    global snake
    snake = Snake('W', 10, 10)
    x = random.randint(1, 18)
    y = random.randint(1, 18)
    apple.spawn(x, y)

def runGame():
    drawBoard()
    snake.update()
    snake.checkCollisions()

playButton = Button(170, 200, 300, 100, 'StartGame', buttonColour)
quitButton = Button(170,350, 300, 100, 'quit', buttonColour)
def mainMenu():

    #Fills in background of main menu screen
    for i in range(gridSize):
        for j in range(gridSize):
            displayTile(backgroundTile, i, j)

    Game.blit(title, (210, 50))
    playButton.draw()
    playButton.click(1)
    quitButton.draw()
    quitButton.click(10)

menuButton = Button(170, 200, 300, 100, 'MainMenu', buttonColour)
restartButton = Button(170, 350, 300, 100, 'Restart', buttonColour)

def deathScreen():

    # Fills in background of death screen screen
    for i in range(gridSize):
        for j in range(gridSize):
            displayTile(backgroundTile, i, j)

    Game.blit(deathMessage, (150, 50))
    menuButton.draw()
    if menuButton.click(0):
        resetGame()
        pygame.time.delay(100) #delays to prevent double clicking the play button back into the game
    restartButton.draw()
    restartButton.click(1)

resumeButton = Button(170, 350, 300, 100, 'Resume', buttonColour)
def pauseScreen():

    # Fills in background of pause screen
    for i in range(gridSize):
        for j in range(gridSize):
            displayTile(backgroundTile, i, j)

    Game.blit(pauseTitle, (185,50))
    menuButton.draw()
    if menuButton.click(0):
        resetGame()
        pygame.time.delay(100) #delays to prevent double clicking the play button back into the game
    resumeButton.draw()
    resumeButton.click(1)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and gameState == 1:
            if event.key == pygame.K_w:
                snake.updateDirection('W')
            if event.key == pygame.K_a:
                snake.updateDirection('A')
            if event.key == pygame.K_s:
                snake.updateDirection('S')
            if event.key == pygame.K_d:
                snake.updateDirection('D')
            if event.key == pygame.K_ESCAPE:
                gameState = 3
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseClick = True
        else:
            mouseClick = False
    if gameState == 0:
        mainMenu()
    if gameState == 1:
        runGame()
    if gameState == 2:
        deathScreen()
    if gameState == 3:
        pauseScreen()
    if gameState == 10:
        sys.exit()
    pygame.display.update()
    FPS.tick(30)  # sets a framerate limit to 30
