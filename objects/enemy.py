import arcade
import random

class Enemy:
    def __init__(self, x, y):
        super().__init__(":resources:images/enemies/wormGreen.png", scale = 0.5)
        self.center_x = x
        self.center_y = y
        self.change_x = random.choice([-2, 2])