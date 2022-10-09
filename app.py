import pygame
import yaml
from common.game_config import GameConfig
from common.game import Game

def run():
    pygame.init()
    clock = pygame.time.Clock()

    with open("app.yaml", "r") as game_config:
        gc = GameConfig(yaml.safe_load(game_config))

    game = Game(gc)

    while not game.finished:
        game.process_events()
        game.run_logic()
        game.display_frames()
        clock.tick(gc.general_fps)

    pygame.quit()

if __name__ == '__main__':
    run()
