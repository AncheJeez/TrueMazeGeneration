import pygame as pg
from .settings import *

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        #super().__init__(game.all_sprites)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.last_update = pg.time.get_ticks()

        self.pressed_a = False
        self.pressed_d = False
        self.pressed_w = False
        self.pressed_s = False
    
    def move(self, dx=0, dy=0):
        # if not self.collide_with_walls(dx, dy):
        #     self.x += dx
        #     self.y += dy
        now = pg.time.get_ticks()
        elapsed_time = now - self.last_update

        if elapsed_time >= 100:  # Adjust this value to control the movement frequency
            if not self.collide_with_walls(dx, dy):
                self.x += dx
                self.y += dy
            self.last_update = now

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        if self.pressed_a: self.move(dx=-1)
        if self.pressed_d: self.move(dx=1)
        if self.pressed_w: self.move(dy=-1)
        if self.pressed_s: self.move(dy=1)
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def events(self, event_list):
        key_mapping = {
            pg.K_a: 'pressed_a',
            pg.K_d: 'pressed_d',
            pg.K_w: 'pressed_w',
            pg.K_s: 'pressed_s',
        }
        for event in event_list:
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                for key, attribute in key_mapping.items():
                    if event.key == key:
                        setattr(self, attribute, event.type == pg.KEYDOWN)



class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Boundary_wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(DARKGREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Path(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE