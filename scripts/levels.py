from pygame import ConfigParser

maps_folder="resources/maps/"
#decided on a shared tile type, because this is just an experiment
key = {
    '.':"hole",
    '#':"floor",
    '%':"wall",
    '^':"water"
}

class Level(object):
    def load_file(self, filename):
        self.map = []
        parser = ConfigParser.ConfigParser()
        parser.read(maps_folder+"filename")
        self.tileset = parser.get("level","tileset")
        self.map = parser.get("level","map").split('\n')
        self.width = len(self.map[0])
        self.height = len(self.map)
    
    def get_tile(self, x, y):
        try:
            char = self.map[y,x]
            # speculation:
            # it searches by y,x because of how it is laid out
            # i.e, in 
            #[[a,b,c],
            # [d,e,f]]
            # y goes from top to bottom
            # and x goes from left to right
        except IndexError:
            return {}
        try:
            return key[char]
        except KeyError:
            return {}
    
    def render(self, width, height):
        """
        will create an image of the map
        and also an overlay image of the borders

        width, is the grid width, height is the grid height
        """
        # find a way to center the level in the image
        startx = width//2 - self.width//2
        starty = height//2 - self.height//2