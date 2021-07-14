"""
moved these here for convenience
these values are shared among many files
"""
from scripts.levels import Level
import scripts.character as cr

# layout features
# size of tiles in pixels
tilesize = 80
# the grid's size in tiles
grid = gwidth,gheight = 16,12
# the width of the inentory bar in tiles
invBarWidth = 4
# the width of the margin on both sides of the inventory bar, in pixels
invBarMargin = 10
# the overall size of the window in pixels
size = width,height = (gwidth*tilesize)+(invBarWidth*tilesize)+(invBarMargin*2),(gheight*tilesize)

# object types
character_types = ["dev1","dev2","player"]
item_types = []
env_object_types = ["teleporter","elevator","chest"]

# system framerate
# calculations are framerate-dependant
framerate = 30

# storage of some globally accessed features, such as the level
level = Level()
objects = None
player = cr.Character("Player","player.char", 10, 7)

# a helper function
def check_chars_pos(x,y,name):
    # default return of true, meaning this space is empty
    # will eventually do some logic for different object types, like items and teleporters
    rval = True
    if name !=player and ((player.x == x and player.y == y)or (x,y)==player.moving_to()):
        # if the player is in the position
        rval = False
    else:
        for char in objects:
            # checking the other objects
            if name != char and ((char.x == x and char.y == y) or (x,y)==char.moving_to()):
                # if the object isn't this object and is in the position
                # or the object is moving to the position
                rval = False
    return rval