import pygame as pg, sys, time
from vector import Vector
from sound import Sound
from settings import Settings
from ship import Ship
from laser import Lasers
from alien import Aliens


class Game:
    def __init__(self): 
        pg.init()
        self.settings = Settings()
        self.window_height, self.window_width = self.settings.screen_height, self.settings.screen_width
        self.screen = pg.display.set_mode((self.window_width, self.window_height), 0, 32)
        pg.display.set_caption('Alien Invasion')
        self.speed = 3
        self.finished = False
        self.sound = Sound()
        self.sound.play_background()
        self.ship = Ship(game=self)
        self.aliens = Aliens(game=self)
        self.lasers = Lasers(game=self)
        self.ship.set_lasers(self.lasers)


    def handle_events(self):
        up, down, left, right = Vector(0, -1), Vector(0, 1), Vector(-1, 0), Vector(1, 0)
        keys_dir = {pg.K_w: up, pg.K_UP: up,
                    pg.K_s: down, pg.K_DOWN: down,
                    pg.K_a: left, pg.K_LEFT: left,
                    pg.K_d: right, pg.K_RIGHT: right}
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_over()
            elif event.type == pg.KEYDOWN:
                key = event.key
                if key in keys_dir:
                    self.ship.v = self.speed * keys_dir[key]
                elif key == pg.K_SPACE:
                    self.ship.open_fire()
            elif event.type == pg.KEYUP:
                key = event.key
                if key in keys_dir:
                    self.ship.v = Vector()
                elif key == pg.K_SPACE:
                    self.ship.cease_fire()

    def restart(self): pass

    def game_over(self):
        self.finished = True
        self.sound.play_gameover()
        self.sound.stop_background()
        pg.quit()
        sys.exit()

    def play_again(self): pass

    def play(self):
        while not self.finished:
            self.handle_events() 
                
            self.screen.fill(self.settings.bg_color)
            self.ship.update()
            self.lasers.update()
            self.aliens.update()
            pg.display.update()
            # time.sleep(0.02)


def main():
    g = Game()
    g.play()
    
    
if __name__ == '__main__':
    main()

 