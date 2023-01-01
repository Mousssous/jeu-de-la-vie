from itertools import count
import random
from venv import create

from numpy import False_


def create_grid_lc(lin, col, val):
    """Retourne une grille de 'lin' lignes et 'col' colonnes
    initialisées à 'val'"""
    return [[val for j in range(col)] for i in range(lin)]


def create_random_grid_lc(lin, col, vals):
    """Retourne une grille de 'lin' lignes et 'col' colonnes
    initialisés aléatoirement avec des valeurs de la liste 'vals'"""
    return [[random.choice(vals) for j in range(col)] for i in range(lin)]


def nb_lines(grid):
    """Retourne le nombre de lignes de la grille 'grid'"""
    return len(grid)


def nb_columns(grid):
    """Retourne le nombre de colonnes de la grille 'grid'"""
    return len(grid[0])


def line2str(grid, line, sep="\t"):
    """Retourne la chaine de caractère correspondant à la ligne 'line'.
    Les caractères sont séparés par le caractère 'sep'"""
    return sep.join([str(i) for i in grid[line]])


def grid2str(grid, sep="\t"):
    """Retourne la chaine de caractère correspondant à la grille 'grid'.
    Les caractères de chaque ligne de 'grid' sont séparés par le caractère 'sep'"""
    lignes=nb_lines(grid)

    return sep.join([line2str(grid, lin, sep) for lin in range(len(grid))])


def neighbour(grid, lin, col, delta, tore=True):
    """Retourne le voisin de la cellule 'grid[lin][col]' selon le tuple 'delta' = (delta_lin, delta_col).
    Si 'tore' est à 'True' le voisin existe toujours en considérant 'grid' comme un tore.
    Si 'tore' est à 'False' retourne 'None' lorsque le voisin est hors de la grille 'grid'."""
    if tore == True:
        if lin + delta[0] >= nb_lines(grid) and col + delta[1] >= nb_columns(grid):
            return (lin + delta[0] - nb_lines(grid), col + delta[1] - nb_columns(grid))
        elif lin + delta[0] >= nb_lines(grid):
            return (lin + delta[0] - nb_lines(grid), col + delta[1])
        elif col + delta[1] >= nb_columns(grid):
            return (lin + delta[0], col + delta[1] - nb_columns(grid))
        else:
            return (lin + delta[0], col + delta[1])
    else:
        if lin + delta[0] > nb_lines(grid) or col + delta[1] > nb_columns(grid):
            return None
        else:
            return (lin + delta[0], col + delta[1])


def neighborhood(grid, lin, col, deltas, tore=True):
    """Retourne pour la grille 'grid' la liste des N voisins de 'grid[lin][col]'
    correspondant aux N (delta_lin, delta_col) fournis par la liste 'deltas'.
    Si 'tore' est à 'True' le voisin existe toujours en considérant 'grid' comme un tore.
    Si 'tore' est à 'False' un voisin hors de la grille 'grid' n'est pas considéré."""
    return [neighbour(grid, lin, col, i, tore) for i in deltas]


if __name__ == "__main__":
    """Définitions des variables de test et des tests de chaque fonction"""
    # Tuple des déplacements (delta_lig, delta_col) pour repérer une cellule voisine dans une grille de Conway.
    # Les 8 directions possibles dans l'ordre sont : NO, N, NE, O, E, SO, S, SE.
    DELTAS_CONWAY = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    print(create_grid_lc(10, 2, 0))
    print(create_random_grid_lc(3, 3, [1, 2, 3, 4, 5]))
    print(nb_lines(create_grid_lc(3, 3, 1)))
    print(nb_columns(create_grid_lc(3, 3, 1)))
    print(line2str(create_grid_lc(3, 3, 1), 3))
    print(grid2str(create_grid_lc(3, 3, 1)))
    print(neighbour(create_grid_lc(3, 3, 1), 0, 0, (0, 4)))
    print(neighborhood(create_grid_lc(3, 3, 0), 1, 2, DELTAS_CONWAY))
