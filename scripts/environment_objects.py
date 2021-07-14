"""
holds the environment objects and associated code
"""

from configparser import ConfigParser
from scripts.objects import GameObject
import pygame
import scripts.load_images as li
import scripts.manifest as mf
import abc

env_obj_configs = "resources/environment_objects/"

class EnvironmentObject(GameObject, abc.Abc):
    """
    the environment object class
    i want these to be drawn in the background (behind characters)
    but have their action animations be overlays in the foreground (on top of characters)
    i think that i will have specific game objects be subclasses
    """
    def __init__(self,name,target,config,x=0,y=0):
        # open config
        parser = ConfigParser()
        parser.read(env_obj_configs+config)
        # get the sprite
        sprite_name = parser.get("details","sprite")
        sprite = pygame.image.load(li.location+'sprites/environment/'+sprite_name+'.png')
        # get our size
        size = int(parser.get("details","size"))
        # do our superclass initializer
        GameObject.__init__(self,name,sprite,x,y,size)
        # get the animation
        anim = parser.get('details','animation')
        self.animation = li.load_animations(anim,size,type='environment')
        # getting our destination
        self.destination = parser.get('details','destination')
        # can we be walked on?
        travel = parser.get('details','traversable')
        if travel == 'true':
            self.traversable = True
        else:
            self.traversable = False
        # control variables
        self.frame = -1
    
    @abc.abstractclassmethod
    def do_action(self,character):
        """
        this is the function which must behave differently per type
        and i don't feel like writing case-by-case if's
        this will be called whenever a character somehow interracts with the object
        """
        pass

    def get_overlay(self):
        """
        returns the animation for this object, if it is currently running
        """
        rval = None
        if 0 <= self.frame < len(self.animation):
            rval = self.animation[self.frame]
            self.frame+=1
        return rval
    
class Elevator(EnvironmentObject):
    """
    the elevator class
    only overrides the do_action function
    """
    def do_action(self, character):
        if character == mf.player:
            # do stuff