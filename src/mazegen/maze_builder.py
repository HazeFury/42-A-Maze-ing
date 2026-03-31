import random
from mazegen.cell import Cell


class MazeBuilder:
    """Builder class responsible for the physical construction of the maze
    (walls and loops)."""

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

    def _get_neighbor_coords(
            self, x: int, y: int, direction: str
            ) -> tuple[int, int]:
        """Calculate neighbor coordinates based on the given direction."""
        neighbors = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
        dx, dy = neighbors[direction]
        return (x + dx, y + dy)

    def _get_unvisited_neighbors(
            self,
            cell: Cell
            ) -> list[tuple[Cell, str]]:
        """
        Find all adjacent cells that are within bounds
        and not yet visited.
        """
        unvisited_neighbors = []

        directions = ('N', 'E', 'S', 'W')

        for direction in directions:
            nx, ny = self._get_neighbor_coords(cell.x, cell.y, direction)
            neighbor = self._get_cell(nx, ny)
            if neighbor and not neighbor.visited:
                unvisited_neighbors.append((neighbor, direction))

        return unvisited_neighbors

    def _remove_walls(
            self, cell: Cell, neighbor: Cell, direction: str
            ) -> None:
        """Break the walls between the current cell and its neighbor."""
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[direction]
        cell.break_wall(direction)
        neighbor.break_wall(opposite)

    def _repair_walls(
            self, cell: Cell, neighbor: Cell, direction: str
            ) -> None:
        """Restore the walls between the current cell and its neighbor."""
        opposite = {'N': 'S', 'S': 'N', 'E': 'W', 'W': 'E'}[direction]
        cell.repair_wall(direction)
        neighbor.repair_wall(opposite)

    def _is_creating_forbidden_area(
            self, x: int, y: int, direction: str
            ) -> bool:
        """Check if breaking a wall violates the 3x3 open area constraint."""

        nx, ny = self._get_neighbor_coords(x, y, direction)
        neighbor = self._get_cell(nx, ny)
        current = self._get_cell(x, y)

        if not current or not neighbor:
            return True

        self._remove_walls(current, neighbor, direction)

        has_3x3 = False
        for i in range(x - 2, x + 1):
            for j in range(y - 2, y + 1):
                if self._is_3x3_area_empty(i, j):
                    has_3x3 = True
                    break

        if has_3x3:
            self._repair_walls(current, neighbor, direction)

        return has_3x3

    def _is_3x3_area_empty(self, start_x: int, start_y: int) -> bool:
        """"
        Check if a specific 3x3 block
        is completely free of internal walls.
        """

        if (
            start_x < 0 or start_y < 0
            or start_x + 2 >= self.width
            or start_y + 2 >= self.height
        ):
            return False

        for i in range(start_x, start_x + 3):
            for j in range(start_y, start_y + 3):
                cell = self._get_cell(i, j)
                if not cell:
                    continue

                if i < start_x + 2 and cell.walls['E']:
                    return False

                if j < start_y + 2 and cell.walls['S']:
                    return False

        return True

    def degrade_perfection(self, amount: int) -> None:
        """Add cycles to the maze by breaking additional walls at random."""
        broken = 0
        attempts = 0
        max_attempts = amount * 20

        while broken < amount and attempts < max_attempts:
            attempts += 1
            x = self.rng.randint(0, self.width - 1)
            y = self.rng.randint(0, self.height - 1)
            direction = self.rng.choice(['N', 'E', 'S', 'W'])

            current = self._get_cell(x, y)
            nx, ny = self._get_neighbor_coords(x, y, direction)
            neighbor = self._get_cell(nx, ny)

            if (current and neighbor and
                not current.is_part_of_42 and
                not neighbor.is_part_of_42 and
                    current.walls[direction]):
                if not self._is_creating_forbidden_area(x, y, direction):
                    broken += 1

    def generate(self) -> None:
        """
        Generate a perfect maze
        using the Iterative Backtracking algorithm.
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
                neighbor, direction = self.rng.choice(
                    unvisited_neighbors
                    )
                self._remove_walls(current_cell, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)

            else:
                stack.pop()
