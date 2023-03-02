import pygame
import time
from grid import Grid

pygame.font.init()


def redraw_window(win, board, time, strikes):
    # Fill the window with white color
    win.fill((255, 255, 255))

    # Draw time
    fnt = pygame.font.SysFont("comicsans", 40)
    text = fnt.render("Time: " + format_time(time), 1,
                      (0, 0, 0))  # Create a text object with the current time, using a specified font and color
    win.blit(text, (540 - 160, 560))  # Draw the text object on the window at a specific position

    # Draw Strikes
    text = fnt.render("X " * strikes, 1, (255, 0,
                                          0))  # Create a text object with a number of X's equal to the current number of strikes, using a specified font and color
    win.blit(text, (20, 560))  # Draw the text object on the window at a specific position

    # Draw grid and board
    board.draw()  # Call the draw method of the board object to draw the game board


def format_time(secs):
    # Calculate the number of seconds, minutes, and hours from the total number of seconds
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    # Create a string with the formatted time (MM:SS)
    mat = " " + str(minute) + ":" + str(sec)
    return mat  # Return the formatted time string


def main():
    # Initialize Pygame window
    win = pygame.display.set_mode((720, 800))
    pygame.display.set_caption("Sudoku")

    # Create Sudoku grid
    board = Grid(9, 9, 540, 540, win)

    # Initialize variables
    key = None
    run = True
    start = time.time()
    strikes = 0

    # Main game loop
    while run:
        # Calculate play time
        play_time = round(time.time() - start)

        # Handle Pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Handle number key presses
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    # Clear selected cube
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    # Solve the puzzle automatically
                    board.solve_gui()

                if event.key == pygame.K_RETURN:
                    # Check if player input is correct and update strikes
                    i, j = board.selected
                    if board.cubes[i][j].temp != 0:
                        if board.place(board.cubes[i][j].temp):
                            print("Success")
                        else:
                            print("Wrong")
                            strikes += 1
                        key = None

                        # Check if the game is finished
                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Handle mouse clicks
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        # Sketch the selected cube with the current key
        if board.selected and key is not None:
            board.sketch(key)

        # Redraw the game window
        redraw_window(win, board, play_time, strikes)
        pygame.display.update()


main()
pygame.quit()
