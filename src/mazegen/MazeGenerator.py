from mazegen.Cell import Cell
from mazegen.generator import IterativeBacktracker
from mazegen.Solver import Solver
import random


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int | None = None):
        self.width = width
        self.height = height
        self.rng = random.Random(seed)  # générateur de hasard isolé et sécurisé !

        # L'Hybride : Une matrice 2D remplie d'objets (Nœuds)
        self.grid = [[Cell(x, y) for x in range(width)] for y in range(height)]

    # =========================================================================
    def replace_seed(self, new_seed: int | None = None) -> None:
        """Change the seed of the MazeGenerator. Useful if you want to
        generate a maze based on a nez seed"""
        print(f"avant : {self.rng}")
        self.rng = random.Random(new_seed)
        print(f"apres : {self.rng}")
        # si le paramètre est None, on se base sur l'heure pour le random

    # =========================================================================
    def get_cell(self, x: int, y: int) -> Cell | None:
        """
        Return the cell at coordinates (x, y) or None if out of bounds.
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
        self.grid = [[Cell(x, y) for x in range(self.width)]
                     for y in range(self.height)]

    # =========================================================================
    def generate_maze(self) -> None:
        """
        Prépare le terrain et lance la stratégie de génération choisie.
        """
        # 1. On applique le motif 42 (qui mettra certaines cases en visited=True et is_part_of_42=True)
        self._apply_42_pattern()

        # 2. On instancie notre algorithme (la stratégie)
        algo = IterativeBacktracker(
            self.grid, self.width, self.height, self.rng
            )

        # 3. L'algorithme fait son job directement sur notre matrice en mémoire !
        algo.generate()

        # (Optionnel) Si PERFECT=False, c'est ici qu'on viendrait
        # casser quelques murs supplémentaires pour créer des boucles.

    def solve_path(
            self, entry_coord: tuple[int, int], exit_coord: tuple[int, int]
            ) -> None:
        # (Code théorique)
        solver = Solver(
            self.grid, self.width, self.height, entry_coord, exit_coord
            )
        solver.solve()
        # Parfait, on a une solution ! On peut marquer les cellules du chemin.
