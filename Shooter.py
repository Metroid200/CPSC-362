import pygame
import os
import time
import random
pygame.font.init()

# Display Settings
WIDTH, HEIGHT = 1600, 900
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Place Holder Shooter")

# Player
MAIN_SHIP = pygame.image.load(os.path.join("Assets", "Player.png"))
MAIN_SHIP = pygame.transform.scale(MAIN_SHIP, (100, 100))

# Background Layer
BG = pygame.image.load(os.path.join("Assets", "Purple_Space.jpg"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.cool_down_counter = 0

     # Currently Draws the hitbox
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = MAIN_SHIP
        self.mask = pygame.mask.from_surface(self.ship_img)


def main():
    run = True
    FPS = 60
    level = 1
    lives = 3
    player_velocity = 10
    main_font = pygame.font.SysFont("comicsans", 50)

    # Test Ship creation and starting location.
    player = Player(750, 650)

    # Keeps Game FPS consistant on every machine.
    clock = pygame.time.Clock()

    # Refreshes the page
    def redraw_window():
        WINDOW.blit(BG, (0, 0))
        # Basic UI
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player.draw(WINDOW)

        pygame.display.update()

    while run:

        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            # Quit Game
            if event.type == pygame.QUIT:
                run = False

        # Registers button pressing
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_velocity > 0:  # Moves Left
            player.x -= player_velocity
        if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH:  # Moves Right
            player.x += player_velocity
        if keys[pygame.K_w] and player.y - player_velocity > 0:  # Moves Up
            player.y -= player_velocity
        if keys[pygame.K_s] and player.y + player_velocity + player.get_height() < HEIGHT:  # Moves Down
            player.y += player_velocity


main()
