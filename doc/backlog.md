## Backlog du Projet : A-Maze-ing

### Epic 1 : Infrastructure & Packaging

Cette Epic regroupe tout ce qui concerne la structure du projet, les outils de build et les normes de code exigées par le sujet.

- **US 1.1 - Initialisation du repository :** En tant que développeur, je veux créer l'arborescence du projet avec le dossier src/, le Makefile et le pyproject.toml pour avoir une base saine.
- **US 1.2 - Configuration du Linter et Typage :** En tant que développeur, je veux configurer les commandes Makefile pour flake8 et mypy (en mode strict) afin de garantir que mon code respecte la norme dès le premier jour.
- **US 1.3 - Création du module distribuable :** En tant qu'utilisateur, je veux pouvoir installer le moteur de génération via pip (fichiers .whl et .tar.gz) pour pouvoir le réutiliser dans un futur projet.

### Epic 2 : Parsing & Sécurité

Cette Epic concerne la lecture du fichier `config.txt` par le script principal `a_maze_ing.py`. L'objectif est la robustesse absolue.

- **US 2.1 - Lecture des paires Clé/Valeur :** En tant qu'utilisateur, je veux que le programme lise mon fichier de configuration, en ignorant les lignes vides et les commentaires (lignes commençant par #).
- **US 2.2 - Validation des types :** En tant que développeur, je veux m'assurer que les valeurs récupérées (WIDTH, HEIGHT, ENTRY, EXIT) sont bien des entiers valides et que les coordonnées sont dans les limites du labyrinthe.
- **US 2.3 - Gestion des erreurs (Crash-test) :** En tant qu'utilisateur, je veux que le programme affiche un message d'erreur clair et s'arrête proprement (sans traceback Python) si le fichier de configuration est introuvable ou mal formaté.

### Epic 3 : Le Moteur de Génération (Le Cerveau - Module `mazegen`)

C'est le cœur de la librairie mathématique. Elle ne gère aucun affichage ni fichier, uniquement de la donnée en mémoire.

- **US 3.1 - Initialisation de la structure :** En tant que développeur, je veux modéliser le labyrinthe en mémoire (Matrice 2D ou Graphe) avec toutes les cellules initialement fermées (4 murs).
- **US 3.2 - Algorithme de génération :** En tant que développeur, je veux implémenter un algorithme (ex: Recursive Backtracker) pour creuser des chemins aléatoires en fonction d'une "seed" donnée.
- **US 3.3 - Connectivité et couloirs :** En tant que développeur, je veux garantir qu'aucune cellule n'est inaccessible et que les couloirs ne dépassent pas 2 cellules de largeur.
- **US 3.4 - Le motif "42" :** En tant qu'utilisateur, je veux qu'un motif "42" fait de cellules totalement fermées soit généré au centre du labyrinthe (si la taille le permet).
- **US 3.5 - Mode Perfect :** En tant qu'utilisateur, si l'option PERFECT est activée, je veux que le labyrinthe ne contienne qu'un seul et unique chemin possible entre l'entrée et la sortie (pas de boucles).
- **US 3.6 - Résolution (Pathfinding) :** En tant que développeur, je veux implémenter un algorithme (ex: BFS ou A\*) pour trouver et stocker le chemin le plus court entre l'entrée et la sortie.

### Epic 4 : Exportation & Livrable (Le Traducteur)

Cette Epic gère la conversion des données en mémoire vers le fichier de sortie lisible par la Moulinette.

- **US 4.1 - Conversion Hexadécimale :** En tant que développeur, je veux traduire l'état des murs de chaque cellule en une valeur hexadécimale (0 à F) en utilisant les opérations binaires (Nord=1, Est=2, Sud=4, Ouest=8).
- **US 4.2 - Écriture du fichier output :** En tant qu'utilisateur, je veux que le programme génère le fichier texte de sortie contenant la grille hexadécimale, une ligne vide, puis les coordonnées et la solution (suite de lettres N, E, S, W).

### Epic 5 : Interface Utilisateur (Le Visuel)

Cette Epic concerne l'affichage du labyrinthe et les interactions de l'utilisateur avec celui-ci (Terminal ASCII ou MiniLibX).

- **US 5.1 - Rendu visuel de base :** En tant qu'utilisateur, je veux voir le labyrinthe s'afficher à l'écran, avec une distinction claire entre les murs, les couloirs, l'entrée, la sortie et le motif "42".
- **US 5.2 - Interaction : Régénération :** En tant qu'utilisateur, je veux pouvoir appuyer sur une touche pour générer et afficher instantanément un tout nouveau labyrinthe.
- **US 5.3 - Interaction : Affichage de la solution :** En tant qu'utilisateur, je veux pouvoir masquer ou afficher le chemin le plus court reliant l'entrée à la sortie.
- **US 5.4 - Interaction : Personnalisation :** En tant qu'utilisateur, je veux pouvoir changer les couleurs des murs en appuyant sur une touche dédiée.
