import arcade
from objects.game import Game
from constants import *

def main():
    game_window = Game()
    game_window.setup()
    arcade.run()


if __name__ == "__main__":
    main()