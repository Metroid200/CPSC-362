import pygame

# All enemie data is located in this object.
# Can initiate different kinds of enemies and controls enemie movement


class Enemie(pygame.sprite.Sprite):
    def __init__(self, type, pattern, pos):
        super().__init__()
        file_path = "graphics/" + type + ".png"
        self.image = pygame.image.load(file_path).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 180, 1.4)
        self.rect = self.image.get_rect(center=pos)
        self.pattern = pattern
        self.ready = True  # Data for speed timer
        self.speed_limit = 0  # Data for speed timer
        self.speed_time = 0  # Data for speed timer
        self.speed_cooldown = 200  # Millisecond cooldown for speed shifts

    def update(self):
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
