from Drone import *

class Service():



    def searchAStar(self,mapM, droneD, initialX, initialY, finalX, finalY):
        found = False  # false while no complete path was found
        visited = []  # cells visited, closed list
        to_visit = [(initialX, initialY)]  # priority queue, open list
        parent = {}
        cost_so_far = {}
        cost_so_far[(initialX, initialY)] = 0


        while to_visit and found == False:
            if not to_visit:
                return False

            cell = to_visit[-1]
            visited.append(cell)  # popped the cell and marked as visited
            current_x = cell[0]
            current_y = cell[1]
            del to_visit[-1]

            if current_x == finalX and current_y == finalY:
                found = True  # we check if we haven't got to the desired coordinates


            else:

                if current_x > 0 and mapM.surface[current_x - 1][current_y] == 0 and (current_x - 1, current_y) not in visited:

                    new_cost = cost_so_far[(current_x, current_y)] + 1
                    if (current_x - 1, current_y) not in cost_so_far or new_cost < cost_so_far[(current_x - 1, current_y)]:
                        cost_so_far[(current_x - 1, current_y)] = new_cost
                        parent[(current_x - 1, current_y)] = cell
                        to_visit.append((current_x - 1, current_y))

                if current_y < 19 and mapM.surface[current_x][current_y + 1] == 0 and (current_x, current_y + 1) not in visited:

                    new_cost = cost_so_far[(current_x, current_y)] + 1
                    if (current_x, current_y + 1) not in cost_so_far or new_cost < cost_so_far[(current_x, current_y + 1)]:
                        cost_so_far[(current_x, current_y + 1)] = new_cost
                        parent[(current_x, current_y+1)] = cell
                        to_visit.append((current_x, current_y+1))

                if current_x < 19 and mapM.surface[current_x + 1][current_y] == 0 and (current_x + 1, current_y) not in visited:

                    new_cost = cost_so_far[(current_x, current_y)] + 1
                    if (current_x + 1, current_y) not in cost_so_far or new_cost < cost_so_far[(current_x + 1, current_y)]:
                        cost_so_far[(current_x + 1, current_y)] = new_cost
                        parent[(current_x + 1, current_y)] = cell
                        to_visit.append((current_x + 1, current_y))

                if current_y > 0 and mapM.surface[current_x][current_y - 1] == 0 and (current_x, current_y - 1) not in visited:

                    new_cost = cost_so_far[(current_x, current_y)] + 1
                    if (current_x, current_y - 1) not in cost_so_far or new_cost < cost_so_far[(current_x, current_y - 1)]:
                        cost_so_far[(current_x, current_y - 1)] = new_cost
                        parent[(current_x, current_y - 1)] = cell
                        to_visit.append((current_x, current_y - 1))


                to_visit = sorted(to_visit, key=lambda tup: function_h(finalX, tup[0], finalY, tup[1]), reverse=True)
                to_visit = sorted(to_visit, key=lambda tup: function_f(finalX, tup[0], finalY, tup[1], initialX, initialY, cost_so_far), reverse=True)# sort by function f(...), add cost_so_far
                                            # f(...)= h(...) + g(...)
                                            # we must sort twice so that in case
                                            # of equality of function f(...) we use
                                            # function h(...) as a secondary criterion

        path = []
        current_x = finalX
        current_y = finalY

        while ((current_x, current_y) in parent):
            path.append((current_x, current_y))
            aux_x = parent[(current_x, current_y)][0]
            aux_y = parent[(current_x, current_y)][1]
            current_x = aux_x
            current_y = aux_y
        path.append((initialX, initialY))

        return path






    def searchGreedy(self,mapM, droneD, initialX, initialY, finalX, finalY):

        found = False #false while no complete path was found
        visited = [] #cells visited
        to_visit = [(initialX, initialY)] #priority queue
        parent = {}#here we store the parent of each node

        while to_visit and found == False:
            if not to_visit:
                return False

            cell = to_visit[-1]
            visited.append(cell) #popped the cell and marked as visited
            current_x = cell[0]
            current_y = cell[1]
            del to_visit[-1]

            if current_x == finalX and current_y == finalY:
                found = True #we check if we haven't got to the desired coordinates


            else:
                aux = [] #auxiliary list

                if current_x > 0 and mapM.surface[current_x - 1][current_y] == 0 and (current_x - 1, current_y) not in visited:
                    parent[(current_x - 1, current_y)] = cell
                    aux.append((current_x-1, current_y))

                if current_y < 19 and mapM.surface[current_x][current_y + 1] == 0 and (current_x, current_y + 1) not in visited:
                    parent[(current_x, current_y + 1)] = cell
                    aux.append((current_x, current_y+1))
                if current_x < 19 and mapM.surface[current_x + 1][current_y] == 0 and (current_x + 1, current_y) not in visited:
                    parent[(current_x + 1, current_y)] = cell
                    aux.append((current_x+1, current_y))

                if current_y > 0 and mapM.surface[current_x][current_y - 1] == 0 and (current_x, current_y - 1) not in visited:
                    parent[(current_x, current_y - 1)] = cell
                    aux.append((current_x, current_y-1))

                to_visit = to_visit + aux
                to_visit = sorted(to_visit, key=lambda tup: function_h(finalX, tup[0], finalY, tup[1]), reverse=True)#sort by euclidean distance
                #between state and final state
                #h(x)= sqrt((x2-x1)^2 + (y2-y1)^2)

        path = []
        current_x = finalX
        current_y = finalY

        while ((current_x, current_y) in parent):
            path.append((current_x, current_y))
            aux_x = parent[(current_x, current_y)][0]
            aux_y = parent[(current_x, current_y)][1]
            current_x = aux_x
            current_y = aux_y
        path.append((initialX, initialY))

        return path





    def dummysearch(self):
        #example of some path in test1.map from [5,7] to [7,11]
        return [[5,7],[5,8],[5,9],[5,10],[5,11],[6,11],[7,11]]

    def displayWithPath(self,image, path):
        mark = pygame.Surface((20,20))
        mark.fill(GREEN)
        for move in path:
            image.blit(mark, (move[1] *20, move[0] * 20))

        return image