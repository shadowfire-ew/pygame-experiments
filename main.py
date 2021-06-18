import pygame
pygame.init()

size = width,height = 1280,960
# planning for 80x80 tiles
#would make the grid 16 , 12

bg = 255,0,255

def main():
    print("start main")
    looping = True
    screen = pygame.display.set_mode(size)
    while True:
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