import math
import pygame
import random
from common.asteroid import Asteroid
from common.direction import Direction
from common.enemy import Enemy
from common.game_config import GameConfig
from common.player import Player
from common.speed import Speed
from common.speed_line import SpeedLine

class Game:

    def __init__(self, gc: GameConfig):
        self.gc = gc
        self.finished = False
        self.fire_tick = 0
        self.score = 0
        self.lifes = 5
        self.respawn_tick = 0
        self.respawning = False
        # Configura o background
        self.bg_offset = Speed.DEFAULT.value
        self.bg_image = self.gc.background_image_default
        self.bg_columns = math.ceil(
            self.gc.screen_width / self.bg_image.get_width()
        )
        self.bg_lines = math.ceil(
            self.gc.screen_height / self.bg_image.get_height()
        )
        # Configura os headers
        self.title_font = pygame.font.SysFont(
            self.gc.title_font,
            self.gc.title_size,
            True,
            False
        )
        self.title_render = self.title_font.render(
            'SPACE INVADERS',
            True,
            self.gc.color_light
        )
        # Configura a tela
        self.screen = self.gc.screen
        # Instancia grupos de sprites
        self.all_sprites_list = pygame.sprite.LayeredUpdates()
        self.enemy_list = pygame.sprite.Group()
        self.asteroid_list = pygame.sprite.Group()
        self.laser_list = pygame.sprite.Group()
        self.explosion_list = pygame.sprite.Group()
        # Instancia os sprites
        self.player = Player(self.gc)
        self.enemy = Enemy(self.gc)
        self.asteroid = Asteroid(self.gc)
        for i in range(1):
            speed_line = SpeedLine(self.gc)
            self.all_sprites_list.add(speed_line)
        # Associa os sprites aos grupos
        self.all_sprites_list.add(self.player)
        self.all_sprites_list.add(self.enemy)
        self.all_sprites_list.add(self.asteroid)
        self.enemy_list.add(self.enemy)
        self.asteroid_list.add(self.asteroid)

    def process_events(self):
        # Eventos de tecla pressionada
        self.process_keypressed()
        # Outros eventos
        for event in pygame.event.get():
            # Eventos do teclado
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.finished = True

    def run_logic(self):
        # Termina o jogo caso as vidas do jogador acabem
        if (self.score == 0):
            self.finished = True
        # Trata o retorno do jogador após a colisão
        self.check_respawning()
        # Remove explosões anteriores do grupo de sprites
        self.clear_explosions()
        # Trata a colisão do laser com o inimigo
        self.laser_enemy_collision()
        # Trata a colisão do laser com o asteroid
        self.laser_asteroid_collision()
        # Trata a colisão do player com o inimigo
        self.player_enemy_collision()
        # Trata a colisão do player com o asteroid
        self.player_asteroid_collision()
        # Remove lasers que saíram da tela
        self.remove_lost_lasers()
        # Atualiza todos os sprites
        self.all_sprites_list.update()

    def display_frames(self):
        # Preenche o background com a imagem padrão
        for i in range(self.bg_columns):
            for j in range(-1, self.bg_lines):
                self.screen.blit(
                    self.bg_image,
                    [
                        i * self.bg_image.get_width(),
                        j * self.bg_image.get_height() + self.bg_offset
                    ]
                )
        # Desenha os sprites na tela
        self.all_sprites_list.draw(self.screen)
        self.screen.blit(self.title_render, [20, 20])
        self.score_render = self.title_font.render(
            f'SCORE: {self.score}',
            True,
            [159, 139, 166]
        )
        self.lifes_render = self.title_font.render(
            f'X {self.lifes}',
            True,
            [159, 139, 166]
        )
        self.screen.blit(self.score_render, [20, 60])
        self.screen.blit(self.gc.life_image_default, [20, 100])
        self.screen.blit(self.lifes_render, [75, 103])
        # Atualiza o display
        pygame.display.flip()
        # Move o background para baixo
        if self.bg_offset <= self.bg_image.get_height():
            self.bg_offset += Speed.DEFAULT.value
        else:
            self.bg_offset = 0

    # process_events

    def process_keypressed(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.player.move(Direction.LEFT)
        if keys[pygame.K_w]:
            self.player.move(Direction.UP)
        if keys[pygame.K_d]:
            self.player.move(Direction.RIGHT)
        if keys[pygame.K_s]:
            self.player.move(Direction.DOWN)
        if keys[pygame.K_RCTRL]:
            time_tick = pygame.time.get_ticks()
            if time_tick - self.fire_tick > 125:
                laser = self.player.fire()
                self.all_sprites_list.add(laser)
                self.laser_list.add(laser)
                self.fire_tick = time_tick

    # run_logic

    def check_respawning(self):
        respawn_tick = pygame.time.get_ticks()
        if self.respawning:
            if respawn_tick - self.respawn_tick > 2000:
                self.respawn_tick = respawn_tick
                self.respawning = False
                self.player.set_respawn(False)

    def add_asteroid(self):
        asteroid = Asteroid(self.gc)
        self.all_sprites_list.add(asteroid)
        self.asteroid_list.add(asteroid)

    def add_enemy(self):
        enemy = Enemy(self.gc)
        self.all_sprites_list.add(enemy)
        self.enemy_list.add(enemy)

    def change_difficulty(self):
        number = random.randint(1, 100)
        if number > 95 and len(self.enemy_list) < 5:
            self.add_enemy()

    def clear_explosions(self):
        time = pygame.time.get_ticks()
        for explosion in self.explosion_list:
            if time - explosion.time > 1000:
                self.all_sprites_list.remove(explosion)
                self.explosion_list.remove(explosion)

    def laser_asteroid_collision(self):
        collided_list = pygame.sprite.groupcollide(
            self.laser_list, self.asteroid_list, True, False
        )
        for collided_laser in collided_list.keys():
            explosion = collided_laser.explode()
            self.all_sprites_list.add(explosion)
            self.explosion_list.add(explosion)

    def laser_enemy_collision(self):
        collided_list = pygame.sprite.groupcollide(
            self.laser_list, self.enemy_list, True, True
        )
        for collided_laser in collided_list.keys():
            explosion = collided_laser.explode()
            self.all_sprites_list.add(explosion)
            self.explosion_list.add(explosion)
            self.add_enemy()
            self.score += 1

    def player_enemy_collision(self):
        if not self.respawning:
            collided_list = pygame.sprite.spritecollide(
                self.player, self.enemy_list, True
            )
            if collided_list:
                self.add_enemy()
                self.all_sprites_list.remove(self.player)
                self.respawn_tick = pygame.time.get_ticks()
                self.respawning = True
                self.player = Player(self.gc)
                self.player.set_respawn(True)
                self.all_sprites_list.add(self.player)
                self.lifes -= 1

    def player_asteroid_collision(self):
        if not self.respawning:
            collided_list = pygame.sprite.spritecollide(
                self.player, self.asteroid_list, True
            )
            if collided_list:
                self.add_asteroid()
                self.all_sprites_list.remove(self.player)
                self.respawn_tick = pygame.time.get_ticks()
                self.respawning = True
                self.player = Player(self.gc)
                self.player.set_respawn(True)
                self.all_sprites_list.add(self.player)
                self.lifes -= 1

    def remove_lost_lasers(self):
        for laser in self.laser_list:
            if (laser.rect.y + laser.rect.height) < 0:
                self.laser_list.remove(laser)
                self.all_sprites_list.remove(laser)
