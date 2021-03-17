from Service import *

class UI():


    def print_menu(self):
        print("Give option: \n")
        print("1.Search with A*: \n")
        print("2.Search with Greedy: \n")

    def start(self):
        self.print_menu()
        option = input()

        if option == "1" or option == "2":
            return option

        else:
            print("Invalid Option! Program will terminate...")
            quit()



