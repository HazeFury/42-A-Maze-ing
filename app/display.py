import curses
from mazegen.maze_generator import MazeGenerator


class MazeDisplay:
    def __init__(
            self, maze: MazeGenerator, entry_coord: tuple[int, int],
            exit_coord: tuple[int, int]) -> None:

        self.maze = maze
        self.WALL_CHAR = "██"
        self.PATH_CHAR = "  "
        self.P42_CHAR = "██"
        self.SOL_CHAR = "██"
        self.entry_coord = entry_coord
        self.exit_coord = exit_coord
        self.wall_colors = [6, 7, 8, 9, 10, 11]
        self.current_wall_color_idx = 0

    def _init_colors(self) -> None:
        """
        Initialize pair color for curses.

        Structure is => curses.init_pair(ID, Text_color, Background)
        """
        curses.start_color()

        # ========  ITEMS  =============
        # Red background for error message
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)
        # Yellow inside "42" pattern
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        # Cyan for solution path
        curses.init_pair(3, curses.COLOR_CYAN, curses.COLOR_BLACK)
        # Red for entry point
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        # Green for exit point
        curses.init_pair(5, curses.COLOR_GREEN, curses.COLOR_BLACK)

        # ========  WALLS  ==============
        # White (basic color)
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)
        # Violet (magenta)
        curses.init_pair(7, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        # Blue
        curses.init_pair(8, curses.COLOR_BLUE, curses.COLOR_BLACK)
        # Orange
        curses.init_pair(9, 166, curses.COLOR_BLACK)
        # Rose
        curses.init_pair(10, 163, curses.COLOR_BLACK)
        # Grey
        curses.init_pair(11, 244, curses.COLOR_BLACK)

    def _draw_maze(self, stdscr: curses.window, is_showing_path: bool) -> None:
        """Renders the maze grid onto the extended ASCII screen."""

        curr_maze_color_id = self.wall_colors[self.current_wall_color_idx]
        entry_x, entry_y = self.entry_coord
        exit_x, exit_y = self.exit_coord

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)

                if not cell:
                    continue

                screen_y = (y * 2) + 1
                screen_x = (x * 2) * 2 + 2

                try:
                    # --- CHOOSE CENTER COLOR & CHARACTER ---
                    color = curses.color_pair(6)
                    char_to_draw = self.PATH_CHAR

                    if cell.is_part_of_42:
                        color = curses.color_pair(2)
                        char_to_draw = self.P42_CHAR

                    elif cell.x == entry_x and cell.y == entry_y:
                        color = curses.color_pair(4)
                        char_to_draw = self.SOL_CHAR

                    elif cell.x == exit_x and cell.y == exit_y:
                        color = curses.color_pair(5)
                        char_to_draw = self.SOL_CHAR

                    elif cell.is_solution and is_showing_path:
                        color = curses.color_pair(3)
                        char_to_draw = self.SOL_CHAR

                    # function to draw a character on screen :
                    # stdscr.addstr(y, x, texte, options)
                    stdscr.addstr(screen_y, screen_x, char_to_draw, color)

                    # --- DRAW PATH JUNCTIONS ---
                    if cell.is_solution and is_showing_path:
                        solution_color = curses.color_pair(3)

                        if cell.path_connections["N"]:
                            stdscr.addstr(screen_y - 1, screen_x,
                                          self.SOL_CHAR, solution_color)
                        if cell.path_connections["S"]:
                            stdscr.addstr(screen_y + 1, screen_x,
                                          self.SOL_CHAR, solution_color)
                        if cell.path_connections["W"]:
                            stdscr.addstr(screen_y, screen_x - 2,
                                          self.SOL_CHAR, solution_color)
                        if cell.path_connections["E"]:
                            stdscr.addstr(screen_y, screen_x + 2,
                                          self.SOL_CHAR, solution_color)

                    wall_color = curses.color_pair(curr_maze_color_id)

                    # --- DRAW WALLS ---
                    if cell.walls["N"]:
                        stdscr.addstr(screen_y - 1, screen_x, self.WALL_CHAR,
                                      wall_color)

                    if cell.walls["S"]:
                        stdscr.addstr(screen_y + 1, screen_x, self.WALL_CHAR,
                                      wall_color)

                    if cell.walls["W"]:
                        stdscr.addstr(screen_y, screen_x - 2, self.WALL_CHAR,
                                      wall_color)

                    if cell.walls["E"]:
                        stdscr.addstr(screen_y, screen_x + 2, self.WALL_CHAR,
                                      wall_color)

                    # --- DRAW WALLS CORNERS ---
                    if cell.walls["N"] or cell.walls["W"]:
                        stdscr.addstr(
                            screen_y - 1, screen_x - 2, self.WALL_CHAR,
                            wall_color)

                    if cell.walls["N"] or cell.walls["E"]:
                        stdscr.addstr(
                            screen_y - 1, screen_x + 2, self.WALL_CHAR,
                            wall_color)

                    if cell.walls["S"] or cell.walls["W"]:
                        stdscr.addstr(
                            screen_y + 1, screen_x - 2, self.WALL_CHAR,
                            wall_color)

                    if cell.walls["S"] or cell.walls["E"]:
                        stdscr.addstr(
                            screen_y + 1, screen_x + 2, self.WALL_CHAR,
                            wall_color)

                except curses.error:
                    pass

    def _draw_loop(self, stdscr: curses.window) -> None:
        """
        Executes the main event loop for the interactive curses interface.
        """
        curses.curs_set(0)
        self._init_colors()
        is_showing_path: bool = True
        margin: int = 12
        no_gen_msg: str = "WARNING: Maze has not been generated yet"
        no_solv_base: str = "WARNING: Maze has any solution"
        cause_42_msg: str = "(entry or exit point is in the '42' pattern)"
        too_small_for_42: str = "WARNING: Maze too small for '42' pattern"

        required_y = (self.maze.height * 2) + margin
        required_x = (self.maze.width * 4) + margin

        #  === START DISPLAY ===
        while True:
            stdscr.clear()
            # get the size of the current screen
            max_y, max_x = stdscr.getmaxyx()

            if max_y < required_y or max_x < required_x:
                warning: list[str] = [
                    " ⚠️  ",
                    "   Terminal too small !   ",
                    "    Enlarge the window.   ",
                    " Press 'q' or '4' to quit "
                    ]

                # display warning messages on the center of the screen
                # if size is too small
                try:
                    start_y = (max_y - len(warning)) // 2
                    for i, line in enumerate(warning):
                        stdscr.addstr(start_y + i, (max_x - len(line)) // 2,
                                      line, curses.A_REVERSE | curses.A_BOLD)
                except curses.error:
                    raise Exception("Terminal (very) too small! Please"
                                    " enlarge the window to launch display")

            else:
                # else, we draw the maze
                self._draw_maze(stdscr, is_showing_path)

                if not self.maze._has_been_generated:
                    stdscr.addstr(max_y - 9, 2, no_gen_msg,
                                  curses.color_pair(1))

                if not self.maze._has_been_solved:
                    no_solv_msg: str = f"{no_solv_base} {cause_42_msg}" \
                        if self.maze._has_been_generated else no_solv_base
                    stdscr.addstr(max_y - 8, 2, no_solv_msg,
                                  curses.color_pair(1))

                if self.maze.width < 9 or self.maze.height < 7:
                    stdscr.addstr(max_y - 10, 2, too_small_for_42,
                                  curses.color_pair(1))

                instructions: list[str] = [
                    "============  A-Maze-ing  ============",
                    " 1. Re-generate a new maze            ",
                    " 2. Show/Hide path from entry to exit ",
                    " 3. Rotate maze colors                ",
                    " 4. Quit                              "
                    ]
                try:
                    for i, line in enumerate(instructions):
                        stdscr.addstr(max_y - ((len(instructions) + 1) - i), 2,
                                      line, curses.A_REVERSE)
                except curses.error:
                    pass

            stdscr.refresh()

            # start listening key's event (screen resize is also an event)
            key = stdscr.getch()

            if key == ord('4') or key == ord('q'):
                break
            if key == ord('2'):
                is_showing_path = not is_showing_path
            if key == ord('3'):
                self.current_wall_color_idx = (
                    (self.current_wall_color_idx + 1) % len(self.wall_colors)
                )

            elif key == ord('1'):
                self.maze.replace_seed()
                self.maze.reset_grid()
                self.maze.generate_maze()
                self.maze.solve_path(self.entry_coord, self.exit_coord)

    def start(self) -> None:
        """Secure entry point to launch the interactive display."""
        curses.wrapper(self._draw_loop)
