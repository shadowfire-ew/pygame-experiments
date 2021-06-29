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
        tx = self.x*ly.tilesize + (ly.tilesize-self.width)
        ty = self.x*ly.tilesize + (ly.tilesize-self.height)
        return(tx,ty)