from scripts.character import Character
from scripts.levels import Level
import scripts.manifest as mf
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
    screen = pygame.display.set_mode(mf.size)
    pygame.display.set_caption("Grid-Based Game Test")

    # Setting up the fps
    fpsClock = pygame.time.Clock()

    # loading the level
    test_level = Level()
    test_level.load_file("dev.map")
    level_image, level_objects = test_level.render()

    i = 0

    while True:
        #main loop
        
        for event in pygame.event.get():
            # checking the event queue

            # checking if we have our exit event
            looping = (event.type != pygame.QUIT)

        # actually exiting
        if not looping: break
        # do stuff

        i += 4
        if (i >= 400):
            level_objects[1].turn(i)
            i -=399

        # update display
        # clear background
        screen.fill(bg)
        # update the background
        screen.blit(level_image,(0,0))
        # the overlays
        # fore ground stuff
        for obj in level_objects:
            image = obj.draw()
            pos = obj.get_location()
            screen.blit(image,pos)
        # complete display
        pygame.display.flip()
        # ticking the clock to allow consistent framerate
        fpsClock.tick(mf.framerate)

    # returning a code
    return "good"

if __name__ == "__main__":
    print("exit = " + main())
    print("finished")