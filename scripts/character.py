"""
this file sill describe the general character class
"""
from configparser import ConfigParser, NoSectionError
from scripts.objects import GameObject
import pygame
import scripts.load_images as li
import scripts.manifest as mf
import random
from queue import PriorityQueue

character_config_folder = "resources/characters/"

directions = {
    'up':0,
    'left':1,
    'down':2,
    'right':3
}

modes = {
    "stationary":[],
    "walk":["floor"],
    "swim":["water"],
    "amphibous":["water","floor"],
    "fly":["floor","hole","water"],
    "ghost":["floor","hole","water","wall"]
}

def direction_to_change(direction):
    """
    this wonky equation means that x is only influenced when direction is left or right (1,3)
    and that y is only influenced when direction is up or down (0,2)
    such that up and left will subtract from y and x respectively
    and vice versa
    """
    return (direction-2)*(direction%2), (direction-1)*((direction+1)%2)

class Character(GameObject):
    """
    the character object
    """
    def __init__(self,name, config, x = 0, y = 0):
        # some internal controll vairables
        self.animation = 0
        self.frame = 0
        self.moving = 0
        self.direction = 0
        self.speed = 0.5
        # loading the config for the character type
        parser = ConfigParser()
        parser.read(character_config_folder+config)
        # getting our size (pixels)
        size = int(parser.get("character","size"))
        # getting our idle wait timer
        # it is stored as seconds on the config
        self.idle_time = int(parser.get("character","idle"))*mf.framerate
        # getting our movement mode
        self.mode = parser.get("character","mode")
        # getting our base sprite name and savving our sprite image
        sprite_name = parser.get('character','single')
        sprite = pygame.image.load(li.location+'sprites/characters/'+sprite_name+'.png')
        # getting the actions we can take
        acts = parser.get('character','actions').split('\n')
        # a dict to look up actions and associated animations
        self.actions = {}
        # populating the dict
        for a in acts:
            anim_name = parser.get(a,'sheet')+'.png'
            if a != "return":
                # our reserved path name
                self.actions[a]=li.load_animations(anim_name,size)
            else:
                raise Exception("'return' is a reserved path name")
        # instancing our superclass game object
        GameObject.__init__(self,name,sprite,x,y,size)
        # getting the character's path
        # prep the variables used in paths
        # our current paths
        self.paths = {}
        # some controll variables
        self.walk_timer = 0
        self.current_path = None
        self.next_path = None
        self.wait_timer = 0
        self.wait_ammount = 0
        self.path_timer = 0
        self.destination = None
        self.nogos = 0
        # the home x and home y are the home square
        self.home_x = self.x
        self.home_y = self.y
        self.home = self.home_x,self.home_y
        # only open this 
        if 'move' in self.actions:
            # want to try opening the path
            parser.read("resources/paths/"+self.name+".pth")
            try:
                path_names = parser.get('main','paths').split('\n')
                for path_n in path_names:
                    path = []
                    path_strings = parser.get(path_n,'path').split('\n')
                    for walk in path_strings:
                        x,y = walk.split(',')
                        y = int(y)
                        try:
                            # try to make x an int
                            x = int(x)
                        except Exception:
                            # if it cannot be an int, then it should be left as is
                            pass
                        path.append((x,y))
                    self.paths[path_n] = path
            except NoSectionError:
                print("no paths found for this object: "+self.name)
            
    
    def draw(self):
        """
        the function to get the current sprite
        is also the function which updates all frame-based functions
        """
        # a base return value
        rval = self.sprite
        # the rate at which frames change relative to the overall framerate
        rate = 3
        # moving up our internal frame counter
        self.frame += 1
        # doing our movement update
        self.__update_pos()
        # checking our path and updating our waiting
        if not self.__do_waiting(): self.__walk()
        if self.animation:
            # if we are in an animation
            if self.frame//rate >= len(self.actions[self.animation]):
                # resetting the internal frame counter
                self.frame = 0
                # changing direction randomly when idle
                # putting this here to make it less frequent
                if self.animation == 'idle' and 'move' in self.actions:
                    # only rotates when they character can move
                    # i want this to favor staying in the same direction while idle
                    a = random.randint(0,7)
                    if a >= 4:
                        a = self.direction
                    self.direction = a
            else:
                # otherwise, intend to return the current frame
                rval = self.actions[self.animation][self.frame//rate]
        else:
            # when we arent in an animation
            # and we have an idle animatin and the idle timer is up
            if ('idle' in self.actions) and (self.frame >= self.idle_time):
                # we attempt to go idle
                self.animate('idle')
        return pygame.transform.rotate(rval,90*self.direction)
    
    
    def animate(self, action):
        """
        this function sets the current state
        does not override any state beside idle
        """
        # there are 3 things checked:
        # that this character can do the intended animation
        # that they are not currently in an animation
        # and if they are, that they are currently in idle, which i want to be interruptable
        if action in self.actions and (not self.animation or self.animation=='idle'):
            self.animation = action
            self.frame = -1
    
    def turn(self, direction):
        """
        this function handles rotating
        """
        if type(direction) is str:
            direction = directions[direction]
        if type(direction) is int:
            self.direction = direction%4
        else:
            self.direction = 0

    def move(self, direction):
        """
        this function will be used to prepare for moving in a specific direction
        """
        if 'move' in self.actions and not self.animation == 'move' and not self.__waiting():
            self.turn(direction)
            c_x , c_y = direction_to_change(self.direction)
            check_x = self.x + c_x
            check_y = self.y + c_y
            if self.can_enter(check_x,check_y):
                # need to check that the tile is movable to
                self.moving = int(mf.tilesize//(self.speed*mf.framerate))
                self.animate('move')
                # when this object can move
                return True
        # default return value, when the object cannot move
        return False
    
    def __done_moving(self):
        """
        a function to be called when the character reaches its desitnation
        """
        # get the adjustment ammount for our x and y
        c_x , c_y = direction_to_change(self.direction)
        # adjusting our x and y
        self.y += c_y
        self.x += c_x
        # we are no longer moving
        self.moving = 0
        # our visual offset no longer needs to be anything
        self.offx = 0
        self.offy = 0
        # stop our animation
        self.animation = 0
        self.frame = 0

    def __update_pos(self):
        """
        a helper function to help update offsets
        """
        if self.moving:
            # if we have any moving ammount
            if abs(self.offx) >= mf.tilesize or abs(self.offy) >= mf.tilesize:
                # when we reach our destination
                self.__done_moving()
            else:
                # otherwise, just adjust our visual offset according to our direction
                c_x , c_y = direction_to_change(self.direction)
                self.offx += self.moving*c_x
                self.offy += self.moving*c_y
    
    def get_paths(self):
        "just returns the list of path names this character can take"
        return self.paths.keys()
    
    def set_next_path(self, path):
        """
        sets the next path for this character
        the character will first attempt to go home before traversing the path
        """
        self.current_path = 'return'
        if path in self.paths or path is None:
            self.next_path = path
            self.walk_timer = 0
            self.wait(0)

    def wait(self, time):
        """
        makes the character stop moving for the specified time
        time must be seconds
        """
        self.wait_timer = 0
        self.wait_ammount = time*mf.framerate
    
    def can_enter(self, x, y):
        """
        checks if this character can enter a given square
        """
        # adjusted co-ordinates for the level
        adjust_x = x - mf.level.startx
        adjust_y = y - mf.level.starty
        return mf.level.get_tile(adjust_x,adjust_y) in modes[self.mode] and mf.check_chars_pos(x,y,self.name)
    
    def find_path(self, pos = None):
        """
        trys to find a path pased on current world situation to the destination
        maybe going to try a modified verison of A*
        """
        if pos is None:
            pos = self.home
        x,y = pos
        if not self.can_enter(x,y):
            # don't even try if destination is occupied or untraversable
            return "occupied"
        else:
            # setting up the frontier/edge
            edge = PriorityQueue()
            # our starting node
            start = (self.x,self.y)
            # stored like this to sort by priority
            edge.put((0,start))
            # our end node for checking equality
            end = (x,y)
            # the relative costs to get to the nodes
            costs = {}
            # the cost of the start is 0
            costs[start] = 0
            # the parents of the nodes, for backtracing
            parents = {}
            # the start has no parents, for an end condition
            parents[start] = None

            # while we still have enqueued objects 
            while not edge.empty():
                p,node = edge.get()
                if node == end:
                    # do stuff to find relative path
                    # perhaps convert it into a string series of directions?
                    nodes = []
                    cnode = node
                    while cnode is not None:
                        nodes.append(cnode)
                        cnode = parents[cnode]
                    walk = []
                    pnode = nodes[-1]
                    for cnode in nodes[-2::-1]:
                        sx,sy = pnode
                        nx,ny = cnode
                        if sx<nx:
                            walk.append('right')
                        elif sx>nx:
                            walk.append('left')
                        elif sy<ny:
                            walk.append('down')
                        elif sy>ny:
                            walk.append('up')
                        pnode = cnode
                    return walk
                
                for next in self.neighbor_cells(node):
                    # using + 1 because I want to treat all cells as equal, for now
                    new_cost = costs[node] + 1
                    if next not in costs or new_cost < costs[next]:
                        costs[next] = new_cost
                        # using taxicab distance as heuristic
                        h = abs(end[0]-next[0])+abs(end[1]-next[1])
                        priority = new_cost+h
                        edge.put((priority,next))
                        parents[next] = node
                
            # if we do not find the path, we will end up here
            return "blocked"

    def neighbor_cells(self,pos=None):
        """
        a function which takes a postition and returns the traversable neighbors of it
        if no position is provided, the character's position is used
        """
        if pos is None:
            pos = (self.x,self.y)
        
        rval = []

        for a in [-1,1]:
            b = (pos[0]+a,pos[1])
            if self.can_enter(b[0],b[1]):
                rval.append(b)
            c = (pos[0],pos[1]+a)
            if self.can_enter(c[0],c[1]):
                rval.append(c)
        return rval

    def __waiting(self):
        """
        does checking on the wait timer
        """
        return 0 < self.wait_ammount
    
    def __do_waiting(self):
        """""
        does the waiting arithametic
        returns true or false based on if the object is waiting at the time of checking
        """
        if self.__waiting():
            self.wait_timer += 1
            if self.wait_timer >= self.wait_ammount:
                # when we pass the wait timer
                # we set our waiting to 0
                self.wait(0)
            return True
        else:
            return False
    
    def __walk(self):
        """
        this function is what controls how the chracter moves
        it allows the character to wlak along it's designated path nodes
        it needs to be called (almost) every loop (and thus, in the draw function)
        """
        if not self.moving and self.__follow_path():
            # don't want to do any of these checks when moving
            # nor when we are still on a path
            # if we have this path
            if self.current_path in self.paths:
                # if we haven't finished the path
                if self.walk_timer < len(self.paths[self.current_path]):
                    # get the next step
                    step = (self.paths[self.current_path][self.walk_timer])
                    # if the step is a movement
                    if type(step[0]) is int:
                        self.goto(step)
                    else:
                        # otherwise, we just wait for the time
                        self.wait(step[1])
                    # get ready for the next step
                    self.walk_timer += 1
                else:
                    # and when we have finished the path, we just go home and do nothing
                    self.set_next_path(None)
            # when our path is to return. thus, we want to make return a reserved keyword, 
            # and should probably throw an exception when parsing the paths
            elif self.current_path == 'return':
                # when we need to go home
                if self.pos == self.home:
                    self.current_path = self.next_path
                    self.next_path = None
                else:
                    self.goto()

    def __follow_path(self):
        """
        this function will do all the checking for the pathfinding
        will return true when the path is complete
        or when we are not currently following a path
        """
        if self.destination:
            # only want to check these if we have a destination to go to
            # when we are not done walking the path
            if self.pos != self.destination and self.path_timer < len(self.path_to_walk):
                # get the next desination
                success = self.move(self.path_to_walk[self.path_timer])
                if not success:
                    # if our path is blocked since we found the path
                    # recalculate the path
                    self.goto(self.destination)
                self.path_timer += 1
                return False
            else:
                self.destination = None
                return True
        else:
            return True

    
    def goto(self,pos = None):
        if pos is None:
            pos = self.home
        self.destination = pos
        path = self.find_path(pos)
        if path == "occupied" or path == "blocked":
            # just wait a seccond to see if the path becomes unblocked
            self.wait(1)
            # also have an internal timer for if our path is blocked too many times
            self.nogos +=1
            if self.nogos >= 5:
                # when that happens, we go home and do nothing
                self.set_next_path(None)
        else:
            self.path_to_walk = path
            self.path_timer = 0
            self.nogos = 0
