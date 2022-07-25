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
    mf.load_level("dev.map")

    #initializing the player
    #TODO: Make player position dynamic with level loading (looking for elevator name 'entrance' perhaps?)
    player = mf.player
    player.x = 10
    player.y = 7

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
                    print(mf.characters[1].get_paths())
                elif event.key == pygame.K_h:
                    mf.characters[1].set_next_path(None)
                elif event.key == pygame.K_c:
                    mf.characters[1].set_next_path('circle')
                elif event.key == pygame.K_m:
                    mf.characters[1].set_next_path('mozy')
                elif event.key == pygame.K_e:
                    print(player.find_path(5,6))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx,my =  pygame.mouse.get_pos()
                # normalize mouse position to tile number
                dx,dy = mx//mf.tilesize,my//mf.tilesize
                # determine if the click is within bounds
                if 0<=dx<mf.gwidth and 0<=dy<mf.gheight:
                    player.goto((dx,dy))
                

            # checking if we have our exit event
            looping = (event.type != pygame.QUIT)

        # actually exiting
        if not looping: break
        
        # update display
        # clear background
        screen.fill(bg)
        # update the background
        screen.blit(mf.level_image,(0,0))
        # the overlays
        # fore ground stuff
        for char in mf.characters:
            image = char.draw()
            pos = char.get_location()
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