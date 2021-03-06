import pygame
import random
from math import floor
from components.background import Background
from components.boss import Boss
from components.enemy import Enemy
from components.player import Player
from components.bullet import Bullet
from components.hud import Hud
from components.wobble import Wobble_shot
from components.asteroid import Asteroid, Asteroid_group
from components.chain_lightning import Chain_Lightning
from components.crosshair import Crosshair
from components.on_screen_dmg import OnScreenDmg
from components.falling_mssg import FallingMssg
from score import scores
from gamestate import GameState
import parallax
from components.signaly import signaly

BACKGROUND = 'assets/background1.png'
BL0 = 'assets/000.png'
BL1 = 'assets/001.png'
BL2 = 'assets/002.png'
BL3 = 'assets/003.png'

WHITE = (255, 255, 255)
WIDTH = 1050
HEIGHT = 600

class Level1(GameState):

    def __init__(self):
        super().__init__()
        self.scores = scores
        self.next_state = 'START'

    def startup(self, persistent):

        # pygame.mixer.music.load('assets/music/Omega.ogg')
        # pygame.mixer.music.set_volume(0.5)
        # pygame.mixer.music.play(-1, 0.0)
        pygame.mouse.set_visible(False)

        bg = parallax.ParallaxSurface((1400, 400), pygame.RLEACCEL)
        bg.add(BL3, 8, (WIDTH*2, HEIGHT))
        bg.add(BL2, 6, (WIDTH*2, HEIGHT))
        bg.add(BL1, 3, (WIDTH*2, HEIGHT))
        bg.add(BL0, 2, (WIDTH*2, HEIGHT))

        self.background = bg
        self.finished = False

        self.phase = 0

        self.num_of_enemies = 0
        self.score = 0
        self.shots_fired = 0
        self.streak = 1
        self.misses = 0

        self.mssg_group = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.asteroid_list = Asteroid_group()
        self.boss_list = pygame.sprite.Group()
        self.hud_items = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.player = Player(self.player_list)
        self.crosshair = Crosshair()

        self.wave1()

        signaly.subscribe('GAME_OVER', self.game_over, 1)
        signaly.subscribe('PLAYER_MSSG', self.player_mssg)

        super().startup(persistent)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            self.done = True
            pygame.quit()
            quit()

        self.player.get_event(event,
                              enemy_list=self.enemy_list,
                              boss_list=self.boss_list,
                              shots_fired=self.shots_fired,
                              done=self.done)

    def game_over(self):
        print('game over')
        FallingMssg('DEFEATED BY HEDGELORD', (255, 255, 255, 255), self.end, ((WIDTH/2), -10), 30, self.mssg_group)

    def player_mssg(self, mssg):
        # amt = str(amount).replace('0', '', 1)
        OnScreenDmg('+{}'.format(mssg), (0,135,236, 200), self.player.rect.center, 17, self.mssg_group)

    def end(self):
        self.done = True

    def bullet_mechanics(self, multiplier):
         # --- calculate mechanics for each bullet
        pos = (self.player.rect.center[0]-2, self.player.rect.center[1]+2)
        self.player.weapon.fire(pos)
        self.shots_fired += 1

        for boss in self.boss_list:
            for bullet in boss.bullets:
                enemy_bullet_player_hit_list = pygame.sprite.spritecollide(
                    bullet, self.player_list, False, pygame.sprite.collide_mask)


                if enemy_bullet_player_hit_list:
                    self.player.collision_detected(1)
                    if not self.player.dying:
                        OnScreenDmg('{}'.format('HIT'), (255, 255, 255, 200), bullet.rect.center, 25, self.mssg_group)
                    if self.player.hp <= 0:
                        pygame.mixer.music.fadeout(1000)
                        # message_display('YOU LOOSE HIT BY BULLET!!!', WHITE, pygame.display.get_surface(), (700, 400))
                        self.player.explode()
                    if not self.player.hp <=0:
                        bullet.kill()


        for bullet in self.player.weapon.bullets:

            # see if bullet hit a enemy
            enemy_hit_list = pygame.sprite.spritecollide(
                bullet, self.enemy_list, False)

            # see if asteroid hit ship
            asteroid_hit_list = pygame.sprite.spritecollide(
                bullet, self.asteroid_list, False)

            boss_hit_list = pygame.sprite.spritecollide(
                bullet, self.boss_list, False, pygame.sprite.collide_mask)

            for boss in boss_hit_list:
                if not boss.hit:
                    crit_roll = random.randint(1, 101)
                    will_crit = crit_roll > 96
                    if will_crit:
                        dmg = 5 * floor(random.randint(1.0,5.0))
                        OnScreenDmg('{}'.format(dmg), (255, 31, 31, 230), bullet.rect.center, 25, self.mssg_group)
                    else:
                        dmg = 5
                        OnScreenDmg('{}'.format(dmg), (255, 51, 51, 175), bullet.rect.center, 20, self.mssg_group)
                    boss.hp -= dmg
                    boss.collision_detected()
                    bullet.kill()

                    if boss.hp <= 0:
                        self.score += (150 * multiplier)
                        boss.explode()

            for asteroid in asteroid_hit_list:
                asteroid.hp -= 3
                if asteroid.hp <= 0:
                    self.score += 20
                bullet.kill()

            # for each enemy hit, remove the bullet and add to the score
            for enemy in enemy_hit_list:

                if not enemy.hit:
                    bullet.kill()
                    self.score += (1 * multiplier)
                    self.streak += 1
                    enemy.explode()

             # remove the bullet if it flies up off the screen
            if bullet.rect.y < -50:
                self.streak = 0
                self.misses += 1

    def player_collisions(self):
         # --- handle collisions
        player_hit_list = pygame.sprite.spritecollide(
            self.player, self.asteroid_list, False, pygame.sprite.collide_mask)

        if player_hit_list:
            pygame.mixer.music.fadeout(1000)
            message_display('YOU LOOSE HIT BY ASTEROID!!!', WHITE, pygame.display.get_surface(), (700, 400))

            self.done = True

        player_enemy_hit_list = pygame.sprite.spritecollide(
            self.player, self.enemy_list, False, pygame.sprite.collide_mask)

        if player_enemy_hit_list:
            for enemy in player_enemy_hit_list:
                if not enemy.hit:
                    pygame.mixer.music.fadeout(1000)
                    message_display('YOU LOOSE HIT BY ENEMY!!!', WHITE, pygame.display.get_surface(), (700, 400))

                    self.done = True

        player_boss_hit_list = pygame.sprite.spritecollide(
            self.player, self.boss_list, False, pygame.sprite.collide_mask)

        if player_boss_hit_list:
            for boss in player_boss_hit_list:
                if not boss.hit:
                    pygame.mixer.music.fadeout(1000)
                    message_display('YOU LOOSE HIT BY ENEMY!!!', WHITE, pygame.display.get_surface(), (700, 400))

                    self.done = True

    def check_game_over(self, total_score):
        # checking enemy list is empty ensures that the last explode() has completed
        # before ending game;)
        if not self.enemy_list and not self.boss_list:
            if self.phase == 0:
                self.phase = 1
                Boss((200, -70), self.boss_list)
                return

            if not self.finished:
                print('winner', self.shots_fired, self.score, total_score)
                pygame.mixer.music.fadeout(1000)

                if total_score > self.scores.top_score:
                    self.scores.update_ts(total_score)

                if self.player.weapon.ammo == 0:
                    FallingMssg('CLOSE ONE, YOU WIN!! score: {}'
                        .format(str(total_score)), (255, 255, 255, 255), self.end, ((WIDTH/2), -10), 30, self.mssg_group)
                else:
                    FallingMssg('YOU DESTOYED HEDGELORD'
                        .format(str(total_score)), (255, 255, 255, 255), self.end, ((WIDTH/2), -10), 30, self.mssg_group)
                self.finished = True

    def wave1(self):
        for i in range(self.num_of_enemies):
            Enemy(self.enemy_list)

    def update(self, dt):
        multiplier = int(self.streak/2) or 1
        total_score = int(self.score * 100) or 0
        # self.hud_ammo.prop = self.player.weapon.ammo
        # self.hud_score.prop = total_score
        # self.hud_multiplier.prop = multiplier

        self.check_game_over(total_score)

        # call the update method on all the sprites
        self.player.update(dt)
        self.mssg_group.update(dt)
        self.crosshair.update()
        self.boss_list.update(dt, self.player.rect.center)
        self.enemy_list.update(dt, self.player.rect.center)
        self.asteroid_list.update()
        self.hud_items.update()

        self.player_collisions()
        self.bullet_mechanics(multiplier)

    def draw(self, surface):
        surface.fill(WHITE)
        # surface.blit(self.background.image, self.background.rect)
        # direction = -1 if self.player.vel[0] < 0 else 1
        self.background.scroll(self.player.vel[0]/28)


        self.background.draw(surface)
        self.hud_items.draw(surface)
        self.mssg_group.draw(surface)
        self.asteroid_list.draw(surface)
        self.enemy_list.draw(surface)
        self.boss_list.draw(surface)
        for boss in self.boss_list:
            boss.bullets.draw(surface)
            boss.health_bar.draw(surface)
        self.player.weapon.bullets.draw(surface)
        self.player.health_bar.draw(surface)
        self.crosshair.draw(surface)
        self.player.draw(surface)
