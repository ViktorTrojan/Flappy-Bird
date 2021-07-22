import pygame
import random

# manages Pipes
class Pipes:

    def __init__(self, WIDTH, bird, img, sfx_hit):
        self.WIDTH = WIDTH
        self.img = img
        self.pipes = [Pipe(self.WIDTH, 550, 4, self.img)]
        self.bird = bird
        self.gameOver = False
        self.sfx_hit = sfx_hit

    def update(self):
        add_pipe = False
        remove_pipes = []
        for pipe in self.pipes:
            if self.gameOver:
                return
            if pipe.collide(self.bird):
                self.gameOver = True
                pygame.mixer.Sound.play(self.sfx_hit)
                self.bird.vel = -8
                return

            pipe.move()

            if pipe.x + pipe.topPipe.get_width() < 0:
                remove_pipes.append(pipe)
                continue

            if not pipe.passed and pipe.x < self.bird.boundingBox[0]:
                pipe.passed = True
                add_pipe = True
                continue

        for remove_pipe in remove_pipes:
            self.pipes.remove(remove_pipe)

        if add_pipe:
            self.pipes.append(Pipe(self.WIDTH, 550, 4, self.img))
            return True

    def draw(self, window):
        for pipe in self.pipes:
            pipe.draw(window)

class Pipe:

    margin = 50
    gap = 200

    def __init__(self, x, length, vel, img):
        self.x = x
        self.top = 0
        self.bottom = 0
        self.height = 0
        self.passed = False
        self.vel = vel
        self.bottomPipe = img
        self.topPipe = pygame.transform.flip(img, False, True)
        self.summonPipe(length)

    def collide(self, bird):
        # bottom Pipe collision check
        if bird.boundingBox[0] + bird.boundingBox[2] > self.x and bird.boundingBox[1] + bird.boundingBox[3] > self.bottom and bird.boundingBox[0] < self.x + self.bottomPipe.get_width():
            return True

        # top Pipe collision check
        if bird.boundingBox[0] + bird.boundingBox[2] > self.x and bird.boundingBox[1] < self.top + self.topPipe.get_height() and bird.boundingBox[0] < self.x + self.topPipe.get_width():
           return True

        return False

    def summonPipe(self, length):
        self.height = random.randrange(0+self.margin, length - self.margin)
        self.top = self.height - self.topPipe.get_height()
        self.bottom = self.height + self.gap

    def move(self):
        self.x -= self.vel

    def draw(self, window):
        window.blit(self.topPipe, (self.x, self.top))
        window.blit(self.bottomPipe, (self.x, self.bottom))