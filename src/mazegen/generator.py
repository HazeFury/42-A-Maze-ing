# code de test

class MazeGenerator:
    def __init__(self, width: int = 10, height: int = 10, seed: int = None):
        self.width = width
        self.height = height

    def generate(self):
        print(f"Génération d'un labyrinthe {self.width}x{self.height}...")
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        return self.grid
