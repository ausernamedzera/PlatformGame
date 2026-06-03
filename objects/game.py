import arcade
from objects.player import Player
from constants import *

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        self.platform_list = arcade.SpriteList() #Belongs to arcade, hold objects

    def on_draw(self):
        self.clear()

    def on_update(self, delta_time):
        self.physics_engine.update()