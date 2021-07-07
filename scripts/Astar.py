"""
making a* its own function in a module
"""

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
        this is our heuristic
        """
        return abs(self.x-x)+abs(self.y-y)
    def path_to(self):
        if self.parent is not None:
            return self.parent.path_to()+[(self.x,self.y)]
        else:
            return [(self.x,self.y)]

class Priority_Queue:
    def __init__(self,object,priority):
        self.obj = object
        self.priority = priority
        self.next = None
    
    def enqueue(self,other):
        if self.priority > other.priority:
            # doing this so that lower priority comes first
            other.enqueue(self)
    
    def dequeue(self):
        return self.object,self.next