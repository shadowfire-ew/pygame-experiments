from scripts.load_tile_table import load_tile_table
import pygame


tilesize = 80
grid = gwidth,gheight = 16,12
size = width,height = (gwidth*tilesize),(gheight*tilesize)
# planning for 80x80 tiles
# would make the grid 16 , 12

bg = 115,0,115

images = "resources/images/"

def main():
    """
    the main function
    contains the main loop

    returns strings with statuses
    """
    pygame.init()
    # controll variable
    looping = True
    # setting up the screen
    screen = pygame.display.set_mode(size)

    tiles = load_tile_table(images+"/tilesets/lab-tiles.png",[tilesize])
    borders = load_tile_table(images+"/tilesets/lab-borders.png",[tilesize//2])
    while True:
        #main loop
        
        for event in pygame.event.get():
            # checking the event queue

            # checking if we have our exit event
            looping = (event.type != pygame.QUIT)

        # actually exiting
        if not looping: break
        # do stuff

        # update display
        # clear background
        screen.fill(bg)
        # update the background
        for x in range(gwidth):
            for y in range(gheight):
                screen.blit(tiles[(x//4)%2][(y//3)%2],(x*80,y*80))
        # the overlays
        
        # fore ground stuff
        # complete display
        pygame.display.flip()

    # returning a code
    return "good"

if __name__ == "__main__":
    print("exit = " + main())
    print("finished")