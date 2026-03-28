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
            ):
        """Initialize the maze generator with dimensions and randomness settings."""
        self.width = width
        self.height = height
        self.perfect = perfect
        self.rng = random.Random(seed)  # générateur de hasard isolé et sécurisé !

        # L'Hybride : Une matrice 2D remplie d'objets (Nœuds)
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]

    # =========================================================================
    def replace_seed(self, new_seed: int | None = None) -> None:
        """Change the seed of the MazeGenerator. Useful if you want to
        generate a maze based on a new seed"""
        print(f"avant : {self.rng}")
        self.rng = random.Random(new_seed)
        print(f"apres : {self.rng}")
        # si le paramètre est None, on se base sur l'heure pour le random

    # =========================================================================
    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Return the cell at coordinates (x, y)
        or None if out of bounds.
        """
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    # =========================================================================
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

    # =========================================================================
    def reset_grid(self) -> None:
        """Reset the grid by creating new Cell objects for every coordinate."""
        self.grid = [[Cell(x, y) for x in range(self.width)]
                     for y in range(self.height)]

    # =========================================================================
    def generate_maze(self, imperfection_rate: float | None = None) -> None:
        """
        Coordinate the maze construction process.

        Apply the '42' pattern and handle both perfect and
        imperfect maze generation based on settings.
        """
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

    def solve_path(
            self, entry_coord: tuple[int, int], exit_coord: tuple[int, int]
            ) -> None:
        # (Code théorique)
        solver = Solver(
            self.grid, self.width, self.height, entry_coord, exit_coord
            )
        solver.solve()
        # Parfait, on a une solution ! On peut marquer les cellules du chemin.

    def export_maze_to_file(
            self, entry_coord: tuple[int, int],
            exit_coord: tuple[int, int],
            filename: str
            ) -> None:

        exporter = Exporter(
            self.grid,
            self.width,
            self.height,
            entry_coord,
            exit_coord,
            filename
            )

        exporter.write_output_file()
