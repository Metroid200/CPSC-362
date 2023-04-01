import pygame
from Laser import Laser

# Everything related to the player characters will be located here.
# This object can create lasers and holds player controls.


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, speed):
        super().__init__()
        self.image = pygame.image.load("Graphics/peridot.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.8)
        self.rect = self.image.get_rect(midbottom=pos)
        self.speed = speed
        self.max_x_constraint = constraint  # Right edge of the screen.
        self.ready = True  # Data for laser cooldown
        self.laser_time = 0  # Data for laser cooldown
        self.laser_cooldown = 100  # Cooldown timer in milliseconds

        # Container to hold lasers fired by the player.
        self.lasers = pygame.sprite.Group()

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        elif keys[pygame.K_d]:
            self.rect.x += self.speed

        if keys[pygame.K_RCTRL] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

    # Recharge for the lasers fire rate.
    def recharge(self):
        if not self.ready:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_time >= self.laser_cooldown:
                self.ready = True

    # Keeps the player character inside the window at all times
    def constraint(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

    # Pew Pew Pew
    def shoot_laser(self):
        self.lasers.add(Laser(self.rect.center, -15, self.rect.bottom))

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
