import pygame


class Cube:
    # class variables for the number of rows and columns in the grid
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        # initialize the cube object with a value, position, and size
        self.value = value
        self.temp = 0 # temporary value for user input
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False # whether the cube is currently selected

    def draw(self, win):
        # draw the cube on the screen
        fnt = pygame.font.SysFont("comicsans", 40) # set the font and font size

        gap = self.width / 9 # calculate the size of the gap between each cube
        x = self.col * gap # calculate the x position of the cube
        y = self.row * gap # calculate the y position of the cube

        # if the cube has a temporary value but not a permanent value, draw the temporary value
        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 5, y + 5))
        # if the cube has a permanent value, draw the permanent value
        elif not (self.value == 0):
            text = fnt.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        # if the cube is selected, draw a red border around it
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def draw_change(self, win, g=True):
        # draw the change made to the cube on the screen
        fnt = pygame.font.SysFont("comicsans", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        # draw a white rectangle over the previous value of the cube
        pygame.draw.rect(win, (255, 255, 255), (x, y, gap, gap), 0)

        # draw the new value of the cube in black
        text = fnt.render(str(self.value), 1, (0, 0, 0))
        win.blit(text, (x + (gap / 2 - text.get_width() / 2), y + (gap / 2 - text.get_height() / 2)))

        # if the change is valid, draw a green border around the cube; otherwise, draw a red border
        if g:
            pygame.draw.rect(win, (0, 255, 0), (x, y, gap, gap), 3)
        else:
            pygame.draw.rect(win, (255, 0, 0), (x, y, gap, gap), 3)

    def set(self, val):
        # set the permanent value of the cube
        self.value = val

    def set_temp(self, val):
        # set the temporary value of the cube
        self.temp = val

