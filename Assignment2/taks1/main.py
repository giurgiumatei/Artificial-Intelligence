from Service import *


# define a main function
def main():

    # we create the map
    m = Map()
    #m.randomMap()
    #m.saveMap("test2.map")
    m.loadMap("test1.map")


    # initialize the pygame module
    pygame.init()
    # load and set the logo
    logo = pygame.image.load("logo32x32.png")
    pygame.display.set_icon(logo)
    pygame.display.set_caption("Path in simple environment")

    # we position the drone somewhere in the area
    x = randint(0, 19)
    y = randint(0, 19)

    #create drona
    d = Drone(x, y)



    # create a surface on screen that has the size of 400 x 480
    screen = pygame.display.set_mode((400,400))
    screen.fill(WHITE)


    # define a variable to control the main loop




    screen.blit(d.mapWithDrone(m.image()),(0,0))
    pygame.display.flip()

    #path = dummysearch() #de schimbat aici
    service = Service()
    start_time = time.time()
    #path = service.searchAStar(m,d,0,3,19,19) #de schimbat aici
    path = service.searchGreedy(m,d,0,3,19,19) #de schimbat aici
    end_time = time.time()
    duration = end_time - start_time
    print("Program executed in: " + duration.__str__() + " seconds")
    screen.blit(service.displayWithPath(m.image(), path),(0,0))

    pygame.display.flip()
    time.sleep(60)
    pygame.quit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()