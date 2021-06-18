import pygame

def load_tile_table(filename, size):
    """
    will load the tileset as an array of subsurfaces
    parameters:
        filename (string) - the filename
        size (tuple) - size of image in pixels 
            shape determines how it is parsed
    """
    # setting up the width and height
    width = size[0]
    height = size[0]

    if len(size) == 2:
        # in case a height is included
        height = size[1]

    image = pygame.image.load(filename).convert()
    im_width, im_height = image.get_size()
    tile_table = []
    for tile_x in range(0, im_width/width):
        line = []
        for tile_y in range(0, im_height/height):
            rect = (tile_x*width, tile_y*height,width,height)
            line.append(image.subsurface(rect))
        tile_table.append(line)
    return tile_table