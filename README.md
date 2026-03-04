# Jeu de la Vie — Conway Game of Life

Ce projet est une implémentation du **Jeu de la vie de Conway** en **Python** avec une interface graphique réalisée avec **Tkinter**.

Le programme permet de créer, modifier et observer l'évolution d'une population de cellules sur une grille selon les règles classiques du Game of Life.

---

## Principe

Le **Jeu de la vie** est un automate cellulaire inventé par le mathématicien **John Conway** en 1970.

Chaque cellule d'une grille peut être dans l'un des deux états suivants :

- vivante
- morte

À chaque génération, l'état des cellules évolue selon les règles suivantes :

1. Une cellule vivante avec moins de **2 voisines vivantes** meurt (sous-population).
2. Une cellule vivante avec **2 ou 3 voisines vivantes** survit.
3. Une cellule vivante avec plus de **3 voisines vivantes** meurt (surpopulation).
4. Une cellule morte avec exactement **3 voisines vivantes** devient vivante (naissance).

Ces règles simples peuvent produire des comportements complexes et émergents.

---

## Fonctionnalités

- Interface graphique avec **Tkinter**
- Création de grilles :
  - aléatoire
  - vide
  - pleine
- Modification des cellules avec la souris
- Simulation **pas à pas** ou **automatique**
- Sauvegarde et chargement de modèles dans le dossier `templates`

---

## Installation

### Prérequis

- Python **3.10 ou supérieur**

Les dépendances sont définies dans le fichier `pyproject.toml`.

### Installation avec uv (recommandé)

Si vous utilisez **uv**, installez simplement les dépendances avec :

```bash
uv sync
