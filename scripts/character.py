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
        super.__init__(self,name,sprite,x,y,ly.tilesize)
    
    def draw(self):
        """
        the function to get the current sprite
        """
        rval = None
        self.frame += 1
        if self.animation:
            rval = self.actions[self.animation][self.frame]
            if self.frame >= len(self.actions[self.animation]):
                self.frame = 0
                self.animation = 0
        else:
            if ('idle' in self.actions) and (self.frame == 30):
                self.animate('idle')
            rval = self.sprite()
    
    
    def animate(self, action):
        if action in self.actions and not self.animation:
            self.animation = action
            self.frame = -1