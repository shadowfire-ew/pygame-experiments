import scripts.manifest as mf
import abc
class GameObject(abc.ABC):
    """
    the base object from which all other objects inherit
    """
    def __init__(self,name,sprite,x,y, width, height = None):
        self.name = name
        self.x,self.y = x,y
        self.offx = 0
        self.offy = 0
        self.width = width
        if height is None:
            height = width
        self.height = height
        self.sprite = sprite
    
    def draw(self):
        return self.sprite
    
    def get_position(self):
        "returns grid co-ords"
        return (self.x,self.y)
    
    def get_location(self):
        "returns the true location in the image"
        tx = self.x*mf.tilesize + (mf.tilesize-self.width)//2 + self.offx
        ty = self.y*mf.tilesize + (mf.tilesize-self.height)//2 + self.offy
        return(tx,ty)