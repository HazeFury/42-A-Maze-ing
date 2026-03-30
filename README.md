*This project has been created as part of the 42 curriculum by marberge, stmaire.*

# A-Maze-ing 

## I. Description

**A-Maze-ing** is a comprehensive Python package dedicated to the generation and resolution of two-dimensional mazes. Developed as part of the 42 curriculum, this project implements fundamental graph theory algorithms to transform a blank grid into a complex, structured puzzle.

### Project Goals

The primary objective is to provide a robust library capable of:

* **Generating** mazes of variable dimensions ($N \times M$), ensuring either a **perfect maze** (a unique path with no loops) or an **imperfect maze** (multiple possible paths via an adjustable imperfection rate).
* **Solving** for the shortest path between two given coordinates efficiently using a graph traversal algorithm.
* **Exporting** data in a standardized format, including a hexadecimal representation of the grid (wall encoding) and the sequence of cardinal directions (N, S, E, W) constituting the solution.

### Technical Overview

The project is built on an object-oriented architecture where each **Cell** manages its own wall states. The core engine, the `MazeGenerator`, orchestrates the various stages: from grid initialization to the production of an output file compliant with the subject's specifications. 

## II. Instructions

This project includes a Makefile to automate setup, execution, and code quality control. Python 3.10+ is required.

### 1. Installation

The installation process sets up a virtual environment and installs all dependencies (including build, flake8, and mypy).

**Using Makefile:**

```bash
make install
```

**Manual Alternative:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip build
pip install -e ".[dev]"
```

### 2. Compilation / Build

This step generates the standalone reusable package (.whl) required for the project submission.

**Using Makefile:**
The `make install` rule automatically triggers the build process.

**Manual Alternative:**

```bash
# Generate the distribution files
python3 -m build

# Copy the wheel to the root as required by the subject
cp dist/mazegen-1.0.0-py3-none-any.whl .

```

### 3. Execution & Debug

You can run the generator or launch it in debug mode to inspect the execution flow.

**Standard Run:** Executes the main script with the default configuration.

```bash
# Using Makefile
make run

# Manual
python3 a_maze_ing.py config.txt
```

**Debug Mode:** Runs the script using Python's built-in debugger (pdb).

```bash
# Using Makefile
make debug

# Manual
python3 -m pdb a_maze_ing.py config.txt
```

### 4. Quality Control & Maintenance

To ensure the code meets the project's rigorous standards, the following rules are available:

* **Linting (Mandatory):** Checks code style and type hinting with specific safety flags.

```bash
# Using Makefile
make lint

# Manual
flake8 a_maze_ing.py src/ app/
mypy a_maze_ing.py src/ app/ --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs
```

* **Linting (Strict):** Enhanced checking for maximum type safety. Runs: flake8 and mypy with --warn-return-any, --disallow-untyped-defs, etc.

```bash
# Using Makefile
make lint-strict

# Manual
flake8 a_maze_ing.py src/ app/
mypy a_maze_ing.py src/ app/ --strict
```
* **Cleaning:**

```bash
# Using Makefile (standard clean)
make clean

