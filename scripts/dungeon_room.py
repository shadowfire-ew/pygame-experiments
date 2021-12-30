"""
the dungeon room object
"""

class DungeonRoom:
    """
    the dungeon room object
    initiated with roomID

    Functions:
    - LoadRoom()
    - DeLoadRoom()

    has a publically accessible dictionary of exits
    """
    exits = {}
    
    def __init__(self,roomID):
        """
        roomId is used for loading
        """
        self._rID = roomID
    
    def LoadRoom(self):
        """
        loads the room image and details to memory
        """
        self._details = {}
        self._im = None
    
    def DeLoadRoom(self):
        """
        de-loads the room objects and details from memory
        without deleting the room
        """
        self._details = {}
        self._im = None

    def GetDetail(self,key):
        """
        returns the value of the internal details dictionary
        """
        return self._details[key]
    
    def GetImage(self):
        """
        returns the image of the room
        """
        return self._im

    def IsLoaded(self):
        """
        returns true if the room is already loaded
        """
        return self._im is not None