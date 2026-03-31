from mazegen.cell import Cell
from collections import deque


class Solver:
    """
        Solve a maze using the Breadth-First Search (BFS) algorithm.

        This class takes a generated grid and finds the shortest path between
        an entry point and an exit point by exploring accessible neighbors.
        """
    def __init__(
        self,
        grid: list[list[Cell]],
        width: int,
        height: int,
        entry_coord: tuple[int, int],
        exit_coord: tuple[int, int]
    ) -> None:
        """
        Initialize the solver
        with grid data and entry and exit coordinates.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.entry_x, self.entry_y = entry_coord
        self.exit_x, self.exit_y = exit_coord
        self.path: list[Cell] = []

    def _get_cell(self, x: int, y: int) -> Cell | None:
        """
        Return the Cell object at the given coordinates if within bounds.

        Return None if coordinates are outside the grid dimensions.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def solve(self) -> bool:
        """
        Execute the BFS algorithm to find the shortest path to the exit.

        Return True if a path is found and reconstructed, False otherwise.
        """
        start_node = self._get_cell(self.entry_x, self.entry_y)
        exit_node = self._get_cell(self.exit_x, self.exit_y)

        if not start_node or not exit_node:
            return False

        queue = deque([start_node])

        child_from: dict[Cell, Cell | None] = {}
        child_from[start_node] = None

        while queue:
            current = queue.popleft()

            if current == exit_node:
                self._reconstruct_path(child_from, exit_node)
                return True

            for neighbor in self._get_accessible_neighbors(current):
                if neighbor not in child_from:
                    child_from[neighbor] = current
                    queue.append(neighbor)

        return False

    def _get_accessible_neighbors(self, cell: Cell) -> list[Cell]:
        """
        Identify adjacent cells reachable from the current cell.

        A neighbor is accessible only if there is no wall between it
        and the current cell.
        """
        accessible_neighbors: list[Cell] = []

        adjacent_cells: tuple[tuple[int, int, str], ...]
        adjacent_cells = ((0, -1, 'N'), (1, 0, 'E'), (0, 1, 'S'), (-1, 0, 'W'))

        for adjacent_cell in adjacent_cells:
            dx, dy, direction = adjacent_cell
            if not cell.walls[direction]:
                neighbor = self._get_cell(dx + cell.x, dy + cell.y)
                if neighbor:
                    accessible_neighbors.append(neighbor)

        return accessible_neighbors

    def _reconstruct_path(
            self, child_from: dict[Cell, Cell | None], exit_node: Cell
            ) -> None:
        """
        Backtrack from the exit node to the start node to build the path.

        Update self.path with the ordered list of Cells and mark them
        as part of the solution.
        """
        path = []
        current_node: Cell | None = exit_node

        while current_node is not None:
            path.append(current_node)

            current_node.is_solution = True

            parent_node = child_from[current_node]
            if parent_node:

                if current_node.x == parent_node.x:

                    if current_node.y > parent_node.y:
                        current_node.path_connections["N"] = True
                        parent_node.path_connections["S"] = True
                    else:
                        current_node.path_connections["S"] = True
                        parent_node.path_connections["N"] = True
                else:
                    if current_node.x > parent_node.x:
                        current_node.path_connections["W"] = True
                        parent_node.path_connections["E"] = True
                    else:
                        current_node.path_connections["E"] = True
                        parent_node.path_connections["W"] = True

            current_node = parent_node

        self.path = path[::-1]
