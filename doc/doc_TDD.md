# 🧪 Guide de Survie : Le TDD (Test Driven Development)

Salut ! Si tu lis ça, c'est qu'on va coder comme des pros. J'ai préparé le terrain pour la validation de notre fichier de configuration en écrivant d'abord les tests unitaires. On va donc utiliser la méthode TDD pour développer notre parseur.

## C'est quoi le TDD ?
Le TDD (Développement Dirigé par les Tests), c'est une façon de concevoir le code à l'envers. Au lieu d'écrire la fonction puis de chercher comment la tester, on écrit le test d'abord, on le regarde planter, et ensuite on écrit le code pour le réparer.

Ça se passe en 3 étapes (le fameux cycle "Red-Green-Refactor") :
1. **🔴 RED (Rouge) :** Tu lances le test. Comme la logique n'existe pas encore dans le code, il échoue. C'est normal et voulu !
2. **🟢 GREEN (Vert) :** Tu écris le code minimum nécessaire pour que le test réussisse.
3. **✨ REFACTOR (Nettoyage) :** Une fois que c'est vert, tu peux optimiser ou rendre ton code plus propre, avec la garantie absolue que si ça repasse au rouge, c'est que tu as cassé un truc.

## Ta Mission pour le MazeConfig
J'ai écrit les tests dans le dossier `tests/`. Ton objectif est de rendre tous ces tests verts en développant la logique dans notre modèle Pydantic `MazeConfig` (dans `app/parser.py`).

### Les commandes magiques du Makefile

Pour lancer absolument tous les tests du projet d'un coup :
	make test

Pour te concentrer uniquement sur le fichier sur lequel tu bosses (c'est ce qu'il te faut pour l'instant) :
	make test-file FILE=tests/test_parser.py

### Comment procéder pas à pas :
1. Lance `make test-file FILE=tests/test_parser.py`. Tu vas voir de belles erreurs rouges. Pas de panique !
2. Lis la première erreur. Par exemple, le test va hurler parce que la valeur `"0,0"` lue dans le fichier n'est pas un tuple valide.
3. Va dans `app/parser.py`, et implémente ton validateur (ex: un `@field_validator(mode='before')`) pour `entry_coord` afin de transformer la string en tuple.
4. Relance la commande de test. Le premier test devrait passer au vert !
5. Passe à l'erreur suivante (ex: vérifier que l'entrée et la sortie sont différentes).
6. Répète jusqu'à ce que toute la console soit verte !

Bon courage ! Tu vas voir, quand tous les tests s'illuminent en vert d'un coup, c'est hyper satisfaisant. 🚀