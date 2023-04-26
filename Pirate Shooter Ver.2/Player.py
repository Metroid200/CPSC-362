import pygame
from Laser import Laser

screen_width = 1450
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Everything related to the player characters will be located here.
# This object can create lasers and holds player controls.


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, constraint, name):
        super().__init__()
        file_name = "Graphics/" + name + ".png"
        self.image = pygame.image.load(file_name).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 0.7)
        self.rect = self.image.get_rect(midbottom=pos)
        self.max_x_constraint = constraint  # Right edge of the screen.

        # Initiating Base Stats
        if name == "tourmaline":
            self.max_hp = 1500
            self.max_shield = 1000
            self.regen = 0.5
            self.speed = 7
            self.laser_cooldown = 300
        elif name == "peridot":
            self.max_hp = 900
            self.max_shield = 500
            self.regen = 0.3
            self.speed = 10
            self.laser_cooldown = 150
        elif name == "tanzanite":
            self.max_hp = 500
            self.max_shield = 300
            self.regen = 0.2
            self.speed = 17
            self.laser_cooldown = 75

        # Health Bar Information
        self.current_hp = self.max_hp
        self.target_hp = self.max_hp
        self.hp_bar_length = 400
        self.hp_change_speed = 5
        self.hp_ratio = self.max_hp / self.hp_bar_length

        # Shield Bar Information
        self.current_shield = self.max_shield
        self.target_shield = self.max_shield
        self.shield_bar_length = 400
        self.shield_change_speed = 1
        self.shield_ratio = self.max_shield / self.shield_bar_length

        # Laser Information
        self.ready = True  # Data for laser cooldown
        self.laser_time = 0  # Data for laser cooldown
        self.lasers = pygame.sprite.Group()  # Container for lasers

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        elif keys[pygame.K_d]:
            self.rect.x += self.speed

        if pygame.mouse.get_pressed()[0] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

        if pygame.mouse.get_pressed()[2]:
            self.shield_energy(2)

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

    # Damage the Player
    def get_damage(self, amount):
        if self.current_hp > 0:
            self.current_hp -= amount
        if self.current_hp <= 0:
            self.current_hp = 0

    # Player Health bar
    def health(self):
        transition_width = 0

        if self.target_hp > self.current_hp:
            self.target_hp -= self.hp_change_speed
            transition_width = int(
                (self.target_hp - self.current_hp)/self.hp_ratio)

        hp_bar_rect = pygame.Rect(10, 15, self.current_hp/self.hp_ratio, 25)
        transition_rect = pygame.Rect(
            hp_bar_rect.right, 15, transition_width, 25)

        pygame.draw.rect(screen, (255, 0, 0), hp_bar_rect)
        pygame.draw.rect(screen, (250, 200, 0), transition_rect)
        pygame.draw.rect(screen, (255, 255, 255),
                         (10, 15, self.hp_bar_length, 25), 4)

    # Drains the shield
    def shield_energy(self, amount):
        if self.current_shield > 0:
            self.current_shield -= amount
        if self.current_shield <= 0:
            self.current_shield = 0

    # Shield Regeneration
    def shield_regen(self):
        if self.current_shield < self.max_shield:
            self.current_shield += self.regen
            self.target_shield += self.regen
        if self.current_shield >= self.max_shield:
            self.current_shield = self.max_shield
            self.target_shield = self.max_shield

    # Player Shield Bar
    def shield(self):
        transition_width = 0

        if self.target_shield > self.current_shield:
            self.target_shield -= self.shield_change_speed
            transition_width = int(
                (self.target_shield - self.current_shield)/self.shield_ratio)

        shield_bar_rect = pygame.Rect(
            10, 40, self.current_shield/self.shield_ratio, 25)
        transition_rect = pygame.Rect(
            shield_bar_rect.right, 40, transition_width, 25)

        pygame.draw.rect(screen, (0, 0, 255), shield_bar_rect)
        pygame.draw.rect(screen, (255, 0, 255), transition_rect)
        pygame.draw.rect(screen, (255, 255, 255),
                         (10, 40, self.shield_bar_length, 25), 4)

    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
        self.health()
        self.shield()
        self.shield_regen()
