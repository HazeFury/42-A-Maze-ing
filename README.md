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

## IV. Technical Choices

### 1. Configuration File Structure

### 2. Maze Generation Algorithm

### 3. Why this Algorithm?

## V. Reusability

## VI. Project Management

### 1. Team Roles

### 2. Planning & Evolution

### 3. Retrospective

### 4. Tools Used

## VII. Resources

### 1. References

### 2. AI Usage Disclosure