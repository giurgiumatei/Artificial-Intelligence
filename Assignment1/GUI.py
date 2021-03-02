

from Service import *

window = pygame.display.set_mode((700,700))
window.fill( (255,255,255) )

class Button:

    def __init__(self, color, x, y, width, height, text=""):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw(self, window, outline = None):
        if outline:
            pygame.draw.rect(window, outline, (self.x-2, self.y -2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(window,self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != "":
            pygame.font.init()
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, True, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height()/2)))


    def isOver(self, pos):

        if self.x < pos[0] < self.x + self.width:
            if self.y < pos[1] < self.y + self.height:
                return True
        return False


def redrawWindow():
    window.fill((255, 255, 255))
    greeenButton.draw(window, (0, 0, 0))

run = True
greeenButton = Button((0,255,0), 150, 225, 450, 100, "Start the Exploration")

while run:
    redrawWindow()
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if greeenButton.isOver(pos):
                start()
                run = False


        if event.type == pygame.MOUSEMOTION:
            if greeenButton.isOver(pos):
                greeenButton.color = (255, 0, 0)
            else:
                greeenButton.color = (0, 255, 0)

