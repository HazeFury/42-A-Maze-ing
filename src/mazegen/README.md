# mazegen

A standalone Python package to generate and solve mazes.

## Installation & Build

From the root of the project, build the package:

```bash
python3 -m build
```

## Usage

### Basic Example

```python
from mazegen import MazeGenerator

# Create a generator instance with default parameters (10x10)
mg = MazeGenerator(width=10, height=10)

# Generate the maze
mg.generate_maze()

# Solve the maze from entry (0, 0) to exit (9, 9)
if mg.solve_path(entry_coord=(0, 0), exit_coord=(9, 9)):
    # Access solution directions via the solver attribute of the mg instance
    print(mg.solver.get_solution_directions())

### Custom Parameters

You can instantiate the generator with custom parameters:

```python
from mazegen import MazeGenerator

# Create a generator with custom size and seed for reproducibility
mg = MazeGenerator(width=15, height=15, seed=42)

# Generate the maze (includes 42 pattern if dimensions allow >= 9x7)
mg.generate_maze()

# Solve the maze
mg.solve_path(entry_coord=(0, 0), exit_coord=(14, 14))
```

**Constructor parameters:**
- `width` (int): Width of the maze (default: 10)
- `height` (int): Height of the maze (default: 10)
- `seed` (int | None): Random seed for reproducibility (default: None)

### Methods

#### `generate_maze()`
Generates the maze using the Iterative Backtracker algorithm. If dimensions allow (minimum 9x7), automatically marks a '42' pattern in the grid.

```python
mg.generate_maze()
```

#### `solve_path(entry_coord, exit_coord)`
Solves the maze using BFS algorithm and marks solution cells. Returns None but updates cell properties.

```python
# Solve from top-left to bottom-right
mg.solve_path(entry_coord=(0, 0), exit_coord=(9, 9))

# Check if path was found
if any(cell.is_solution for row in mg.grid for cell in row):
    print("Path found!")
```

#### `replace_seed(new_seed)`
Changes the random seed for generating a different maze.

```python
mg.replace_seed(new_seed=123)
mg.generate_maze()  # Generates a different maze
```

### Accessing the Generated Structure

```python
from mazegen import MazeGenerator

mg = MazeGenerator(width=10, height=10, seed=42)
mg.generate_maze()
mg.solve_path(entry_coord=(0, 0), exit_coord=(9, 9))

# Access the grid directly (List of List of Cell objects)
grid = mg.grid

# Example: Check if the top-left cell has a North wall
first_cell = grid[0][0]
print(f"North wall exists: {first_cell.walls['N']}")

# Get all solution cells
solution_cells = [cell for row in grid for cell in row if cell.is_solution]
print(f"Solution length: {len(solution_cells)} cells")
```

### Cell Structure

Each cell in the maze has the following properties:

```python
cell = mg.grid[0][0]

# Coordinates
print(f"Position: ({cell.x}, {cell.y})")

# Walls (dict with keys: 'N', 'S', 'E', 'W')
# True = wall exists, False = wall broken (passage exists)
print(cell.walls)  # {'N': True, 'S': False, 'E': True, 'W': False}

# Visited by generation algorithm
print(f"Visited: {cell.visited}")

# Part of the 42 pattern (if applicable)
print(f"Part of 42 pattern: {cell.is_part_of_42}")

# Part of the solution path
print(f"Solution path: {cell.is_solution}")
```

## Quick Test (Virtual Environment)

To verify the package is correctly built and standalone:

### 1. Create and activate a virtual environment

```bash
cd /path/to/repo/root  # Navigate to where mazegen-1.0.0-py3-none-any.whl is located
python3 -m venv venv_test && source venv_test/bin/activate
```

### 2. Install the generated wheel

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### 3. Run a full integration test (Generation + Solving)

```bash
cat <<EOF > test_mazegen.py
from mazegen import MazeGenerator

try:
    # 1. Initialize Generator (20x20 grid)
    mg = MazeGenerator(width=20, height=20, seed=42)

    # 2. Generate Maze
    mg.generate_maze()
    print("✅ Generation: Success!")

    # 3. Solve from Top-Left (0,0) to Bottom-Right (19,19)
    # This function returns None, but populates mg.solver
    mg.solve_path(entry_coord=(0, 0), exit_coord=(19, 19))

    # 4. Check if a solution was actually found by looking at the solver
    if mg.solver and len(mg.solver.get_solution_directions()) > 0:
        print("✅ Solving: Success! Path found.")
        directions = mg.solver.get_solution_directions()
        print(f"Path Length: {len(directions)} steps")
        print(f"First 20 moves: {directions[:20]}...")
    else:
        print("❌ Solving: No path found.")

except Exception as e:
    print(f"❌ Error: {e}")
EOF

python3 test_mazegen.py
```
