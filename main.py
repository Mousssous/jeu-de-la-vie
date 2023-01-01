import grid_manager
import grid_tk
import conway_tk
from tkinter import *
from tkinter import ttk
import os

#initialisation des paramètres du jeu
nbGenerations=0
grille=0
grilleInitiale=0
nomSaveFichier=0
nomLoadFichier=0
enPause=True; boutonPause=0; repetition=0
fenetreParametres=0
fenetreJeu=0
lines=0; columns=0; size_cell=0; margin=0; gutter=0; show_vals=0; outline=0; delai=0

#dictionnaire de traduction des couleurs
couleurs = {
            "Noir": "black",
            "Blanc": "white",
            "Rouge": "red",
            "Cyan": "cyan",
            "Magenta": "magenta",
            "Bleu": "blue",
            "Vert": "green",
            "Jaune": "yellow",
            "Pas de bordures": "",
}
#création d'une liste de couleurs ordonée, pour qu'elles apparaissent toujours dans le même ordre car list(couleurs.keys()) ne conserve pas l'ordre des clés
listeCouleurs=list(couleurs.keys())
listeCouleurs.sort()

#fonction de sauvegarde dans le même dossier que le ce fichier
def sauvegarder(grille):
    with open(os.path.dirname(__file__)+"/templates/"+nomSaveFichier.get()+".mdl", "w") as f:
        f.write(str(grille))

#fonction appelée à chaque fois qu'on passe à la génération suivante (via le bouton ou de façon périodique)
def evolution(canvas, periode):
    #le parametre "periode" est une chaîne de caractères qui permet de savoir comment la fonction a été appelée (par un bouton ou par l'actualisation périodique)
    #il vaut "pause" la fonction a été appelée par le bouton Pause/Reprendre
    #il vaut "after" si la fonction a été appelée par la fonction "after" (évolution périodique)
    #il vaut "evoluer" si la fonction a été appelée par le bouton d'évolution manuelle
    #remarque: "evoluer" ne sert pas
    global nbGenerations
    global enPause
    global repetition

    nbGenerations+=1

    if nbGenerations==1:
        global grilleInitiale
        grilleInitiale=grille

    #si on clique sur le bouton alors qu'il y est écrit "Reprendre", c'est que l'on est actuellment en pause
    if periode=="pause" and not enPause:
        fenetreJeu.after_cancel(repetition)
        enPause=True
        return None #juste pour sortir de la fonction sans exécuter le reste

    if periode=="pause" and enPause:
        enPause=False

        #rappel de la fonction méthode "after" pour conserver l'actualisation périodique si elle existe
        repetition=fenetreJeu.after(delai.get(), evolution, canvas, "after")
    
    if periode=="after":
        #rappel de la fonction méthode "after" pour conserver l'actualisation périodique si elle existe
        repetition=fenetreJeu.after(delai.get(), evolution, canvas, "after")
    
    #fonction d'évolution dans conway_tk
    conway_tk.evolve_conway(canvas, grid_tk.get_grid(canvas))

