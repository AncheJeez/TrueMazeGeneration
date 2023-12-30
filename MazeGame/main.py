import pygame as pg
from game.game import Game
from game.menu import StartMenu, GameMenu
from game.settings import *

def main():

    running = True

    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH,HEIGHT))
    #screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
    clock = pg.time.Clock()

    # implement menus
    start_menu = StartMenu(screen, clock)
    game_menu = GameMenu(screen, clock)

    # implement game
    game = Game(screen, clock)

    while running:

        playing = True

        while playing:
            # game loop
            game.run()
            # pause loop
            playing = game_menu.run()

        game.reset_game()

if __name__ == "__main__":
    main()