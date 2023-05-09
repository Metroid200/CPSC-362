import pygame
from random import choice, randint
from Laser import Laser
from Enemie import Enemie

screen_width = 1450
screen_height = 800
# Enemie pattern logic is all created in this py file.
# Every object in this file will create enemies and enemie lasers.

# The Curve object can spawn enemies which will curve downward and shoot randomly.
# Curve can spawn enemies from the right or from the left by passing a string.


class Curve(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.ready = True
        self.direction = direction
        self.limit = 0  # Limit varible is later adjusted for max enemies.
        self.enemie_time = 0  # Captures the time an enemie spawns
        self.enemie_cooldown = 100  # Time in Milisections for next enemie spawn
        self.timer = randint(0, 25)  # Timer for random laser fire

        # Container that holds enemie and laser objects.
        self.enemies = pygame.sprite.Group()
        self.enemie_laser = pygame.sprite.Group()

    # Timer delays the spawn of the next enemie based on the Cooldown variable.
    def delay(self):
        if self.direction == "curve_right":
            if self.ready and self.limit < 8:
                self.spawn((-100, 100))
                self.ready = False
                self.enemie_time = pygame.time.get_ticks()
            if not self.ready:
                current_time = pygame.time.get_ticks()
                if current_time - self.enemie_time > self.enemie_cooldown:
                    self.limit += 1
                    self.ready = True
        if self.direction == "curve_left":
            if self.ready and self.limit < 8:
                self.spawn((screen_width + 100, 100))
                self.ready = False
                self.enemie_time = pygame.time.get_ticks()
            if not self.ready:
                current_time = pygame.time.get_ticks()
                if current_time - self.enemie_time > self.enemie_cooldown:
                    self.limit += 1
                    self.ready = True

    # Random Enemie will shoot randomly
    def enemie_shoot(self):
        if self.enemies.sprites() and self.shoot_timer():
            random_enemy = choice(self.enemies.sprites())
            laser = Laser(
                random_enemy.rect.center, 12, screen_height, -90, "red_laser")
            self.enemie_laser.add(laser)

    # Timer to fire lasers randomly. Rate can be adjusted by changing random index.
    def shoot_timer(self):
        if self.enemies.sprites():
            self.timer -= 1
            if self.timer <= 0:
                self.timer = randint(0, 25)
                return True
            return False

    # Just spawns an enemie
    def spawn(self, pos):
        self.enemies.add(Enemie("normal", self.direction, pos))

    def damage(self, amount):
        for enemie in self.enemies:
            enemie.health -= amount

    def update(self):
        self.delay()
        self.enemie_shoot()
        self.enemie_laser.update()
        self.enemies.update()


# The Line object summons enemies in a line formation and travel downward.
class Line(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.ready = True
        self.direction = direction
        self.limit = 8  # Limit varible is later adjusted for max enemies.
        self.enemie_time = 0  # Captures the time an enemie spawns
        self.enemie_cooldown = 100  # Time in Milisections for next enemie spawn
        self.timer = randint(0, 25)  # Timer for random laser fire

        # Container that holds enemie and laser objects.
        self.enemies = pygame.sprite.Group()
        self.enemie_laser = pygame.sprite.Group()

    def delay(self):
        x_offset = -375
        for enemie in range(self.limit):
            self.spawn(((screen_width/2) + x_offset, -100))
            x_offset += 100
        self.ready = False

    # Random Enemie will shoot randomly

    def enemie_shoot(self):
        if self.enemies.sprites() and self.shoot_timer():
            random_enemy = choice(self.enemies.sprites())
            laser = Laser(
                random_enemy.rect.center, 12, screen_height, -90, "red_laser")
            self.enemie_laser.add(laser)

    # Timer to fire lasers randomly. Rate can be adjusted by changing random index.
    def shoot_timer(self):
        if self.enemies.sprites():
            self.timer -= 1
            if self.timer <= 0:
                self.timer = randint(0, 25)
                return True
            return False

    # Just spawns an enemie
    def spawn(self, pos):
        self.enemies.add(Enemie("normal", self.direction, pos))

    def update(self):
        if self.ready == True:
            self.delay()
        self.enemie_shoot()
        self.enemie_laser.update()
        self.enemies.update()


# The Heavy Object can spawn from left,right, or top of the screen.
# They have a larger health pool, and shotgun type laser.
class Heavy(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.ready = True
        self.direction = direction
        self.limit = 0  # Limit varible is later adjusted for max enemies.
        self.enemie_time = 0  # Captures the time an enemie spawns
        self.enemie_cooldown = 100  # Time in Milisections for next enemie spawn
        self.timer = randint(0, 25)  # Timer for random laser fire

        # Container that holds enemie and laser objects.
        self.enemies = pygame.sprite.Group()
        self.enemie_laser = pygame.sprite.Group()

    # Timer delays the spawn of the next enemie based on the Cooldown variable.
    def delay(self):
        if self.direction == "right":
            self.spawn((-100, 0))
            self.limit += 1
        if self.direction == "left":
            self.spawn((screen_width + 100, 0))
            self.limit += 1
        if self.direction == "heavy_down":
            self.spawn((screen_width/2, -100))
            self.limit += 1

    # Random Enemie will shoot randomly
    def enemie_shoot(self):
        if self.enemies.sprites() and self.shoot_timer():
            random_enemy = choice(self.enemies.sprites())
            ammo = [250, 270, 290]

            for lasers in range(3):
                laser = Laser(
                    random_enemy.rect.center, 12, screen_height, ammo[lasers], "red_laser")
                self.enemie_laser.add(laser)

    # Timer to fire lasers randomly. Rate can be adjusted by changing random index.
    def shoot_timer(self):
        if self.enemies.sprites():
            self.timer -= 1
            if self.timer <= 0:
                self.timer = randint(0, 100)
                return True
            return False

    # Just spawns an enemie
    def spawn(self, pos):
        self.enemies.add(Enemie("heavy", self.direction, pos))

    def update(self):
        if self.limit < 1:
            self.delay()
        self.enemie_shoot()
        self.enemie_laser.update()
        self.enemies.update()


# Elite enemies will always spawn from the top, and will not leave the screen until it is shot down
# They have largest health pool, and have dual laser fire.
class Elite(pygame.sprite.Sprite):
    def __init__(self, direction):
        super().__init__()
        self.ready = True
        self.direction = direction
        self.limit = 0  # Limit varible is later adjusted for max enemies.
        self.enemie_time = 0  # Captures the time an enemie spawns
        self.enemie_cooldown = 100  # Time in Milisections for next enemie spawn
        self.timer = randint(0, 25)  # Timer for random laser fire

        # Container that holds enemie and laser objects.
        self.enemies = pygame.sprite.Group()
        self.enemie_laser = pygame.sprite.Group()

    # Timer delays the spawn of the next enemie based on the Cooldown variable.
    def delay(self):
        if self.direction == "strafe":
            self.spawn(((screen_width/2), -100))
            self.limit += 1

    # Random Enemie will shoot randomly
    def enemie_shoot(self):
        if self.enemies.sprites() and self.shoot_timer():
            random_enemy = choice(self.enemies.sprites())

            temp = list(random_enemy.rect.center)
            temp[0] = temp[0] - 25
            left_laser = tuple(temp)

            temp = list(random_enemy.rect.center)
            temp[0] = temp[0] + 25
            right_laser = tuple(temp)

            laser = Laser(
                left_laser, 12, screen_height, 270, "red_laser")
            self.enemie_laser.add(laser)
            laser = Laser(
                right_laser, 12, screen_height, 270, "red_laser")
            self.enemie_laser.add(laser)

    # Timer to fire lasers randomly. Rate can be adjusted by changing random index.
    def shoot_timer(self):
        if self.enemies.sprites():
            self.timer -= 1
            if self.timer <= 0:
                self.timer = randint(0, 100)
                return True
            return False

    # Just spawns an enemie
    def spawn(self, pos):
        self.enemies.add(Enemie("elite", self.direction, pos))

    def update(self):
        if self.limit < 1:
            self.delay()
        self.enemie_shoot()
        self.enemie_laser.update()
        self.enemies.update()
