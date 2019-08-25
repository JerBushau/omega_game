import pygame
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
from score import scores
from gamestate import GameState
import parallax

BACKGROUND = 'assets/background1.png'
BL0 = 'assets/000.png'
BL1 = 'assets/001.png'
BL2 = 'assets/002.png'
BL3 = 'assets/003.png'

WHITE = (255, 255, 255)
WIDTH = 1050
HEIGHT = 600

# these functions should be moved to a class
def text_objects(text, font, color):
    """Creates 'text objects' for displaying messages"""
    text_surf = font.render(text, True, color)
    return text_surf, text_surf.get_rect()


def message_display(text, color, surface, screenDimentions):
    large_text = pygame.font.Font('freesansbold.ttf',30)
    # create text 'objects'
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = ((screenDimentions[0]/2), (screenDimentions[1]/2))
    # blit the text object to the screen
    surface.blit(text_surf, text_rect)
    pygame.display.update()
    # pause for a moment to allow player to see message
    # this is terrible need legit timer - don't want to freeze game
    pygame.time.delay(1500)


class Level1(GameState):

    def __init__(self):
        super().__init__()
        self.scores = scores
        self.next_state = 'START'

    def startup(self, persistent):
        pygame.mixer.music.load('assets/music/Omega.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
        pygame.mouse.set_visible(False)

        bg = parallax.ParallaxSurface((1400, 400), pygame.RLEACCEL)
        bg.add(BL3, 8, (WIDTH*2, HEIGHT))
        bg.add(BL2, 6, (WIDTH*2, HEIGHT))
        bg.add(BL1, 3, (WIDTH*2, HEIGHT))
        bg.add(BL0, 2, (WIDTH*2, HEIGHT))

        self.background = bg

        self.phase = 0

        self.num_of_enemies = 1
        self.score = 0
        self.shots_fired = 0
        self.streak = 1
        self.misses = 0

        self.enemy_list = pygame.sprite.Group()
        self.asteroid_list = Asteroid_group()
        self.boss_list = pygame.sprite.Group()
        self.hud_items = pygame.sprite.Group()
        self.player_list = pygame.sprite.Group()
        self.player = Player(self.player_list)

        self.crosshair = Crosshair()
        self.hud_score = Hud(WIDTH-130, HEIGHT-50, 120, 40, 'SCORE')
        self.hud_ammo = Hud(WIDTH-130, HEIGHT-100, 120, 40, 'AMMO')
        self.hud_multiplier = Hud(WIDTH-190, HEIGHT-50, 50, 40, '', 'x', True)
        self.hud_items.add(self.hud_score)
        self.hud_items.add(self.hud_ammo)
        self.hud_items.add(self.hud_multiplier)

        self.wave1()

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
                    self.player.hp -= 1
                    bullet.kill()
                    if self.player.hp == 0:
                        pygame.mixer.music.fadeout(1000)
                        message_display('YOU LOOSE HIT BY BULLET!!!', WHITE, pygame.display.get_surface(), (700, 400))

                        self.done = True


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
                boss.hp -= 5
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

            print('winner', self.shots_fired, self.score, total_score)
            pygame.mixer.music.fadeout(1000)
            perfect = self.shots_fired <= self.num_of_enemies and not self.misses

            if total_score > self.scores.top_score:
                self.scores.update_ts(total_score)

            if perfect:
                message_display('PERFECT!! YOU WIN!! score: {}'
                    .format(str(total_score)), WHITE, pygame.display.get_surface(), (700, 400))
            elif self.player.weapon.ammo == 0:
                message_display('CLOSE ONE, YOU WIN!! score: {}'
                    .format(str(total_score)), WHITE, pygame.display.get_surface(), (700, 400))
            else:
                message_display('YOU WIN!!! total score: {}'
                    .format(str(total_score)), WHITE, pygame.display.get_surface(), (700, 400))
            self.done = True

    def wave1(self):
        for i in range(self.num_of_enemies):
            Enemy(self.enemy_list)

    def update(self, dt):
        multiplier = int(self.streak/2) or 1
        total_score = int(self.score * 100) or 0
        self.hud_ammo.prop = self.player.weapon.ammo
        self.hud_score.prop = total_score
        self.hud_multiplier.prop = multiplier

        self.check_game_over(total_score)

        # call the update method on all the sprites
        self.player.update(dt)
        self.crosshair.update()
        self.player.weapon.bullets.update(dt)
        for boss in self.boss_list:
            boss.bullets.update(dt)
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
        self.asteroid_list.draw(surface)
        self.enemy_list.draw(surface)
        self.boss_list.draw(surface)
        for boss in self.boss_list:
            boss.bullets.draw(surface)
        self.player.weapon.bullets.draw(surface)
        self.crosshair.draw(surface)
        self.player.draw(surface)
