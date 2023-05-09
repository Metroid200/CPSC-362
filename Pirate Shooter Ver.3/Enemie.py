import pygame
from random import randint

screen_width = 1450
screen_height = 800

# All enemie data is located in this object.
# Can initiate different kinds of enemies and controls enemie movement


class Enemie(pygame.sprite.Sprite):
    def __init__(self, type, pattern, pos):
        super().__init__()
        file_path = "graphics/" + type + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()

        # Enemy Block, scales different sizes based on type of enemie.
        if type == "normal":
            self.image = pygame.transform.rotozoom(self.image, 180, 1.2)
            self.health = 1
        elif type == "heavy":
            self.image = pygame.transform.rotozoom(self.image, 180, 1.5)
            self.health = 5
        elif type == "elite":
            self.image = pygame.transform.rotozoom(self.image, 180, 1.4)
            self.health = 10

        self.rect = self.image.get_rect(center=pos)
        self.pattern = pattern
        self.ready = True  # Data for speed timer
        self.speed_limit = 0  # Data for speed timer
        self.speed_time = 0  # Data for speed timer
        self.speed_cooldown = 200  # Millisecond cooldown for speed shifts

    # It uhhh destorys the object when it passes the death barrier
    def destroy(self):
        if self.rect.y >= screen_height + 100:
            self.kill()
        if self.health <= 0:
            self.kill()

    # Calculates Damage
    def get_damage(self, amount):
        if self.health > 0:
            self.health -= amount
        if self.health <= 0:
            self.health = 0

    # Constraints for enemy ships that may need it.
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width:
            self.rect.right = screen_width

    # I admit, movement logic can be done better, but we too late into development
    # It will cost more to fix it, and it currently works!
    def update(self):
        self.destroy()

        # Standard movment
        if self.pattern == "curve_right" or self.pattern == "curve_left":
            speed = [2, 4, 8]  # List to increase the speed and make a curve.
            self.rect.y += speed[self.speed_limit]
            if self.pattern == "curve_right":
                self.rect.x += 15
            else:
                self.rect.x -= 15
            if self.ready and self.speed_limit < 2:  # Will increase speed
                self.ready = False
                self.speed_time = pygame.time.get_ticks()
            if not self.ready:
                current_time = pygame.time.get_ticks()
                if current_time - self.speed_time > self.speed_cooldown:
                    self.speed_limit += 1
                    self.ready = True

        # Heavy or Line of Normals move down.
        if self.pattern == "down" or self.pattern == "heavy_down":
            if self.rect.y <= 150:
                self.rect.y += 4
                self.ready = False
                self.speed_time = pygame.time.get_ticks()
            if not self.ready:
                current_time = pygame.time.get_ticks()
                if current_time - self.speed_time > 200:
                    self.rect.y += 6

        # Heavy Enemie travels Left or Right
        if self.pattern == "right":
            self.rect.x += 4
            self.rect.y += 2
        if self.pattern == "left":
            self.rect.x -= 4
            self.rect.y += 2

        # Elite Enemie Logic
        if self.pattern == "strafe":

            # Keeping the Elite ship on screen until destroyed.
            self.constraint()

            if self.rect.y <= 150:
                self.rect.y += 4

            if self.ready:
                self.strafe = randint(0, 100)
                self.ready = False
                self.speed_time = pygame.time.get_ticks()
            if not self.ready:
                current_time = pygame.time.get_ticks()
                if current_time - self.speed_time > 1000:
                    self.ready = True
            if self.strafe <= 50 and self.rect.x <= screen_width:
                self.rect.x += 5
            else:
                self.rect.x -= 5
