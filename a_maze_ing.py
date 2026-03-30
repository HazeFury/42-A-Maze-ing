import sys
from app.parser import parsing_config_file
from mazegen.maze_generator import MazeGenerator
from app.display import MazeDisplay


def red_text(text: str) -> str:
    return f"\033[31m{text}\033[0m"


def main() -> None:

    if len(sys.argv) > 2:
        print(f"[{red_text('ERROR')}] Too many arguments!"
              " This project takes only 1 argument to work")
        print("Try the following commands :"
              "\n'python3 a_maze_ing.py config.txt'")
        print("or simply just :\n'make run'")
        sys.exit(1)

    try:
        data = parsing_config_file(sys.argv[1])
        # TODO: Est-ce que Steph est ok avec cette approche ?
        if data.width < 9 or data.height < 7:
            print("[WARNING]: Maze size is too small to draw the '42' "
                  "pattern.\n The maze will be generated without it.")
    except Exception as e:
        print(f"[{red_text('ERROR')}] An error occured during parsing.")
        print(f"More details below :\n\n=> {e}")
        sys.exit(1)

    try:
        maze = MazeGenerator(
            width=data.width,
            height=data.height,
            perfect=data.perfect,
            seed=data.seed
            )

        maze.generate_maze(imperfection_rate=data.imperfection_rate)
        maze.solve_path(
            entry_coord=data.entry_coord,
            exit_coord=data.exit_coord
        )
        maze.export_maze_to_file(
            entry_coord=data.entry_coord,
            exit_coord=data.exit_coord,
            filename=data.output_file
            )
    except Exception as e:
        print(f"[{red_text('ERROR')}] An error occured in the program.")
        print(f"More details below :\n\n=> {e}")
    else:
        try:
            display = MazeDisplay(
                maze,
                entry_coord=data.entry_coord,
                exit_coord=data.exit_coord
                )
            display.start()
        except Exception as e:
            print(f"[{red_text('ERROR')}] An error occured when trying"
                  "to display")
            print(f"More details below :\n\n=> {e}")


if __name__ == "__main__":
    main()
