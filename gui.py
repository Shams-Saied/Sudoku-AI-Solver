import tkinter as tk
from tkinter import messagebox
from board import SudokuBoard
from algorithms import solve_ac3, generate_random_puzzle

BG          = "#ffffff"  
PANEL       = "#16213e"  
BOX_BG      = "#ffffff"   
CELL_NORMAL = "#ffffff"   
CELL_FIXED  = "#cecece"   
CELL_SOLVE  = "#1b4332"   
CELL_ERR    = "#4a1020"   
ACCENT      = "#e94560"   
BTN_PRI     = "#e94560"
BTN_SEC     = "#0f3460"
FG_FIXED    = "#4F4F4F"  
FG_USER     = "#000000"  
FG_ANIM     = "#69f0ae"   
FG_DIM      = "#607080"
BORDER_BOX  = "#2e2e2e"  
BORDER_CELL = "#2a3a5a" 

CELL_W, CELL_H = 52, 52
FONT_NUM  = ("Segoe UI", 20, "bold")
FONT_BTN  = ("Segoe UI", 10, "bold")
FONT_STAT = ("Segoe UI", 9)


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku AI Solver")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.current_board = SudokuBoard()
        self.fixed_cells: set[tuple] = set()    # Coordinates of given clues
        self.mode = "auto"
        self._stop = False        

        self._build_ui()
        self.change_mode()          # load sample puzzle

    def _build_ui(self):
        # Title bar
        tk.Label(self.root, text="SUDOKU", font=("Segoe UI", 28, "bold"), bg=BG, fg=ACCENT).pack(pady=(18, 2))
        tk.Label(self.root, text="A I   S O L V E R", font=("Segoe UI", 10), bg=BG, fg=FG_DIM).pack()

        # Mode toggle
        mf = tk.Frame(self.root, bg=BG)
        mf.pack(pady=12)
        self.mode_var = tk.StringVar(value="auto")
        for text, val in [("Auto Solve", "auto"), ("User Input", "manual")]:
            tk.Radiobutton(mf, text=text, variable=self.mode_var, value=val, command=self.change_mode, bg=BG, fg="#aaaaaa", selectcolor=PANEL, activebackground=BG, activeforeground=ACCENT, font=FONT_STAT, indicatoron=0, relief=tk.FLAT, padx=14, pady=5, bd=0).pack(side=tk.LEFT, padx=4)

        # Grid canvas 
        self.canvas = tk.Canvas(self.root, bg=PANEL,
                                width=CELL_W*9+3, height=CELL_H*9+3,
                                highlightthickness=2,
                                highlightbackground=BORDER_BOX)
        self.canvas.pack(padx=20, pady=10)
        self.cells = [[None]*9 for _ in range(9)]
        self._draw_grid()

        # Buttons
        bf = tk.Frame(self.root, bg=BG)
        bf.pack(pady=10)
        self.btn_solve    = self._btn(bf, "SOLVE",    self.solve_puzzle,   BTN_PRI, 0)
        self.btn_new      = self._btn(bf, "NEW GAME", self.generate_random, BTN_SEC, 1)
        self.btn_check    = self._btn(bf, "CHECK",    self.check_user_input,BTN_SEC, 2)
        self.btn_clear    = self._btn(bf, "CLEAR",    self.clear_board,    "#333355", 3)
        self.btn_check.grid_remove()

        # Status
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.status_var, bg=PANEL, fg=FG_DIM, font=FONT_STAT, pady=6, anchor="w", padx=12).pack(side=tk.BOTTOM, fill=tk.X)

        # Stats line
        self.stats_var = tk.StringVar()
        tk.Label(self.root, textvariable=self.stats_var, bg=BG, fg=FG_DIM, font=FONT_STAT).pack(pady=(0, 6))

        # Key binding for manual mode
        self.canvas.bind("<Button-1>", self._on_click)
        self.root.bind("<Key>", self._on_key)
        self._selected = None   # (row, col)

    def _btn(self, parent, text, cmd, color, col):
        b = tk.Button(parent, text=text, command=cmd, bg=color, fg="white", font=FONT_BTN, padx=16, pady=7, relief=tk.FLAT, activebackground=ACCENT, activeforeground="white", cursor="hand2", bd=0)
        b.grid(row=0, column=col, padx=5)
        return b

    def _draw_grid(self):
        c = self.canvas
        c.delete("grid")
        ox, oy = 3, 3   # origin offset for outer border

        for i in range(9):
            for j in range(9):
                x1 = ox + j * CELL_W
                y1 = oy + i * CELL_H
                x2 = x1 + CELL_W
                y2 = y1 + CELL_H
                # cell rect
                c.create_rectangle(x1, y1, x2, y2, fill=CELL_NORMAL, outline=BORDER_CELL, width=1, tags="grid")
                # text placeholder
                tid = c.create_text(x1 + CELL_W//2, y1 + CELL_H//2,
                                    text="", font=FONT_NUM, fill=FG_USER,
                                    tags=("num", f"cell_{i}_{j}"))
                self.cells[i][j] = tid

        # Thick 3×3 box borders
        for b in range(4):
            x = ox + b * 3 * CELL_W
            y = oy + b * 3 * CELL_H
            c.create_line(ox, y, ox + 9*CELL_W, y, fill=BORDER_BOX, width=2, tags="grid")
            c.create_line(x, oy, x, oy + 9*CELL_H, fill=BORDER_BOX, width=2, tags="grid")

    def _cell_bbox(self, row, col):
        ox, oy = 3, 3
        x1 = ox + col * CELL_W
        y1 = oy + row * CELL_H
        return x1, y1, x1 + CELL_W, y1 + CELL_H

    def _set_cell_bg(self, row, col, color):
        x1, y1, x2, y2 = self._cell_bbox(row, col)
        # find the rectangle item under the text
        items = self.canvas.find_overlapping(x1+1, y1+1, x2-1, y2-1)
        for item in items:
            if "num" not in self.canvas.gettags(item):
                self.canvas.itemconfig(item, fill=color)
                break

    def _set_cell_text(self, row, col, text, color):
        self.canvas.itemconfig(self.cells[row][col], text=text, fill=color)

    def change_mode(self):
        self._abort()
        self.mode = self.mode_var.get()
        self._selected = None

        if self.mode == "auto":
            self.btn_check.grid_remove()
            self.status_var.set("Auto mode — click SOLVE to watch the AI")
            self.load_sample_puzzle()
        else:
            self.btn_check.grid()
            self.status_var.set("User input — click a cell and type a number")
            self.clear_board()

    def load_sample_puzzle(self):
        sample = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
        self.current_board = SudokuBoard(sample)
        self._load_board_to_display()

    def _load_board_to_display(self):
        self.fixed_cells = set()
        for i in range(9):
            for j in range(9):
                v = self.current_board.get_cell(i, j)
                if v != 0:
                    self._set_cell_text(i, j, str(v), FG_FIXED)
                    self._set_cell_bg(i, j, CELL_FIXED)
                    self.fixed_cells.add((i, j))
                else:
                    self._set_cell_text(i, j, "", FG_USER)
                    self._set_cell_bg(i, j, CELL_NORMAL)


    def _on_click(self, event):
        if self.mode != "manual":
            return
        ox, oy = 3, 3
        col = (event.x - ox) // CELL_W
        row = (event.y - oy) // CELL_H
        if 0 <= row < 9 and 0 <= col < 9:
            if self._selected:
                pr, pc = self._selected
                bg = CELL_FIXED if (pr, pc) in self.fixed_cells else CELL_NORMAL
                self._set_cell_bg(pr, pc, bg)
            self._selected = (row, col)
            self._set_cell_bg(row, col, "#1e3a5f")   # highlight selected

    def _on_key(self, event):
        if self.mode != "manual" or not self._selected:
            return
        row, col = self._selected
        if (row, col) in self.fixed_cells:
            return
        if event.keysym in ("BackSpace", "Delete", "0"):
            self.current_board.set_cell(row, col, 0)
            self._set_cell_text(row, col, "", FG_USER)
            self._set_cell_bg(row, col, "#1e3a5f")
        elif event.char.isdigit() and event.char != "0":
            num = int(event.char)
            if self.current_board.is_valid_placement(row, col, num):
                self.current_board.set_cell(row, col, num)
                if self.current_board.is_solvable():
                    self._set_cell_text(row, col, str(num), FG_USER)
                    self._set_cell_bg(row, col, "#1e3a5f")
                else:
                    self.current_board.clear_cell(row, col)
                    self._set_cell_text(row, col, str(num), ACCENT)
                    self._set_cell_bg(row, col, CELL_ERR)
            else:
                self._set_cell_text(row, col, str(num), ACCENT)
                self._set_cell_bg(row, col, CELL_ERR)

    class _AbortSolve(Exception):
        pass

    def _abort(self):
        self._stop = True

    def solve_puzzle(self):
        self._stop = False
        self.stats_var.set("")
        self._read_board_from_canvas()
        self.status_var.set("Solving…")
        self.root.update()

        try:
            solved, success, nodes, t = solve_ac3(self.current_board, step_callback=self._anim_cb)
        except SudokuGUI._AbortSolve:
            return  # user aborted mid-solve
        if self._stop:
            return
        if success:
            self.current_board = SudokuBoard(solved)
            self._refresh_solved(solved)
            self.status_var.set(f"Solved!  Nodes: {nodes}  |  Time: {t:.3f}s")
            self.stats_var.set(f"Nodes explored: {nodes}   |   Solve time: {t:.3f} s")
        else:
            self.status_var.set("No solution exists for this puzzle")
            messagebox.showerror("No solution", "This puzzle has no solution.")

    def _anim_cb(self, row, col, num):
        if self._stop:
            raise SudokuGUI._AbortSolve()  # instantly unwinds the recursion
        if num != 0:
            self._set_cell_text(row, col, str(num), FG_ANIM)
            self._set_cell_bg(row, col, CELL_SOLVE)
        else:
            self._set_cell_text(row, col, "", FG_USER)
            self._set_cell_bg(row, col, CELL_NORMAL)
        self.root.update()

    def _refresh_solved(self, board):
        for i in range(9):
            for j in range(9):
                if (i, j) not in self.fixed_cells:
                    self._set_cell_text(i, j, str(board[i][j]), FG_USER)
                    self._set_cell_bg(i, j, CELL_NORMAL)

    def _read_board_from_canvas(self):
        for i in range(9):
            for j in range(9):
                txt = self.canvas.itemcget(self.cells[i][j], "text")
                val = int(txt) if txt.isdigit() else 0
                self.current_board.set_cell(i, j, val)

    def generate_random(self):
        self._abort()
        self.stats_var.set("")
        self.status_var.set("Generating new puzzle…")
        self.root.update()
        self._stop = False

        puzzle, _ = generate_random_puzzle(32)
        self.current_board = puzzle
        self._load_board_to_display()
        self.status_var.set("New puzzle ready — click SOLVE")

    def clear_board(self):
        self._abort()
        self._stop = False
        self.stats_var.set("")
        self.fixed_cells = set()
        self.current_board = SudokuBoard()
        self._selected = None
        for i in range(9):
            for j in range(9):
                self._set_cell_text(i, j, "", FG_USER)
                self._set_cell_bg(i, j, CELL_NORMAL)
        self.status_var.set("Board cleared")

    def check_user_input(self):
        self._read_board_from_canvas()
        valid, msg = self.current_board.validate_full_board()
        if valid:
            if self.current_board.is_complete():
                messagebox.showinfo("Complete!", "Congratulations — puzzle solved!")
            elif not self.current_board.is_solvable():
                messagebox.showinfo("Invalid", "Board isn't solvable!")
            else:
                messagebox.showinfo("Valid", "No conflicts so far!")
            self.status_var.set("Board is valid")
        else:
            messagebox.showerror("Invalid", msg)
            self.status_var.set("Board has errors")


if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()