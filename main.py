import pygame
pygame.init()

size = width,height = 1080,960

bg = 255,0,0

def main():
    print("start main")
    looping = True
    screen = pygame.display.set_mode(size)
    while looping:
        # do stuff

        # update display
        # do background
        screen.fill(bg)
        # fore ground stuff
        # complete display
        pygame.display.flip()

        # at the end of the loop
        for event in pygame.event.get():
            # checking if we have our exit event
            looping = (event.type != pygame.QUIT)
        
    return "good"

if __name__ == "__main__":
    print("exit = " + main())
    print("finished")