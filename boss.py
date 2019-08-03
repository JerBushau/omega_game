import pygame
from random import randint, uniform
vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400
# Boss properties
BOSS_SIZE = 32
MAX_SPEED = 5
MAX_FORCE = 0.05
APPROACH_RADIUS = 120

ENEMY = pygame.image.load('assets/enemy.png')
DESTRO_ENEMY = pygame.image.load('assets/destro_enemy.png')

class Boss(pygame.sprite.Sprite):
    """Boss entity"""

    def __init__(self):
        super().__init__()
        self.hp = 100
        self.image = self.image = pygame.transform.scale(ENEMY.convert_alpha(), (60, 60))
        self.rect = self.image.get_rect()
        self.pos = vec(100, 100)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.timer = 0
        self.timer_is_active = False
        self.attack_mode = False
        self.attack_duration = randint(180, 360)


    def reset_timer(self):
        self.timer_is_active = False
        self.timer = 0


    def start_timer(self):
        self.timer_is_active = True
        if self.timer_is_active:
            self.timer += 1


    def seek_with_approach(self, target):
        self.desired = (target - self.pos)
        dist = self.desired.length()
        self.desired.normalize_ip()
        if dist < APPROACH_RADIUS:
            self.desired *= dist / APPROACH_RADIUS * MAX_SPEED
        else:
            self.desired *= MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer


    def seek_with_approach_for_duration(self, target, duration):
        """Seek target for given amount of time"""
        pass

    def draw(self, screen):
        """ draw boss specifically """
        screen.blit(self.image, self.rect)


    def update(self, target):

        self.start_timer()

        if (self.timer > self.attack_duration):
            self.reset_timer()
            self.attack_mode = not self.attack_mode

        if self.attack_mode == False:
            actual_target = (0, 10)
        else:
            actual_target = target


        self.acc = self.seek_with_approach(actual_target)
        # equations of motion
        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
        self.rect.center = self.pos

        print(self.pos)
