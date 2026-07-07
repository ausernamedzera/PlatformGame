import arcade
from objects.player import Player
from constants import *
import random
from objects.enemy import Enemy

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        self.player = None
        self.platform_list = None
        self.physics_engine = None
        self.camera = None
        self.coin_list = None
        self.enemy_list = None
        self.enemies_killed = 0
        self.score = 0
        self.last_platform_x = 0
        self.lives = 3
        self.game_over = False
        self.stage = 1
        self.last_tower_y = 32

    def setup(self):
        self.platform_list = arcade.SpriteList() #Belongs to arcade, hold objects
        self.player = Player()
        self.camera = arcade.Camera2D()
        self.coin_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()

        # platform
        for i in range(20):
            platform = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                scale=0.5
            )
            platform.center_x = i * 128
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
        if self.game_over:
            if key == arcade.key.ESCAPE:
                arcade.exit()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_draw(self):
        self.clear()

        #camera
        with self.camera.activate():
            self.enemy_list.draw()
            self.platform_list.draw()
            arcade.draw_circle_filled(self.player.center_x, self.player.center_y, 20, arcade.color.BLUE)
            # coin
            self.coin_list.draw()
            arcade.draw_text(f"Score: {self.score}",
                             self.camera.position[0] - SCREEN_WIDTH/2 + 10,
                            self.camera.position[1] + SCREEN_HEIGHT/2 - 30,
                            arcade.color.BLACK_OLIVE, 16)
        arcade.draw_text(f"Health: {self.lives}", 10, SCREEN_HEIGHT - 50, arcade.color.BLACK_OLIVE, 16)
        arcade.draw_text(f"Stage: {self.stage}", 10, SCREEN_HEIGHT - 70, arcade.color.BLACK_OLIVE, 16)
        #check the old code later
        if self.game_over:
            arcade.draw_text("GAME OVER",SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2, arcade.color.RED, 50)
        #border
        if self.platform_list:
            left_most = min(p.center_x for p in self.platform_list)
            if self.player.center_x < left_most:
                self.player.center_x = left_most

    def on_update(self, delta_time):
        if self.game_over:
            return
        if self.physics_engine:
            self.physics_engine.update()
        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1
            if self.score >= 10 and self.stage == 1:
                self.stage = 2

        #respawn
        if self.player.center_y < -100:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            self.player.center_y = 200
            self.player.center_x = 100
            self.player.change_x = 0
            self.player.change_y = 0

        #platform
        if self.player.center_x+400 > self.last_platform_x:
            self.last_platform_x += 64
            platform = arcade.Sprite(
                ":resources:images/tiles/grassMid.png",
                scale=0.5
            )
            platform_width = random.randint(3, 6)
            for j in range(platform_width):
                platform = arcade.Sprite(
                    ":resources:images/tiles/grassMid.png",
                    scale=0.5
                )
                platform.center_x = self.last_platform_x + j * 64
                platform.center_y = 32
                self.platform_list.append(platform)
            self.last_platform_x += platform_width * 64 + random.randint(80, 160)
            # coin
            if random.random() < 0.8:
                coin = arcade.Sprite(":resources:images/items/coinGold.png", scale=0.5)
                coin.center_x = random.randint(self.last_platform_x+100, self.last_platform_x + 400)
                coin.center_y = random.randint(90, 200)
                self.coin_list.append(coin)
        to_remove = [p for p in self.platform_list if p.center_x < self.player.center_x - 3000]
        for p in to_remove:
            p.remove_from_sprite_lists()
        self.camera.position = (self.player.center_x, self.player.center_y)

        #enemy
        if self.stage == 2:
            if random.random() < 0.006:
                if self.platform_list:
                    ahead_platforms = [p for p in self.platform_list if p.center_x > self.player.center_x]
                    if ahead_platforms:
                        random_platform = random.choice(ahead_platforms)
                        enemy = Enemy(random_platform.center_x, random_platform.center_y + 50, self.platform_list)
                        self.enemy_list.append(enemy)
            for enemy in self.enemy_list:
                enemy.move()

        if self.stage == 2:
            enemies_hit =  arcade.check_for_collision_with_list(self.player, self.enemy_list)
            for enemy in enemies_hit:
                if self.player.center_y < enemy.center_y-10:
                    self.lives -= 1
                    enemy.remove_from_sprite_lists()
                else:
                    self.enemies_killed += 1
                    self.score += 2
                    self.player.change_y= PLAYER_JUMP_SPEED
                    enemy.remove_from_sprite_lists()

                if self.enemies_killed >= 10:
                    self.stage = 3

        if self.stage == 3:
            print(f"last_tower_y: {self.last_tower_y}, player_y: {self.player.center_y}")
            if self.player.center_y + 300 > self.last_tower_y:
                self.last_tower_y += random.randint(100,150)
                platform = arcade.Sprite(":resources:images/tiles/grassMid.png", scale=0.5)
                platform.center_x = random.randint(100, 700)
                platform.center_y = self.last_tower_y
                self.platform_list.append(platform)

        to_remove_enemies = [e for e in self.enemy_list if e.center_y < -200]
        for e in to_remove_enemies:
            e.remove_from_sprite_lists()