from mazegen.Cell import Cell
from typing import Tuple

class Solver:
    def __init__(
        self,
        grid: list[list[Cell]],
        width: int,
        height: int,
        entry_coord: tuple[int, int],
        exit_coord: tuple[int, int]
    ):
        """
        Le Solver reçoit la grille déjà générée, ses dimensions,
        et les points d'entrée et de sortie.
        """
        self.grid = grid
        self.width = width
        self.height = height
        self.entry_x, self.entry_y = entry_coord
        self.exit_x, self.exit_y = exit_coord

        # C'est ici qu'on stockera le résultat une fois le chemin trouvé
        self.path: list[Cell] = []

    # =========================================================================
    def _get_cell(self, x: int, y: int) -> Cell | None:
        """Méthode utilitaire pour sécuriser l'accès à la grille."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    # =========================================================================
    def solve(self) -> bool:
        """
        Le cœur du réacteur. Lance l'algorithme (ex: BFS).
        Retourne True si on a trouvé la sortie, False sinon.
        """
        pass

    # =========================================================================
    def _get_accessible_neighbors(self, cell: Cell) -> list[Cell]:
        """
        Crucial ! Contrairement au générateur qui regarde le
        cases non visitées, le Solver doit regarder les cases adjacentes
        OÙ IL N'Y A PAS DE MUR.
        """
        accessible_neighbors: list[Cell] = []

        adjacent_cells: Tuple[Tuple[int, int, str], ...]
        adjacent_cells = ((0, -1, 'N'), (1, 0, 'E'), (0, 1, 'S'), (-1, 0, 'W'))

        for adjacent_cell in adjacent_cells:
            dx, dy, direction = adjacent_cell
            if not cell.walls[direction]:
                neighbor = self.get_cell(dx + cell.x, dy + cell.y)
                if neighbor:
                    accessible_neighbors.append(neighbor)

    # =========================================================================
    def _reconstruct_path(
            self, came_from: dict[Cell, Cell], current_cell: Cell
            ) -> None:
        """
        Une fois la sortie atteinte, l'algorithme remonte la piste de case
        en case grâce au dictionnaire 'came_from' pour remplir self.path
        dans le bon ordre.
        """
        pass

    # =========================================================================
    def get_solution_directions(self) -> str:
        """
        Traduit la liste self.path en une chaîne de lettres (N, S, E, W).
        Indispensable pour formater la solution dans le output.txt !
        """
        pass
