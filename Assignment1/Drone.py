import pyautogui as pyautogui
from pygame.locals import *
from DMap import *


class Drone():
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, detectedMap):
        pressed_keys = pygame.key.get_pressed()
        if self.x > 0:
            if pressed_keys[K_UP] and detectedMap.surface[self.x-1][self.y]==0:
                self.x = self.x - 1
        if self.x < 19:
            if pressed_keys[K_DOWN] and detectedMap.surface[self.x+1][self.y]==0:
                self.x = self.x + 1

        if self.y > 0:
              if pressed_keys[K_LEFT]and detectedMap.surface[self.x][self.y-1]==0:
                  self.y = self.y - 1
        if self.y < 19:
              if pressed_keys[K_RIGHT] and detectedMap.surface[self.x][self.y+1]==0:
                  self.y = self.y + 1

    def moveDSF(self, detectedMap):
        if stack:
            visited.append((self.x, self.y))

            if self.x > 0 and detectedMap.surface[self.x - 1][self.y] == 0 and (self.x - 1, self.y) not in visited:
                self.x = self.x - 1
                stack.append((self.x, self.y))
            elif self.y < 19 and detectedMap.surface[self.x][self.y + 1] ==0 and (self.x, self.y + 1) not in visited:
                self.y = self.y + 1
                stack.append((self.x, self.y))
            elif self.x < 19 and detectedMap.surface[self.x + 1][self.y] ==0 and (self.x + 1, self.y) not in visited:
                self.x = self.x + 1
                stack.append((self.x, self.y))
            elif self.y > 0 and detectedMap.surface[self.x][self.y - 1] ==0 and (self.x, self.y - 1) not in visited:
                self.y = self.y - 1
                stack.append((self.x, self.y))
            else:
                #
                # current_element=stack[-1]
                # current_x=current_element[0]
                # current_y=current_element[1]
                del stack[-1]

                try:
                    element = stack[-1]

                    #this while proves that it won't "jump" and that it will always go to a child of a node (UP,RIGHT,DOWN,LEFT)
                    #because the program never enters this while (ran it with the debugger)
                    # while not ( (element[0] == current_x-1 and element[1] == current_y) or (element[0] == current_x and element[1] == current_y+1) or
                    #             (element[0] == current_x+1 and element[1] == current_y) or (element[0] == current_x and element[1] == current_y-1) ):
                    #     del stack[-1]
                    #     element = stack[-1]

                    self.x = element[0]
                    self.y = element[1]
                except:
                   # print("Area was explored!")

                    pyautogui.alert("Area was explored!")
