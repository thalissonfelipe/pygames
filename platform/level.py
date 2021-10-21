import pygame

from tiles import Tile
from settings import tile_size


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)
        self.world_shift = 0

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()

        for i, row in enumerate(layout):
            for j, col in enumerate(row):
                if col == 'X':
                    pos = (j * tile_size, i * tile_size)
                    tile = Tile(pos, tile_size)
                    self.tiles.add(tile)

    def run(self):
        self.tiles.update(self.world_shift)
        self.tiles.draw(self.display_surface)
