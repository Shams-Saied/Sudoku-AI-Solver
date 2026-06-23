import time
import random
from board import SudokuBoard
from ac3 import AC3

# HELPERS
def is_valid(board, row, col, num):
    # Check row
    for j in range(9):
        if board[row][j] == num:
            return False
    
    # Check column
    for i in range(9):
        if board[i][col] == num:
            return False
    
    # Check 3x3 box
    box_row, box_col = (row // 3) * 3, (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[box_row + i][box_col + j] == num:
                return False
    
    return True

def find_empty(board):
    # Find first empty cell (value 0)
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

def reset_counter():
    global nodes_explored
    nodes_explored = 0

def get_nodes_explored():
    return nodes_explored

# BACKTRACKING
nodes_explored = 0
def backtrack(board, step_callback=None):

    global nodes_explored
    nodes_explored += 1
    # Find empty cell
    empty_pos = find_empty(board)
    if not empty_pos:
        return True  # Board is complete
    
    row, col = empty_pos
    
    # Try numbers 1-9
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            # Place the number
            board[row][col] = num
            
            # Callback for visualization
            if step_callback:
                step_callback(row, col, num)
            
            # Recurse
            if backtrack(board, step_callback):
                return True
            
            # Backtrack
            board[row][col] = 0
            
            # Callback for backtracking visualization
            if step_callback:
                step_callback(row, col, 0)
    
    return False

def solve_bt(board, step_callback=None):
    start_time = time.time()
    reset_counter() 
    
    # convert to list
    if isinstance(board, SudokuBoard):
        working_board = board.get_board_copy()
    else:
        working_board = [row[:] for row in board]
    
    # Solve recursively
    success = backtrack(working_board, step_callback)
    
    solve_time = time.time() - start_time
    nodes = get_nodes_explored()
    if success:
        return working_board, True, nodes, solve_time
    else:
        return None, False, nodes, solve_time

def solve_ac3(board, step_callback=None):
    start_time = time.time()
    reset_counter()
    
    # convert to list
    if isinstance(board, SudokuBoard):
        working_board = board.get_board_copy()
    else:
        working_board = [row[:] for row in board]
    
    # apply AC3
    ac3 = AC3()
    reduced_board, ac3_success, ac3_nodes = ac3.solve(working_board, step_callback)

    ac3.print_full_tree()

    if not ac3_success:
        solve_time = time.time() - start_time
        return None, False, ac3_nodes, solve_time
    
    # apply backtracking
    success = backtrack(reduced_board, step_callback)
    solve_time = time.time() - start_time
    total_nodes = ac3_nodes + get_nodes_explored()
    
    if success:
        return reduced_board, True, total_nodes, solve_time
    else:
        return None, False, total_nodes, solve_time

# PUZZLE GENERATION FUNCTIONS
def fill_diagonal_boxes(board):
    for box in range(0, 9, 3):
        nums = list(range(1, 10))
        random.shuffle(nums)
        for i in range(3):
            for j in range(3):
                board[box + i][box + j] = nums.pop()

def has_unique_solution(board):
    solutions = []
    # early termination
    def count_solutions(board, pos=0):
        if len(solutions) > 1:
            return
        # base case
        if pos == 81:
            solutions.append([row[:] for row in board])
            return
        
        i, j = pos // 9, pos % 9
        
        if board[i][j] != 0:
            count_solutions(board, pos + 1) # if cell filled move to next cell
        else:
            for num in range(1, 10):
                if is_valid(board, i, j, num):
                    board[i][j] = num
                    count_solutions(board, pos + 1)
                    board[i][j] = 0
    
    board_copy = [row[:] for row in board]
    count_solutions(board_copy)
    return len(solutions) == 1


def generate_random_puzzle(num_clues=30):
    # Start with empty board
    board = [[0 for _ in range(9)] for _ in range(9)]
    
    # Generate a complete solved board first
    fill_diagonal_boxes(board)
    backtrack(board)  # Fill the rest
    
    # Store the solution
    solution = [row[:] for row in board]
    
    # Remove cells to create puzzle
    cells = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(cells)
    
    for i, j in cells:
        if sum(cell != 0 for row in board for cell in row) <= num_clues:
            break
        
        temp = board[i][j]
        board[i][j] = 0
        
        # Check if puzzle still has unique solution
        if not has_unique_solution(board):
            board[i][j] = temp
    
    return SudokuBoard(board), SudokuBoard(solution)
