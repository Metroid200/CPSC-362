import pygame
import sys
from Player import Player
from Pattern import *


# Everytime related to the games logic goes in here.0000
class Game:
    def __init__(self, level):
        self.level = level

        # Creating a player object
        player_sprite = Player(
            (screen_width/2, screen_height - 10), screen_width, "tanzanite")

        # Creating a container for the player
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Test case for Curve Object
        self.right = Line("down")

    # Checks for collisions everywhere (>)o_o)>
    def collision_checks(self):
        # Player Lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Enemie Collisions
                if pygame.sprite.spritecollide(laser, self.right.enemies, True):
                    laser.kill()

        # Enemie Lasers
        if self.right.enemie_laser:
            for laser in self.right.enemie_laser:
                # Player Collisions
                if pygame.sprite.spritecollide(laser, self.player, False):
                    self.player.sprite.get_damage(100)
                    laser.kill()

    # Main Gameplay loop.
    def run(self):
        # Enemie Info
        # Level 1 for now :(
        if self.level == 1:
            self.right.enemies.draw(screen)
            self.right.enemie_laser.draw(screen)
            self.right.update()

        # Player Info
        self.player.sprite.lasers.draw(screen)
        self.player.update()
        self.player.draw(screen)
        self.collision_checks()


if __name__ == "__main__":
    pygame.init()
    screen_width = 1450
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game(1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
