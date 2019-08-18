import pygame
from random import randint, uniform, choice
from components.entity import Entity
from timer import Timer
vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400

ENEMY = pygame.image.load('assets/enemy.png')
DESTRO_ENEMY = pygame.image.load('assets/destro_enemy.png')

class Boss(Entity):
    """Boss entity"""

    def __init__(self, s_pos=(-30, -30)):
        super().__init__(pygame.transform.scale(ENEMY.convert_alpha(), (60, 60)), (200, 200, 120), s_pos)
        self.hp = 600
        self.is_in_attack_mode = False
        self.attack_duration = 5000
        self.attack_timer = Timer(self.attack_duration)
        self.death_animation_timer = Timer(6000)
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.hit = False
        self.return_point = choice([(600, 100), (50, 200), (350, 90)])

    def explode(self):
        """ mark enemy as hit """

        self.hit = True
        self.max_speed = 75
        self.destruction_sound.play()
        self.death_animation_timer.start()
        self.image = pygame.transform.scale(DESTRO_ENEMY.convert_alpha(), (60, 60))


    def death_animation(self):
        """Enemy movement once marked as hit"""

        if self.death_animation_timer.is_finished():
            self.kill()
        else:
            self.acc = self.seek((self.pos.x, HEIGHT + 40))


    def update(self, dt, target):

        if not self.attack_timer.is_active:
            self.attack_timer.start()

        if self.is_in_attack_mode == True:
            self.attack_timer.set_duration(self.attack_duration / 1.8)
        else:
            self.attack_timer.set_duration(self.attack_duration)

        if self.attack_timer.is_finished():
            self.is_in_attack_mode = not self.is_in_attack_mode
            self.return_point = choice([(600, 100), (100, 200), (350, 90)])

        if self.is_in_attack_mode == False:
            actual_target = self.return_point
        else:
            actual_target = target

        self.acc = self.seek_with_approach(actual_target)

        if self.death_animation_timer.is_active and self.hit:
            self.death_animation()
        super().update(dt)
