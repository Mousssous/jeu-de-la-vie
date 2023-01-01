from operator import invert
from tkinter import *

from matplotlib.pyplot import fill

import grid_manager

# Dictionnaires des paramètres de forme d'une grille
COLORS = {"bg": "white", "fg": "red", "outline": "black", "text_val": "black"}
FONT = {"text_val": "Arial"}

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
    longueurTableau = grid_manager.nb_columns(grid) * (size_cell + gutter)
    hauteurTableau = grid_manager.nb_lines(grid) * (size_cell + gutter)
    c = Canvas(
        master,
        bg=COLORS["bg"],
        highlightthickness=0,
        width=margin + longueurTableau + margin,
        height=margin + hauteurTableau + margin,
    )

    for x, i in enumerate(range(margin, hauteurTableau + margin, size_cell + gutter)):
        for y, j in enumerate(range(margin, longueurTableau + margin, size_cell + gutter)):
            c.create_rectangle(j, i, j + size_cell, i + size_cell, tags=f"c_{x}_{y}", outline=outline)
            set_color_cell(c, x, y, COLORS["fg"] if grid[x][y] == 1 else COLORS["bg"])
            c.tag_bind(f"c_{x}_{y}", "<Button-1>", lambda event: swap_cell_colors(
                    event,
                    int((event.y - c.coords(c.find_withtag("c_0_0"))[0]) // (size_cell + gutter)),
                    int((event.x - c.coords(c.find_withtag("c_0_0"))[1]) // (size_cell + gutter)),
                    outline,
                ),
            )

            c.create_text(
                j + size_cell / 2,
                i + size_cell / 2,
                font=FONT["text_val"] + f" {int(2*size_cell/3)}",
                fill=COLORS["text_val"],
                text=(grid[x][y] if show_vals == True else ""),
                tags=f"t_{x}_{y}",
            )
            
            c.tag_bind(f"t_{x}_{y}", "<Button-1>", lambda event: swap_cell_colors(
                    event,
                    int((event.y - c.coords(c.find_withtag("c_0_0"))[0]) // (size_cell + gutter)),
                    int((event.x - c.coords(c.find_withtag("c_0_0"))[1]) // (size_cell + gutter)),
                    outline,
                ),
            )
    return c


def get_lines_columns(can):
    """Retourne le nombre de lignes et de colonnes de la grille représentée par le Canvas 'can'."""
    return (len([can.gettags(i) for i in can.find_all() if can.gettags(i)[0][-2:] == "_0" and can.gettags(i)[0][0] == "c"  ]), len([can.gettags(i) for i in can.find_all() if can.gettags(i)[0][0:4] == "c_0_"]))

def get_grid(can):
    """Retourne la grille représentée par le Canvas 'can'."""
    nbLignes=get_lines_columns(can)[0]
    nbColonnes=get_lines_columns(can)[1]

    return [[0 if can.itemcget(f"c_{lin}_{col}", "fill") == COLORS["bg"] else 1 for col in range(nbColonnes)] for lin in range(nbLignes)]

def get_color_cell(can, i, j):
    """Retourne la couleur de la cellule ('i', 'j') de la grille représentée par le Canvas 'can'."""
    return can.itemcget(f"c_{i}_{j}", "fill")


def set_color_cell(can, i, j, color, outline=True):
    """Rempli la cellule ('i', 'j') de la grille représentée par le Canvas 'can' par la couleur 'color'.
    Dessine ses bordures avec la couleur 'color' si 'outline' a la valeur 'True'."""
    can.itemconfig(f"c_{i}_{j}", fill=color)


def get_color_text(can, i, j):
    """Retourne la couleur du texte de la cellule ('i', 'j') de la grille représentée par le Canvas 'can'."""
    return can.itemcget(f"t_{i}_{j}", "fill")


def set_color_text(can, i, j, color):
    """Rempli le texte de la cellule ('i', 'j') de la grille représentée par le Canvas 'can' par la couleur 'color'."""
    can.itemconfig(f"t_{i}_{j}", fill=color)


def set_cell_text(can, i, j, val):
    """Change la valeur du texte de la cellule ('i', 'j') du Canvas 'can' avec la valeur 'val'"""
    can.itemconfig((f"t_{i}_{j}"), text=val)


def swap_cell_colors(event, lin, col, outline=True):
    """Handler de l'événement 'event' produit par un click bouton gauche sur la cellule ('lin', 'col') d'une grille.
    Dessine les bordures du 'widget' appelant selon la valeur booléenne de 'outline'."""
    set_color_cell(
        event.widget,
        lin,
        col,
        COLORS["fg"] if get_color_cell(event.widget, lin, col) == COLORS["bg"] else COLORS["bg"],
    )

    if event.widget.itemcget(f"t_{lin}_{col}", "text") == "1":
        set_cell_text(event.widget, lin, col, "0")
        
    elif event.widget.itemcget(f"t_{lin}_{col}", "text") == "0":
        set_cell_text(event.widget, lin, col, "1")


def set_cell(can, grid, i, j, val, color_case, show_vals=True, outline=True, color_text=COLORS["text_val"]):
    """Modifie la grille 'grid' et le Canvas 'can' en affectant la valeur 'val' à la cellule ('i', 'j').
    Change la couleur du texte par 'color_text' et la valeur par 'val' si 'show_vals' a la valeur 'True'.
    Dessine les bordures de la cellule selon la valeur booléenne de 'outline'."""
    grid[i][j] = val
    can.itemconfig(f"t_{i}_{j}", fill=color_text)
    can.itemconfig(f"t_{i}_{j}", text=val) if show_vals else None
    can.itemconfig(f"c_{i}_{j}", outline=can.itemcget(f"c_{0}_{0}", "outline") if outline else None)
    can.itemconfig(f"c_{i}_{j}", fill=color_case)


if __name__ == "__main__":
    """Définitions des variables de test et des tests de chaque fonction"""
    w = Tk()
    grille = grid_manager.create_random_grid_lc(2, 3, [0, 1])
    c = grid_canvas(w, grille, 20, 10, 0, show_vals=True, outline=True)
    c.pack()
    w.mainloop()
