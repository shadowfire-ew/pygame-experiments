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