def lancerPartie(mode):
    #seule la façon dont la grille est générée change en fonction des modes de jeu donc on la crée avant pour ensuite la donner à la fonction générale grid_canvas dans grid_tk
    global grille

    #grille aléatoire
    if mode == "Nouvelle partie aléatoire":
        grille = grid_manager.create_random_grid_lc(
            int(lines.get()),
            int(columns.get()),
            [0, 1],
        )

    #grille remplie de 1 (toutes les cellules sont allumées)
    elif mode == "Nouvelle partie pleine":
        grille = grid_manager.create_grid_lc(
            int(lines.get()),
            int(columns.get()),
            1,
        )

    #grille remplie de 0 (toutes les cellules sont éteintes)
    elif mode == "Nouvelle partie vierge":
        grille = grid_manager.create_grid_lc(
            int(lines.get()),
            int(columns.get()),
            0,
        )

    #création de la grille selon les données du fichier
    if mode=="Modèles sauvegardés":

        if nomLoadFichier.get()=="":
            raise Exception("Vous n'avez pas renseigné de modèle")

        #remplissage d'une grille conforme au paramètres donnés sur fenetreParametres
        grille=[[0 for col in range(columns.get())] for lin in range(lines.get())]

        with open(os.path.dirname(__file__)+"/templates/"+nomLoadFichier.get()+".mdl") as f:
            #fichier chargé au milieu de la grille
            modeleCharge=eval(f.read())

        #création des indices de début et de fin pour l'insertion du modèle dans une grille plus grande
        ligneDebut=len(grille)//2-len(modeleCharge)//2
        ligneFin=ligneDebut + len(modeleCharge)
        colonneDebut=len(grille[0])//2-len(modeleCharge[0])//2
        colonneFin=colonneDebut + len(modeleCharge[0])

        # Insérer les valeurs de la liste 2 au centre du tableau
        for i in range(ligneDebut, ligneFin):
            for j in range(colonneDebut, colonneFin):
                grille[i][j]=modeleCharge[i-ligneDebut][j-colonneDebut]
        
        if lines.get()<grid_manager.nb_lines(modeleCharge) or columns.get()<grid_manager.nb_columns(modeleCharge):
            raise Exception(f"Le modèle ({grid_manager.nb_lines(grille)}x{grid_manager.nb_columns(grille)}) est trop grand pour la grille ({lines.get()}x{columns.get()})")


    global fenetreJeu
    
    #création de la fenêtre de jeu
    fenetreJeu = Toplevel()
    fenetreJeu.title(mode)
    parametres={   
        "master": fenetreJeu,
        "grid": grille,
        "size_cell": size_cell.get(),
        "margin": margin.get(),
        "gutter": gutter.get(),
        "show_vals": True if show_vals.get() == "Oui" else False,
        "outline": couleurs[outline.get()],
    }
    #création du canvas dans la fenetre fenetreJeu avec les paramètres listés ci-dessus
    canvas = grid_tk.grid_canvas(**parametres)
    canvas.pack()

    #bouton pour sauvegarder un état initial dans un fichier
    global nomSaveFichier
    nomSaveFichier=StringVar()
    nomSaveFichier.set("Nom du fichier")
    Button(
        fenetreJeu,
        text="Sauvegarder l'état initial",
        name="sauvegarder",
        command=lambda: sauvegarder(grilleInitiale)
    ).pack(side=BOTTOM, pady=10)

    #champ accompagnant le bouton pour saisir un nom pour le fichier
    Entry(
        fenetreJeu,
        textvariable=nomSaveFichier,
    ).pack(side=BOTTOM)

    #bouton pour commencer l'évolution périodique si définie (d'où le "if")
    if delai.get() != 0:
        global boutonPause
        boutonPause=Button(
            fenetreJeu,
            text="Commencer l'évolution automatique",
            name="pause",
            command=lambda: (
                evolution(canvas, "pause"),
                boutonPause.config(text="Reprendre") if boutonPause.cget("text")=="Pause" else boutonPause.config(text="Pause")
            ),
        )
        boutonPause.pack(side=BOTTOM, pady=5)

    #bouton pour passer à la génération suivante qui sera crée dans tous les cas
    Button(
        fenetreJeu,
        text="Evoluer",
        name="evolution manuelle",
        command=lambda: evolution(canvas, "evoluer"),
    ).pack(side=BOTTOM, pady=5)

    #bouton retour
    Button(
        fenetreJeu,
        text="Fermer",
        command=lambda: (fenetreJeu.destroy(), nbGenerations:=0),
    ).pack(side=BOTTOM, pady=5)

    global repetition
    repetition=fenetreJeu.after(delai.get(), evolution, canvas, True)
    #after s'exécute lors de l'affectation donc on l'annule tout de suite pour ne pas avoir d'évolution dès le début
    fenetreJeu.after_cancel(repetition)

    fenetreJeu.mainloop()


