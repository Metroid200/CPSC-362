import pygame
from Laser import Laser
import random
from random import randint

screen_width = 1450
screen_height = 800

# All logic dealing with the boss is located here.
# This object will create a boss enemie and laser objects.


class Boss(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("Graphics/boss.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 180, 1)
        self.rect = self.image.get_rect(center=pos)
        self.speed = 8  # Default movement speed
        self.switch = "left"  # Default direction movement
        self.health = 500   # Default Health Value

        # Laser Information
        self.ready = True  # Data for laser cooldown
        self.timer = randint(0, 5)  # Timer for Laser Fire Rate
        self.laser_time = 0  # Data for laser cooldown switch
        self.laser_cooldown = 3000
        self.lasers = pygame.sprite.Group()  # Container for lasers
        self.fire_type = "dual"  # Boss Default Rate of Fire

    # Keep boss on the screen
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width:
            self.rect.right = screen_width

    # Boss will die at 0 health
    def destroy(self):
        if self.health <= 0:
            self.kill()

    # Recharge for the lasers fire rate style
    def shoot_timer(self):
        self.timer -= 1
        if self.timer <= 0:
            if self.fire_type == "dual" or self.fire_type == "spread":
                self.timer = randint(0, 25)
                return True
            if self.fire_type == "rapid_dual" or self.fire_type == "rapid_spread":
                self.timer = randint(0, 10)
                return True
        return False

    # Method chooses the laser type at random.
    def laser_type(self):
        if self.ready:
            self.ready = False
            self.laser_time = pygame.time.get_ticks()
            fire = ["spread", "rapid_spread", "dual", "rapid_dual"]
            self.fire_type = random.choice(fire)
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    # Method controls all the shooting
    def boss_shoot(self):
        if self.shoot_timer():
            if self.fire_type == "dual" or self.fire_type == "rapid_dual":
                temp = list(self.rect.center)
                temp[0] = temp[0] - 25
                left_laser = tuple(temp)

                temp = list(self.rect.center)
                temp[0] = temp[0] + 25
                right_laser = tuple(temp)

                laser = Laser(
                    left_laser, 12, screen_height, 270, "red_laser")
                self.lasers.add(laser)
                laser = Laser(
                    right_laser, 12, screen_height, 270, "red_laser")
                self.lasers.add(laser)

            if self.fire_type == "spread" or self.fire_type == "rapid_spread":
                ammo = [250, 270, 290]

                for lasers in range(3):
                    laser = Laser(
                        self.rect.center, 12, screen_height, ammo[lasers], "red_laser")
                    self.lasers.add(laser)

    # Logic for boss movement
    def boss_movement(self):
        if self.rect.y <= 75:
            self.rect.y += self.speed

        if self.switch == "left":
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.switch = "right"
                self.speed = randint(4, 10)
        if self.switch == "right":
            self.rect.x += self.speed
            if self.rect.right >= screen_width:
                self.switch = "left"
                self.speed = randint(4, 10)

    # It just updates like for realz
    def update(self):
        self.constraint()
        self.boss_shoot()
        self.laser_type()
        self.boss_movement()
        self.lasers.update()
        self.destroy()
