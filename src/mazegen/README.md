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

7. Créer un fichier qui importe le MazeGenerator en copiant-collant dans le terminal:
```
cat <<EOF > test_engine.py
from mazegen.generator import MazeGenerator

try:
    # On teste le moteur de manière autonome
    mg = MazeGenerator(width=10, height=10, seed=42)
    grid = mg.generate()
    print("✅ Succès : Le moteur 'mazegen' est bien installé et autonome !")
    print(f"Structure générée : {len(grid)}x{len(grid[0])} cellules.")
except ImportError:
    print("❌ Erreur : Le module 'mazegen' est introuvable.")
except Exception as e:
    print(f"❌ Erreur lors de l'utilisation du moteur : {e}")
EOF
```

7. 6. **Lancer le test** :
```bash
python3 test_engine.py
```

8. Un message apparaît en cas de succès :
   ```
   ✅ Succès : Le moteur 'mazegen' est bien installé et autonome !
	Structure générée : 10x10 cellules.
   ```