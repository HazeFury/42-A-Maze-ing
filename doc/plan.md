# A-Maze-ing : Générateur et Résolveur de Labyrinthes

## 1. Description du Projet

Ce projet consiste à créer un générateur de labyrinthes procédural en Python. L'objectif principal est de concevoir un outil modulaire, divisé en deux parties distinctes : une librairie réutilisable (`mazegen`) et un programme principal (`a_maze_ing.py`) gérant l'interface utilisateur et les entrées/sorties

## 2. Architecture et Séparation des Responsabilités

Pour garantir la réutilisabilité du code, notamment pour une future installation via `pip`, l'architecture repose sur une séparation stricte :

- **Le Moteur (`mazegen`) :** Une librairie "boîte noire". Elle ne gère aucune lecture de fichier, aucun affichage et aucun print. Elle prend des paramètres en entrée, exécute l'algorithme de génération en mémoire, et expose les données de la structure générée.
- **La Carrosserie (`a_maze_ing.py`) :** Le script principal. Il gère l'interaction avec l'utilisateur, la sécurité, le parsing, le système de fichiers et l'affichage visuel.

## 3. Flux d'Exécution (Les Grandes Étapes)

### Étape 1 : Le Parsing et la Sécurité

Le programme lit le fichier de configuration passé en argument. Il s'assure que toutes les données sont valides et gère les erreurs proprement pour éviter tout crash.

Exemple de configuration lue :

- WIDTH=20
- HEIGHT=15
- ENTRY=0,0
- EXIT=19,14
- OUTPUT_FILE=maze.txt
- PERFECT=True

### Étape 2 : La Génération en Mémoire

Le programme principal instancie la classe génératrice issue de notre module `mazegen`, en lui passant les paramètres validés. Le générateur crée la structure de données en mémoire, applique l'algorithme de génération en utilisant une seed pour la reproductibilité. Il intègre le motif "42" au centre , s'assure de la connectivité et, si demandé, garantit un chemin unique parfait. Tout se passe en mémoire (RAM).

### Étape 3 : L'Exportation (Le Livrable)

Une fois le labyrinthe généré, le programme principal interroge le générateur pour récupérer l'état des murs. Il traduit ces données en format hexadécimal, où chaque bit représente un mur (0 pour Nord, 1 pour Est, 2 pour Sud, 3 pour Ouest). Il génère ensuite le fichier de sortie contenant ces données, les coordonnées, et le chemin le plus court.

### Étape 4 : La Visualisation et les Interactions

Enfin, le programme affiche le labyrinthe à l'utilisateur via le terminal ou une interface graphique MLX. Il entre dans une boucle d'événements permettant à l'utilisateur de regénérer un nouveau labyrinthe, d'afficher ou masquer la solution, et de changer les couleurs des murs.
