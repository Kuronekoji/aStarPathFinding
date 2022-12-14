from main import *
from pygame import *


class Spot:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.g = 0
        self.f = float("inf")
        self.h = float("inf")


    def show(self):
        square = Rect(self.x * (width/squares), self.y * (height/squares), width/squares, height/squares)
        screen.fill((0, 0, 0), square)
        draw.rect(screen, (255, 255, 255), square)
