import pygame
from common.direction import Direction
from common.game_config import GameConfig
from common.laser import Laser
from common.speed import Speed

class Player(pygame.sprite.Sprite):

    def __init__(self, gc: GameConfig):
        pygame.sprite.Sprite.__init__(self)
        self.gc = gc
        self.image = self.gc.player_image_default
        self.rect = self.image.get_rect()
        self.rect.x = self.gc.screen_center[0] - self.rect.width / 2
        self.rect.y = self.gc.screen_center[1] - self.rect.height / 2
        self._layer = 3

    def fire(self) -> Laser:
        channel = pygame.mixer.find_channel()
        channel.play(self.gc.laser_sound_default)
        laser = Laser(
            self.gc, self.rect.x + self.rect.width / 2, self.rect.y
        )
        return laser

    def move(self, direction: Direction):
        if direction == Direction.LEFT:
            self.rect.x -= Speed.DEFAULT.value
        elif direction == Direction.UP:
            self.rect.y -= Speed.DEFAULT.value
        elif direction == Direction.RIGHT:
            self.rect.x += Speed.DEFAULT.value
        elif direction == Direction.DOWN:
            self.rect.y += Speed.DEFAULT.value

    def update(self):
        pass
