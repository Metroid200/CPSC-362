import pygame
import sys
from Player import Player
from Boss import Boss
from Pattern import *
import random


# Everytime related to the games logic goes in here.0000
class Game:
    def __init__(self):

        # Creating a player object
        player_sprite = Player(
            (screen_width/2, screen_height - 10), screen_width, "peridot")
        # Creating a container for the player
        self.player = pygame.sprite.GroupSingle(player_sprite)

        # Creating a Boss Object
        boss_sprite = Boss((screen_width/2, -300))
        # Creating a boss container
        self.boss = pygame.sprite.GroupSingle(boss_sprite)
        # Summons the boss when it is time
        self.spawn_boss = False

        # Enemie Wave Data
        self.wave = []
        self.create_enemy_wave()
        self.wave_num = 0

    # Create enemie wave at random
    def create_enemy_wave(self, type="curve_left"):

        if type == "curve_right":
            self.wave.append(Curve("curve_right"))
        if type == "curve_left":
            self.wave.append(Curve("curve_left"))
        if type == "down":
            self.wave.append(Line("down"))
        if type == "right":
            self.wave.append(Heavy("right"))
        if type == "left":
            self.wave.append(Heavy("left"))
        if type == "heavy_down":
            self.wave.append(Heavy("heavy_down"))
        if type == "strafe":
            self.wave.append(Elite("strafe"))

    # Checks for collisions everywhere (>)o_o)>
    def collision_checks(self):
        # Player Lasers
        if self.player.sprite.lasers:
            for laser in self.player.sprite.lasers:
                # Enemie Collisions
                for enemie in self.wave:
                    for ship in enemie.enemies:
                        if ship.health == 1:
                            if pygame.sprite.spritecollide(laser, enemie.enemies, True):
                                laser.kill()
                        else:
                            if pygame.sprite.spritecollide(laser, enemie.enemies, False):
                                ship.health -= 1
                                laser.kill()
                if pygame.sprite.spritecollide(laser, self.boss, False):
                    self.boss.sprite.health -= 1
                    print(self.boss.sprite.health)
                    laser.kill()

        # Enemie Lasers
        for enemie in self.wave:
            if enemie.enemie_laser:
                for laser in enemie.enemie_laser:
                    # Player Collisions
                    if pygame.sprite.spritecollide(laser, self.player, False):
                        self.player.sprite.shield_absorb()
                        self.player.sprite.get_damage(50)
                        laser.kill()

        # Boss Lasers
        if self.boss.sprite.lasers:
            for laser in self.boss.sprite.lasers:
                # Boss Collisions
                if pygame.sprite.spritecollide(laser, self.player, False):
                    self.player.sprite.get_damage(50)
                    self.player.sprite.shield_absorb()
                    laser.kill()

    # Main Gameplay loop.
    def run(self):
        # Enemie Info
        for enemie in self.wave:
            enemie.enemies.draw(screen)
            enemie.enemie_laser.draw(screen)
            enemie.update()

        # Player Info
        self.player.sprite.lasers.draw(screen)
        self.player.update()
        self.player.draw(screen)
        self.collision_checks()

        # Boss Info
        if self.spawn_boss and self.boss.sprite.health > 0:
            self.boss.sprite.lasers.draw(screen)
            self.boss.update()
            self.boss.draw(screen)
        elif self.boss.sprite.health <= 0:
            # Boss is dead, clear the screen of enemies.
            for group in self.wave:
                pygame.sprite.Group.empty(group.enemies)

            # And whoosh away! (>)O_O)>
            self.player.sprite.rect.y -= 10.


if __name__ == "__main__":
    pygame.init()
    screen_width = 1450
    screen_height = 800
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    game = Game()
    formation = ["curve_left", "curve_right", "down",
                 "left", "right", "heavy_down",
                 "strafe"]

    timer = 2000
    SPAWN_WAVE = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_WAVE, timer)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # This loop will keep spawning enemies until the boss is taken out.
            if event.type == SPAWN_WAVE and game.boss.sprite.health > 0:
                if game.wave_num <= 15:
                    timer = randint(1500, 2500)
                    spawn = random.choice(formation)
                    game.create_enemy_wave(spawn)
                    game.wave_num += 1
                else:
                    timer = randint(4500, 6000)
                    spawn = random.choice(formation)
                    game.create_enemy_wave(spawn)
                    game.wave_num += 1
                    game.spawn_boss = True

        screen.fill((30, 30, 30))
        game.run()

        pygame.display.flip()
        clock.tick(60)
