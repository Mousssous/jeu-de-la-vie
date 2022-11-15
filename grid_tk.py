from operator import invert
from tkinter import *

from matplotlib.pyplot import fill

import grid_manager

# Dictionnaires des paramètres de forme d'une grille
COLORS = {'bg': 'white', 'fg': 'red', 'outline': 'black', 'text_val': 'black'}
FONT = {'text_val': 'Arial'}


def grid_canvas(master, grid, size_cell, margin, gutter, show_vals, outline):
    """Retourne un 'Canvas' placé dans la fenêtre 'master'. Celui-ci est construit à partir de la grille 'grid'
    en s'appuyant sur les modules 'grid_manager' et 'tkinter' ainsi que sur les dictionnaires des paramètres de forme.
    La largeur et la hauteur du Canvas sont calculés en considérant la taille 'size_cell' d'une cellule, la valeur de
    marge 'margin' autour de la grille et d'une taille de gouttière 'gutter' entre les lignes et les colonnes.
    Chaque cellule affichera en son centre le texte correspondant à son contenu si 'show_vals' est à la valeur 'True'.
    Les bordures des cellules ne s'afficheront que si 'outline' est à la valeur 'True'.
    Chaque cellule sera taguée par la chaine 'c_lin_col' et leur texte par la chaine 't_lin_col'.
    De plus, les deux seront taguées en plus par la chaine 'lin_col'.
    Un click avec le bouton gauche de la souris sur une cellule échangera ses couleurs de fond et d'avant-plan."""
    longueurTableau=grid_manager.nb_columns(grid)*(size_cell+gutter)+gutter
    hauteurTableau=grid_manager.nb_lines(grid)*(size_cell+gutter)+gutter
    c = Canvas(master, bg=COLORS['bg'], highlightthickness=0, width=margin+longueurTableau+margin, height=margin+hauteurTableau+margin)
    for y,i in enumerate(range(margin, hauteurTableau+margin, size_cell+gutter)):
        for x,j in enumerate(range(margin, longueurTableau+margin, size_cell+gutter)):
            c.create_rectangle(j, i, j+size_cell, i+size_cell, fill="ivory", tags="c_{}_{}".format(str(x), str(y)), outline=COLORS['outline'] if outline==True else "")
            c.create_text(j+size_cell/2, i+size_cell/2, font=FONT['text_val'], fill=COLORS['text_val'], text=(grid[y][x] if show_vals==True else ""), tags="t_{}_{}".format(str(x), str(y)))

    def onclick(x,y):
        tag = "c_{}_{}".format((x-margin-gutter)//size_cell, (y-margin-gutter)//size_cell)

        if c.itemcget(tag, "fill")==COLORS["fg"]:
            c.itemconfig(tag, fill="ivory")
        else:
            c.itemconfig(tag, fill=COLORS["fg"])
        #print(get_color_cell(cnv,tag[2], tag[-1]))
    c.bind("<Button-1>", lambda event: onclick(event.x, event.y))
    return c

def get_lines_columns(can):
    """Retourne le nombre de lignes et de colonnes de la grille représentée par le Canvas 'can'."""
    return (len([can.gettags(i) for i in can.find_all() if can.gettags(i)[0][0:4]=="c_0_"]), len([can.gettags(i) for i in can.find_all() if can.gettags(i)[0][-2:]=="_0" and can.gettags(i)[0][0]=="c"]))


def get_grid(can):
    """Retourne la grille représentée par le Canvas 'can'."""
    return [[can.itemcget("t_{}_{}".format(j,i), "text") for j in range(get_lines_columns(can)[1])] for i in range(get_lines_columns(can)[0])]


def get_color_cell(can, i, j):
    """Retourne la couleur de la cellule ('i', 'j') de la grille représentée par le Canvas 'can'."""
    return can.itemcget("c_{}_{}".format(i,j), "fill")


def set_color_cell(can, i, j, color, outline=True):
    """Rempli la cellule ('i', 'j') de la grille représentée par le Canvas 'can' par la couleur 'color'.
    Dessine ses bordures avec la couleur 'color' si 'outline' a la valeur 'False'."""
    can.itemconfig("c_{}_{}".format(i,j), fill=color)
    if outline:
        can.itemconfig("c_{}_{}".format(i,j), outline=color)


def get_color_text(can, i, j):
    """Retourne la couleur du texte de la cellule ('i', 'j') de la grille représentée par le Canvas 'can'."""
    return can.itemcget("t_{}_{}".format(i,j), "fill")


def set_color_text(can, i, j, color):
    """Rempli le texte de la cellule ('i', 'j') de la grille représentée par le Canvas 'can' par la couleur 'color'."""
    can.itemconfig("t_{}_{}".format(i,j), fill=color)


def set_cell_text(can, i, j, val):
    """Change la valeur du texte de la cellule ('i', 'j') du Canvas 'can' avec la valeur 'val'"""
    can.itemconfig(("t_{}_{}".format(i,j)), text=val)


def swap_cell_colors(event, lin, col, outline=True):
    """Handler de l'événement 'event' produit par un click bouton gauche sur la cellule ('lin', 'col') d'une grille.
    Dessine les bordures du 'widget' appelant selon la valeur booléenne de 'outline'."""
    pass


def set_cell(can, grid, i, j, val, color_case, show_vals=True, outline=True, color_text=COLORS['text_val']):
    """Modifie la grille 'grid' et le Canvas 'can' en affectant la valeur 'val' à la cellule ('i', 'j').
    Change la couleur du texte par 'color_text' et la valeur par 'val' si 'show_vals' a la valeur 'True'.
    Dessine les bordures de la cellule selon la valeur booléenne de 'outline'."""
    grid[i][j]=val
    can.itemconfig("t_{}_{}".format(i,j), fill=color_text)
    can.itemconfig("t_{}_{}".format(i,j), text=val) if show_vals else None
    can.itemconfig("c_{}_{}".format(i,j), outline=COLORS["outline"] if outline else "")
    can.itemconfig("c_{}_{}".format(i,j), fill=color_case)


if __name__ == "__main__":
    """Définitions des variables de test et des tests de chaque fonction"""
    fen = Tk()
    grille = grid_manager.create_random_grid_lc(5, 6, [0, 1])
    cnv=grid_canvas(fen, grille, 20, 10, 0, show_vals=True, outline=True)
    cnv.pack()
    print(get_lines_columns(cnv))
    #print(get_grid(cnv))
    set_color_cell(cnv, 1, 1, "green", outline=True)
    set_color_text(cnv, 1, 1, "purple")
    set_cell_text(cnv, 1, 1, 8)
    set_cell(cnv, grid_manager.create_random_grid_lc(5, 5, [0, 1]), 1, 1, 2, "white")
    print(get_grid(cnv))
    fen.mainloop()