def creerFenetreParametres(mode):
    global fenetreParametres, fenetreJeu, lines, columns, size_cell, margin, gutter, show_vals, outline, delai, nomLoadFichier

    fenetreParametres = Toplevel()

    fenetreParametres.title(str(mode))

    #variables contenant les valeurs des champs de saisie
    lines=IntVar(); columns=IntVar(); size_cell=IntVar(); margin=IntVar(); gutter=IntVar(); delai=IntVar()
    show_vals=StringVar(); outline=StringVar(); nomLoadFichier=StringVar()

    #valeurs par défaut
    lines.set(20)
    columns.set(20)
    size_cell.set(20)
    margin.set(10)
    gutter.set(0)
    show_vals.set("Non")
    outline.set("Noir")
    delai.set(500)

    #tous les widgets de saisie et leur Label
    
    Label(fenetreParametres, text="Nombre de lignes").grid(row=1, column=1, padx=10)
    Spinbox(fenetreParametres, name="lines", from_=1, to=1000, textvariable=lines).grid(
        row=2, column=1, padx=10, pady=10
    )

    Label(fenetreParametres, text="Nombre de colonnes").grid(row=1, column=2, padx=10)
    Spinbox(fenetreParametres, name="columns", from_=1, to=1000, textvariable=columns).grid(
        row=2, column=2, padx=10, pady=10
    )

    Label(fenetreParametres, text="Taille des cellules").grid(row=1, column=3, padx=10)
    Spinbox(fenetreParametres, name="size_cell", from_=1, to=100, textvariable=size_cell).grid(
        row=2, column=3, padx=10, pady=10
    )

    Label(fenetreParametres, text="Taille de la marge").grid(row=1, column=4, padx=10)
    Spinbox(fenetreParametres, name="margin", from_=0, to=100, textvariable=margin).grid(
        row=2, column=4, padx=10, pady=10
    )

    Label(fenetreParametres, text="Taille de la goutière").grid(row=3, column=1, padx=10)
    Spinbox(fenetreParametres, name="gutter", from_=0, to=100, textvariable=gutter).grid(
        row=4, column=1, padx=10, pady=10
    )

    Label(fenetreParametres, text="Afficher les valeurs").grid(row=3, column=2, padx=10)
    ttk.Combobox(fenetreParametres, name="show_vals", values=["Oui", "Non"], state="readonly", textvariable=show_vals).grid(
        row=4, column=2, padx=10, pady=10
    )

    Label(fenetreParametres, text="Couleur des bordures").grid(row=3, column=3, padx=10)
    ttk.Combobox(
        fenetreParametres,
        name="outline",
        values=listeCouleurs,
        state="readonly",
        textvariable=outline,
    ).grid(row=4, column=3, padx=10, pady=10)

    Label(fenetreParametres, text="Délai avant la génération suivante (en millisecondes)").grid(
        row=3, column=4, padx=10,
    )
    Spinbox(fenetreParametres, name="delai", from_=1, to=10000, textvariable=delai).grid(
        row=4, column=4, padx=10, pady=10,
    )

    if mode=="Modèles sauvegardés":
        Label(fenetreParametres, text="Choix du fichier à charger").grid(row=5, column=1, padx=10)
        ttk.Combobox(
            fenetreParametres,
            textvariable=nomLoadFichier,
            values=[i[0:-4] for i in os.listdir(os.path.dirname(__file__)+"/templates/") if i.endswith(".mdl")],
            state="readonly",
        ).grid(row=6, column=1, padx=10, pady=10)

    Button(
        fenetreParametres,
        text="Lancer",
        command=lambda: lancerPartie(fenetreParametres.title()),
    ).grid(row=5, column=4, padx=10, pady=10)

    Button(fenetreParametres, text="Retour", command=fenetreParametres.destroy).grid(
        row=6, column=4, padx=10, pady=10
    )
    
#menu principal
menu = Tk()

Button(
    menu,
    text="Nouvelle partie aléatoire",
    command=lambda: creerFenetreParametres("Nouvelle partie aléatoire"),
).grid(row=2, column=1, padx=10, pady=10)

Button(
    menu,
    text="Nouvelle partie vierge",
    command=lambda: creerFenetreParametres("Nouvelle partie vierge"),
).grid(row=3, column=1, padx=10, pady=10)

Button(
    menu,
    text="Nouvelle partie pleine",
    command=lambda: creerFenetreParametres("Nouvelle partie pleine"),
).grid(row=4, column=1, padx=10, pady=10)

Button(
    menu,
    text="Modèles sauvegardés",
    command=lambda: creerFenetreParametres("Modèles sauvegardés"),
).grid(row=5, column=1, padx=10, pady=10)

Button(menu, text="Fermer", command=menu.destroy).grid(row=6, column=1, padx=10, pady=20)
menu.mainloop()
