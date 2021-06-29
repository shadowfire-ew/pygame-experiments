"""
this file sill describe the general character class
"""
from configparser import ConfigParser
from scripts.objects import GameObject
import pygame
import scripts.load_images as li
import scripts.layout as ly

character_config_folder = "resources/characters/"

class Character(GameObject):
    """
    the character object
    """
    def __init__(self,name, config, x = 5, y = 5):
        self.animation = 0
        self.frame = 0
        self.actions = {}
        parser = ConfigParser()
        parser.read(character_config_folder+config)
        sprite_name = parser.get('character','single')
        print('"'+sprite_name+'"')
        sprite = pygame.image.load(li.location+'sprites/characters/'+sprite_name+'.png')
        acts = parser.get('character','actions').split('\n')
        for a in acts:
            anim_name = parser.get(a,'sheet')+'.png'
            self.actions[a]=li.load_animations(anim_name,ly.tilesize)
        GameObject.__init__(self,name,sprite,x,y,ly.tilesize)
    
    def draw(self):
        """
        the function to get the current sprite
        """
        rval = self.sprite
        rate = 50
        self.frame += 1
        if self.animation:
            if self.frame//rate >= len(self.actions[self.animation]):
                self.frame = 0
                self.animation = 0
            else:
                rval = self.actions[self.animation][self.frame//rate]
        else:
            if ('idle' in self.actions) and (self.frame == 20*rate):
                self.animate('idle')
        return rval
    
    
    def animate(self, action):
        if action in self.actions and not self.animation:
            self.animation = action
            self.frame = -1