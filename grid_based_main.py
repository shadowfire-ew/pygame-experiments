import scripts.character as cr
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
    test_level = mf.level
    test_level.load_file("dev.map")
    level_image, mf.objects = test_level.render()
    level_objects = mf.objects

    #initializing the player
    mf.player = cr.Character("Player","player.char", 10, 7)
    player = mf.player

    while True:
        #main loop
        
        for event in pygame.event.get():
            # checking the event queue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.move('left')
                elif event.key == pygame.K_RIGHT:
                    player.move('right')
                elif event.key == pygame.K_UP:
                    player.move('up')
                elif event.key == pygame.K_DOWN:
                    player.move('down')
                elif event.key == pygame.K_p:
                    print(level_objects[1].get_paths())
                elif event.key == pygame.K_h:
                    level_objects[1].set_next_path(None)
                elif event.key == pygame.K_c:
                    level_objects[1].set_next_path('circle')
                elif event.key == pygame.K_m:
                    level_objects[1].set_next_path('mozy')

            # checking if we have our exit event
            looping = (event.type != pygame.QUIT)

        # actually exiting
        if not looping: break
        
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
        # the player
        image = player.draw()
        pos = player.get_location()
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