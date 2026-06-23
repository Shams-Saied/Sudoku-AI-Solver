# Sudoku AI Solver

An AI-powered Sudoku Solver developed as part of the Artificial Intelligence course at Alexandria University. This project models Sudoku as a Constraint Satisfaction Problem (CSP) and uses Arc Consistency (AC-3) together with Backtracking Search to efficiently solve puzzles. The application includes an interactive Tkinter-based graphical user interface, puzzle generation, solution visualization, and user input validation.

---

## Project Overview

Sudoku is a logic-based puzzle played on a 9×9 grid. The objective is to fill the grid with numbers from 1 to 9 such that:

- Each row contains all digits from 1 to 9 exactly once.
- Each column contains all digits from 1 to 9 exactly once.
- Each 3×3 subgrid contains all digits from 1 to 9 exactly once.

This project models Sudoku as a Constraint Satisfaction Problem (CSP), applies Arc Consistency (AC-3) to reduce domains, and then uses Backtracking Search to find a complete solution when necessary.

---

## Features

### GUI Features

- Modern Tkinter-based graphical interface
- Auto Solve mode
- User Input mode
- Interactive board editing
- Real-time validation of user entries
- Visual AI solving animation
- Random puzzle generation
- Puzzle solvability checking
- Statistics display (nodes explored and solving time)

### AI Features

- Constraint Satisfaction Problem (CSP) representation
- Arc Consistency (AC-3) preprocessing
- Backtracking Search solver
- Domain reduction visualization
- Random puzzle generation with unique solutions
- Solvability verification

---

## Algorithms Implemented

### 1. Constraint Satisfaction Problem (CSP)

Sudoku is represented as a CSP:

#### Variables

Each cell in the Sudoku grid is considered a variable.

#### Domains

- Filled cells → singleton domain {value}
- Empty cells → domain {1,2,3,4,5,6,7,8,9}

#### Constraints

- No duplicate values in a row
- No duplicate values in a column
- No duplicate values in a 3×3 box

---

### 2. Arc Consistency (AC-3)

The AC-3 algorithm is used to reduce variable domains before applying search.

#### Steps

1. Initialize domains for all cells.
2. Create arcs between related cells.
3. Apply the Revise operation.
4. Remove inconsistent values.
5. Reinsert affected arcs into the queue.
6. Continue until no more reductions are possible.

The implementation records domain reductions and can display the Arc Consistency Tree for analysis.

---

### 3. Backtracking Search

Backtracking is used for:

- Solving remaining unsolved cells after AC-3
- Verifying puzzle solvability
- Generating complete Sudoku boards
- Ensuring generated puzzles have unique solutions

#### Backtracking Process

1. Find an empty cell.
2. Try values 1–9.
3. Check constraint satisfaction.
4. Recurse.
5. Backtrack if a conflict occurs.

---

## Project Structure

```text
Sudoku-AI-Solver/
│
├── gui.py
├── board.py
├── algorithms.py
├── ac3.py
├── notebook.ipynb
│
├── report.pdf
├── README.md
├── requirements.txt
│
└── screenshots/
    ├── gui.png
    ├── solving.png
    └── random_generation.png
```

### File Descriptions

#### gui.py

Contains the Tkinter graphical user interface.

Responsibilities:

- Drawing the Sudoku board
- Handling user interaction
- Visualizing solving progress
- Managing game modes

#### board.py

Represents the Sudoku board.

Responsibilities:

- Board storage
- Cell access and updates
- Constraint checking
- Solvability validation

#### ac3.py

Implements the Arc Consistency (AC-3) algorithm.

Responsibilities:

- Domain initialization
- Arc generation
- Domain reduction
- Arc consistency tree generation

#### algorithms.py

Contains all solving and puzzle generation algorithms.

Responsibilities:

- Backtracking search
- AC-3 integration
- Puzzle generation
- Solution uniqueness checking

#### notebook.ipynb

Contains experiments, performance analysis, and comparison between different Sudoku difficulties.

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/Sudoku-AI-Solver.git
cd Sudoku-AI-Solver
```

### Install Requirements

```bash
pip install -r requirements.txt
```

---

## Running the Application

Launch the GUI:

```bash
python gui.py
```

---

## Using the Application

### Auto Solve Mode

1. Start the application.
2. A sample Sudoku puzzle is loaded automatically.
3. Click **SOLVE**.
4. Watch the AI solve the puzzle using AC-3 and Backtracking.

### User Input Mode

1. Select **User Input** mode.
2. Enter a custom Sudoku puzzle.
3. Use **CHECK** to validate the board.
4. Click **SOLVE** to let the AI solve it.

### Generate Random Puzzle

1. Click **NEW GAME**.
2. A new random Sudoku puzzle is generated.
3. Click **SOLVE** to watch the AI solve it.

---

## Example Output Statistics

After solving a puzzle, the application displays:

```text
Solved!
Nodes explored: 1542
Solve time: 0.032 s
```

These values may vary depending on puzzle difficulty.

---

## Arc Consistency Tree

The implementation records domain reductions during AC-3 execution.

Example:

```text
Cell (0, 2)
 ├── remove 5 (conflict with row)
 ├── remove 3 (conflict with row)
 └── remaining {1, 2, 4}

Cell (1, 1)
 ├── remove 6 (conflict with column)
 ├── remove 9 (conflict with box)
 └── remaining {1, 2, 4, 7}
```

This information is printed in the console and can be included in the project report.

---

## Performance Analysis

The notebook and report compare solving performance across different puzzle difficulties.

Metrics evaluated:

- Solving time
- Nodes explored
- AC-3 domain reductions
- Search efficiency

Example comparison:

| Difficulty | Nodes Explored | Time (s) |
| ---------- | -------------- | -------- |
| Easy       | 532            | 0.012    |
| Medium     | 1542           | 0.032    |
| Hard       | 7841           | 0.118    |

---

## Screenshots

### Main Interface

Insert screenshot:

```text
screenshots/gui.png
```

### AI Solving Visualization

Insert screenshot:

```text
screenshots/solving.png
```

### Random Puzzle Generation

Insert screenshot:

```text
screenshots/random_generation.png
```

---

## Course Information

**Course:** Artificial Intelligence

**Faculty:** Faculty of Engineering

**University:** Alexandria University

**Assignment:** Assignment 3 – CSP to Solve Sudoku

---

## Future Improvements

Potential enhancements include:

- Advanced Sudoku solving heuristics
- MRV (Minimum Remaining Values)
- Forward Checking
- Constraint Propagation
- Multiple board sizes
- Difficulty selection
- Better visualization of the AC-3 process
- Exporting solving statistics

---

## Author

Developed as part of the Artificial Intelligence course project.

```text
Name: Shams Saied
ID: 8756

---

## License

This project is intended for educational purposes and course evaluation.

---

## Acknowledgments

Special thanks to the Artificial Intelligence teaching staff at Alexandria University for providing the project requirements and guidance.
```
