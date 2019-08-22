import pygame
import random
from components.entity import Entity
from timer import Timer

vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400
ENEMY = pygame.image.load('assets/enemy.png')
DESTRO_ENEMY = pygame.image.load('assets/destro_enemy.png')

class Enemy(Entity):
    """ represents the enemy """

    def __init__(self, *groups):
        super().__init__(ENEMY, (175, 550, 120), vec(random.randint(0, 700), random.randint(0, 200)), groups)
        self.return_pos = vec(random.choice([random.randint(-10, -5), random.randint(701, 720)]), random.randint(50, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.hit = False
        self.attacking = False
        self.death_animation_timer = Timer(1100)
        self.attack_timing = random.randrange(2000, 6000)
        self.attack_timer = Timer(self.attack_timing)


    def explode(self):
        """ mark enemy as hit """

        self.hit = True
        self.max_speed = 135
        self.destruction_sound.play()
        self.death_animation_timer.start()
        self.image = DESTRO_ENEMY


    def attack(self):
        """ attempt to attack the player """

        if not self.attacking:
            self.attacking = True


    def death_animation(self):
        """Enemy movement once marked as hit"""

        if self.death_animation_timer.is_finished():
            self.kill()
        else:
            self.acc = self.seek((self.pos.x, HEIGHT + 40))


    def update(self, dt, target):
        """ update movement and state of enemy """

        if not self.attack_timer.is_active:
            self.attack_timer.start()

        if self.attack_timer.is_finished():
            self.attacking = not self.attacking

        if self.pos.y > 360:
            self.attacking = False
            self.attack_timer.reset()

        if self.attacking:
            self.acc = self.seek(target)
        else:
            self.acc = self.seek(self.return_pos)

        if self.death_animation_timer.is_active and self.hit:
            self.death_animation()

        super().update(dt)
