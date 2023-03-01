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

# Enemies
NORMAL_ENEMY = pygame.image.load(os.path.join("Assets", "Normal_Enemy.png"))
NORMAL_ENEMY = pygame.transform.scale(NORMAL_ENEMY, (100, 100))

# Bullets
RED_LASER = pygame.image.load(os.path.join("Assets", "Red_Laser.png"))
GREEN_LASER = pygame.image.load(os.path.join("Assets", "Green_Laser.png"))
GREEN_LASER = pygame.transform.scale(GREEN_LASER, (50, 25))
GREEN_LASER = pygame.transform.rotate(GREEN_LASER, 90)


# Background Layer
BG = pygame.image.load(os.path.join("Assets", "Purple_Space.jpg"))
BG = pygame.transform.scale(BG, (WIDTH, HEIGHT))


class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity):
        self.y += velocity

    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Ship:
    COOLDOWN = 10

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

     # Currently Draws the hitbox
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = MAIN_SHIP
        self.laser_img = GREEN_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move_lasers(self, velocity, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(velocity)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for object in objs:
                    if laser.collision(object):
                        objs.remove(object)
                        self.lasers.remove(laser)


class Enemy(Ship):
    ENEMY_TYPE = {
        "normal": (NORMAL_ENEMY, RED_LASER)
    }

    def __init__(self, x, y, type, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.ENEMY_TYPE[type]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity):
        self.y += velocity


def collide(obj_1, obj_2):
    offset_x = obj_2.x - obj_1.x
    offset_y = obj_2.y - obj_1.y
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 1
    lives = 3
    main_font = pygame.font.SysFont("comicsans", 50)

    # Enemy Data
    enemies = []
    wave_length = 5
    enemy_velocity = 5
    enemy_laser = 10

    # Test Ship creation and starting location.
    player = Player(750, 650)
    player_velocity = 10
    player_laser = -10

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

        for enemy in enemies:
            enemy.draw(WINDOW)

        player.draw(WINDOW)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()

        if len(enemies) == 0:
            for enemy in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100),
                              random.randrange(-500, -100),
                              random.choice(["normal"]))
                enemies.append(enemy)

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
        if pygame.mouse.get_pressed()[0]:
            player.shoot()

        # Enemy A.I
        for enemy in enemies:
            enemy.move(enemy_velocity)
            enemy.move_lasers(enemy_laser, player)

        player.move_lasers(player_laser, enemies)


main()
