import pygame
from random import randint, uniform, choice
from components.entity import Entity
from timer import Timer
from components.weapon import Weapon
from components.bullet import Bullet
from components.energy_blast import EnergyBlast
from sprite_sheet_loader import sprite_sheet

vec = pygame.math.Vector2

WIDTH = 700
HEIGHT = 400

HEDGEHOG = pygame.image.load('assets/space-hedgehog.png')

class Boss(Entity):
    """Boss entity"""

    def __init__(self, s_pos=(-30, -30), *groups):
        super().__init__(pygame.transform.scale(HEDGEHOG.convert_alpha(), (80, 80)), (105, 400, 120), s_pos, groups)
        self.hp = 600
        self.sheet = sprite_sheet((32,32), 'assets/space_hedgehog_sheet.png');
        self.sprite_animation_timer = Timer(120)
        self.current_sprite_index = 0
        self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (80, 80))
        self.is_in_attack_mode = False
        self.attack_duration = 5000
        self.attack_timer = Timer(self.attack_duration)
        self.death_animation_timer = Timer(6000)
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.hit = False
        self.possible_points = [(350, 70), (200, 80), (350, 100), (500, 70)]
        self.point = 0
        self.return_point = self.possible_points[self.point]
        self.energy_blast_timer = Timer(100)
        self.bullets = pygame.sprite.Group()

        self.sprite_animation_timer.start_repeating()

    def explode(self):
        """ mark enemy as hit """

        self.hit = True
        self.max_speed = 75
        self.destruction_sound.play()
        self.death_animation_timer.start()


    def start_energy_blast(self):
        print('started')
        self.energy_blast_timer.start()


    def death_movement(self):
        """Enemy movement once marked as hit"""

        if self.death_animation_timer.is_finished():
            self.kill()
        else:
            self.acc = self.seek((self.pos.x, HEIGHT + 40))


    def sprite_animation(self):
        cap = 4
        if self.hit:
            self.sheet = sprite_sheet((32, 32), 'assets/dedgehog_sheet.png')
            self.sprite_animation_timer.set_duration(275)
            cap = 12
        if self.sprite_animation_timer.is_finished() and self.current_sprite_index < cap:
            self.current_sprite_index+=1
            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (80, 80))
            if self.current_sprite_index == cap:
                if cap == 12:
                    self.current_sprite_index = 9
                else:
                    self.current_sprite_index = 0


    def update(self, dt, target):
        self.sprite_animation()
        self.bullets.update(dt)
        distance_from_return_point = self.pos - self.return_point;

        if (distance_from_return_point.length() < 40
            and not self.energy_blast_timer.is_active):
            self.start_energy_blast()

        if self.energy_blast_timer.is_finished() and not self.hit and distance_from_return_point.length() < 100:
            print('blast!')
            EnergyBlast(self.rect.center, target, self.bullets)
            self.is_in_attack_mode = True
            if not self.attack_timer.is_active:
                self.attack_timer.start()

        if self.is_in_attack_mode == True:
            self.attack_timer.set_duration(self.attack_duration / 1.8)
        else:
            self.attack_timer.set_duration(self.attack_duration)

        if self.attack_timer.is_finished():
            self.is_in_attack_mode = False
            self.point += 1
            if self.point == 4:
                self.point = 0
            self.return_point = self.possible_points[self.point]

        actual_target = self.return_point

        self.acc = self.seek_with_approach(actual_target)

        if self.death_animation_timer.is_active and self.hit:
            self.death_movement()
        super().update(dt)
