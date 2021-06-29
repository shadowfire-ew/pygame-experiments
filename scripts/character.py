"""
this file sill describe the general character class
"""
from configparser import ConfigParser
import pygame
import scripts.load_images as li

character_config_folder = "resources/characters/"

class Character:
    """
    the character object
    """
    def __init__(self,name, config, x = 5, y = 5):
        self.name = name
        self.x = x
        self.y = y
        self.actions = {}
        parser = ConfigParser()
        parser.read(character_config_folder+config)
        sprite_name = parser.get('character','single')
        print('"'+sprite_name+'"')
        self.sprite = pygame.image.load(li.location+'sprites/characters/'+sprite_name+'.png')
        acts = parser.get('character','actions').split('\n')
        for a in acts:
            anim_name = parser.get(a,'sheet')+'.png'
            self.actions[a]=li.load_animations(anim_name,80)