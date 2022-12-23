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
    coordonneesVoisins=[]
    for lin in range(grid_tk.get_lines_columns(can)[0]):
        coordonneesVoisins.append([grid_manager.neighborhood(grid, lin, col, DELTAS_CONWAY) for col in range(grid_tk.get_lines_columns(can)[1])])
    
    valeursVoisins=coordonneesVoisins
    for lin in range(len(coordonneesVoisins)):
        for col in range(len(coordonneesVoisins[lin])):
            numeroVoisin=0
            for voisin in coordonneesVoisins[lin][col]:
                valeursVoisins[lin][col][numeroVoisin]=grid[voisin[0]][voisin[1]]
                numeroVoisin+=1

    for lin in range(grid_tk.get_lines_columns(can)[0]):
        for col in range(grid_tk.get_lines_columns(can)[1]):

            if valeursVoisins[lin][col].count("1")<2 or valeursVoisins[lin][col].count(1)>3:
                grid_tk.set_cell(can, grid, lin, col, 0, grid_tk.COLORS["bg"])

            elif valeursVoisins[lin][col].count("1")==3:
                grid_tk.set_cell(can, grid, lin, col, 1, grid_tk.COLORS["fg"])
    

if __name__ == "__main__":
    """Définitions des variables de test et des tests de chaque fonction"""
    DELTAS_CONWAY = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    w=Tk()
    c=create_alea_conway(10, 15, 30, 10, 0, True, True)
    c[1].pack()
    w.bind("<Return>", lambda event: evolve_conway(c[1], grid_tk.get_grid(c[1])))
    w.after(500, evolve_conway, c[1], grid_tk.get_grid(c[1]))
    w.mainloop()