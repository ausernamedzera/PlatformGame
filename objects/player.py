import arcade
from constants import *

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_circle_texture(40, arcade.color.BLUE)
        self.center_x = 100
        self.center_y = 200

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y