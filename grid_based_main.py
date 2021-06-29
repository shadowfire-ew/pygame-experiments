from scripts.character import Character
from scripts.levels import Level
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
    pygame.display.set_caption("Grid-Based Game Test")


    # loading the level
    test_level = Level()
    test_level.load_file("dev.map")
    level_image, level_objects = test_level.render()

    # loading a test character
    test_char = Character('Chili','dev.char')
    level_objects.append(test_char)

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
        screen.blit(level_image,(0,0))
        # the overlays
        # fore ground stuff
        for obj in level_objects:
            image = obj.draw()
            pos = obj.get_location()
            screen.blit(image,pos)
        # complete display
        pygame.display.flip()

    # returning a code
    return "good"

if __name__ == "__main__":
    print("exit = " + main())
    print("finished")