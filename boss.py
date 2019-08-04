import pygame
from random import randint, uniform
from entity import Entity
from timer import Timer
vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400

ENEMY = pygame.image.load('assets/enemy.png')
DESTRO_ENEMY = pygame.image.load('assets/destro_enemy.png')

class Boss(Entity):
    """Boss entity"""

    def __init__(self):
        super().__init__(pygame.transform.scale(ENEMY.convert_alpha(), (60, 60)), (200, 100, 120))
        self.hp = 600
        self.attack_timer = Timer()
        self.is_in_attack_mode = False
        self.attack_duration = randint(180, 360)
        self.time = None
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.hit = False


    def explode(self):
        """ mark enemy as hit """

        self.hit = True
        self.max_speed = 75
        self.destruction_sound.play()
        self.time = pygame.time.get_ticks()
        self.image = pygame.transform.scale(DESTRO_ENEMY.convert_alpha(), (60, 60))


    def death_animation(self):
        """Enemy movement once marked as hit"""

        time_diff = pygame.time.get_ticks() - self.time
        if (time_diff) < 6000:
            self.acc = self.seek((self.pos.x, HEIGHT + 40))
        else:
            self.alive = False
            self.kill()


    def draw(self, screen):
        """ draw boss specifically """
        screen.blit(self.image, self.rect)


    def update(self, dt, target):

        self.attack_timer.start_timer()
    
        if self.is_in_attack_mode == True:
            duration = self.attack_duration / 2
        else:
            duration = self.attack_duration

        if (self.attack_timer.now > self.attack_duration):
            self.attack_timer.reset_timer()
            self.is_in_attack_mode = not self.is_in_attack_mode

        if self.is_in_attack_mode == False:
            actual_target = (randint(0, 700), randint(0, 100))
        else:
            actual_target = target

        self.acc = self.seek_with_approach(actual_target)

        if self.time and self.hit:
            self.death_animation()
        # equations of motion
        super().update(dt)
