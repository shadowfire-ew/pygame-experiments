from scripts.levels import Level
from scripts.load_tile_table import load_tile_table
import scripts.layout as ly
import pygame

bg = 115,0,115

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
    screen = pygame.display.set_mode(ly.size)


    # loading the level
    test_level = Level()
    test_level.load_file("dev.map")
    level_image, level_overlay = test_level.render()

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
        # the overlays
        # fore ground stuff
        # complete display
        pygame.display.flip()

    # returning a code
    return "good"

if __name__ == "__main__":
    print("exit = " + main())
    print("finished")