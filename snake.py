import pygame
import random
import sys

# We will use FPS for difficulty
# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
FPS = 10

# Screen Size
WIDTH = 640
HEIGHT = 480

# Colors
RED = pygame.color.THECOLORS['red']
BLACK = pygame.color.THECOLORS['black']
BLUE = pygame.color.THECOLORS['blue']
WHITE = pygame.color.THECOLORS['white']
GREEN = pygame.color.THECOLORS['green']

# Game
pygame.init()
pygame.mixer.init()

# Set game title
pygame.display.set_caption('RedBall')

# Set game icon
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Set game music
pygame.mixer.music.load('game.mp3')
# play game music in loop mode
pygame.mixer.music.play(-1)
# Other game sounds
end = pygame.mixer.Sound('game_over.wav')
hurt = pygame.mixer.Sound('hurt.wav')
eat = pygame.mixer.Sound('eat.wav')

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

SCORE = 0
RAD = 10
STEP = 2*RAD
LENGTH = 5
x = WIDTH//2
y = HEIGHT//2

# Group to contain all sprites of the game
all_sprites = pygame.sprite.Group()
# Group to contain the sprites used to make the body of the snake
snakeGroup = pygame.sprite.Group()
# Group ro contain the sprites used to make food
foodGroup = pygame.sprite.Group()

class Body(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        
         # load ball image
        self.image = pygame.image.load('red.png')
        
        # resize ball image
        self.image = pygame.transform.scale(self.image, (2*RAD, 2*RAD))

        # self.image = pygame.Surface((2*RAD, 2*RAD))
        # pygame.draw.circle(self.image, RED, (RAD, RAD), RAD)
        
        self.image.set_colorkey(self.image.get_at((0,0)))
        
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def update(self):
        pass        

class Snake(pygame.sprite.Sprite):
    def __init__(self):
        # initialize super class
        pygame.sprite.Sprite.__init__(self)
        
        # load ball image
        self.image = pygame.image.load('red.png')
        
        # resize ball image
        self.image = pygame.transform.scale(self.image, (2*RAD, 2*RAD))
        
        # self.image = pygame.Surface((2*RAD, 2*RAD))
        # pygame.draw.circle(self.image, RED, (RAD, RAD), RAD)
                
        # remove the black square bounding the circle
        self.image.set_colorkey(self.image.get_at((0, 0)))
        
        # get rect for image
        self.rect = self.image.get_rect()
        
        # center image at center of game screen initially
        self.rect.center = (x,y)
        
        # direction of snake
        self.dir_X = 1
        self.dir_Y = 0
        
        # self.step = RAD*2 + 5
        self.step = STEP

        self.length = LENGTH
        
        self.body = []
        for i in range(self.length-1):
            if self.body == []:
                self.body.append(Body((self.rect.centerx - 2*RAD, self.rect.centery)))
            else:
                self.body.append(Body((self.body[-1].rect.centerx - 2*RAD, self.body[-1].rect.centery)))
            all_sprites.add(self.body)
            snakeGroup.add(self.body)

    def update(self):
        # modify head position
        key = pygame.key.get_pressed()
        if (key[pygame.K_UP] or key[pygame.K_w]) and self.dir_Y != 1:
            self.dir_X = 0
            self.dir_Y = -1
        if (key[pygame.K_DOWN] or key[pygame.K_s]) and self.dir_Y != -1:
            self.dir_X = 0
            self.dir_Y = 1
        if (key[pygame.K_LEFT] or key[pygame.K_a]) and self.dir_X != 1:
            self.dir_X = -1
            self.dir_Y = 0
        if (key[pygame.K_RIGHT] or key[pygame.K_d]) and self.dir_X != -1:
            self.dir_X = 1
            self.dir_Y = 0
                    
        # Check for border crossing
        self.checkIsAlive()
        
        # modify rest of the snake body
        for i in range(self.length-2, -1, -1):
            self.body[i].rect.center = self.body[i-1].rect.center
        self.body[0].rect.center = self.rect.center
        
        # modify head of snake
        self.rect.move_ip((self.dir_X * self.step, self.dir_Y * self.step))

        # Growing Mechanism
        if pygame.sprite.spritecollide(self, foodGroup, False):
            part = Body((self.body[-1].rect.centerx, self.body[-1].rect.centery))
            self.body.append(part)
            self.length += 1
            snakeGroup.add(part)
            all_sprites.add(part)

    def checkIsAlive(self):
        if self.rect.right > WIDTH or self.rect.left < 0 or self.rect.top < 0 or self.rect.bottom > HEIGHT:
             self.kill()
             hurt.play()
        for x in self.body:
            pygame.sprite.collide_rect_ratio(0.5)
            hits = pygame.sprite.spritecollide(self, snakeGroup, False, pygame.sprite.collide_rect)
            if len(hits) > 1:
                self.kill()
                hurt.play()

class Food(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(0, WIDTH-10), random.randint(10, HEIGHT-10))

    def update(self):
        if pygame.sprite.spritecollide(self, snakeGroup, False):
            self.rect.center = (random.randint(0, WIDTH-10), random.randint(10, HEIGHT-10))
            global SCORE
            eat.play()
            SCORE += 1

# Displaying Score
def showScore(mode='play'):
    text = f'SCORE: {SCORE}'
    if mode is 'play':
        font = pygame.font.SysFont('opensans', 20, bold=True)
        textSurface = font.render(text, True, BLACK)
        textPosition = textSurface.get_rect()
        textPosition.x, textPosition.y = 20, 10
    if mode is 'over':
        font = pygame.font.SysFont('opensans', 50, bold=True)
        textSurface = font.render(text, True, BLACK)
        textPosition = textSurface.get_rect()
        textPosition.center = (x, y)
    screen.blit(textSurface, textPosition)

def gameOver():
    screen.fill(WHITE)
    text = 'Game Over'
    font = pygame.font.SysFont('opensans', 70, bold=True)
    textSurface = font.render(text, True, RED)
    textPosition = textSurface.get_rect()
    textPosition.center = (x, y-100)
    screen.blit(textSurface, textPosition)
    showScore(mode='over')
    pygame.display.update()
    pygame.display.flip()
        

# Made a snake
snake = Snake()
# Add it to respective groups
all_sprites.add(snake)
snakeGroup.add(snake)

# Same goes for Food
food = Food()
foodGroup.add(food)
all_sprites.add(food)

game_over = False
running = True
while running:
    clock.tick(FPS)
    # For catching events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False                                        
    
    # Game Logic
    if not snake.alive() and not game_over:
        game_over = True
        gameOver()
        pygame.mixer.music.stop()
        end.play()
        
    if snake.alive():
        screen.fill(WHITE)    

        showScore()
        all_sprites.update()
        all_sprites.draw(screen)

        pygame.display.update()
        pygame.display.flip()

pygame.mixer.quit()
pygame.quit()
sys.exit()