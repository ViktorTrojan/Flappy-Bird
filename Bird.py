import pygame
import os

def blitRotateCenter(window, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

        window.blit(rotated_image, new_rect)

class Bird:

    gravityConstant = 9.80665
    gravity = 0.06
    flapping = -25
    limit = -10
    animation_time = 10

    def __init__(self, x, y, imgs, sfx_wing):
        
        self.x = x
        self.y = y
        self.imgs = imgs
        self.img = self.imgs[0]
        self.sfx_wing = sfx_wing
        self.tilt = 0
        self.vel = 0
        self.img_counter = 0
        self.boundingBox = (self.x+26, self.y+2, self.img.get_width()-34, self.img.get_height()-4)
        self.height = self.boundingBox[1]
        self.startScreen = True

    def fly(self):
        self.vel = max(self.vel + self.gravityConstant * self.gravity, self.limit)
        tiltPH = self.tilt

        # tilt up
        if self.vel < 0 or self.boundingBox[1] + self.boundingBox[3] < self.height:  
            tiltPH = self.tilt + 20
        else:  # tilt down
            tiltPH = self.tilt - 8

        # limit(clamp) self.tilt
        self.tilt = min(25, max(-90, tiltPH))

    def update(self):
        self.y = min(800-70-self.boundingBox[3], max(-15 - self.boundingBox[3], self.y + self.vel))  # set hight bounding limit
        # set the bounding box
        self.boundingBox = (self.x+26, self.y+2, self.img.get_width()-34, self.img.get_height()-4)

        if not self.startScreen:
            self.fly()

        if self.tilt == -90:
            self.img = self.imgs[1]
            return

        self.img_counter += 1
        if self.img_counter < self.animation_time:
            self.img = self.imgs[0]
        elif self.img_counter < self.animation_time*2:
            self.img = self.imgs[1]
        elif self.img_counter < self.animation_time*3:
            self.img = self.imgs[2]
        elif self.img_counter == self.animation_time*3+1:
            self.img = self.imgs[0]
            self.img_counter = 0

    def jump(self):
        if self.startScreen:
            self.startScreen = False
        self.vel = self.flapping
        self.height = self.boundingBox[1] - self.boundingBox[3]
        pygame.mixer.Sound.play(self.sfx_wing)

    def draw(self, window):
        # draw height line
        pygame.draw.line(window, (255,0,0, 100), (self.x, self.height), (self.boundingBox[0] + self.boundingBox[2], self.height), 1)

        # draw bounding box
        pygame.draw.rect(window, (0,0,255, 100), self.boundingBox, 1)

        blitRotateCenter(window, self.img, (self.x, self.y), self.tilt)