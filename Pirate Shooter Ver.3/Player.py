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
        self.max_firepower = 0

        # Shield image
        self.shield_image = pygame.image.load(
            "Graphics/shield.png").convert_alpha()
        self.shield_image = pygame.transform.rotozoom(
            self.shield_image, 0, 0.23)
        self.shield_rect = self.shield_image.get_rect(
            midbottom=(screen_width/2, screen_height))

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
            self.regen = 0.7
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
        self.shield_active = False
        self.shield_overheat = False
        self.shield_power = 0
        self.shield_stage = 0
        self.shield_color = 255
        self.shield_color_2 = 255

        # Laser Information
        self.ready = True  # Data for laser cooldown
        self.laser_time = 0  # Data for laser cooldown
        self.lasers = pygame.sprite.Group()  # Container for lasers

    # It uhhh gets the input. For like controlling the player and stuff
    def get_input(self):
        keys = pygame.key.get_pressed()

        # Move Left
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            self.shield_rect.x -= self.speed
        # Move Right
        elif keys[pygame.K_d]:
            self.rect.x += self.speed
            self.shield_rect.x += self.speed

        # Pew Pew Pew Pew
        if pygame.mouse.get_pressed()[0] and self.ready:
            self.shoot_laser()
            self.ready = False
            self.laser_time = pygame.time.get_ticks()

        # BBZZZzzzzzttttttttbbzzz
        if pygame.mouse.get_pressed()[2] and not self.shield_overheat:
            self.shield_active = True
            self.shield_energy(2)
            screen.blit(self.shield_image, self.shield_rect)
        else:
            self.shield_active = False

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

        if self.shield_rect.left <= -10:
            self.shield_rect.left = -10

        if self.rect.right >= self.max_x_constraint:
            self.rect.right = self.max_x_constraint

        if self.shield_rect.right >= self.max_x_constraint + 10:
            self.shield_rect.right = self.max_x_constraint + 10

    # Pew Pew Pew
    def shoot_laser(self):
        if self.shield_stage == 0:
            self.lasers.add(Laser(self.rect.center, -15, self.rect.bottom))

        if self.shield_stage == 1:

            temp = list(self.rect.center)
            temp[0] = temp[0] - 25
            left_laser = tuple(temp)

            temp = list(self.rect.center)
            temp[0] = temp[0] + 25
            right_laser = tuple(temp)

            self.lasers.add(Laser(
                right_laser, -15, self.rect.bottom, 90, "blue_laser"))
            self.lasers.add(Laser(
                left_laser, -15, self.rect.bottom, 90, "blue_laser"))

        if self.shield_stage == 2:
            ammo = [100, 90, 80]

            for lasers in range(3):
                laser = Laser(
                    self.rect.center, -15, screen_height, ammo[lasers], "purple_laser")
                self.lasers.add(laser)

        if self.shield_stage >= 3:
            ammo = [100, 95, 90, 85, 80]

            if self.max_firepower > 0:
                for lasers in range(5):
                    laser = Laser(
                        self.rect.center, -20, screen_height, ammo[lasers], "pink_laser")
                    self.lasers.add(laser)
                self.max_firepower -= 1
            else:
                self.shield_stage = 2
                self.shield_color_2 = 200

    # Damage the Player
    def get_damage(self, amount):
        if not self.shield_active:
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
            self.shield_overheat = True

    # Shield Regeneration
    def shield_regen(self):
        if self.current_shield < self.max_shield:
            self.current_shield += self.regen
            self.target_shield += self.regen
        if self.current_shield >= self.max_shield:
            self.current_shield = self.max_shield
            self.target_shield = self.max_shield
        if self.shield_overheat:
            if self.current_shield >= 100:
                self.shield_overheat = False

    # Player Shield Bar its just the bar mechanics
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

        absorb_bar_rect = pygame.Rect(10, 65, self.shield_power, 20)
        pygame.draw.rect(screen, (0, 255, 150), absorb_bar_rect)
        pygame.draw.rect(screen, (255, self.shield_color_2,
                         self.shield_color), (10, 65, 200, 20), 4)

    # Calculates the amount of damaget he player has absorb
    def shield_absorb(self):
        if self.shield_active and self.shield_power <= 200:
            if self.shield_stage == 1:
                self.shield_power += 10
            if self.shield_stage == 2:
                self.shield_power += 5
            else:
                self.shield_power += 20
        if self.shield_power >= 200:
            self.shield_power = 0
            self.shield_stage += 1
            if self.shield_stage >= 3:
                self.max_firepower = 20
        if self.shield_stage == 1:
            self.shield_color = 0
        elif self.shield_stage == 3:
            self.shield_color_2 = 100

    # Still just updates.
    def update(self):
        self.get_input()
        self.constraint()
        self.recharge()
        self.lasers.update()
        self.health()
        self.shield()
        self.shield_regen()
