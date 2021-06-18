from scripts.load_tile_table import load_tile_table
import pygame

size = width,height = 1280,960
# planning for 80x80 tiles
#would make the grid 16 , 12

bg = 115,0,115

images = "resources/images/"

def main():
    pygame.init()
    print("start main")
    looping = True
    screen = pygame.display.set_mode(size)

    floors = load_tile_table(images+"/tilesets/lab-tiles.png",[80])
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
        # do background
        screen.fill(bg)
        # fore ground stuff
        # complete display
        pygame.display.flip()

        
    return "good"

if __name__ == "__main__":
    print("exit = " + main())
    print("finished")