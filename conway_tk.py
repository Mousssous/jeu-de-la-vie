import grid_manager
import grid_tk
from tkinter import *
from time import sleep


def create_alea_conway(lines, columns, size_cell, margin, gutter, show_vals, outline):
    """Retourne un Canvas et une grille d'un automate de Conway initialisé aléatoirement par des 0 et des 1."""
    grille = grid_manager.create_random_grid_lc(lines, columns, [0, 1])
    return (
        grille,
        grid_tk.grid_canvas(fenetreJeu, grille, size_cell, margin, gutter, show_vals, outline),
    )

def evolve_conway(can, grid):
    """Fait évoluer la grille 'grid' et le Canvas 'can' selon les règles de l'automate de Conway"""
    DELTAS_CONWAY = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))

    nbLignes=grid_manager.nb_lines(grid)
    nbColonnes=grid_manager.nb_columns(grid)

    #nombre de uns parmi les voisins de la cellule ('lin', 'col')
    nbUns=[[[grid[i[0]][i[1]] for i in grid_manager.neighborhood(grid, lin, col, DELTAS_CONWAY)].count(1) for col in range(nbColonnes)] for lin in range(nbLignes)]

    for lin in range(nbLignes):
        for col in range(nbColonnes):
            if nbUns[lin][col]<2 or nbUns[lin][col]>3:
                grid_tk.set_color_cell(
                    can, lin, col,
                    grid_tk.COLORS["bg"],
                    False if can.itemcget("t_0_0", "text") == "" else True,
                )
                if can.itemcget("t_0_0", "text")!="":
                    grid_tk.set_cell_text(can, lin, col, 0)

            elif nbUns[lin][col]==3:
                grid_tk.set_color_cell(
                    can, lin, col,
                    grid_tk.COLORS["fg"],
                    False if can.itemcget("t_0_0", "text") == "" else True,
                )
                if can.itemcget("t_0_0", "text")!="":
                    grid_tk.set_cell_text(can, lin, col, 1)


if __name__ == "__main__":
    """Définitions des variables de test et des tests de chaque fonction"""
    DELTAS_CONWAY = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    fenetreJeu = Tk()
    c = create_alea_conway(10, 15, 30, 10, 0, True, True)
    c[1].pack()
    fenetreJeu.bind("<Return>", lambda event: evolve_conway(c[1], grid_tk.get_grid(c[1])))
    fenetreJeu.after(500, evolve_conway, c[1], grid_tk.get_grid(c[1]))
    fenetreJeu.mainloop()
