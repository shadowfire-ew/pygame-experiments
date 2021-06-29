import scripts.layout as ly
class GameObject:
    """
    the base object from which all other objects inherit
    """
    def __init__(self,name,sprite,x,y, width, height = None):
        self.name = name
        self.x = x
        self.y= y
        self.width = width
        self.height = height
        self.sprite = sprite
    
    def draw(self):
        return self.sprite
    
    def get_position(self):
        return (self.x,self.y)
    
    def get_location(self):
        tx = self.x*ly.tilesize + (ly.tilesize-self.width)
        ty = self.x*ly.tilesize + (ly.tilesize-self.height)