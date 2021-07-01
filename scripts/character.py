"""
this file sill describe the general character class
"""
from configparser import ConfigParser
from scripts.objects import GameObject
import pygame
import scripts.load_images as li

character_config_folder = "resources/characters/"

class Character(GameObject):
    """
    the character object
    """
    def __init__(self,name, config, x = 0, y = 0):
        # some internal controll vairables
        self.animation = 0
        self.frame = 0
        self.move = 0
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
    
    def draw(self):
        """
        the function to get the current sprite
        """
        # a base return value
        rval = self.sprite
        # the rate at which frames change relative to the overall framerate
        rate = 2
        # moving up our internal frame counter
        self.frame += 1
        if self.animation:
            # if we are in an animation
            if self.frame//rate >= len(self.actions[self.animation]):
                # resetting the internal frame counter
                self.frame = 0
                # resetting our current animation
                # to be removed when improving idle
                self.animation = 0
            else:
                # otherwise, intend to return the current frame
                rval = self.actions[self.animation][self.frame//rate]
        else:
            # when we arent in an animation
            # and we have an idle animatin and the idle timer is up
            if ('idle' in self.actions) and (self.frame == 20*rate):
                # we attempt to go idle
                self.animate('idle')
        return rval
    
    
    def animate(self, action):
        if action in self.actions and not self.animation:
            self.animation = action
            self.frame = -1