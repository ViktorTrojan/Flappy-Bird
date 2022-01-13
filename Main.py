import pygame
import time

pygame.init()
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption('Flappy-Bird') # set app title

infoObject = pygame.display.Info() # get screen size
HEIGHT = int(infoObject.current_h - infoObject.current_h / 10)
WIDTH =  int(HEIGHT - HEIGHT / 3)

window = pygame.display.set_mode((WIDTH, HEIGHT)) # set window size

from Game import Game
game = Game(WIDTH, HEIGHT)

def update():
    game.update()

def draw():
    game.draw(window)
    pygame.display.update()

def returnDown(event):
    game.returnDown(event)

def spaceDown(event):
    game.spaceDown(event)

def mouseDown(event):
    game.mouseDown(event)

ns = 1000000000 / 60; # 60 fps the second
delta = 0
lastTime = time.time_ns()

# used for constant updates(e.g. 60p.s.) and unlimited drawing
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
            if event.type == pygame.QUIT:
                running = False
                break
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    returnDown(event)

                elif event.key == pygame.K_SPACE:
                    spaceDown(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouseDown(event)

        fpsLoop()

    pygame.quit()
    quit()

main()