import pygame
from constants import *
from circleshape import CircleShape

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt
        if (self.position.x < -SHOT_RADIUS or self.position.x > SCREEN_WIDTH + SHOT_RADIUS
                or self.position.y < -SHOT_RADIUS or self.position.y > SCREEN_HEIGHT + SHOT_RADIUS):
            self.kill()
