import pygame
import random
from common.game_config import GameConfig
from common.speed import Speed

class Enemy(pygame.sprite.Sprite):

    def __init__(self, gc: GameConfig):
        pygame.sprite.Sprite.__init__(self)
        self.gc = gc
        self.configure()
        self._layer = 2

    def configure(self):
        image = self.gc.enemy_images[random.randint(0, 1)]
        self.image = pygame.transform.rotate(image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(
            self.rect.width,
            self.gc.screen_width - (self.rect.width * 2)
        )
        self.rect.y = -self.rect.height
        self.speed = Speed.HIPER_SLOW.value

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > self.gc.screen_height \
            or self.rect.x > self.gc.screen_width \
            or self.rect.x < -self.rect.width:
            self.configure()
