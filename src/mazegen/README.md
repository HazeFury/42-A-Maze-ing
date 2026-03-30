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
2. **Generate`generate_maze()`** to build the internal structure. If `perfect` is `False`, you can pass an `imperfection_rate` (0.0 to 1.0) to break extra walls and create loops.
3. **Solve the maze `solve_path()`** with parameters : `entry_coord`, `exit_coord`. It returns `True` if a path is found and marks the corresponding cells internally.
4. **Retrieve the solution**: Once solved, use `get_solution_in_str()` with parameters : `entry_coord`, `exit_coord` to get the cardinal directions.
5. **Export the maze** to a formatted file (`filename`) using `export_maze_to_file()`, with parameters : `entry_coord`, `exit_coord`, `filename`.

### Basic Example

```python
from mazegen import MazeGenerator

# Create a generator instance with default parameters (10x10, perfect=True)
mg = MazeGenerator(width=10, height=10, perfect=True)

# Generate the maze
mg.generate_maze()

# Find and display the solution
mg.solve_path((0, 0), (9, 9))
print(f"Solution: {mg.get_solution_in_str((0, 0), (9, 9))}")

# Export to a standardized file
mg.export_maze_to_file((0, 0), (9, 9), "maze.txt")
```

### Custom Parameters

You can instantiate the generator with custom parameters:

```python
from mazegen import MazeGenerator

# Create a generator with custom size and seed for reproducibility
mg = MazeGenerator(width=15, height=15, perfect=False, seed=42)

# Generate with a custom imperfection rate (e.g., 20% of walls broken)
mg.generate_maze(imperfection_rate=0.2)
```
`seed`: Can be int, str, float. Ensures the same maze is generated every time.
`imperfection_rate`: Float (between 0.0 to 1.0). Only used when perfect=False.

### Constructor Parameters

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `width` | `int` | **Required** | Width of the maze (minimum 2). |
| `height` | `int` | **Required** | Height of the maze (minimum 2). |
| `perfect` | `bool` | **Required** | `True` for a unique path, `False` for loops. |
| `seed` | `int, str, float, None` | `None` | Seed for reproducibility (accepts `int`, `str`, `float`). |
| `imperfection_rate` | `float` | `0.1` | Only for non-perfect mazes. Defines the percentage of additional walls to remove (0.0 to 1.0) to create loops and multiple paths. |


### Accessing the Generated Structure

The module provides direct access to the internal data for programmatic use.

### The Cell Object

The maze is composed of a 2D grid of `Cell` objects.

| Attribute | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `x`, `y` | `int` | **Required** | The horizontal and vertical coordinates in the grid. |
| `visited` | `bool` | `False` | Used by the `MazeBuilder` to track progress during generation. |
| `walls` | `dict` | `All True` | A dictionary `{"N", "E", "S", "W"}` representing the 4 physical walls. |
| `is_part_of_42` | `bool` | `False` | Flag identifying if the cell belongs to the decorative "42" pattern. |
| `is_solution` | `bool` | `False` | Flag identifying if the cell is part of the shortest path found by the solver. |
| `path_connections`| `dict` | `All False` | Stores the directions (`N, E, S, W`) of the solution path for rendering. |

#### Logic & Connectivity
Initially, each cell is a **solid block** with all four walls set to `True`. 
* **Maze Generation**: The `MazeBuilder` "sculpts" the maze by breaking walls (setting them to `False`) to create passages between cells.
* **Pathfinding**: Once solved, the `is_solution` flag is toggled for all cells on the solution path. The `path_connections` attribute specifically stores the flow of the solution, which is used to generate the final cardinal direction string (N, S, E, W).

#### The Grid Structure

The maze is stored as a 2D array (list of lists) of `Cell` objects. Each cell knows its own coordinates and the binary state of its four walls.

```python
# Access the 2D grid
grid = mg.grid  # List[List[Cell]]

# Inspect a specific cell (e.g., at row 2, column 5)
cell = grid[2][5]
print(f"Coordinates: x={cell.x}, y={cell.y}")

# Check walls (True means the wall exists/is closed)
# The dictionary keys are 'N', 'S', 'E', 'W'
print(f"Walls state: {cell.walls}")
# Example output: {'N': True, 'S': False, 'E': True, 'W': False}
```

#### Accessing the Solution

After calling `solve_path()`, the solution is encoded directly into the grid's metadata. You can access it in two distinct ways:

**A. Solution Flags (Unordered)**

Each Cell object involved in the shortest path has its is_solution attribute set to True. This is ideal for highlighting the path in a graphical interface.

```python
# After running mg.solve_path(entry, exit)
# Check if a specific cell is part of the path
if mg.grid[y][x].is_solution:
    print("This cell is part of the shortest path.")

# Extract all solution coordinates (Note: this list will be unordered)
solution_points = [
    (c.x, c.y) for row in mg.grid for c in row if c.is_solution
]

print(f"Cells part of the solution (unordered): {solution_points}")
```

**B. Solution Sequence (Ordered)**
To get the exact sequence of moves from the entry to the exit, use the dedicated getter. This provides the solution in the cardinal direction format required by the project.

```python
# Returns the ordered sequence of directions
path_sequence = mg.get_solution_in_str((0, 0), (9, 9))

print(f"Path directions: {path_sequence}")
# Example output: "EENSSW"
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

This script demonstrates a complete workflow: instantiating a maze, generating its structure with imperfections, solving it, and exporting the result.

**The test will:**
- Create a 20×20 non-perfect maze with a fixed seed for reproducibility
- Generate the maze with a 15% imperfection rate (creating loops and multiple paths)
- Solve the maze and export the result to `test.map`

**Copy and paste this command into your terminal:**

```bash
cat <<EOF > test_mazegen.py
from mazegen import MazeGenerator

try:
    mg = MazeGenerator(width=20, height=20, perfect=False, seed=42)
    # Generate with 15% imperfection
    mg.generate_maze(imperfection_rate=0.15)
    
    # Export handles solving and file writing
    mg.export_maze_to_file((0, 0), (19, 19), "test.map")
    print("✅ Success: 'test.map' generated!")
except Exception as e:
    print(f"❌ Error: {e}")
EOF

python3 test_mazegen.py
```