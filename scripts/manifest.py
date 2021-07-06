"""
moved these here for convenience
these values are shared among many files
"""
from scripts.levels import Level

tilesize = 80
grid = gwidth,gheight = 16,12
size = width,height = (gwidth*tilesize),(gheight*tilesize)

character_types = ["dev1","dev2"]
item_types = []
env_object_types = []

framerate = 30

level = Level()
objects = None
player = None