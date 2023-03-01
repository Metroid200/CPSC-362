import colors

from colors import LIGHT_GREY, DARK_GREY, LIGHT_RED, RED, BLACK


class Settings:
    def __init__(self):
        self.screen_width, self.screen_height = 1200, 800
        self.bg_color = LIGHT_RED

        self.ship_image = 'images/ship.bmp'
        self.ship_speed = 3

        self.alien_image = 'images/alien.bmp'
        self.alien_speed_factor = 1
        self.fleet_drop_speed = 10

        self.laser_speed_factor = 4
        self.laser_width = 2
        self.laser_height = 30
        self.lasers_allowed = 3000
        self.laser_color = RED
