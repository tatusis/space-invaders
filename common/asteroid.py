import pygame
import random
from common.game_config import GameConfig
from common.speed import Speed

class Asteroid(pygame.sprite.Sprite):

    def __init__(self, gc: GameConfig):
        pygame.sprite.Sprite.__init__(self)
        self.gc = gc
        self.configure()
        self._layer = 1

    def configure(self):
        image = self.gc.asteroid_images[random.randint(0, 1)]
        self.image = pygame.transform.rotate(image, random.random() * 360)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(
            0,
            self.gc.screen_width - self.rect.width
        )
        self.rect.y = -self.rect.height
        self.speed = random.choice(
            [
                Speed.SUPER_SLOW.value,
                Speed.VERY_SLOW.value,
                Speed.DEFAULT.value
            ]
        )
        self.side = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.side
        self.rect.y += self.speed
        if self.rect.y > self.gc.screen_height \
            or self.rect.x > self.gc.screen_width \
            or self.rect.x < -self.rect.width:
            self.configure()
