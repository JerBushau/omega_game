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
from score import scores
from gamestate import GameState


BACKGROUND = 'assets/background.png'
WHITE = (255, 255, 255)


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
        self.background = Background(BACKGROUND, [0,0])
        self.next_state = 'START'

    def startup(self, persistent):
        pygame.mixer.music.load('assets/music/Omega.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)

        self.num_of_enemies = 15
        self.score = 0
        self.shots_fired = 0
        self.streak = 1
        self.misses = 0
        self.ammo = int(self.num_of_enemies * 10)

        self.enemy_list = pygame.sprite.Group()
        self.asteroid_list = Asteroid_group()
        self.bullet_list = pygame.sprite.Group()
        self.boss_list = pygame.sprite.Group()
        self.hud_items = pygame.sprite.Group()
        self.boss = Boss()
        self.player = Player()

        for i in range(self.num_of_enemies):
            enemy = Enemy()
            self.enemy_list.add(enemy)

        self.boss_list.add(self.boss)

        self.hud_score = Hud(570, 350, 120, 40, 'SCORE')
        self.hud_ammo = Hud(570, 300, 120, 40, 'AMMO')
        self.hud_multiplier = Hud(510, 350, 50, 40, '', 'x', True)
        self.hud_items.add(self.hud_score)
        self.hud_items.add(self.hud_ammo)
        self.hud_items.add(self.hud_multiplier)

        super().startup(persistent)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            self.done = True
            pygame.quit()
            quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            can_fire = self.ammo > 0
            if can_fire and event.button == 1:
                self.player.weapon.begin_fire()
                bullet = self.player.weapon.ammo_type(self.player.rect.center)
                self.bullet_list.add(bullet)
                self.shots_fired += 1
                self.ammo -= 1

            elif can_fire and event.button == 3:
                for i in range(3):
                    bullet = Chain_Lightning(self.player.rect.center)
                    bullet.find_next_target(self.enemy_list.sprites() + self.boss_list.sprites())
                    self.bullet_list.add(bullet)
                    self.shots_fired += 1
                    self.ammo -= 1

            elif event.button == 2:
                self.ammo += 30

            elif not can_fire:
                print('you loose')
                pygame.mixer.music.fadeout(1000)
                message_display('YOU LOOSE OUT OF AMMO!!!', WHITE, pygame.display.get_surface(), (700, 400))

                self.done = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.player.weapon.cease_fire()

    def update(self, dt):
        multiplier = int(self.streak/2) or 1
        total_score = int(self.score * 100) or 0
        self.hud_ammo.prop = self.ammo
        self.hud_score.prop = total_score
        self.hud_multiplier.prop = multiplier

        if self.player.weapon.firing_timer.is_finished() and self.ammo > 0:
            bullet = self.player.weapon.ammo_type(self.player.rect.center)
            self.bullet_list.add(bullet)
            self.shots_fired += 1
            self.ammo -= 1

        # --- Game logic

        # call the update method on all the sprites
        self.player.update()
        self.bullet_list.update(dt)
        self.boss_list.update(dt, self.player.rect.center)
        self.enemy_list.update(dt, self.player.rect.center)
        self.asteroid_list.update()
        self.hud_items.update()

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


        # --- calculate mechanics for each bullet
        for bullet in self.bullet_list:

            # see if bullet hit a enemy
            enemy_hit_list = pygame.sprite.spritecollide(
                bullet, self.enemy_list, False)

            # see if asteroid hit ship
            asteroid_hit_list = pygame.sprite.spritecollide(
                bullet, self.asteroid_list, False)

            boss_hit_list = pygame.sprite.spritecollide(
                bullet, self.boss_list, False)

            for boss in boss_hit_list:
                boss.hp -= 15
                self.bullet_list.remove(bullet)

                if boss.hp <= 0:
                    self.score += (150 * multiplier)
                    self.boss.explode()

            for asteroid in asteroid_hit_list:
                asteroid.hp -= 3
                if asteroid.hp <= 0:
                    self.score += 20
                self.bullet_list.remove(bullet)

            # for each enemy hit, remove the bullet and add to the score
            for enemy in enemy_hit_list:

                if not enemy.hit:
                    self.bullet_list.remove(bullet)
                    self.score += (1 * multiplier)
                    self.streak += 1
                    enemy.explode()

             # remove the bullet if it flies up off the screen
            if bullet.rect.y < -50:
                self.bullet_list.remove(bullet)
                self.streak = 0
                self.misses += 1

        # checking enemy list is empty ensures that the last explode() has completed
        # before ending game;)
        if not self.enemy_list and not self.boss_list:
            print('winner', self.shots_fired, self.score, total_score)
            pygame.mixer.music.fadeout(1000)
            perfect = self.shots_fired <= self.num_of_enemies and not self.misses

            if total_score > self.scores.top_score:
                self.scores.update_ts(total_score)

            if perfect:
                message_display('PERFECT!! YOU WIN!! score: {}'
                    .format(str(total_score)), WHITE, pygame.display.get_surface(), (700, 400))
            elif self.ammo == 0:
                message_display('CLOSE ONE, YOU WIN!! score: {}'
                    .format(str(total_score)), WHITE, pygame.display.get_surface(), (700, 400))
            else:
                message_display('YOU WIN!!! total score: {}'
                    .format(str(total_score)), WHITE, pygame.display.get_surface(), (700, 400))
            self.done = True

    def draw(self, surface):
        surface.fill(WHITE)
        surface.blit(self.background.image, self.background.rect)

        self.hud_items.draw(surface)
        self.asteroid_list.draw(surface)
        self.enemy_list.draw(surface)
        self.boss_list.draw(surface)
        self.bullet_list.draw(surface)
        self.player.draw(surface)
