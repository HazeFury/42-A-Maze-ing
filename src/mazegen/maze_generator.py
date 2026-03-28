from mazegen.cell import Cell
from mazegen.maze_builder import MazeBuilder
from mazegen.solver import Solver
from mazegen.exporter import Exporter
import random


class MazeGenerator:
    """
    Handle the maze lifecycle from grid initialization
    to generation and solving.
    """
    def __init__(
            self,
            width: int,
            height: int,
            perfect: bool,
            seed: int | None = None,
            ) -> None:
        """Initialize the maze generator with dimensions and randomness settings."""
        if (not isinstance(width, int) or
            not isinstance(height, int) or
                width < 2 or height < 2):
            raise ValueError("Maze dimensions must be at least 2x2")

        if not isinstance(perfect, bool):
            raise TypeError("The 'perfect' parameter must be a boolean.")

        if seed is not None:
            if not isinstance(seed, int) or seed < 0:
                raise ValueError("The 'seed' parameter must be a positive integer.")

        self.width = width
        self.height = height
        self.perfect = perfect
        self.rng = random.Random(seed)  # générateur de hasard isolé et sécurisé !

        # L'Hybride : Une matrice 2D remplie d'objets (Nœuds)
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]
        # attribut qui passera à `true` quand le maze aura été généré. Permettra de vérifier que
        # le maze existe avant d'appeler le solver pour éviter le crash.
        self._has_been_generated: bool = False
        # attribut qui passera à `true` quand une solution aur été toruvée. Permettra de vérifier que
        # la solution existe avant d'essayer de l'exporter.
        self._has_been_solved: bool = False

    def replace_seed(self, new_seed: int | float | str | None = None) -> None:
        """Change the seed of the MazeGenerator. Useful if you want to
        generate a maze based on a new seed"""

        if new_seed is None:
            self.rng = random.Random(None)
            return

        if not isinstance(new_seed, (int, float, str)):
            raise TypeError("'seed' parameter must be an integer, a float,"
                            " a string or None.")

        self.rng = random.Random(new_seed)
        # si le paramètre est None, on se base sur l'heure pour le random

    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Return the cell at coordinates (x, y)
        or None if out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def _apply_42_pattern(self) -> None:
        """
        Marks a '42' pattern in the grid if dimensions allow (min 9x7).
        """
        if self.width < 9 or self.height < 7:
            return
        pattern_w, pattern_h = 7, 5
        centered_x = (self.width - pattern_w) // 2
        centered_y = (self.height - pattern_h) // 2

        four = [
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 2), (2, 3), (2, 4)
             ]

        two = [
            (4, 0), (5, 0), (6, 0),
            (6, 1), (6, 2),
            (5, 2), (4, 2),
            (4, 3), (4, 4),
            (5, 4), (6, 4)
            ]

        for x, y in four + two:
            target_x = centered_x + x
            target_y = centered_y + y
            cell = self.grid[target_y][target_x]
            cell.is_part_of_42 = True
            cell.visited = True

    def reset_grid(self) -> None:
        """Reset the grid by creating new Cell objects for every coordinate."""
        self.grid = [[Cell(x, y) for x in range(self.width)]
                     for y in range(self.height)]
        self._has_been_generated = False
        self._has_been_solved = False

    def generate_maze(self, imperfection_rate: float | None = None) -> None:
        """
        Coordinate the maze construction process.

        Apply the '42' pattern and handle both perfect and
        imperfect maze generation based on settings.
        """
        if imperfection_rate is not None:
            if not isinstance(imperfection_rate, float) or \
                        imperfection_rate <= 0.0 or imperfection_rate >= 1.0:
                raise ValueError("The 'imperfection_rate' parameter must be"
                                 " a float.\nValue must be : "
                                 "0.0 > imperfection_rate < 1.0.")

        # 1. On applique le motif 42 (qui mettra certaines cases en visited=True et is_part_of_42=True)
        self._apply_42_pattern()

        # 2. On instancie notre algorithme (la stratégie)
        builder = MazeBuilder(
            self.grid, self.width, self.height, self.rng
            )

        # 3. L'algorithme fait son job directement sur notre matrice en mémoire !
        builder.generate()

        # (Optionnel) Si PERFECT=False, c'est ici qu'on viendrait
        # casser quelques murs supplémentaires pour créer des boucles.
        if not self.perfect:
            # On définit ici combien de murs on veut casser (ex: 10 de la grille)
            rate = imperfection_rate if imperfection_rate is not None else 0.1
            nb_to_break = int((self.width * self.height) * rate)
            builder.degrade_perfection(nb_to_break)

        self._has_been_generated = True

    def solve_path(
            self, entry_coord: tuple[int, int], exit_coord: tuple[int, int]
            ) -> None:
        """
        Solve the maze using BFS algorithm.

        Args:
            entry_coord (tuple): (x, y) coordinates for the start.
            exit_coord (tuple): (x, y) coordinates for the end.

        Raises:
            ValueError: If coordinates are out of grid bounds.
            RuntimeError: If the maze has not been generated yet.
        """
        # vérifie que entry et exit sont bien dans les limites du maze
        if not self.get_cell(*entry_coord) or not self.get_cell(*exit_coord):
            raise ValueError("Invalid entry or exit.")

        # vérifie que le maze a été instancié avant qu on appelle le solver:
        if not getattr(self, "_has_been_generated", False):
            raise RuntimeError("You must generate maze before calling solver.")

        solver = Solver(
            self.grid, self.width, self.height, entry_coord, exit_coord
            )
        if solver.solve():
            self._has_been_solved = True

    def get_solution_in_str(
            self,
            entry_coord: tuple[int, int],
            exit_coord: tuple[int, int]) -> str:

        exporter = Exporter(
            self.grid,
            self.width,
            self.height,
            entry_coord,
            exit_coord,
            )

        return exporter.get_solution_directions()

    def export_maze_to_file(
            self, entry_coord: tuple[int, int],
            exit_coord: tuple[int, int],
            filename: str
            ) -> None:
        """
        Export the maze structure, coordinates, and solution to a file.

        The exported file contains the hexadecimal representation of the grid,
        followed by the entry/exit coordinates and the cardinal directions
        of the solution path.
        """

        exporter = Exporter(
            self.grid,
            self.width,
            self.height,
            entry_coord,
            exit_coord,
            )

        exporter.write_output_file(self._has_been_generated, filename)
