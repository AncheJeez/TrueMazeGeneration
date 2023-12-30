import pygame as pg
import sys
from .settings import *
from game.map import Maze, Camera
from game.sprites import Player, Wall

class Game:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()
        self.width, self.height = self.screen.get_size() # this for hud

        self.reset_game()

    # method run
    def run(self):
        self.reset_game()
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        event_list = pg.event.get()
        for event in event_list:
            self.player.events(event_list)
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def update(self):
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.maze.draw()
        self.paths.draw(self.screen)
        #for sprite in self.all_sprites:
        #    self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.all_sprites.draw(self.screen)
        pg.display.flip()

    def reset_game(self):
        # kill all the sprites
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.paths = pg.sprite.Group()
        self.maze = Maze(self, self.screen, self.clock)
        self.player = Player(self, 1, 1)
        self.camera = Camera(GRIDWIDTH, GRIDHEIGHT)
        #for x in range(10, 20):
        #    Wall(self, x, 5)

    def quit(self):
        pg.quit()
        sys.exit()
