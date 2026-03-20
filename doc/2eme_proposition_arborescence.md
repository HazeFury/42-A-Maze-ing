# Deuxième Proposition d'Arborescence

## Sondage auprès des étudiants

J'ai pris la température ce matin auprès des autres studs :

### Question du package et de son contenu

#### SOLVER
- Mis à part Yannick qui ne comptait intégrer au package que la génération de maze, et qui se pose désormais des questions...
- Tous ceux que je suis allée voir (Quentin D, Adrien, Vincent, Léo et Quentin, Lucia, Paul) ont intégré au package le solver. (le sujet demande bien « access at least a solution » p 13)

#### PARSER
- 3 groupes avaient intégré le parser
- 4 non (avec l'argument assez convaincant que la config de pacman sera différente)

### Ma proposition pour le package
- ✓ Intégrer le solver mais pas le parser
- ✓ Ne pas mettre de `main.py` dans le package
- ✓ Remplacer par une proposition de main dans le README interne au package
- ✓ Mettre un exemple de config valide dans le README interne au package

---

## Question de la classe MazeGenerator

### Arguments des groupes

#### Cluster du haut
Dans le cluster du haut, on a souvent séparé les responsabilités :
- Générateur dans le `MazeGenerator`
- Solver séparé

**Arguments** : clarté, séparation des responsabilités

#### Cluster du bas
On lit dans le sujet :
> *"You must implement the maze generation as a unique class (e.g., 'MazeGenerator') inside a standalone module that can be imported in a future project."*

Interprétation comme une injonction à tout mettre dans la classe `MazeGenerator` : le générateur, le solver et même pour le groupe d'Adrien et pour celui de Vincent le parser.

**Arguments** : respect de la consigne, longueur moyenne de la classe (~300 lignes)

### Ma proposition : Approche Hybride

Créer une classe `MazeGenerator` avec deux méthodes :

```python
class MazeGenerator:
    def generate(self):
        """Génère le labyrinthe"""
        return grid
    
    def solve(self, entry, exit):
        """Résout le labyrinthe"""
        return path
```

**Arguments** : 
- Une seule classe comme le demande le sujet
- Code propre et maintenable


## Proposition de Structure Révisée

À partir de là, j'amende la proposition de structure :

```
A-Maze-ing/
├── a_maze_ing.py                # Le point d'entrée (très court, le chef d'orchestre)
├── config.txt
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── tests/                        # Le laboratoire de tests
│   ├── test_parsing.py
│   └── test_generator.py
├── src/                          # LE MOTEUR EXPORTABLE (Epic 3)
│   └── mazegen/
│       ├── __init__.py
│       ├── generator.py          # Ta fameuse classe MazeGenerator et sa logique
│       ├── exporter.py           # Conversion hexadécimale et écriture de output.txt
│       ├── solver.py             # Calcul du chemin le plus court entre départ et arrivé
│       └── README.md
└── app/                          # LA LOGIQUE LOCALE (Epics 2, 4 et 5)
    ├── __init__.py
    ├── parser.py                 # Lecture, sécurisation et validation de config.txt
    └── display.py                # Rendu MLX/ASCII et gestion des inputs clavier
```
 |


    