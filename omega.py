import pygame
import random
import time
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
from timer import Timer2
from gamestate import GameState
# create a file for constant vars colors bgs etc

BACKGROUND = 'assets/background.png'
START_BG = 'assets/start_bg.png'
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

#
# handy functions from a tutorial needs re-write to better suit my needs
def text_objects(text, font, color):
    """Creates 'text objects' for displaying messages"""
    text_surf = font.render(text, True, color)
    return text_surf, text_surf.get_rect()

# uses text objects to display messages on screen
# same here, ok for now...
def message_display(text, color, surface, screenDimentions):
    large_text = pygame.font.Font('freesansbold.ttf',30)
    # create text 'objects'
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = ((screenDimentions[0]/2), (screenDimentions[1]/2))
    # blit the text object to the screen
    surface.blit(text_surf, text_rect)
    pygame.display.update()
    # pause for a moment to allow player to see message
    pygame.time.delay(1500)


# create a button class rather than this function
def button(msg, x, y, width, height, colors, surface, action=None):
    """Function to easily create buttons"""

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(surface, colors[0], (x, y, width, height))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(surface, colors[1], (x, y, width, height))

    small_text = pygame.font.Font('freesansbold.ttf',20)
    text_surf, text_rect = text_objects(msg, small_text, colors[2])
    text_rect.center = ((x + (width/2)),(y + (height / 2)))
    surface.blit(text_surf, text_rect)
    pygame.display.update()


class StartScreen(GameState):

    def __init__(self):
        super().__init__()
        self.background = Background(START_BG, [0, 0])
        self.top_score_hud = Hud(10, 350, 200, 40, "TOP SCORE")
        self.scores = scores
        self.next_state = 'LEVEL1'


    def startup(self, persistent):
        pygame.mouse.set_visible(True)
        super().startup(persistent)


    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True


    def end(self):
        self.done = True


    def draw(self, surface):
        surface.blit(self.background.image, self.background.rect)
        self.top_score_hud.update(dest=surface)

        large_text = pygame.font.Font('freesansbold.ttf',80)
        text_surf, text_rect = text_objects("OMEGA!", large_text, (210,208,224))
        text_rect.center = ((700/2),(400/2.75))
        surface.blit(text_surf, text_rect)
        button('PLAY', ((700/2) - 50), 240, 100, 40,
              ((37,31,71), (108,100,153), (210,208,224)), surface, self.end)


    def update(self, dt):
        self.top_score_hud.prop = self.scores.top_score



class Level1(GameState):

    def __init__(self):
        super().__init__()
        self.scores = scores
        self.background = Background(BACKGROUND, [0,0])
        self.num_of_enemies = 15
        self.score = 0
        self.shots_fired = 0
        self.ammo = int(self.num_of_enemies * 10)
        self.streak = 1
        self.misses = 0
        self.next_state = 'START'


    def startup(self, persistent):
        pygame.mixer.music.load('assets/music/Omega.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)

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


class Game(object):
    """
    A single instance of this class is responsible for
    managing which individual game state is active
    and keeping it updated. It also handles many of
    pygame's nuts and bolts (managing the event
    queue, framerate, updating the display, etc.).
    and its run method serves as the "game loop".
    """
    def __init__(self, screen, states, start_state):
        """
        Initialize the Game object.

        screen: the pygame display surface
        states: a dict mapping state-names to GameState objects
        start_state: name of the first active game state
        """
        self.done = False
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pygame.event.get():
            self.state.get_event(event)

    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update active state.

        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)

    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """
        while not self.done:
            dt = self.clock.tick(self.fps) / 1000
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()


if __name__ == '__main__':
    pygame.mixer.pre_init(frequency=22050, size=8, channels=2, buffer=1024)
    pygame.init()
    screen = pygame.display.set_mode((700, 400))
    states = {"START": StartScreen(),
              "LEVEL1": Level1()}
    game = Game(screen, states, "START")
    game.run()


    pygame.quit()
    quit()
