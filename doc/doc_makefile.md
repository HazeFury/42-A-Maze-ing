# Notes sur le Makefile

## Commandes et Options Utilisées

- **`@`** : permet de ne pas afficher dans le terminal la commande en cours d'exécution.
- **`@python3 -c "import sys; exit(1) if sys.version_info < (3, 10) else exit(0)"`**  
  Vérifie grâce aux infos du module `sys` qu'on est bien sur une version au moins 3.10 de Python.
- **`-m`**  
  Option pour Python : permet d'exécuter un module installé, plutôt que de chercher un fichier.
- **`@$(PIP) install -e .`**  
  Permet d'installer le projet en **mode éditable** dans l'environnement virtuel en passant par un lien symbolique.  
  Le package est reconnu par Python pour les imports, et les modifications du code sont prises en compte sans avoir à réinstaller tout le module.  
  C'est le standard pour le développement de packages Python.
- **`@cp dist/$(WHL) .`**  
  Copie le fichier `.whl` généré par la commande build et le place à la racine du dépôt comme demandé.
- **`@touch $(VENV)`**  
  Met à jour la date de modification du venv.  
  Permet au Makefile de savoir que le venv est à jour par rapport au `requirements.txt`.  
  Évite le relink.
- **`@find . -type d -name "__pycache__" -exec rm -rf {} +`**  
  `{}` correspond au dossier trouvé, `+` permet de supprimer plusieurs dossiers d'un coup.

## Notes sur les Modifications du Makefile

### 1. `@$(PIP) install -e ".[dev]"`

C'est la commande qui fait le pont entre ton code et ton environnement de dev.

- **`[dev]` (Extra dependencies)** : C'est la partie magique. On dit à pip : "Installe le projet, mais installe AUSSI les outils de développement listés sous `[project.optional-dependencies]` dev dans le .toml (Pydantic, Pytest, Flake8, Mypy)".

### 2. Le `-m` dans `@$(PYTHON) -m flake8`

C'est la solution ultime au problème "Module Not Found".

**Le problème classique** : Si tu tapes juste `flake8`, ton ordinateur cherche un fichier exécutable nommé flake8 dans ton PATH. S'il ne le trouve pas au bon endroit, ça plante (Erreur 127).

**La solution `-m` (Module)** : En écrivant `python3 -m flake8`, tu ne lances pas un fichier, tu demandes à l'interpréteur Python du venv de chercher dans ses propres bibliothèques s'il possède le module flake8.

**Pourquoi c'est plus robuste** : Tant que flake8 est installé dans le venv (via le `.[dev]`), Python le trouvera à coup sûr, même si le binaire n'est pas dans le dossier bin/.