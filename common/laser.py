import pygame
from common.explosion import Explosion
from common.game_config import GameConfig
from common.speed import Speed

class Laser(pygame.sprite.Sprite):

    def __init__(self, gc: GameConfig, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.gc = gc
        self.image = self.gc.laser_image_green
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height
        self._layer = 3

    def explode(self) -> Explosion:
        channel = pygame.mixer.find_channel()
        channel.play(self.gc.explosion_sound_default)
        explosion = Explosion(
            self.gc,
            self.rect.x + self.rect.width / 2,
            self.rect.y
        )
        return explosion

    def update(self):
        self.rect.y -= Speed.HIPER_FAST.value
