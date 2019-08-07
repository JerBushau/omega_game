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

    def __init__(self):
        super().__init__(ENEMY, (175, 450, 120), vec(random.randint(0, 700), random.randint(0, 200)))
        self.return_pos = vec(random.choice([random.randint(-10, -5), random.randint(701, 720)]), random.randint(50, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.time = None
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.hit = False
        self.attacking = False
        self.alive = True
        self.attack_timing = random.randrange(100, 1200)
        self.attack_timer = Timer()


    def explode(self):
        """ mark enemy as hit """

        self.hit = True
        self.max_speed = 135
        self.destruction_sound.play()
        self.time = pygame.time.get_ticks()
        self.image = DESTRO_ENEMY


    def attack(self):
        """ attempt to attack the player """

        if not self.attacking:
            self.attacking = True


    def death_animation(self, current_ticks):
        """Enemy movement once marked as hit"""

        time_diff = current_ticks - self.time
        if (time_diff) < 1100:
            self.acc = self.seek((self.pos.x, HEIGHT + 40))
        else:
            self.alive = False
            self.kill()


    def update(self, dt, target):
        """ update movement and state of enemy """

        current_ticks = pygame.time.get_ticks()

        self.attack_timer.start_timer()

        if self.attack_timer.now >= self.attack_timing:
            self.attack()
            self.attack_timer.reset_timer()

        if self.pos.y > 300:
            self.attacking = False

        if self.attacking:
            self.acc = self.seek(target)
        else:
            self.acc = self.seek(self.return_pos)

        if self.time and self.hit:
            self.death_animation(current_ticks)

        super().update(dt)
