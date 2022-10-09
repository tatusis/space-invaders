import pygame
from common.game_config import GameConfig

class Explosion(pygame.sprite.Sprite):

    def __init__(self, gc: GameConfig, x: int, y: int):
        pygame.sprite.Sprite.__init__(self)
        self.gc = gc
        self.image = self.gc.explosion_image_green.copy()
        self.image.set_alpha(255)
        self.rect = self.image.get_rect()
        self.rect.x = x - self.rect.width / 2
        self.rect.y = y - self.rect.height / 2
        self.time = pygame.time.get_ticks()
        self._layer = 2

    def update(self):
        alpha = self.image.get_alpha()
        if alpha > 0:
            self.image.set_alpha(alpha - 5)
