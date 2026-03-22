import sys
from app.parser import parsing_config_file


def main():

    if len(sys.argv) > 2:
        print("Too many arguments ! This project takes only one argument to work")
        print("Try the following command : 'python3 a_maze_ing.py config.txt'")
        sys.exit(1)

    data = parsing_config_file()
    print(data)


if __name__ == "__main__":
    main()
