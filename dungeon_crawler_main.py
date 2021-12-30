"""
something to test out my dungeon crawler concept

because of the way rooms are generated, 
over-all dungeon layouts will not make sense in euclidean space
"""

from scripts.dungeon_room import DungeonRoom


class DungeonGame:
    """
    the class that controlls the game
    """
    def __init__(self):
        self._startRoom = DungeonRoom("starter")
        self._playerRoom = self._startRoom
        self._startRoom.LoadRoom()
    
    def Draw(self):
        """
        draws the room and objects within
        """
        roomim = self._playerRoom

    def GenerateNeighbors(self):
        """
        randomly generates the neighbor rooms
        sets the cardinal rooms of the current room object
        as informed by the details of the room
        """

    def ChangeRoom(self,direction):
        """
        lets player enter the next room
        """
        oldroom = self._playerRoom
        try:
            self._playerRoom = self._playerRoom.exits[direction]
        except KeyError:
            print("room unavailable")
            return
        self._playerRoom.LoadRoom()
        oldroom.DeLoadRoom()
        self.GenerateNeighbors()