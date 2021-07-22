import pygame
import os

class Scrolling:

    def __init__(self, y, vel, img):
        self.y = y
        self.vel = vel
        self.x1 = 0
        
        self.base_img = img
        self.WIDTH = self.base_img.get_width()
        self.IMG = self.base_img
        self.x2 = self.WIDTH

    def move(self):
        self.x1 -= self.vel
        self.x2 -= self.vel
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))