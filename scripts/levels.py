import scripts.character as cr
import scripts.load_images as li
import pygame
from configparser import ConfigParser
import scripts.manifest as mf

maps_folder="resources/maps/"
#decided on shared tile types, because this is just an experiment
key = {
    '.':"hole",
    'f':"floor",
    '+':"wall",
    '^':"water"
}

# TODO: have a procedural/random level generation algorithm (i.e. wavefunction collapse, gausian sound?)
class Level:
    def load_file(self, filename):
        self.map = []
        parser = ConfigParser()
        name = maps_folder+filename
        parser.read(name)
        self.tileset = parser.get("level","tileset")
        self.map = parser.get("level","map").split('\n')
        self.width = len(self.map[0])
        self.height = len(self.map)
        population = parser.get("level","population")
        self.characters = []
        if population != "none":
            population = population.split('\n')
            for individual in population:
                itype = parser.get(individual,"type")
                ix = int(parser.get(individual,"x"))
                iy = int(parser.get(individual,"y"))
                self.characters.append([individual,itype,ix,iy])
        # find a way to center the level in the image
        self.startx = mf.gwidth//2 - self.width//2
        self.starty = mf.gheight//2 - self.height//2
    
    def get_tile(self, x, y):
        char = '+'
        try:
            if (0<=x<self.width) and (0<= y < self.height):
                char = self.map[y][x]
            # speculation:
            # it searches by y,x because of how it is laid out
            # i.e, in 
            #[[a,b,c],
            # [d,e,f]]
            # y goes from top to bottom
            # and x goes from left to right
        except IndexError:
            print("error getting char")
            # returns a dict to cause an error
            return {}
        try:
            return key[char]
        except KeyError:
            print("error getting key[char]")
            # returns a dict to cause an error
            return {}
    
    def render(self):
        """
        will create an image of the map
        and also an overlay image of the borders

        width, is the grid width, height is the grid height
        """
        

        # load the images
        tiles = li.load_tile_table(self.tileset+"-tiles.png", mf.tilesize)
        borders = li.load_tile_table(self.tileset+"-borders.png", mf.tilesize//2)

        # prepare the canvas
        image = pygame.Surface(mf.size)

        # filling the canvas
        for x in range(mf.gwidth):
            for y in range(mf.gheight):
                # the background tiles
                tile=-1
                nx = x - self.startx
                ny = y - self.starty
                # the get_tile now handles when the nx and ny are out of range
                label = self.get_tile(nx,ny)
                tile = li.base[label]
                # getting the tile from the table
                tile_image = tiles[tile][0]
                # applying the image
                image.blit(tile_image,(x*mf.tilesize,y*mf.tilesize))
                # now for the overlays
                if (-1<=nx<=self.width) and (-1<=ny<=self.height):
                    # only need to worry about the tiles in and directly around the map
                    # checking the adjacency of the corners
                    # this list is for contoll
                    ls = [-1,1]
                    for TB in ls:
                        # top-bottom
                        for LR in ls:
                            # left-right (of tile)
                            type = 0
                            #finding the neighbors of this corner
                            a = (label != self.get_tile(nx+LR,ny))
                            b = (label != self.get_tile(nx,ny+TB))
                            # these if's determine which type of corner
                            # 0 is convex or none
                            # 1 is flat
                            # 2 is concave
                            if a:
                                type += 1
                            if b:
                                type += 1
                            if type == 0 and label == self.get_tile(nx+LR,ny+TB):
                                # when all of the neighbors of that corner are the same
                                type = 3
                            # now to add the image
                            if type != 3:
                                # normalizing the TB and LR to 0-1
                                TBa = (TB+1)//2
                                LRa = (LR +1)//2
                                # the base angle of rotation
                                angle = (TBa*(90)+LRa*(90))*(LR)+90
                                # handling wrong angle errors
                                # my initially noticed errors were the corners of differing TB/LR
                                if (TB != LR):
                                    angle -= 180
                                # my remaining errors were only flats
                                if type == 1:
                                    if (a and (TB != LR)) or (b and (TB == LR)):
                                        angle -= 90
                                #getting and rotating the image
                                border_image = pygame.transform.rotate(borders[tile][type],angle)
                                # our x and y for the border image
                                bx = x + LRa/2
                                by = y + TBa/2
                                image.blit(border_image,(bx*mf.tilesize,by*mf.tilesize))
        
        # preparing the objects
        objects = []
        for object in self.characters:
            name, type, ix, iy = object
            if type in mf.character_types:
                char = cr.Character(name, type, ix+self.startx, iy+self.starty)
                objects.append(char)
            else:
                # because population should only be characters
                raise Exception("Population must be only characters. "+type+" not found in manifest")
        return image, objects