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
        self.camera = None
        self.coin_list = None
        self.score = 0
        self.last_platform_x = 0

    def setup(self):
        self.platform_list = arcade.SpriteList() #Belongs to arcade, hold objects
        self.player = Player()
        self.camera = arcade.Camera2D()
        self.coin_list = arcade.SpriteList()

        # platform
        for i in range(20):
            platform = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                scale=0.5
            )
            platform.center_x = i * 64
            platform.center_y = 32
            self.platform_list.append(platform)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player,
            gravity_constant=GRAVITY,
            walls = self.platform_list
        )

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.UP or key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self):
        self.clear()
        #camera
        with self.camera.activate():
            self.platform_list.draw()
            arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 20, arcade.color.BLUE)

        #border
        if self.platform_list:
            left_most = min(p.center_x for p in self.platform_list)
            if self.player.center_x < left_most:
                self.player.center_x = left_most

    def on_update(self, delta_time):
        if self.physics_engine:
            self.physics_engine.update()

        if self.player.center_x+400 > self.last_platform_x:
            self.last_platform_x += 64
            platform = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                scale=0.5
            )
            platform.center_x = self.last_platform_x
            platform.center_y = 32
            self.platform_list.append(platform)
        to_remove = [p for p in self.platform_list if p.center_x < self.player.center_x - 1400]
        for p in to_remove:
            p.remove_from_sprite_lists()
        self.camera.position = (self.player.center_x, self.player.center_y)

        coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
        coin.center_x = self.last_platform_x
        coin.center_y = random.randint(60,200)
        self.coin_list.append(coin)