import pygame

from tiles import Tile
from player import Player
from settings import tile_size


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

        for i, row in enumerate(layout):
            for j, col in enumerate(row):
                pos = (j * tile_size, i * tile_size)
                if col == 'X':
                    self.tiles.add(Tile(pos, tile_size))
                if col == 'P':
                    self.player.add(Player(pos))

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
        self.player.update()
        self.player.draw(self.display_surface)
