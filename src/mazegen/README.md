# mazegen

### A standalone Python package to generate and solve mazes.


This documentation covers the following requirements:
- **Instantiation and Basic Usage**: How to create and use the generator with a basic example.
- **Custom Parameters**: Passing parameters like size and seed.
- **Accessing Generated Structure and Solution**: How to access the maze grid and solution.

### Installation

From the root of the project, install the package:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Instantiation and Usage Overview

To use the maze generator, follow this standard workflow:

1. **Instantiate `MazeGenerator`** with your desired parameters (`width`, `height`, `perfect`, and an optional `seed`).
2. **Call `generate_maze()`** to build the internal structure. If `perfect` is `False`, you can pass an `imperfection_rate` (0.0 to 1.0) to break extra walls and create loops.
3. **Optionally, call `solve_path()`** to find the shortest path between your entry and exit points.
4. **Access the grid** directly for custom logic or **export the maze** to a formatted file using `export_maze_to_file()`.

### Basic Example

```python
from mazegen import MazeGenerator

# Create a generator instance with default parameters (10x10, perfect=True)
mg = MazeGenerator(width=10, height=10, perfect=True)

# Generate the maze
mg.generate_maze()

# Solve the maze from entry (0, 0) to exit (9, 9)
if mg.solve_path(entry_coord=(0, 0), exit_coord=(9, 9)):
    # Access solution directions via the solver attribute of the mg instance
    print(mg.solver.get_solution_directions())

# Export to a file (includes hexadecimal grid and solution path)
mg.export_maze_to_file(
    entry_coord=(0, 0), 
    exit_coord=(9, 9), 
    filename="maze.txt"
)
```

### Custom Parameters

You can instantiate the generator with custom parameters:

```python
from mazegen import MazeGenerator

# Create a generator with custom size and seed for reproducibility
mg = MazeGenerator(width=15, height=15, perfect=False, seed=42)

# Generate with a custom imperfection rate (e.g., 20% of walls broken)
mg.generate_maze(imperfection_rate=0.2)

# Solve and export
mg.export_maze_to_file((0, 0), (14, 14), "maze.txt")
```

**Constructor parameters:**
- `width` (int): Width of the maze (default: 10)
- `height` (int): Height of the maze (default: 10)
- `perfect` (bool): generate a perfect maze if perfect is True
- `seed` (int | None): Random seed for reproducibility (default: None)
- `imperfection_rate` (float | None): Only for non-perfect mazes. Defines the percentage of extra walls to remove (0.0 to 1.0).


### Accessing the Generated Structure

The module provides direct access to the internal data for programmatic use:

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

# Access the solution
# solve_path() uses BFS to find the shortest route
mg.solve_path(entry_coord=(0, 0), exit_coord=(9, 9))

# Get all solution cells
solution_cells = [cell for row in grid for cell in row if cell.is_solution]
print(f"Solution length: {len(solution_cells)} cells")
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
    mg = MazeGenerator(width=20, height=20, perfect=False, seed=42)
    # Generate with 15% imperfection
    mg.generate_maze(imperfection_rate=0.15)
    
    # Export handles solving and file writing
    mg.export_maze_to_file((0,0), (19,19), "test.map")
    print("✅ Success: 'test.map' generated!")
except Exception as e:
    print(f"❌ Error: {e}")
EOF

python3 test_mazegen.py
```
