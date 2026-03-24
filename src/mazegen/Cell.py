class Cell:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.visited = False
        self.is_part_of_42 = False  # Passe a True dans la fonction qui ajoute le 42 pattern dans le maze -> servira à gérer le la couleur lors de l'affichage
        self.is_solution = False  # Passe à true dans le solver du chemin et permettra de gérer l'affichage plus facilement à après
        self.walls = {"N": True, "E": True, "S": True, "W": True}
        # Le Graphe : Les murs représentent l'absence d'arête (pas de chemin).
        # Au début, la cellule est un bloc solide, entourée de 4 murs.

    def break_wall(self, direction: str):
        """Casser un mur revient à créer une arête dans notre graphe."""
        self.walls[direction] = False

    def get_hex_value(self) -> str:
        """
        Traduit l'état de la cellule pour le fichier de sortie.
        """
        # Le sujet impose : Bit 0=North, 1=East, 2=South, 3=West[cite: 148].
        # Un mur fermé met le bit à 1[cite: 151].
        val = 0
        if self.walls["N"]:
            val += 1  # 2^0
        if self.walls["E"]:
            val += 2  # 2^1
        if self.walls["S"]:
            val += 4  # 2^2
        if self.walls["W"]:
            val += 8  # 2^3

        # Convertit l'entier en hexadécimal (ex: 15 -> 'F')
        return hex(val)[2:].upper()
