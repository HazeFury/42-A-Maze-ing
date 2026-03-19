# Tester le package `mazegen` dans un dossier de test

1. Se rendre dans le dossier de test.
2. Créer un environnement virtuel :
   ```bash
   python3 -m venv venv_test
   ```
3. L'activer :
   ```bash
   source venv_test/bin/activate
   ```
4. Installer le package `mazegen` :
   ```bash
   pip install ../A_Maze_ing/mazegen-1.0.0-py3-none-any.whl
   ```
   *(chemin à adapter en fonction de la localisation du dossier !)*
5. Vérifier les dépendances installées :
   ```bash
   pip list
   ```
6. S'assurer de la présence d'un fichier de configuration de maze dans le dossier de test (en copiant `config.txt` ou en créant un autre fichier de configuration).
7. Lancer le programme avec la commande :
   ```bash
   mazegen config.txt
   ```
8. Un message apparaît en cas de succès :
   ```
   Succès : Le package mazegen est bien installé !
   Génération d'un labyrinthe 10x10...
   ```