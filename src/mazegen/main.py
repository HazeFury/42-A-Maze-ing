# ce fichier est le point d'entrée de l'application, 
# il contient la logique pour générer un labyrinthe,
# et l'afficher à l'utilisateur.
# c'est important de le mettre ici car ca permettra 
# à un utilisteur qui aura installé le module de pouvoir 
# lancer l'application facilement. (`python -m mazegen` dans le terminal)
# sinon le module sera bien packagé mais pas utilisable facilement.
# L'utilisateur devrait alors écrire un script de lancement 
# lui même, ce qui n'est pas idéal pour l'expérience utilisateur.
# Le point d'entree est precise dans le.toml : [project.scripts]
#(mazegen = "mazegen.main:main")

#NB : le a_maze_ing.py se contente alors d'appeler cette fonction main.

#code pour tester le fonctionnement:

from mazegen.generator import MazeGenerator


def main():
    print("Succès : Le package mazegen est bien installé !")
    gen = MazeGenerator()
    gen.generate()


if __name__ == "__main__":
    main()
