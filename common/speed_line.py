import pygame
import random
from common.game_config import GameConfig
from common.speed import Speed

class SpeedLine(pygame.sprite.Sprite):

    def __init__(self, gc: GameConfig):
        pygame.sprite.Sprite.__init__(self)
        self.gc = gc
        self.configure()
        self._layer = 1

    def configure(self):
        self.image = self.gc.speed_line_image_default
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(
            self.rect.width,
            self.gc.screen_width - (self.rect.width * 2)
        )
        self.rect.y = -self.rect.height
        self.speed = Speed.SUPER_FAST.value

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.gc.screen_height:
            self.configure()
