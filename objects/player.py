import arcade
from constants import *

class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.texture = arcade.make_soft_circle_texture(40, arcade.color.BLUE)