import pygame

class GameConfig(object):

    def __init__(self, gc: dict):
        self.gc = gc
        self.configure()
        self.configure_sound()
        self.configure_background()
        self.configure_screen()
        self.configure_player()
        self.configure_laser()
        self.configure_enemy()
        self.configure_explosion()
        self.configure_asteroid()
        self.configure_speed_line()

    def configure(self):
        pygame.event.set_allowed([pygame.KEYDOWN])
        pygame.mouse.set_visible(False)
        self.general_fps = self.gc['general']['fps']
        self.color_light = self.gc['general']['color_light']
        self.title_font = self.gc['general']['title_font']
        self.title_size = self.gc['general']['title_size']

    def configure_sound(self):
        self.volume = self.gc['sound']['volume']
        pygame.mixer.set_num_channels(self.gc['sound']['num_channels'])

    def configure_background(self):
        self.background_image_default = pygame.image.load(
            self.gc['background']['image_default']
        )

    def configure_screen(self):
        self.screen = pygame.display.set_mode(
            [0, 0],
            pygame.FULLSCREEN | pygame.DOUBLEBUF
        )
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.screen_center = [
            round(self.screen_width / 2),
            round(self.screen_height / 2)
        ]

    def configure_player(self):
        self.player_image_default = pygame.image.load(
            self.gc['player']['image_default']
        ).convert_alpha()

    def configure_laser(self):
        self.laser_image_green = pygame.image.load(
            self.gc['laser']['image_green']
        ).convert_alpha()
        self.laser_sound_default = pygame.mixer.Sound(
            self.gc['laser']['sound_default']
        )
        self.laser_sound_default.set_volume(self.volume)

    def configure_enemy(self):
        self.enemy_images = []
        self.enemy_images.append(pygame.image.load(
            self.gc['enemy']['images'][0]
        ).convert_alpha())
        self.enemy_images.append(pygame.image.load(
            self.gc['enemy']['images'][1]
        ).convert_alpha())

    def configure_explosion(self):
        self.explosion_image_green = pygame.image.load(
            self.gc['explosion']['image_green']
        ).convert_alpha()
        self.explosion_sound_default = pygame.mixer.Sound(
            self.gc['explosion']['sound_default']
        )
        self.explosion_sound_default.set_volume(self.volume)

    def configure_asteroid(self):
        self.asteroid_images = []
        self.asteroid_images.append(pygame.image.load(
            self.gc['asteroid']['images'][0]
        ).convert_alpha())
        self.asteroid_images.append(pygame.image.load(
            self.gc['asteroid']['images'][1]
        ).convert_alpha())

    def configure_speed_line(self):
        self.speed_line_image_default = pygame.image.load(
            self.gc['speed_line']['image_default']
        ).convert_alpha()
