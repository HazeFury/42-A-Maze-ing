# Algoritme Iterative Backtracker 

## 1️⃣ Initialisation

- **Pile (Stack)** : Créer une liste vide pour stocker le chemin actuel
- **Point de départ** : Choisir la cellule `(0, 0)`
- **Marquage** : Marquer cette cellule comme visitée
- **Empiler** : Ajouter cette cellule à la Pile

## 2️⃣ Boucle principale

**Tant que la Pile n'est pas vide :**

### Étape 1 : Obtenir la position actuelle
- `Current` = l'élément au sommet de la Pile (le dernier ajouté)

### Étape 2 : Chercher les voisins disponibles
- Regarder les 4 cellules adjacentes : **Nord, Est, Sud, Ouest**
- Vérifier les conditions pour chaque voisin :
  - ✓ La cellule est dans les limites de la grille
  - ✓ La cellule n'a pas encore été visitée
  - ⚠️ *Note* : Les cases du motif "42" sont ignorées (déjà marquées visitées)

### Étape 3 : Prendre une décision

**SI** au moins un voisin est disponible :
  1. Choisir un voisin au hasard (`Next`) en utilisant la Seed du fichier config
  2. **Casser les murs** : Ouvrir le passage entre `Current` et `Next` (dans les deux sens)
  3. Marquer `Next` comme visité
  4. Empiler `Next` dans la Pile (elle devient la nouvelle position actuelle)

**SINON** (cul-de-sac détecté) :
  1. **Dépiler (Pop)** : Retirer l'élément actuel de la pile
  2. Revenir à la cellule précédente pour chercher un autre chemin