# Pydantic et pyproject.toml

## Introduction

Quand j'ai voulu enlever pydantic des librairies exportées du pyproject.toml pour plus de propreté du package, le module n'était plus du tout exporté. Voici le bilan généré par IA de mes recherches:

## 📝 Synthèse Technique : Pydantic, Makefile et Architecture

### 1. Le problème du "ModuleNotFoundError" (Bug du venv)

Ce qui se passait : Même avec pydantic dans le requirements.txt, make test échouait en disant que le module était introuvable.

La cause : Quand on utilise un pyproject.toml avec pip install -e ., pip synchronise l'environnement avec les dépendances déclarées dans le .toml. Si Pydantic n'y est pas, il est "ignoré" par les outils de build.

La solution : On a forcé l'utilisation de $(PYTHON) -m flake8 dans le Makefile. Cela garantit que l'outil utilise bien l'interpréteur du venv et ses bibliothèques installées.

### 2. 🛠️ Gestion du pyproject.toml (Production vs Dev)

Puisque nous voulons que le package final reste "léger" et sans dépendances forcées, nous avons deux stratégies pour le .toml :

**Les optional-dependencies (Recommandé)** : On liste Pydantic comme un "extra" (un bonus de dev). Il est installé dans notre environnement de travail pour valider le config.txt, mais il n'est pas requis pour que le moteur de labyrinthe tourne seul une fois exporté.

```toml
[project.optional-dependencies]
dev = ["pydantic", "pytest", "flake8"]
```

**L'exclusion manuelle** : Lors de la génération du .whl via make build, on peut configurer l'outil de build pour qu'il n'inclue pas le module parser.py. Ainsi, le package exporté ne contient que les algorithmes "purs".

**Solution choisie** : Les optional-dependencies dans pypoject.toml

### 3. La solution d'Architecture (Séparation des responsabilités)

On a mis en place une isolation stricte entre la validation et l'algorithme :

Le Parser (parser.py) : C'est notre "douane". Il utilise Pydantic pour vérifier les types, les alias (WIDTH vs width) et les erreurs de coordonnées (ex: 0,0 vs EXIT).

Le Moteur (generator.py) : C'est notre cœur de calcul. Il ne connaît PAS Pydantic. Il ne reçoit que des types standards (int, tuple, bool).

Le Chef d'Orchestre (a_maze_ing.py) : C'est lui qui fait le pont.

Il appelle le Parser pour valider le fichier.

Il "déballe" les données (il extrait les valeurs brutes).

Il injecte ces valeurs simples dans le Générateur.

#### ❌ Ce qu'on NE FAIT PAS (Lien fort) :

```python
# Dans generator.py
def __init__(self, config: MazeConfig): # INTERDIT : On dépend de Pydantic ici
    self.w = config.width
```

#### ✅ Ce qu'on FAIT (Isolation totale) :

```python
# Dans a_maze_ing.py
config = MazeConfig(**data) # On valide
# On extrait les données brutes pour le moteur
gen = MazeGenerator(width=config.width, height=config.height)
```

## 🔧 Problèmes Actuels et Corrections Nécessaires

### Erreurs de Linting (make lint - Exit Code 2)

**1. Import inutilisé dans parser.py :**
- Erreur : `F401 'pydantic.ValidationError' imported but unused`
- Cause : ValidationError est importé mais jamais utilisé dans le code
- Solution : Supprimer l'import ou l'utiliser pour gérer les erreurs de validation

**2. Lignes trop longues :**
- Erreur : `E501 line too long (88 > 79 characters)` dans parser.py
- Erreur : `E501 line too long (81 > 79 characters)` dans parser.py
- Erreur : `E501 line too long (80 > 79 characters)` dans generator.py
- Solution : Reformater les lignes pour respecter la limite de 79 caractères

### Recommandations pour la Suite

1. **Migrer pyproject.toml** : Ajouter les optional-dependencies et retirer pydantic des dépendances principales
2. **Corriger les imports** : Nettoyer les imports inutilisés dans parser.py
3. **Respecter PEP 8** : Corriger la longueur des lignes dans tout le code
4. **Tests** : S'assurer que make test passe après les corrections

#### ✅ Ce qu'on FAIT (Isolation totale) :

```python
# Dans a_maze_ing.py
config = MazeConfig(**data) # On valide
# On extrait les données brutes pour le moteur
gen = MazeGenerator(width=config.width, height=config.height)
```