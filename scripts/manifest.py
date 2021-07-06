"""
moved these here for convenience
these values are shared among many files
"""
from scripts.levels import Level

tilesize = 80
grid = gwidth,gheight = 16,12
invBarWidth = 4
invBarMargin = 10
# the overall size of the window in pixels
size = width,height = (gwidth*tilesize)+(invBarWidth*tilesize)+(invBarMargin*2),(gheight*tilesize)

character_types = ["dev1","dev2","player"]
item_types = []
env_object_types = []

framerate = 30

level = Level()
objects = None
player = None
def check_chars_pos(x,y,name):
    print(x,y)
    # default return of true
    rval = True
    if name != "Player" and player.x == x and player.y == y:
        # if the player is in the position
        rval = False
    else:
        for char in objects:
            # checking the other objects
            print(char.name)
            print(char.x,char.y)
            if name != char.name and char.x == x and char.y == y:
                # if the object isn't this object and is in the position
                rval = False
    return rval