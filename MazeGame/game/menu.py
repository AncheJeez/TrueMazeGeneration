import pygame as pg
import sys

class StartMenu:

    def __init__(self,screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw(self.screen)

    def update(self):
        # events
        pass

    def draw(self,screen):
        pg.display.flip()

class GameMenu:

    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.screen_size = self.screen.get_size()
        self.playing = True

    def run(self):
        self.menu_running = True
        while self.menu_running:
            self.clock.tick(60)
            self.update()
            self.draw(self.screen)

    def update(self):
        # events
        pass

    def draw(self,screen):
        pg.display.flip()