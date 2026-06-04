import arcade
from constants import *

class Player(arcade.SpriteCircle):
    def __init__(self):
        super().__init__(20, arcade.color.BLUE)
        self.center_x = 100
        self.center_y = 200
