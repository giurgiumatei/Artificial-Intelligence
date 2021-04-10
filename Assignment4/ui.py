from controller import *
import pygame
import time

n = 20
m = 20
map = Map(n, m)
pygame.init()
screen = pygame.display.set_mode((20 * n, 20 * m))
screen.fill(WHITE)
screen.blit(map.image(), (0, 0))
pygame.display.flip()
map.randomMap()
sensors = []
for i in range(5):
    x = random.randint(0, n-1)
    y = random.randint(0, m-1)
    sensors.append((x, y))
map.Sensors = sensors
controller = Controller(screen, map)


res = controller.searchAStar(map, 1, 2, 15, 4, screen)
best_path = controller.run()
screen.blit(map.image_path([]), (0, 0))
pygame.display.flip()
#time.sleep(3)
for i in range(len(best_path)):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    pygame.time.delay(55)
    solution = best_path[:i]
    screen.blit(map.image_path(solution), (0, 0))
    pygame.display.flip()
    pygame.display.update()
time.sleep(10)



