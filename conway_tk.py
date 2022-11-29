import grid_manager
import grid_tk
from tkinter import *
from time import sleep


def create_alea_conway(lines, columns, size_cell, margin, gutter, show_vals, outline):
    """Retourne un Canvas et une grille d'un automate de Conway initialisé aléatoirement par des 0 et des 1."""
    grille=grid_manager.create_random_grid_lc(lines, columns, [0, 1])
    return (grille, grid_tk.grid_canvas(w, grille, size_cell, margin, gutter, show_vals, outline))


def evolve_conway(can, grid):
    """Fait évoluer la grille 'grid' et le Canvas 'can' selon les règles de l'automate de Conway"""
    voisins=[[grid_manager.neighborhood(grid, lin, col, DELTAS_CONWAY) for col in range(grid_manager.nb_columns(grid))] for lin in range(grid_manager.nb_lines(grid))]
    valeursVoisins=[[[grid[i[0]][i[1]] for i in voisins[lin][col]] for col in range(grid_manager.nb_columns(voisins))] for lin in range(grid_manager.nb_lines(voisins))]

    for lin in range(len(valeursVoisins)):
        for col in range(len(valeursVoisins[lin])):
            if valeursVoisins[lin][col].count(1)==3:
                grid[lin][col]=1
            if valeursVoisins[lin][col].count(1)==2:
                pass
            if valeursVoisins[lin][col].count(1)<2 or valeursVoisins[lin][col].count(1)>3:
                grid[lin][col]=0
    
    for lin in range(grid_manager.nb_lines(grid)):
        for col in range(grid_manager.nb_columns(grid)):
            grid_tk.set_cell_text(can, lin, col, grid[lin][col])
            grid_tk.set_color_cell(can, lin, col)
    

if __name__ == "__main__":
    """Définitions des variables de test et des tests de chaque fonction"""
    DELTAS_CONWAY = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    w=Tk()
    c=create_alea_conway(2, 2, 30, 5, 0, True, True)
    c[1].pack()
    w.bind("<Return>", lambda event: evolve_conway(c[1], c[0]))
    w.mainloop()