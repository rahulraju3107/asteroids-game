import pygame
import random
from constants import *


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        angle = random.uniform(0, 360)
        speed = random.uniform(50, PARTICLE_SPEED)
        self.velocity = pygame.Vector2(0, 1).rotate(angle) * speed
        self.lifetime = PARTICLE_LIFETIME
        self.timer = 0
        self.radius = random.uniform(1, 3)

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifetime:
            self.kill()
            return
        self.position += self.velocity * dt

    def draw(self, screen):
        alpha = 1 - (self.timer / self.lifetime)
        brightness = int(255 * alpha)
        color = (brightness, brightness, brightness)
        pygame.draw.circle(screen, color, (int(self.position.x), int(self.position.y)), int(self.radius))
