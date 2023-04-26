import pygame

# Everything related to laser objects go here.
# Initiates laser color, speed, and direction.


class Laser(pygame.sprite.Sprite):
    def __init__(self, pos, speed, screen_height, rotation=90, color="green_laser"):
        super().__init__()
        self.color = "Graphics/" + color + ".png"
        self.image = pygame.image.load(self.color).convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, rotation, 0.3)
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.height_y_constraint = screen_height  # Screen Edge aka the bottom.

    # Destroys any lasers outside the screen.
    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.height_y_constraint + 50:
            self.kill()

    def update(self):
        self.rect.y += self.speed
        self.destroy()
