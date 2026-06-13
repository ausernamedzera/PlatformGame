import arcade
import random

class Enemy(arcade.Sprite):
    def __init__(self, x, y):
        texture = arcade.load_texture(":resources:images/enemies/wormGreen.png")
        super().__init__(texture)
        self.center_x = x
        self.center_y = y
        self.change_x = random.choice([-2, 2])
        self.start_x = x

    def update(self):
        self.center_x += self.change_x
        if abs(self.center_x - self.start_x) > 100:  
            self.change_x *= -1