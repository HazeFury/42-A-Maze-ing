# code de test

from mazegen.generator import MazeGenerator


def main():
    print("Succès : Le package mazegen est bien installé !")
    gen = MazeGenerator()
    gen.generate()


if __name__ == "__main__":
    main()