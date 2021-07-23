import pygame
import os
from threading import Thread
import time

# game imports
from Bird import Bird
from Ground import Ground
from Background import Background
from Pipe import Pipes
class Game:
    
    # game images
    img_base = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","base.png")).convert_alpha())
    img_pipe = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha())
    img_birdArr = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","bird" + str(x) + ".png"))) for x in range(1,4)]

    # game sounds
    sfx_hit = pygame.mixer.Sound(os.path.join("sounds","sfx_hit.wav"))
    sfx_die = pygame.mixer.Sound(os.path.join("sounds","sfx_die.wav"))
    sfx_point = pygame.mixer.Sound(os.path.join("sounds","sfx_point.wav"))
    sfx_swooshing = pygame.mixer.Sound(os.path.join("sounds","sfx_swooshing.wav"))
    sfx_wing = pygame.mixer.Sound(os.path.join("sounds","sfx_wing.wav"))

    scorePoints = 0
    gameOver = False
    gameOverCheck = False

    def __init__(self, WIDTH, HEIGHT):
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.img_bg = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (WIDTH, HEIGHT))
        # game objects
        self.initGame()

    def initGame(self):
        velocity = 4
        self.background = Background(0, 0.5, self.img_bg)
        self.ground = Ground(self.HEIGHT - 60, velocity, self.img_base)
        self.bird = Bird(self.WIDTH / 4, self.HEIGHT / 2, self.img_birdArr, self.sfx_wing, self.ground.y)
        self.pipes = Pipes(self.WIDTH, self.ground.y, self.img_pipe)
        
    def addPoint(self):
        self.scorePoints += 1
        pygame.mixer.Sound.play(self.sfx_point) # play pickup sound

    def onCollide(self, ground):
        if(self.gameOverCheck != self.gameOver):
            self.gameOverCheck = self.gameOver
            pygame.mixer.Sound.play(self.sfx_hit) # play hit sound

            if not ground:
                self.bird.vel = -8
                time.sleep(0.3)
                pygame.mixer.Sound.play(self.sfx_die) # play die sound

    def update(self):
        if self.ground.isColliding(self.bird):
            self.gameOver = True
            self.onCollide(True)

        self.bird.update()
        if self.gameOver:
            return

        if not self.bird.startScreen: # if not startscreen start showing pipes
            if self.pipes.update(self.bird): # if passed a pipe
                self.addPoint()
            if self.pipes.isColliding(self.bird):
                self.gameOver = True
                t = Thread(target=self.onCollide, args=(False,))
                t.start()
                return
        
        self.background.move()
        self.ground.move()
        

    def draw(self, window):
        self.background.draw(window)
        self.pipes.draw(window)
        self.ground.draw(window)
        self.bird.draw(window)
        drawText(window, str(self.scorePoints), self.WIDTH / 2, 40, 60, (255,255,255), 2)
        if self.bird.startScreen:
            drawText(window, "Tap to start playing!", self.WIDTH / 2, self.HEIGHT / 2.4, 40, (255,255,255), 2)

        if self.gameOver:
            drawText(window, "Press enter to restart!", self.WIDTH / 2, self.HEIGHT / 2.4, 35, (255,255,255), 2)

    def returnDown(self, event):
        if self.gameOver:
            self.gameOverCheck = self.gameOver = False
            self.scorePoints = 0
            self.initGame()

    def spaceDown(self,event):
        if not self.gameOver:
            self.bird.jump()

    def mouseDown(self,event):
        if not self.gameOver:
            self.bird.jump()

def drawCenteredText(window, text, x, y, size, color):
    customFont = pygame.font.Font("font.ttf", size)
    score = customFont.render(text, False, color)
    text_rect = score.get_rect(center=(x, y))

    window.blit(score,text_rect)

def drawText(window, text, x, y, size, color, border):
    drawCenteredText(window, text, x - border, y - border, size, (0,0,0)) # topleft
    drawCenteredText(window, text, x + border, y - border, size, (0,0,0)) # topright
    drawCenteredText(window, text, x - border, y + border, size, (0,0,0)) # bottomleft
    drawCenteredText(window, text, x + border, y + border, size, (0,0,0)) # bottomright
    drawCenteredText(window, text, x, y, size, color) # bottomright