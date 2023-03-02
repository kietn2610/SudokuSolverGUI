import pygame
from cube import Cube

pygame.font.init()


def find_empty(bo):
    # Loop through each row and column in the board
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            # If the cell is empty (contains 0), return its position (row, col)
            if bo[i][j] == 0:
                return (i, j)  # row, col

    # If all cells are filled, return None
    return None


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        # If the number is already in the row and is not in the same position, it's invalid
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        # If the number is already in the column and is not in the same position, it's invalid
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            # If the number is already in the box and is not in the same position, it's invalid
            if bo[i][j] == num and (i, j) != pos:
                return False

    # If the number is valid in the row, column, and box, return True
    return True


# Make a sudoku board
class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    """Takes in the rows, cols, width, height, and win parameters 
    which are used to initialize other attributes of the class."""

    def __init__(self, rows, cols, width, height, win):
        self.rows = rows
        self.cols = cols
        # two-dimensional list of Cube objects, which represent the individual cells of the board.
        self.cubes = [[Cube(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.win = win

    # Update the model attribute to reflect the current state of the board.
    def update_model(self):
        self.model = [[self.cubes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # Takes in a val parameter which represents the value to be placed on the board at the currently selected cell.
    def place(self, val):
        row, col = self.selected
        # Checks if the selected cell is empty and sets the value to val if it is.
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set(val)
            self.update_model()  # update the model attribute

            """ Check if the new value is valid by calling the valid function
                If the value is valid and the board can be solved using the solve function
                valid and solve function are defined later on
                """
            if valid(self.model, val, (row, col)) and self.solve():
                return True
            # Otherwise, it sets the cell value back to 0 and returns False.
            else:
                self.cubes[row][col].set(0)
                self.cubes[row][col].set_temp(0)
                self.update_model()
                return False

    """ Sets the temporary value of the currently selected cell to the given val. 
    This is used to display a temporary value on the cell while the player is 
    deciding on the final value to place there. """

    def sketch(self, val):
        row, col = self.selected
        self.cubes[row][col].set_temp(val)

    """Draw the Sudoku board on the screen. 
    First draws the grid lines by looping through the rows and columns of the board 
    and drawing horizontal and vertical lines with different thickness 
    depending on whether the line is a major line (i.e. every third line) or a minor line."""

    def draw(self):
        # Draw Grid Lines
        gap = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.win, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick)
            pygame.draw.line(self.win, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick)

        # Loops through each cell in the cubes list
        # and calls the draw method of the Cube object to draw the cell on the screen.
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(self.win)

    # Selects a cube at the given row and column and
    # deselects all other cubes.
    def select(self, row, col):
        # Reset all other
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].selected = False
        # Set select cube
        self.cubes[row][col].selected = True
        self.selected = (row, col)

    # Clears the value of the selected cube if it is a temporary value
    # (i.e., not part of the original puzzle).
    def clear(self):
        row, col = self.selected
        if self.cubes[row][col].value == 0:
            self.cubes[row][col].set_temp(0)

    # Takes the position of a mouse click and
    # returns the corresponding row and column of the cube that was clicked.
    def click(self, pos):
        """
        :param: pos
        :return: (row, col)
        """
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return int(y), int(x)
        else:
            return None

    # Checks if the puzzle has been completed by
    # checking if any cube is still empty (i.e., has a value of 0).
    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.cubes[i][j].value == 0:
                    return False
        return True

    def solve(self):
        # Find the first empty cell in the puzzle
        find = find_empty(self.model)

        # If no empty cell is found, the puzzle is solved
        if not find:
            return True
        else:
            row, col = find

        # Try filling the empty cell with an integer between 1 and 9
        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                # If the integer is valid, fill the cell with it
                self.model[row][col] = i

                # Recursively call solve() to fill in the remaining empty cells
                if self.solve():
                    return True

                # If the recursive call does not solve the puzzle, backtrack and try another integer
                self.model[row][col] = 0

        # If no integer between 1 and 9 can solve the puzzle, backtrack
        return False

    def solve_gui(self):
        # Update the model with the current state of the GUI
        self.update_model()

        # Find the next empty cell
        find = find_empty(self.model)
        if not find:
            # If there are no more empty cells, the puzzle is solved
            return True
        else:
            row, col = find

        # Try each possible value for the current empty cell
        for i in range(1, 10):
            if valid(self.model, i, (row, col)):
                # If the value is valid, update the model and the GUI
                self.model[row][col] = i
                self.cubes[row][col].set(i)
                self.cubes[row][col].draw_change(self.win, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(100)

                # Recursively call solve_gui() to solve the rest of the puzzle
                if self.solve_gui():
                    return True

                # If solve_gui() returns False, backtrack and try the next value
                self.model[row][col] = 0
                self.cubes[row][col].set(0)
                self.update_model()
                self.cubes[row][col].draw_change(self.win, False)
                pygame.display.update()
                pygame.time.delay(100)

        # If no valid value is found, backtrack further
        return False
