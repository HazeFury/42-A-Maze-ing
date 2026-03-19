# Notes sur le Makefile

- `@` permet de ne pas afficher dans le terminal la commande en cours d'exécution.
- `@python3 -c "import sys; exit(1) if sys.version_info < (3, 10) else exit(0)"`  
  Vérifie grâce aux infos du module `sys` qu'on est bien sur une version au moins 3.10 de Python.
- `-m`  
  Option pour Python : permet d'exécuter un module installé, plutôt que de chercher un fichier.
- `@$(PIP) install -e .`  
  Permet d'installer le projet en **mode éditable** dans l'environnement virtuel en passant par un lien symbolique.  
  Le package est reconnu par Python pour les imports, et les modifications du code sont prises en compte sans avoir à réinstaller tout le module.  
  C'est le standard pour le développement de packages Python.
- `@cp dist/$(WHL) .`  
  Copie le fichier `.whl` généré par la commande build et le place à la racine du dépôt comme demandé.
- `@touch $(VENV)`  
  Met à jour la date de modification du venv.  
  Permet au Makefile de savoir que le venv est à jour par rapport au `requirements.txt`.  
  Évite le relink.
- `@find . -type d -name "__pycache__" -exec rm -rf {} +`  
  `{}` correspond au dossier trouvé, `+` permet de supprimer plusieurs dossiers d'un coup.