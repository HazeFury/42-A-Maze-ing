class Cell:
    """Represents a single unit in the maze grid.

    Tracks the cell's coordinates, wall states, and pathfinding metadata.
    """
    def __init__(self, x: int, y: int) -> None:
        """Initializes a new Cell with all walls closed.

        Args:
            x (int): The x-coordinate (column) of the cell.
            y (int): The y-coordinate (row) of the cell.
        """
        self.x = x
        self.y = y
        self.visited = False
        self.is_part_of_42 = False
        self.is_solution = False
        self.walls = {"N": True, "E": True, "S": True, "W": True}
        self.path_connections = {
            "N": False, "E": False, "S": False, "W": False
            }

    def break_wall(self, direction: str) -> None:
        """Removes the wall in the specified direction.

        Args:
            direction (str): The cardinal direction ('N', 'S', 'E', or 'W').
        """
        self.walls[direction] = False

    def repair_wall(self, direction: str) -> None:
        """Restores the wall in the specified direction.

        Args:
            direction (str): The cardinal direction ('N', 'S', 'E', or 'W').
        """
        self.walls[direction] = True

    def get_hex_value(self) -> str:
        """Computes the hexadecimal value of the cell's walls.

        Calculates the value based on bitwise flags: North=1, East=2,
        South=4, West=8. A closed wall adds to the total value.

        Returns:
            str: A single uppercase hexadecimal character (e.g., 'F').
        """
        val = 0
        if self.walls["N"]:
            val += 1
        if self.walls["E"]:
            val += 2
        if self.walls["S"]:
            val += 4
        if self.walls["W"]:
            val += 8

        return hex(val)[2:].upper()
