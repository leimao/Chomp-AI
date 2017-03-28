'''
Chomp AI Player
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/3/23
Content: Play Chomp with AI in PyGame Gui.
Acknowledgement: http://programarcadegames.com/
Usage: "python chomp_gui.py x m n". 'x' designates who goes first in the game. it can be either 'Human' or 'AI'. 'm' and 'n' are the length and width of the rectangle. They all do not exceed AI_limit.
'''

import sys
import pygame
import numpy as np
from chomp_ai import AI_data, AI_strategy

# Define AI limit
AI_limit = 12

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
ORANGE = (255, 128, 0)

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 20
HEIGHT = 20

# This sets the margin between each cell
MARGIN = 5

def draw_board(board):
    '''
    Draw board on the screen.
    '''

    # Draw cookies
    for row in range(ROW):
        for column in range(COLUMN):
            color = WHITE
            if board[row,column] == 0:
                color = GRAY
            pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT])

    # Draw poisonous cookie
    color = ORANGE
    pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * 0 + MARGIN, (MARGIN + HEIGHT) * 0 + MARGIN, WIDTH, HEIGHT])

    pygame.display.flip()

def click_animation(coordinates, player):
    '''
    Highlight the grid user clicked.
    '''
    if coordinates != ('NULL', 'NULL'):
        if player == 'Human':
            color = RED
        else:
            color = BLUE
        pygame.draw.rect(screen, color, [(MARGIN + WIDTH) * coordinates[1] + MARGIN, (MARGIN + HEIGHT) * coordinates[0] + MARGIN, WIDTH, HEIGHT])

        pygame.display.flip()
        pygame.time.wait(500)
        
def referee(coordinates, player):
    '''
    Judge who win the game.
    '''
    global game_over

    if coordinates == (0,0):
        if player == 'Human':
            winner = 'AI'
        else:
            winner = 'Human'

        print('Winner: ' + winner)
        game_over = True

        return winner

# -------- Main Program Loop -----------

# Define which player goes first
if (sys.argv[1] == 'Human') or (sys.argv[1] == 'human'):
    player_first = 'Human'
elif (sys.argv[1] == 'AI') or (sys.argv[1] == 'ai'):
    player_first = 'AI'
else:
    raise Exception('Input Error. Check User Manual.')

# Define the size of rectangle
ROW = int(sys.argv[2])
COLUMN = int(sys.argv[3])

# Check the size of rectangle does not exceed AI_limit
if (ROW > AI_limit) or (COLUMN > AI_limit):
    raise Exception('Rectangle Size Exceed AI Limit.')

# Initialize board full of cookies
board = np.full((ROW, COLUMN), fill_value = 1, dtype = int)

# Initialize pygame
pygame.init()

# Set the HEIGHT and WIDTH of the screen
board_size_x = int((WIDTH + MARGIN) * COLUMN)
board_size_y = int((HEIGHT + MARGIN) * ROW)

window_size_x = int(board_size_x)
window_size_y = int(board_size_y * 1.5)

WINDOW_SIZE = [window_size_x, window_size_y]
screen = pygame.display.set_mode(WINDOW_SIZE)

# Set title of screen
pygame.display.set_caption("Chomp Game")

# Loop until the user clicks the close button.
game_over = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Limit to 60 frames per second
clock.tick(60)

# Set the screen background
screen.fill(BLACK)

# Load AI data
print('Loading AI ...')
result_directory = 'data/'
data_file = 'p_positions_' + str(AI_limit) + 'x' + str(AI_limit) + '.txt'
p_positions_file = result_directory + data_file
data_AI = AI_data(p_positions_file = p_positions_file, board_size_x = COLUMN, board_size_y = ROW)

# Game starts
player_goes = player_first

# Draw the grid
draw_board(board)

# Players switches to play
while not game_over:
    if player_goes == 'AI':
        # Add some AI delay
        pygame.time.wait(500)
        # AI make strategy
        (row, column) = AI_strategy(board = board, p_positions = data_AI)

    elif player_goes == 'Human':
        user_clicked = False
        while not user_clicked:
            for event in pygame.event.get():  # Human player did something
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Human player clicks the mouse. Get the position
                    pos = pygame.mouse.get_pos()
                    # Change the x/y screen coordinates to grid coordinates
                    column = pos[0] // (WIDTH + MARGIN)
                    row = pos[1] // (HEIGHT + MARGIN)
                    print("Click ", pos, "Grid coordinates: ", row, column)
                    # Make sure there is still cookie
                    if board[row,column] == 1:
                        user_clicked = True
    
    # Eat cookies
    board[row:,column:] = 0

    # Click animation
    click_animation(coordinates = (row,column), player = player_goes)

    # Draw the grid
    draw_board(board)

    # Check whether the game ends and determine the winner
    winner = referee(coordinates = (row,column), player = player_goes)

    # Switch player
    if player_goes == 'AI':
        player_goes = 'Human'
    elif player_goes == 'Human':
        player_goes = 'AI'

# Print winner information
# Select the font to use, size, bold, italics
font_size = int(0.1 * window_size_y)
font = pygame.font.SysFont('Calibri', font_size, True, False)
message = 'Winner: ' + winner
# Measure the size of message text
message_size = font.size(message) #(width, height)
text = font.render(message, True, WHITE)
text_coordinates = [int(board_size_x*0.5-message_size[0]*0.5),int(board_size_y*1.25-message_size[1]*0.5)]
# Put the image of the text on the screen at 250x250
screen.blit(text, text_coordinates)
pygame.display.flip()
pygame.time.wait(2000)

# Be IDLE friendly. If you forget this line, the program will 'hang' on exit.
pygame.quit()