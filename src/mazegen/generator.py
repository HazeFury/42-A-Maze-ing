import random
from mazegen.Cell import Cell


class IterativeBacktracker:
    """Algorithm class to generate a maze using iterative backtracking."""

    def __init__(
            self, grid: list[list[Cell]], width: int, height: int,
            rng: random.Random
            ) -> None:
        """
        Initializes the generator with the grid and a seeded random instance.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.rng = rng

    def _get_cell(self, x: int, y: int) -> Cell | None:
        """
        Return the cell at coordinates (x, y) or None if out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def _get_unvisited_neighbors(
            self,
            cell: Cell
            ) -> list[tuple[Cell, str]]:
        """
        Find all adjacent cells that are within bounds and not yet visited.
        """
        unvisited_neighbors = []

        adjacent_cells: tuple[tuple[int, int, str], ...]
        adjacent_cells = ((0, -1, 'N'), (1, 0, 'E'), (0, 1, 'S'), (-1, 0, 'W'))

        for adjacent_cell in adjacent_cells:
            dx, dy, direction = adjacent_cell
            neighbor = self._get_cell(dx + cell.x, dy + cell.y)
            if neighbor and not neighbor.visited:
                unvisited_neighbors.append((neighbor, direction))

        return unvisited_neighbors

    def _remove_walls(
            self,
            cell: Cell,
            adjacent_cell: Cell,
            direction: str
            ) -> None:
        """
        Break the wall between the current cell and the chosen neighbor.
        """
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}

        cell.break_wall(direction)
        adjacent_cell.break_wall(opposite[direction])

    def generate(self) -> None:
        """
        Generate a perfect maze using the Iterative Backtracking algorithm.
        """
        if self.width <= 0 or self.height <= 0:
            raise ValueError(f"Invalid maze dimensions: "
                             f"{self.width}x{self.height}")

        stack: list[Cell] = []
        current_cell = self._get_cell(0, 0)

        if current_cell:
            stack.append(current_cell)
            current_cell.visited = True

        while stack:
            current_cell = stack[-1]

            unvisited_neighbors: list[tuple[Cell, str]]
            unvisited_neighbors = self._get_unvisited_neighbors(current_cell)

            if unvisited_neighbors:
                adjacent_cell, direction = self.rng.choice(
                    unvisited_neighbors
                    )
                self._remove_walls(current_cell, adjacent_cell, direction)
                adjacent_cell.visited = True
                stack.append(adjacent_cell)

            else:
                stack.pop()
