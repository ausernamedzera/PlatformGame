import arcade
import random

class Enemy:
    def __init__(self, x, y):
        super().__init__(":resources:images/enemies/wormGreen.png", scale = 0.5)
