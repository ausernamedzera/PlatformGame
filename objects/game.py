import arcade
from objects.player import Player
from constants import *

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.player = None
        self.platform_list = None
        self.physics_engine = None

    def setup(self):
        self.platform_list = arcade.SpriteList() #Belongs to arcade, hold objects
        self.player = Player()

        #platform
        for i in range(20):
            platform = arcade.SpriteSolidColor(40, 20, color=arcade.color.GREEN)
            platform.center_x = i*40
            platform.center_y = 20
            self.platform_list.append(platform)

        #physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.platform_list,
            gravity_constant=GRAVITY
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.center_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.center_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.center_y = PLAYER_MOVEMENT_SPEED

    def on_draw(self):
        self.clear()
        self.platform_list.draw()
        arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 20, arcade.color.BLUE)

    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()
            print(self.player.center_y)