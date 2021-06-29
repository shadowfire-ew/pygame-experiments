import pygame
from functools import lru_cache

location = "resources/images/"


base = {
    "hole":0,
    "floor":1,
    "water":2,
    "wall":3
}
border = {
    "convex":0,
    "straight":1,
    "concave":2
}

#using an lru cache to hold onto some values
@lru_cache(maxsize=10)
def load_tile_table(filename, width, height = None):
    """
    will load the tileset as an array of subsurfaces
    parameters:
        filename (string) - the filename
        width: width of tile in pixels
        height: height of tile in pixels
            - if height is None, height will copy width
    """

    if height is None:
        # in case a height is included
        height = width

    image = pygame.image.load(location+'tilesets/'+filename).convert()
    im_width, im_height = image.get_size()
    tile_table = []
    for tile_y in range(0, im_height//height):
        line = []
        for tile_x in range(0, im_width//width):
            rect = (tile_x*width, tile_y*height,width,height)
            line.append(image.subsurface(rect))
        tile_table.append(line)
    return tile_table