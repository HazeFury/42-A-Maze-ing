import random
from mazegen.Cell import Cell


class IterativeBacktracker:
    def __init__(
            self, grid: list[list[Cell]], width: int, height: int,
            rng: random.Random
            ):
        self.grid = grid
        self.width = width
        self.height = height
        self.rng = rng
        # L'algorithme reçoit uniquement les données pures.
        # Aucun import circulaire ici !

    # =========================================================================
    def get_cell(self, x: int, y: int) -> Cell | None:
        """Petite méthode utilitaire locale pour éviter de sortir
        de la grille."""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    # =========================================================================
    def generate(self) -> None:
        """
        C'est ici que tu vas écrire ta vraie boucle algorithmique !
        """
        # Exemple de point de départ :
        # current_cell = self.get_cell(0, 0)
        # current_cell.visited = True
        # ... à toi de jouer avec pour former le maze
        pass
