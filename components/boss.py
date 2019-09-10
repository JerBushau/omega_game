import pygame
from random import randint, uniform, choice
from components.entity import Entity
from timer import Timer
from components.weapon import Weapon
from components.bullet import Bullet
from components.boss_health_bar import BossHealthBar
from components.energy_blast import EnergyBlast
from sprite_sheet_loader import sprite_sheet

from math import sin, cos, pi, radians

vec = pygame.math.Vector2

WIDTH = 1050
HEIGHT = 600

HEDGEHOG = pygame.image.load('assets/hedgehog.png')

class Boss(Entity):
    """Boss entity"""

    def __init__(self, s_pos=(-30, -30), *groups):
        SHEET = sprite_sheet((100,117), 'assets/hedgehog_pwr_sheet_v0.2.png')
        super().__init__(pygame.transform.scale(SHEET[0], (200, 217)), (105, 400, 120), s_pos, groups)
        self.hp = 1200
        self.sheet = SHEET
        self.sprite_animation_timer = Timer(100)
        self.sprite_animation_type = 'PWR'
        self.current_sprite_index = 0
        self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (200, 217))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.is_in_attack_mode = False
        self.attack_duration = 5000
        self.attack_timer = Timer(self.attack_duration)
        self.destruction_sound = pygame.mixer.Sound('assets/sounds/enemy_hit.ogg')
        self.hit = False
        self.possible_points = [(200, 150), (505, 300), (800, 175), (525, 150)]
        self.point = 0
        self.return_point = self.possible_points[self.point]
        self.energy_blast_timer = Timer(100)
        self.bullets = pygame.sprite.Group()
        self.hit_timer = Timer(175)
        self.is_tinted = False
        self.current_angle = 0
        self.health_bar = BossHealthBar(self.hp)
        self.blast_p3 = 0
        self.blast_p3_points = [i for i in range(20, 36, 10)]

        self.sprite_animation_timer.start_repeating()


    def direction_from_angle(self, angle):
        return vec(cos(angle), sin(angle))

    def collision_detected(self):
        self.is_tinted = True
        if not self.hit_timer.is_active:
            self.hit_timer.start()

    def explode(self):
        """ mark enemy as hit """

        self.hit = True
        self.max_speed = 75
        self.destruction_sound.play()

    def start_energy_blast(self):
        self.energy_blast_timer.start()

    def death_movement(self):
        """Boss movement once marked as hit"""
        self.acc = self.seek((self.pos.x, HEIGHT + 100))

    def sprite_animation(self):
        distance_from_return_point = self.pos - self.return_point;
        cap = 4
        start = 0

        if self.hit and self.sprite_animation_type == 'PWR':
            self.sprite_animation_type = 'DEATH'
            self.current_sprite_index = start
            self.sheet = sprite_sheet((100, 117), 'assets/hedgehog_sheet.png')
            self.sprite_animation_timer.set_duration(500)

        # self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (200, 217))
        # self.mask = pygame.mask.from_surface(self.image)

        if self.is_tinted and not self.hit:
            self.image.fill((7, 7, 7, 10), special_flags=pygame.BLEND_RGB_ADD)


        # uncomment to stop animation when blasting
        if distance_from_return_point.length() < 40 and not self.hit:
            cap = 7
            start = 5
            self.sprite_animation_timer.set_duration(75)
        else:
            cap = 4
            start = 0

        if self.sprite_animation_timer.is_finished():
            self.current_sprite_index+=1

            if self.current_sprite_index > cap:
                if self.hit:
                    self.current_sprite_index = 4
                else:
                    self.current_sprite_index = start


            self.image = pygame.transform.scale(self.sheet[self.current_sprite_index], (200, 217))
            self.mask = pygame.mask.from_surface(self.image)


    def update(self, dt, target):
        self.sprite_animation()

        distance_from_return_point = self.pos - self.return_point;

        if self.hit_timer.is_finished():
            self.is_tinted = False

        if (distance_from_return_point.length() < 40
            and not self.energy_blast_timer.is_active):
            self.start_energy_blast()

        if self.energy_blast_timer.is_finished() and not self.hit and distance_from_return_point.length() < 100:

            # if self.point == 3:
            #     self.energy_blast_timer.set_duration(65)
            #     self.current_angle += 16
            #     if self.current_angle > 360:
            #         self.current_angle = 0
            #     # spiral blast
            #     blast_direction = self.direction_from_angle(radians(self.current_angle))
            #     blast_target = blast_direction.normalize()*self.max_speed
            #     EnergyBlast(self.rect.center, blast_target, False, self.bullets)

            # if self.point == 3:
            #     # circular blast
            #     self.energy_blast_timer.set_duration(1500)
            #     for i in range(0, 361, 20):
            #         blast_direction = self.direction_from_angle(radians(i))
            #         blast_target = blast_direction.normalize()*self.max_speed
            #         EnergyBlast(self.rect.center, blast_target, False, self.bullets)

            if self.point == 1:
                self.energy_blast_timer.set_duration(65)
                self.current_angle += 3
                if self.current_angle > 360:
                    self.current_angle = 0
                # spiral blast
                blast_direction = self.direction_from_angle(self.current_angle)
                blast_target = blast_direction.normalize()*self.max_speed
                EnergyBlast(self.rect.center, blast_target, False, self.bullets)

            elif self.point == 3:
                # circular blast extreme
                self.energy_blast_timer.set_duration(300)
                for i in range(0, 181, self.blast_p3_points[self.blast_p3]):
                    blast_direction = self.direction_from_angle(radians(i))
                    blast_target = blast_direction.normalize()*self.max_speed
                    EnergyBlast(self.rect.center, blast_target, False, self.bullets)

                self.blast_p3+=1
                if self.blast_p3 >= len(self.blast_p3_points):
                    self.blast_p3 = 0

            else:
                self.energy_blast_timer.set_duration(100)
                blast_target = target
                EnergyBlast(self.rect.center, blast_target, True, self.bullets)


            self.is_in_attack_mode = True
            if not self.attack_timer.is_active:
                self.attack_timer.start()

        if self.attack_timer.is_finished():
            self.is_in_attack_mode = False
            self.point += 1
            if self.point == len(self.possible_points):
                self.point = 0
            self.return_point = self.possible_points[self.point]

        actual_target = self.return_point

        self.acc = self.seek_with_approach(actual_target)

        if self.hit:
            self.death_movement()

        self.bullets.update(dt)
        self.health_bar.update(self.hp)

        super().update(dt)

        if self.rect.center[1] > HEIGHT + 65:
            self.kill()
