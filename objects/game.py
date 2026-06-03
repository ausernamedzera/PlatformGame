import arcade
from objects.player import Player
from constants import *

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

    def setup(self):
        self.platform_list = arcade.SpriteList() #Belongs to arcade, hold objects
        self.player = Player()

        #platform
        for i in range(20):
            platform = arcade.SpriteSolidColor(40, 20, arcade.color.GREEN)
            platform.center_x = i*40
            platform.center_y = 20
            self.platform_list.append(platform)

        #physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            self.platform_list,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        self.payer.draw()
        self.platform_list.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()