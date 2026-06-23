
class AC3:
    
    def __init__(self):
        self.domains = {} 
        self.nodes_explored = 0
        self.removal_map = {}  # {(cell): [(value, reason, neighbor), ...]}
    
    def initialize_domains(self, board):
        domains = {}
        for i in range(9):
            for j in range(9):
                if board[i][j] != 0:
                    domains[(i, j)] = {board[i][j]}
                else:
                    domains[(i, j)] = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        return domains
    
    def get_related_cells(self, row, col):
        related = set()
        
        # Same row
        for j in range(9):
            if j != col:
                related.add((row, j))
        
        # Same column
        for i in range(9):
            if i != row:
                related.add((i, col))
        
        # Same box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for i in range(3):
            for j in range(3):
                r = box_row + i
                c = box_col + j
                if r != row or c != col:
                    related.add((r, c))
                    
        return related
    
    def get_conflict_type(self, cell1, cell2):
        r1, c1 = cell1
        r2, c2 = cell2

        if r1 == r2:
            return "row"
        elif c1 == c2:
            return "column"
        else:
            return "box"
    def revise(self, domains, cell1, cell2):
    
        changed = False
        values_to_remove = []

        # check if any value in cell2 doesn't conflict        
        for val1 in domains[cell1]:
            has_support = False
            for val2 in domains[cell2]:
                if val1 != val2:
                    has_support = True
                    break
            
            if not has_support:
                values_to_remove.append(val1)
                changed = True
        
        # LOG before removing
        if values_to_remove:
            for val in values_to_remove:
                reason = self.get_conflict_type(cell1, cell2)

                if cell1 not in self.removal_map:
                    self.removal_map[cell1] = []

                self.removal_map[cell1].append((val, reason, cell2))
        
        # remove values
        for val in values_to_remove:
            domains[cell1].remove(val)
        
        return changed
    
    def solve(self, board, step_callback=None):
        
        self.nodes_explored = 0
        self.domains = self.initialize_domains(board)
        new_board = [row[:] for row in board]
        self.removal_map = {} #reset
        
        # create queue of all arcs (cell1,cell2) where cells are related
        queue = []
        for i in range(9):
            for j in range(9):
                for related in self.get_related_cells(i, j):
                    queue.append(((i, j), related))
        
        # Process queue
        while queue:
            self.nodes_explored += 1
            (cell1, cell2) = queue.pop(0)
            
            if self.revise(self.domains, cell1, cell2):
                # If domain becomes empty, no solution
                if len(self.domains[cell1]) == 0:
                    return None, False, self.nodes_explored
                
                if len(self.domains[cell1]) == 1:
                    i, j = cell1
                    val = list(self.domains[cell1])[0]
                    if new_board[i][j] == 0:
                        new_board[i][j] = val
                        if step_callback:
                            step_callback(i, j, val)
                
                # Add all arcs pointing to cell1 back to queue
                for i in range(9):
                    for j in range(9):
                        if (i, j) != cell2 and (i, j) != cell1:
                            if cell1 in self.get_related_cells(i, j):
                                queue.append(((i, j), cell1))
        
        for (i, j), domain in self.domains.items():
            if len(domain) == 1 and new_board[i][j] == 0:
                new_board[i][j] = list(domain)[0]
                if step_callback:
                    step_callback(i, j, new_board[i][j])
        
        return new_board, True, self.nodes_explored
    
    def print_full_tree(self):
        print("\nFULL ARC CONSISTENCY TREE\n")

        for cell, removals in self.removal_map.items():
            print(f"Cell {cell}")

            # remove duplicates (important!)
            seen = set()
            unique_removals = []
            for val, reason, neighbor in removals:
                if (val, reason) not in seen:
                    seen.add((val, reason))
                    unique_removals.append((val, reason, neighbor))

            for val, reason, neighbor in unique_removals:
                print(f" ├── remove {val} (conflict with {reason})")

            # show final domain
            final_domain = self.domains[cell]
            print(f" └── remaining {final_domain}\n")