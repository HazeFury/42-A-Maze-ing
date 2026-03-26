import sys
from app.parser import parsing_config_file
from mazegen.maze_generator import MazeGenerator
from app.display import MazeDisplay


def main():

    if len(sys.argv) > 2:
        print("Too many arguments! This project takes only 1 argument to work")
        print("Try the following command : 'python3 a_maze_ing.py config.txt'")
        sys.exit(1)

    try:
        data = parsing_config_file(sys.argv[1])
        if data.width < 9 or data.height < 7:
            print("WARNING: Maze size is too small to draw the '42' pattern.")
    except Exception as e:
        print(f"[ERROR] Something went wrong : {e}")
        sys.exit(1)

    maze = MazeGenerator(
        width=data.width,
        height=data.height,
        perfect=data.perfect,
        seed=data.seed
        )

    maze.generate_maze()
    maze.solve_path(
        entry_coord=data.entry_coord,
        exit_coord=data.exit_coord
    )

    display = MazeDisplay(
        maze,
        entry_coord=data.entry_coord,
        exit_coord=data.exit_coord
        )
    display.start()


if __name__ == "__main__":
    main()
