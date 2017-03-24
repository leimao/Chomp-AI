'''
Chomp AI Player
Author: Lei Mao
Website: https://github.com/leimao/
Date: 2017/3/23
Content: Find all p-positions and n-positions of certain chomp rectangle of certain size.
Acknowledgement: Guotu Li
Usage: "python chomp_solver.py m n" where 'm' and 'n' are the length and width of the rectangle.
'''

import sys
import os
import time
import numpy as np

def board_to_state(board):
    '''
    Given a game state on chomp board in numpy array format, return a state in tuple format.
    '''
    size_y, size_x = np.shape(board)
    state = list()
    for k in xrange(size_y):
        state.append(np.sum(board[k]))
    state = tuple(state)
    return state

def state_to_board(state, size_x, size_y):
    '''
    Given a state in tuple format, return a game state on chomp board in numpy array format.
    '''
    board = np.zeros((size_y, size_x), dtype = int)
    for i in xrange(size_y):
        board[i,:state[i]] = 1
    return board

def board_tructation(board, action):
    '''
     Given a game state on chomp board in numpy array format and an action of player, return the resulted game state.
    '''
    board_trucated = board.copy()
    board_trucated[action[0]:,action[1]:] = 0
    return board_trucated

def check_p_position(state):
    '''
    Check whether current state is a p_position or n_position.
    '''
    global p_positions
    global n_positions
    global size_x
    global size_y

    # the state is either p_position or n_position
    if_p_position = True

    # break_sign
    break_sign = False

    # construct a board of the state
    board = state_to_board(state = state, size_x = size_x, size_y = size_y)

    # check each position after truncation
    for i in xrange(size_y):
        for j in xrange(size_x):
            if board[i][j] == 1:
                board_trucated = board_tructation(board = board, action = (i,j))
                state_truncated = board_to_state(board_trucated)
                
                if tuple(state_truncated) in p_positions:
                    if_p_position = False
                    break_sign = True
                if break_sign == True:
                    break
        if break_sign == True:
            break
    
    # Append to p_positions or n_positions list if not exist.
    if if_p_position == True:
        if tuple(state) not in p_positions:
            print('new p_position found: ' + str(tuple(state)))
            #print(state)
            p_positions.append(tuple(state))
    else:
        if tuple(state) not in n_positions:
            n_positions.append(tuple(state))

def loop(state, row):
    '''
    Loop all the possible states from certain rows recursively.
    '''
    state_current = state[:]
    row_current = row

    while ((row_current < size_y - 1) and (state_current[row] >= state_current[row + 1])):
        print('current state: ' + str(tuple(state_current)))
        check_p_position(state_current)
        loop(state_current, row_current + 1)
        state_current[row_current + 1] = state_current[row_current + 1] + 1

def find_p_positions(size_x, size_y):
    '''
    Find all p_positions of certain chomp rectangle of certain size.
    '''
    global p_positions
    global n_positions

    for j in xrange(size_x):
        # Initialize state
        s = j + 1
        state = [s]
        for i in xrange(size_y - 1):
            state.append(0)
        loop(state = state, row = 0)
    print('#' * 80)
    print('All p_positons found:')
    print(p_positions)
    
    return p_positions, n_positions

def tuple_to_string(tuple_input):
    '''
    Format a tuple to a string with its brackets removed.
    '''
    string_output = ''
    for i in tuple_input:
        string_output = string_output + str(i) + ','
    string_output = string_output[:-1]

    return string_output

def sort_positions(positions):
    '''
    Sort positions with its sum from small to large.
    '''
    sum_positions = list()
    for position in positions:
        sum_positions.append(np.sum(position))
    index_sorted = np.argsort(sum_positions)
    positions_sorted = [None] * len(positions)
    for i, index in enumerate(index_sorted):
        positions_sorted[i] = positions[index]
    return positions_sorted

def num_combination(m, n):
    '''
    All as, m and n are integers. They all satisfy:
    0<=a1<=a2<=a3<=...<=am-1<=am<=n
    How many combinations of {a1,a2,a3,...,am-1,am} are there.
    Author: Guotu Li
    '''
    if (m == 0):
        return 0
    
    comb = np.zeros((n+1,m+1))
    comb[0,1:] = 1
    
    if (n>0):
        for i in range(n+1):
            comb[i,1] = i+1
    
    for i in range(1, n+1):
        for j in range(2, m+1):
            comb[i,j] = np.sum(comb[:i+1,j-1])

    return int(comb[n,m])


if __name__ == '__main__':

    size_x = int(sys.argv[1])
    size_y = int(sys.argv[2])

    # Start time
    time_start = time.time()
    # Initialize p_positions list
    p_position = [1]
    for i in xrange(size_y - 1):
        p_position.append(0)
    p_positions = list()
    p_positions.append(tuple(p_position))
    n_positions = list()

    # Calculate p_positions and n_positions lists
    p_positions, n_positions = find_p_positions(size_x, size_y)
    # Sort positions with its sum from small to large
    p_positions = sort_positions(p_positions)
    
    # End time
    time_end = time.time()

    # Print time used
    print('#' * 80)
    print('Time used: %f' %(time_end - time_start))

    # Print the number of states tested
    print('#' * 80)
    # +1 is because of the state whose element is all zero
    num_states_tested = len(p_positions) + len(n_positions) + 1
    print('Number of states tested: %d' %num_states_tested)

    # Check whether all the states have been explored
    num_states_theoretical = num_combination(m = size_x, n = size_y)
    print('Theoretical number of states to be tested: %d' %num_states_theoretical)

    if num_states_tested != num_states_theoretical:
        print('Warning: some states have not been explored.')
    else:
        print('All states have been explored.')

    # Save p_positions to hard drive
    result_directory = 'data/'
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
    data_file = 'p_positions_' + str(size_x) + 'x' + str(size_y) + '.txt'
    fhand = open(result_directory + data_file, "w")
    for position in p_positions:
        fhand.write(tuple_to_string(position))
        fhand.write('\n')
    fhand.close()
