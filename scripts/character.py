"""
this file sill describe the general character class
"""
from configparser import ConfigParser, NoSectionError
from scripts.objects import GameObject
import pygame
import scripts.load_images as li
import scripts.manifest as mf
import random

character_config_folder = "resources/characters/"

directions = {
    'up':0,
    'left':1,
    'down':2,
    'right':3
}

class Character(GameObject):
    """
    the character object
    """
    def __init__(self,name, config, x = 0, y = 0):
        # some internal controll vairables
        self.animation = 0
        self.frame = 0
        self.moving = 0
        self.direction = 0
        self.speed = 0.5
        # loading the config for the character type
        parser = ConfigParser()
        parser.read(character_config_folder+config)
        # getting our size (pixels)
        size = int(parser.get("character","size"))
        # getting our base sprite name and savving our sprite image
        sprite_name = parser.get('character','single')
        sprite = pygame.image.load(li.location+'sprites/characters/'+sprite_name+'.png')
        # getting the actions we can take
        acts = parser.get('character','actions').split('\n')
        # a dict to look up actions and associated animations
        self.actions = {}
        # populating the dict
        for a in acts:
            anim_name = parser.get(a,'sheet')+'.png'
            self.actions[a]=li.load_animations(anim_name,size)
        # instancing our superclass game object
        GameObject.__init__(self,name,sprite,x,y,size)
        # getting the character's path
        # prep the variables used in paths
        self.paths = {}
        self.walk = 0
        self.current_path = None
        self.next_path = None
        # only open this 
        if 'move' in self.actions:
            # want to try opening the path
            parser.read("resources/paths/"+self.name+".pth")
            try:
                path_names = parser.get('main','paths').split('\n')
                for path_n in path_names:
                    path = []
                    path_strings = parser.get(path_n,'path').split('\n')
                    for walk in path_strings:
                        act,num = walk.split(',')
                        num = int(num)
                        path+=[act]*num
                    self.paths[path_n] = path
            except NoSectionError:
                print("no paths found for this object: "+self.name)
            
    
    def draw(self):
        """
        the function to get the current sprite
        is also the function which updates all frame-based functions
        """
        # a base return value
        rval = self.sprite
        # the rate at which frames change relative to the overall framerate
        rate = 3
        # moving up our internal frame counter
        self.frame += 1
        # doing our movement update
        self.__update_pos()
        if self.animation:
            # if we are in an animation
            if self.frame//rate >= len(self.actions[self.animation]):
                # resetting the internal frame counter
                self.frame = 0
                # changing direction randomly when idle
                # putting this here to make it less frequent
                if self.animation == 'idle' and 'move' in self.actions:
                    # only rotates when they character can move
                    # i want this to favor staying in the same direction while idle
                    a = random.randint(0,7)
                    if a >= 4:
                        a = self.direction
                    self.direction = a
            else:
                # otherwise, intend to return the current frame
                rval = self.actions[self.animation][self.frame//rate]
        else:
            # when we arent in an animation
            # and we have an idle animatin and the idle timer is up
            if ('idle' in self.actions) and (self.frame == 20*rate):
                # we attempt to go idle
                self.animate('idle')
        return pygame.transform.rotate(rval,90*self.direction)
    
    
    def animate(self, action):
        """
        this function sets the current state
        does not override any state beside idle
        """
        # there are 3 things checked:
        # that this character can do the intended animation
        # that they are not currently in an animation
        # and if they are, that they are currently in idle, which i want to be interruptable
        if action in self.actions and (not self.animation or self.animation=='idle'):
            self.animation = action
            self.frame = -1
    
    def turn(self, direction):
        """
        this function handles rotating
        """
        if type(direction) is str:
            direction = directions[direction]
        if type(direction) is int:
            self.direction = direction%4
        else:
            self.direction = 0

    def move(self, direction):
        """
        this function will be used to prepare for moving in a specific direction
        """
        if 'move' in self.actions and not self.animation == 'move':
            self.turn(direction)
            adjust_x = self.x - mf.level.startx
            adjust_y = self.y - mf.level.starty
            check_x = adjust_x + (self.direction-2)*(self.direction%2)
            check_y = adjust_y + (self.direction-1)*((self.direction+1)%2)
            if mf.level.get_tile(check_x,check_y) == 'floor':
                # need to check that the tile is movable to
                self.moving = int(mf.tilesize//(self.speed*mf.framerate))
                self.animate('move')
    
    def __done_moving(self):
        self.x += (self.direction-2)*(self.direction%2)
        self.y += (self.direction-1)*((self.direction+1)%2)
        self.offx = 0
        self.moving = 0
        self.offy = 0
        self.animation = 0
        self.frame = 0

    def __update_pos(self):
        """
        a helper function to help update offsets
        """
        if self.moving:
            if abs(self.offx) >= mf.tilesize or abs(self.offy) >= mf.tilesize:
                self.__done_moving()
            else:
                # this wonky equation means that x is only influenced when direction is left or right (1,3)
                # and that y is only influenced when direction is up or down (0,2)
                # and that it up and left will subtract from y and x respectively
                # and vice versa
                # also used in the done moving function
                self.offx += self.moving*(self.direction-2)*(self.direction%2)
                self.offy += self.moving*(self.direction-1)*((self.direction+1)%2)
    
    def get_paths(self):
        return self.paths.keys()
    
    def set_next_path(self, path):
        self.current_path = 'return'
        if path in self.paths or path is None:
            self.next_path = None