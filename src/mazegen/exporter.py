from mazegen.cell import Cell
from mazegen.solver import Solver


class Exporter:
    """Handles the exporting of the maze and its solution to a text file.

    This class converts the maze grid into its hexadecimal representation
    and retrieves the solution path to generate a formatted output file
    according to the project's requirements.
    """
    def __init__(
            self,
            grid: list[list[Cell]],
            width: int,
            height: int,
            entry_coord: tuple[int, int],
            exit_coord: tuple[int, int],
            filename: str
            ) -> None:
        self.grid = grid
        self.width = width
        self.height = height
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord
        self.filename = filename

    def _get_maze_to_hex(self) -> list[str]:
        """Translates the maze grid into a list of hexadecimal strings.

        Iterates through the 2D grid and asks each Cell for its hexadecimal
        value representing its walls.

        Returns:
            list[str]: A list where each string represents a row of the maze
                in hexadecimal format.
        """

        maze_hex: list[str] = []

        for y in range(self.height):
            temp_str: str = ""
            for x in range(self.width):

                cell: Cell = self.grid[y][x]
                temp_str = temp_str + cell.get_hex_value()
            maze_hex.append(temp_str)

        return maze_hex

    def _get_solution_directions(self) -> str:
        """
        Convert the path of Cells into a string of cardinal directions.

        Example: "N S E W". Return an empty string if no path exists.
        """

        solver = Solver(
            self.grid, self.width, self.height, self.entry_coord, self.exit_coord
            )
        solver.solve()

        if not solver.path or len(solver.path) < 2:
            return ""

        directions: list[str] = []

        for i in range(len(solver.path) - 1):
            current_x = solver.path[i].x
            current_y = solver.path[i].y
            next_x = solver.path[i + 1].x
            next_y = solver.path[i + 1].y

            if next_x > current_x:
                directions.append('E')
            elif next_x < current_x:
                directions.append('W')
            elif next_y > current_y:
                directions.append('S')
            elif next_y < current_y:
                directions.append('N')

        return "".join(directions)

    def write_output_file(self) -> None:
        """Writes the maze layout and solution to the specified file.

        The file format includes:
        1. The maze grid in hexadecimal format.
        2. A blank line.
        3. The entry coordinates (x,y).
        4. The exit coordinates (x,y).
        5. The solution path as a string of cardinal directions.

        Raises:
            Exception: If an error occurs during file opening or writing.
        """

        maze_hex_list: list[str] = self._get_maze_to_hex()
        solution_directions: str = self._get_solution_directions()
        entry_x, entry_y = self.entry_coord
        exit_x, exit_y = self.exit_coord

        try:
            with open(self.filename, "w") as output:
                for line in maze_hex_list:
                    output.write(f"{line}\n")

                output.write("\n")
                output.write(f"{entry_x},{entry_y}\n")
                output.write(f"{exit_x},{exit_y}\n")
                if not solution_directions == "":
                    output.write(f"{solution_directions}\n")
        except Exception as e:
            raise Exception(f"ERROR : {e}")
