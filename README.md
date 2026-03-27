*This project has been created as part of the 42 curriculum by marberge, stmaire.*

# A-Maze-ing 🧩

## I. Description

**A-Maze-ing** is a comprehensive Python package dedicated to the generation and resolution of two-dimensional mazes. Developed as part of the 42 curriculum, this project implements fundamental graph theory algorithms to transform a blank grid into a complex, structured puzzle.

### Project Goals
The primary objective is to provide a robust library capable of:
* **Generating** mazes of variable dimensions ($N \times M$), ensuring either a **perfect maze** (a unique path with no loops) or an **imperfect maze** (multiple possible paths via an adjustable imperfection rate).
* **Solving** for the shortest path between two given coordinates efficiently using a graph traversal algorithm.
* **Exporting** data in a standardized format, including a hexadecimal representation of the grid (wall encoding) and the sequence of cardinal directions (N, S, E, W) constituting the solution.

### Technical Overview
The project is built on an object-oriented architecture where each **Cell** manages its own wall states. The core engine, the `MazeGenerator`, orchestrates the various stages: from grid initialization and the application of a specific "42" pattern to the production of an output file compliant with the subject's specifications. 

Security and reliability are central to the implementation, featuring strict object state management (guards) to prevent invalid operations, such as attempting to solve a maze before it has been generated or exporting a file before a solution is found.
## II. Instructions
### 1. Installation
### 2. Compilation / Build
### 3. Execution
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
---