# Manual (standard clean)
rm -rf .mypy_cache .pytest_cache build/ dist/ src/*.egg-info
find . -type d -name "__pycache__" -exec rm -rf {} +

# Using Makefile (full reset)
make fclean

# Manual (full reset)
# Run the manual clean steps above, then:
rm -rf venv/
rm -f mazegen-1.0.0-py3-none-any.whl
```

## III. Usage & Features

The **A-Maze-ing** project is strictly divided into two distinct parts: a standalone, reusable core library (`mazegen`) and an interactive Command Line Interface (CLI) application that utilizes this library.

### 1. Project Architecture

Below is the tree structure of the main components of the repository:

	.
	├── a_maze_ing.py
	├── app/
	│   ├── display.py
	│   ├── __init__.py
	│   └── parser.py
	├── config.txt
	├── src/
	│   └── mazegen/
	│       ├── cell.py
	│       ├── exporter.py
	│       ├── maze_builder.py
	│       ├── maze_generator.py
	│       └── solver.py
	└── tests/
	    └── test_parser.py

### 2. Component Overview

#### The Core Library (`src/mazegen/`)
This module contains the pure algorithmic heart of the project. It is designed to be completely decoupled from the UI, making it fully reusable for future projects (like a Pac-Man game). It operates silently without standard output.
* **`cell.py`**: The fundamental data structure representing a single grid unit, managing its coordinates, wall states (N, S, E, W), and pathfinding metadata.
* **`maze_builder.py` & `maze_generator.py`**: The orchestrators responsible for carving the maze using the Recursive Backtracking algorithm and handling the "42" pattern integration.
* **`solver.py`**: Implements a Breadth-First Search (BFS) algorithm to compute the shortest guaranteed path from the entry to the exit point.
* **`exporter.py`**: Translates the mathematical grid into the required hexadecimal output format and writes the solution file.

#### The CLI Application (`app/` & `a_maze_ing.py`)
This is the interactive wrapper built around the core library. 
* **`a_maze_ing.py`**: The main entry point that ties the configuration, the generation engine, and the display together.
* **`parser.py`**: A robust configuration file parser that extracts, validates, and types the data from `config.txt` before feeding it to the generator.
* **`display.py`**: The visual engine of the application.

#### Reliability (`tests/`)
A dedicated test suite using `pytest` to automatically verify the integrity of the parsing logic and the mathematical correctness of the generated mazes (dimensions, perfect/imperfect states).

### 3. Advanced UI Features

To provide the best User Experience (UX) possible, the project features an advanced Text User Interface (TUI) powered by the Python `curses` library. 

When running the project, the maze is rendered in a dedicated Alternate Screen Buffer with the following interactive features:
* **Extended Grid Rendering**: The maze is displayed using an expanded pixel-like ASCII approach, ensuring perfectly proportioned walls and corridors.
* **Real-time Regeneration**: Pressing a dedicated key dynamically generates a brand-new maze based on a new seed and redraws it instantly without restarting the script.
* **Interactive Pathfinding Toggle**: The BFS solution path (rendered as a continuous, flowing line connecting the Entry and Exit points) can be shown or hidden on the fly.
* **Dynamic Color Switching**: Users can cycle through a curated palette of xterm-256color hex values for the maze walls to customize the display.
* **Responsive Design**: The interface constantly listens for OS-level terminal resize events. If the window becomes too small to display the maze, it safely hides the grid and prompts the user to enlarge the window, preventing visual glitches.

## IV. Technical Choices

### 1. Configuration File Structure
The generator is driven by a `config.txt` file, allowing parameters to be adjusted without modifying the source code. The file follows a clear `KEY=VALUE` format:

```ini
# Maze Configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=False
SEED=42
IMPERFECTION_RATE=0.2
```

| Parameter | Description |
| :--- | :--- |
| **WIDTH / HEIGHT** | Grid dimensions (minimum **2x2**). |
| **ENTRY / EXIT** | Starting and ending coordinates in `x,y` format (e.g., `0,0`). |
| **OUTPUT_FILE** | The filename where the generated maze will be saved (e.g., `.txt` or `.map`). |
| **PERFECT** | `True`: Exactly one path (no loops). `False`: Allows multiple paths and cycles. |
| **SEED** | (Optional) A value to initialize the random generator for reproducible mazes. |
| **IMPERFECTION_RATE** | Used only if `PERFECT=False`. A float (**0.0 to 1.0**) representing the percentage of additional walls to remove to create loops. |

### 2. Maze Generation Algorithm: Recursive Backtracking
We implemented **Recursive Backtracking**, which is based on a **Depth-First Search (DFS)** approach.



#### How it works:
* **Start**: Pick a starting cell and mark it as "visited".
* **Move**: Randomly select an unvisited neighbor, "break" the wall between the two cells, and move to that neighbor.
* **Backtrack**: If a cell has no unvisited neighbors (a dead-end), the algorithm goes back to the previous cell and repeats the process until every cell in the grid has been visited.
* **Imperfection Pass**: If `PERFECT` is set to `False`, the builder performs an extra step to remove a specific percentage of remaining walls, creating shortcuts and cycles.

### 3. Why this Algorithm?
We selected **Recursive Backtracking** for three specific reasons:

* **High-Quality Mazes**: Unlike other methods (like Prim’s), it creates mazes with **long, winding corridors** and fewer intersections. This makes the maze more challenging to solve and more visually interesting.
* **Perfect Logic**: It naturally guarantees a **"perfect" maze** where every cell is reachable and there are no isolated areas. This provides a solid base before we manually add loops for the "non-perfect" mode.
* **Easy Implementation**: The algorithm's need to track "visited" cells and "walls" matches our **`Cell` object** perfectly. Each cell carries its own data, making the generator's movement through the grid simple to code and debug.

## V. Reusability

## VI. Project Management

### 1. Team Roles

### 2. Planning & Evolution

### 3. Retrospective

### 4. Tools Used

## VII. Resources

### 1. References

### 2. AI Usage Disclosure