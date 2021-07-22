import pygame
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption('Flappy-Bird') # set app title

WIDTH = 500
HEIGHT = 800
window = pygame.display.set_mode((WIDTH, HEIGHT)) # set window size

from Game import Game
game = Game(WIDTH, HEIGHT)

def update():
    game.update()

def draw():
    game.draw(window)
    pygame.display.update()

def enterDown(event):
    game.enterDown(event)

def spaceDown(event):
    game.spaceDown(event)

def mouseDown(event):
    game.mouseDown(event)

ns = 1000000000 / 60; # 60 fps the second
delta = 0
lastTime = time.time_ns()

# used for constant updates(e.g. 60p.s.) and many fps
def fpsLoop():
    global delta
    global lastTime
    now = time.time_ns()
    delta += (now - lastTime) / ns
    lastTime = now
    while (delta >= 1): # run 60 times
        update()
        delta-=1
        
    draw()

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enterDown(event)

                elif event.key == pygame.K_SPACE:
                    spaceDown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown(event)

            if event.type == pygame.QUIT:
                running = False

        fpsLoop()

    pygame.quit()
    quit()

main()