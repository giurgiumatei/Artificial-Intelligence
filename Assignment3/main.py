from repository import *
from time import time
from controller import *
from ui import *

def main():

    repository = Repository()
    controller = Controller(repository)
    ui = UI(controller, repository)

    ui.menu()


if __name__ == "__main__":
    main()

