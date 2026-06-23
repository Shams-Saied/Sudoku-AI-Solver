
class SudokuBoard:
    def __init__(self, board=None):
        if board is None:
            self.board = [[0 for _ in range(9)] for _ in range(9)] # 9x9 grid filled with 0s
        else:
            self.board = [row[:] for row in board] # deep copy of the board
    
    def get_cell(self, row, col):
        return self.board[row][col]
    
    def set_cell(self, row, col, value):
        if 1 <= value <= 9 or value == 0:
            self.board[row][col] = value
            return True
        return False
    
    def clear_cell(self, row, col):
        self.board[row][col] = 0
    
    def is_valid_placement(self, row, col, num):
        # Check row
        for j in range(9):
            if self.board[row][j] == num:
                return False
        
        # Check column
        for i in range(9):
            if self.board[i][col] == num:
                return False
        
        # Check 3x3 box
        box_row, box_col = (row // 3) * 3, (col // 3) * 3
        for i in range(3):
            for j in range(3):
                if self.board[box_row + i][box_col + j] == num:
                    return False
        
        return True
    
    # Check if board is complete (no empty cells)
    def is_complete(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def find_empty_cell(self):
        # Find first empty cell (0 value)
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None
    
    def get_board_copy(self):
        return [row[:] for row in self.board]
    
    def validate_full_board(self):
        # Check all filled cells
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    num = self.board[i][j]
                    # Temporarily remove the number to check validity
                    self.board[i][j] = 0
                    if not self.is_valid_placement(i, j, num):
                        self.board[i][j] = num
                        return False, f"Invalid number {num} at position ({i+1}, {j+1})"
                    self.board[i][j] = num
        return True, "Board is valid"
    
    def is_solvable(self):
        from algorithms import backtrack
        return backtrack(self.get_board_copy())
    
    def __str__(self):
        # String representation of the board
        result = []
        for i in range(9):
            if i % 3 == 0 and i != 0:
                result.append("-" * 21)
            row = []
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    row.append("|")
                val = self.board[i][j]
                row.append(str(val) if val != 0 else ".")
            result.append(" ".join(row))
        return "\n".join(result)