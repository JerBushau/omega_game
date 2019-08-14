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
from score import Score
from timer import Timer2
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
    # update the screen to show new text
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


class Game(object):
    """Controls entire game"""
    def __init__(self):
        self.screen = self.pygame_setup()
        self.clock = pygame.time.Clock()
        # global obj to track high scores
        self.scores = Score()
        

    def pygame_setup(self):
        """Initializes pygame and produces a surface to blit on"""
        self.screen_width = 700
        self.screen_height = 400
        screen = pygame.display.set_mode([self.screen_width, self.screen_height])
        # pre init mixer
        pygame.mixer.pre_init(frequency=22050, size=8, channels=2, buffer=1024)
        # init pygame
        pygame.init()
        pygame.mixer.music.load('assets/music/Omega.ogg')
        # by default hide mouse
        # pygame.mouse.set_visible(False) uncomment to hide mouse
        pygame.display.set_caption('OMEGA!')

        return screen


    def start_loop(self):
        """Loop for start screen"""
        selected = False
        background = Background(START_BG, [0, 0])
        top_score = Hud(10, 350, 200, 40, "TOP SCORE")

        def launch_game():
            nonlocal selected
            selected = True
            self.game_loop()

        while not selected:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    selected = True

            top_score.prop = self.scores.top_score
            self.clock.tick(20)
            pygame.mouse.set_visible(True)
            self.screen.blit(background.image, background.rect)

            large_text = pygame.font.Font('freesansbold.ttf',80)
            text_surf, text_rect = text_objects("OMEGA!", large_text, (210,208,224))
            text_rect.center = ((self.screen_width/2),(self.screen_height/2.75))
            self.screen.blit(text_surf, text_rect)

            top_score.update(dest=self.screen)
            button('PLAY', ((self.screen_width/2) - 50), 240, 100, 40,
                  ((37,31,71), (108,100,153), (210,208,224)), self.screen, launch_game)


    def game_loop(self):
        """All gameplay setup and logic"""
        # start the game music 
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0)
        # set the background
        background = Background(BACKGROUND, [0,0])
        # set desired fps
        fps = 60

        num_of_enemies = 15
        score = 0
        shots_fired = 0
        ammo = int(num_of_enemies * 10)
        streak = 1
        misses = 0

        is_firing = False
        firing_timer = Timer2(140)
        # uncomment this line to hide the system mouse when game window is in focus
        # pygame.mouse.set_visible(False) 

        #  list of every sprite
        all_sprites_list = pygame.sprite.Group()
        # list of each enemy in the game
        enemy_list = pygame.sprite.Group()
        # list of each bullet - rename projectile?
        bullet_list = pygame.sprite.Group()

        # --- Create the sprites
        # create all enemies
        for i in range(num_of_enemies):
            enemy = Enemy()
            # Add the enemy to the appropriate lists of sprites
            enemy_list.add(enemy)


        # create a player and starting location
        # player should take in starting location
        player = Player()
        player.rect.y = 330

        boss_list = pygame.sprite.Group()
        boss = Boss()
        boss_list.add(boss)

        # create hud
        hud_items = pygame.sprite.Group()
        hud_score = Hud(570, 350, 120, 40, 'SCORE')
        hud_ammo = Hud(570, 300, 120, 40, 'AMMO')
        hud_multiplier = Hud(510, 350, 50, 40, '', 'x', True)
        hud_items.add(hud_score)
        hud_items.add(hud_ammo)
        hud_items.add(hud_multiplier)

        # create asteroids
        asteroid_list = Asteroid_group()
        # asteroid = Asteroid((40, 40), 20)
        # asteroid2 = Asteroid((60, 60), 20)
        # asteroid3 = Asteroid((60, 60), 20)
        # asteroid_list.add(asteroid)
        # asteroid_list.add(asteroid2)
        # asteroid_list.add(asteroid3)

        # -------- Main Program Loop -----------
        game_over = False
        while not game_over:
            dt = self.clock.tick(fps) / 1000
            pygame.display.set_caption(str(self.clock.get_fps()))

            multiplier = int(streak/2) or 1
            total_score = int(score * 100) or 0
            hud_ammo.prop = ammo
            hud_score.prop = total_score
            hud_multiplier.prop = multiplier

            # --- Event Processing --- Controls 
            for event in pygame.event.get():
                player_pos = player.rect.center

                # uncomment this to see event in the terminal
                # print(event)

                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    game_over = True
                    pygame.quit()
                    quit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    can_fire = ammo > 0
                    if can_fire and event.button == 1:
                        is_firing = True
                        bullet = Bullet(player.rect.center)
                        # add the bullet to lists
                        all_sprites_list.add(bullet)
                        bullet_list.add(bullet)
                        shots_fired += 1
                        ammo -= 1
                        firing_timer.start_repeating()
                        

                    elif can_fire and event.button == 3:
                        for i in range(3):
                            bullet = Chain_Lightning(player_pos)
                            # add the bullet to lists
                            bullet.find_next_target(enemy_list.sprites() + boss_list.sprites())
                            all_sprites_list.add(bullet)
                            bullet_list.add(bullet)
                            shots_fired += 1
                            ammo -= 1
                        # bullet = Wobble_shot(player_pos)
                        # # add the bullet to lists
                        # all_sprites_list.add(bullet)
                        # bullet_list.add(bullet)
                        # shots_fired += 1
                        # ammo -= 1

                    elif event.button == 2:
                        ammo += 30

                    elif not can_fire:
                        print('you loose')
                        pygame.mixer.music.fadeout(1000)
                        message_display('YOU LOOSE OUT OF AMMO!!!', WHITE, self.screen, (self.screen_width, self.screen_height))

                        game_over = True

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        is_firing = False
                        firing_timer.reset()

            # weapon logic
            if firing_timer.is_finished():
                bullet = Bullet(player.rect.center)
                # add the bullet to lists
                all_sprites_list.add(bullet)
                bullet_list.add(bullet)
                shots_fired += 1
                ammo -= 1

            # --- Game logic

            # call the update method on all the sprites
            player.update()
            boss_list.update(dt, player.rect.center)
            all_sprites_list.update(dt)
            enemy_list.update(dt, player.rect.center)
            asteroid_list.update()
            hud_items.update()

            # --- handle collisions
            player_hit_list = pygame.sprite.spritecollide(
                player, asteroid_list, False, pygame.sprite.collide_mask)

            if player_hit_list:
                pygame.mixer.music.fadeout(1000)
                message_display('YOU LOOSE HIT BY ASTEROID!!!', WHITE, self.screen, (self.screen_width, self.screen_height))

                game_over = True

            player_enemy_hit_list = pygame.sprite.spritecollide(
                player, enemy_list, False, pygame.sprite.collide_mask)

            if player_enemy_hit_list:
                for enemy in player_enemy_hit_list:
                    if not enemy.hit:
                        pygame.mixer.music.fadeout(1000)
                        message_display('YOU LOOSE HIT BY ENEMY!!!', WHITE, self.screen, (self.screen_width, self.screen_height))

                        game_over = True

            player_boss_hit_list = pygame.sprite.spritecollide(
                player, boss_list, False, pygame.sprite.collide_mask)

            if player_boss_hit_list:
                for boss in player_boss_hit_list:
                    if not boss.hit:
                        pygame.mixer.music.fadeout(1000)
                        message_display('YOU LOOSE HIT BY ENEMY!!!', WHITE, self.screen, (self.screen_width, self.screen_height))

                        game_over = True


            # --- calculate mechanics for each bullet
            for bullet in bullet_list:

                # see if bullet hit a enemy
                enemy_hit_list = pygame.sprite.spritecollide(
                    bullet, enemy_list, False)

                # see if asteroid hit ship
                asteroid_hit_list = pygame.sprite.spritecollide(
                    bullet, asteroid_list, False)

                boss_hit_list = pygame.sprite.spritecollide(
                    bullet, boss_list, False)

                for boss in boss_hit_list:
                    boss.hp -= 15
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)

                    if boss.hp <= 0:
                        score += (150 * multiplier)
                        boss.explode()

                for asteroid in asteroid_hit_list:
                    asteroid.hp -= 3
                    if asteroid.hp <= 0:
                        score += 20
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)

                # for each enemy hit, remove the bullet and add to the score
                for enemy in enemy_hit_list:

                    if not enemy.hit:
                        bullet_list.remove(bullet)
                        all_sprites_list.remove(bullet)
                        score += (1 * multiplier)
                        streak += 1
                        enemy.explode()

                 # remove the bullet if it flies up off the screen
                if bullet.rect.y < -50:
                    bullet_list.remove(bullet)
                    all_sprites_list.remove(bullet)
                    streak = 0
                    misses += 1

            # checking enemy list is empty ensures that the last explode() has completed
            # before ending game;)
            if not enemy_list and not boss_list:
                print('winner',shots_fired, score, total_score)
                pygame.mixer.music.fadeout(1000)
                perfect = shots_fired <= num_of_enemies and not misses

                if total_score > self.scores.top_score:
                    self.scores.update_ts(total_score)

                if perfect:
                    message_display('PERFECT!! YOU WIN!! score: {}'
                        .format(str(total_score)), WHITE, self.screen, (self.screen_width, self.screen_height))
                elif ammo == 0:
                    message_display('CLOSE ONE, YOU WIN!! score: {}'
                        .format(str(total_score)), WHITE, self.screen, (self.screen_width, self.screen_height))
                else:
                    message_display('YOU WIN!!! total score: {}'
                        .format(str(total_score)), WHITE, self.screen, (self.screen_width, self.screen_height))
                game_over = True

            # clear the screen
            self.screen.fill(WHITE)
            # then background
            self.screen.blit(background.image, background.rect)

            # draw all the spites thier z-index is determined by the order here
            hud_items.draw(self.screen)
            asteroid_list.draw(self.screen)
            enemy_list.draw(self.screen)
            all_sprites_list.draw(self.screen)
            boss_list.draw(self.screen)
            player.draw(self.screen)

            # update the screen
            pygame.display.flip()

            if game_over == True:
                self.start_loop()


if __name__ == '__main__':
    game = Game()
    game.start_loop()

pygame.quit()
quit()
