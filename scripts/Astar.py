"""
making a* its own function in a module
"""
from queue import PriorityQueue

class Node:
    """
    a lightweight node class
    """
    def __init__(self,x,y, parent = None):
        self.x = x
        self.y = y
        self.parent = parent
        if parent is not None:
            self.cost = parent.cost + 1
        else:
            self.cost = 0
    def taxi_to(self,x,y):
        """
        returns the taxicab distance to a given destination
        this is our heuristic (h)
        """
        return abs(self.x-x)+abs(self.y-y)
    def path_to(self):
        """
        returns a list of co-ordinate pairs
        """
        if self.parent is not None:
            return self.parent.path_to()+[(self.x,self.y)]
        else:
            return [(self.x,self.y)]
    def get_f(self,x,y):
        """
        our f function
        """
        return self.cost + self.taxi_to(x,y)
    def __eq__(self, o: object) -> bool:
        return self.x == o.x and self.y == o.y
    def get_pos(self):
        return (self.x,self.y)



def Astar_char(character,goal_x,goal_y):
    start_x = character.x
    start_y = character.y
    blocked = []
    visited = {}
    start_node = Node(start_x,start_y)
    edge = PriorityQueue()
    while head is not None:
        node, head = head.dequeue()
        if node == end_node:
            # when we find our node
            return node.path_to()
        
        neighbors = [(node.x-1,node.y),(node.x+1,node.y),(node.x,node.y-1),(node.x,node.y+1)]
        for neighbor in neighbors:
            # check if we already blacklisted this square
            if neighbor not in blocked:
                neighbor_node = Node(neighbor[0],neighbor[1],node)
        