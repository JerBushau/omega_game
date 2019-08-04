import pygame
from random import randint, uniform

vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400

class Entity(pygame.sprite.Sprite):
    """The base class for any on screen object with movement"""

    def __init__(self, img, movement_options=(200, 100, 120), starting_pos=(100, 100)):
        super().__init__()
        self.image = img
        self.rect = self.image.get_rect()
        self.max_speed = movement_options[0]
        self.max_force = movement_options[1]
        self.approach_radius = movement_options[2]
        self.pos = vec(starting_pos)
        self.vel = vec(0, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        


    def seek(self, target):
        self.desired = (target - self.pos).normalize() * self.max_speed
        steer = (self.desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer


    def seek_with_approach(self, target):
        self.desired = (target - self.pos)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < self.approach_radius:
            self.desired *= dist / self.approach_radius * self.max_speed
        else:
            self.desired *= self.max_speed
        steer = (self.desired - self.vel)
        if steer.length() > self.max_force:
            steer.scale_to_length(self.max_force)
        return steer


    def update(self, delta_time):
        # equations of motion
        self.vel += self.acc * delta_time
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)
        self.pos += self.vel * delta_time + 0.5 * self.acc * delta_time**2
        if self.pos.x > WIDTH:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT + 50:
            self.pos.y = HEIGHT + 50
        elif self.pos.y < -50:
            self.pos.y = -50
        self.rect.center = self.pos
