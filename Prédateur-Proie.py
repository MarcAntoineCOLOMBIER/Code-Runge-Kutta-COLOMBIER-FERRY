# Importation des modules
import tkinter as tk
from tkinter import Canvas
import random as rd
import tkinter.font as tkFont

#==============================================================================
# Classes :
class Proie :    
    def __init__(self, coord, reproduction):
        self.coord = coord   # coord = (x,y) de la Proie
        self.reproduction = reproduction    # Taux de reproduction α intrisèque de la Proie 
                        

class Predateur :    
    def __init__(self, coord, reproduction, mortalite, chasse):
        self.coord = coord   # coord = (x,y) du Prédateur
        self.reproduction = reproduction    # Taux de reproduction du Prédateur δ en fonction de leur faim
        self.mortalite = mortalite   # Taux de mortalité γ intrinsèque du Prédateur
        self.chasse = chasse    # Probabilité β de tuer une Proie située à proximité 
        
#==============================================================================
# Input Fenêtre :
taille_case = 20
nb_lig =30
nb_col = nb_lig
gap = 2
couleur_fond = 'antiquewhite'
couleur_pred = 'red'
couleur_proie = 'cyan'

height = nb_lig * taille_case + gap
width = nb_col * taille_case + gap

fen = tk.Tk()
fen.title("Modèle Prédateur Proie")
fen.resizable(width=True, height=True)
cnv = Canvas(fen, width = width, height = height, bg = couleur_fond)
cnv.pack(side="left")

# Fonctions pour la Grille:
def grille(width, height):
    x1 = gap
    y1 = gap
    x2 = width
    y2 = gap
    cnv.pack(padx=50, pady=50)
    for i in range(nb_lig+1):
        cnv.create_line((x1,y1+i*taille_case),(x2,y2+i*taille_case),fill='black', width = 1)
    x2 = gap
    y2 = height
    for j in range(nb_col+1):
        cnv.create_line((x1+j*taille_case,y1),(x2+j*taille_case,y2),fill='black', width = 1)

def carre(coord,taille, couleur):
    (x,y) = coord
    x = gap + x*taille
    y = gap + y*taille
    cnv.create_rectangle((x,y),(x+taille,y+taille), fill=couleur, outline='black')
    
#==============================================================================
# Input Proie / Prédateurs :
frame = 0
nb_pred = 150
nb_proie = 150
liste_pred = []
liste_proie = []
liste_tot = []

reproduction_proie = 0.5
reproduction_pred = 0.24
mortalite = 0.2
chasse = 0.9

# Initialisation de la liste de Proies
for i in range(nb_proie):
    x = rd.randint(0,nb_col-1)
    y = rd.randint(0,nb_lig-1)
    coord = (x,y)
    while coord in liste_tot :
        x = rd.randint(0,nb_col-1)
        y = rd.randint(0,nb_lig-1)
        coord = (x,y)
    liste_proie.append(Proie(coord, reproduction_proie))
    liste_tot.append(coord)


# Initialisation de la liste de Prédateurs
for i in range(nb_pred):
    x = rd.randint(0,nb_col-1)
    y = rd.randint(0,nb_lig-1)
    coord = (x,y)
    while coord in liste_tot :
        x = rd.randint(0,nb_col-1)
        y = rd.randint(0,nb_lig-1)
        coord = (x,y) 
    liste_pred.append(Predateur(coord, reproduction_pred, mortalite, chasse))
    liste_tot.append(coord)
#==============================================================================
# Création de la grille
grille(width, height)   

# Place les prédateurs sur la grille
for pred in liste_pred:
    coord = pred.coord
    carre(coord,taille_case,couleur_pred)
    
# Place les proies sur la grille
for proie in liste_proie:
    coord = proie.coord
    carre(coord,taille_case,couleur_proie)

# Cherche une coordonnée dans une liste et renvoie son emplacement dans la liste (-1 sinon)
def cherche_indiv(coordonnee, liste):
    for indice in range (len(liste)) :
        indiv = liste[indice]
        if indiv.coord == coordonnee:
            return indice
    return -1
    
#Renvoie les coordonnées d'une case aléatoire parmi les 8 adjacentes --- CONDITIONS AUX LIMITES FIXES ---
# def case_aleatoire_voisine(coordonnee):
#     (x,y) = coordonnee    #x varie de 0 à nb_col-1   y varie de 0 à nb_lig-1
#     delta_x = rd.randint(-1,1)
#     delta_y = rd.randint(-1,1)
#     if x == 0 :
#         delta_x = rd.randint(0,1)
#     if x == nb_col-1 :
#         delta_x = rd.randint(-1,0)
#     if y == 0 :
#         delta_y = rd.randint(0,1)
#     if  y == nb_lig-1:
#         delta_y = rd.randint(-1,0)
#     nv_coord = (x+delta_x, y+delta_y)
#     return nv_coord

#Renvoie les coordonnées d'une case aléatoire parmi les 8 adjacentes --- CONDITIONS AUX LIMITES PERIODIQUES ---
def case_aleatoire_voisine(coordonnee):
    (x,y) = coordonnee    #x varie de 0 à nb_col-1   y varie de 0 à nb_lig-1
    delta_x = rd.randint(-1,1)
    delta_y = rd.randint(-1,1)
    (nv_x, nv_y) = (x+delta_x, y+delta_y)
    if nv_x == -1 :
        nv_x = nb_col-1
    if nv_x == nb_col :
        nv_x = 0
    if nv_y == -1 :
        nv_y = nb_lig-1
    if nv_y == nb_lig :
        nv_y = 0
    nv_coord = (nv_x, nv_y)
    return nv_coord
    
# Cherche un individu appartenant à liste dans les 8 cases voisines à (x,y) et renvoie l'indice de celui-ci (-1 sinon)
def cherche_indiv_voisin(coord, liste):   
    (x,y) = coord
    coord_voisin = coord
    for i in range(-1,2):
        for j in range(-1,2):
            if (i,j) != (0,0):
                coord_voisin = (x+i,y+j)
                indice_voisin = cherche_indiv(coord_voisin, liste)
                if indice_voisin != -1 :
                    return indice_voisin
    return -1


#Renvoie les coordonnées d'une case voisine non occupée (-1 sinon)
def nv_coord_voisine(coordonnee, liste):
    nv_coord = case_aleatoire_voisine(coordonnee)
    indice = cherche_indiv(nv_coord, liste)
    deja_vu = [nv_coord]
    while (indice != -1) & (len(deja_vu) < 8) : #Tant que la case est déjà occupée et qu'on n'a pas essayé les 8 cases voisines, réessayer
        nv_coord = case_aleatoire_voisine(coordonnee)
        while nv_coord in deja_vu :
            nv_coord = case_aleatoire_voisine(coordonnee)
        deja_vu.append(nv_coord)
        indice = cherche_indiv(nv_coord, liste)
    if len(deja_vu) < 8:
        return nv_coord
    return -1


#Dicte les règles pour l'évolution des individus
def evolution():
    global liste_pred, liste_proie, frame

    frame += 1
    liste_pred_add = []
    liste_proie_add = []
    liste_pred_morts = []
    nb_pred_i = len(liste_pred)
    nb_proie_i = len(liste_proie)
    for k in range(nb_pred_i):
        # On s'intéresse d'abord aux Prédateurs :
        pred = liste_pred[k]
        (x,y) = pred.coord
        # Mort du Prédateur :
        tirage = rd.random()
        if tirage < pred.mortalite :  # Si le Prédateur meurt :
            liste_pred_morts.append(k)
            continue
        # Recherche de Proie :
        indice_proie = cherche_indiv_voisin((x,y),liste_proie) # Recherche s'il y a une Proie aux alentours
        #print('indice proie :', indice_proie)
        if indice_proie != -1 :   # S'il y a une Proie dans les parrages :
            tirage = rd.random()
            if tirage < pred.chasse :  # Si le prédateur tue la Proie :
                coord_proie = liste_proie[indice_proie].coord        
                if pred.reproduction < 0.8 :
                    pred.reproduction **=1/3
                del(liste_proie[indice_proie])     # On la retire de la liste des Proies
                carre(coord_proie,taille_case, couleur_fond)       # On retire la Proie mangée de sa position
                # MODIFICATION DES PARAMETRES DU PREDATEUR QUI VIENT DE MANGER ?
            elif pred.reproduction > 0.1 :
                pred.reproduction **=3
        elif pred.reproduction > 0.1:
            pred.reproduction **=3
        # Déplacement du Prédateur :
        nv_coord = nv_coord_voisine((x,y),liste_proie+liste_pred)
        if nv_coord != -1 :
            pred.coord = nv_coord
            carre((x,y),taille_case, couleur_fond)       # On retire le Prédateur de sa position
            carre(nv_coord,taille_case, couleur_pred)    # On le place à sa nouvelle position
        # Reproduction des Prédateurs restants :
        tirage = rd.random()
        if tirage < pred.reproduction:
            nv_coord = nv_coord_voisine((x,y), liste_pred+liste_proie+liste_pred_add)
            if nv_coord != -1 :
                liste_pred_add.append(Predateur(nv_coord, reproduction_pred, mortalite, chasse))
                carre(nv_coord,taille_case, couleur_pred)    # On le place à sa nouvelle position
    for k in liste_pred_morts :
        (x,y) = liste_pred[k].coord
        del(liste_pred[k])   # On le retire de la liste des Prédateurs
        for i in range(len(liste_pred_morts)) :
            liste_pred_morts[i] -= 1    # On modifie la position des prédateurs morts car on a enlevé un élément antérieur
        carre((x,y),taille_case, couleur_fond)       # On retire le Prédateur de sa position
    # Mise à jour des Liste_pred et compteur Prédateurs
    liste_pred = liste_pred + liste_pred_add
    nb_pred_f = len(liste_pred)
    compte_pred.configure(text = nb_pred_f)
    
    # On s'intéresse ensuite aux Proies:
    for k in range(len(liste_proie)):  
        proie = liste_proie[k]
        (x,y) = proie.coord
        # Déplacement de la Proie :
        nv_coord = nv_coord_voisine((x,y),liste_proie+liste_pred)
        if nv_coord != -1 :
            proie.coord = nv_coord
            carre((x,y),taille_case, couleur_fond)       # On retire la Proie de sa position
            carre(nv_coord,taille_case, couleur_proie)    # On la place à sa nouvelle position
        # Reproduction des Proies restantes:
        tirage = rd.random()
        if tirage < proie.reproduction :  # Si la Proie peut se reproduire :
            nv_coord = nv_coord_voisine((x,y),liste_proie+liste_pred)
            if nv_coord != -1 :      
                liste_proie_add.append(Proie(nv_coord,reproduction_proie))  
                carre(nv_coord,taille_case, couleur_proie)    # On le place à sa nouvelle position
    # Mise à jour des Liste_proie et compteur Proies
    liste_proie = liste_proie + liste_proie_add
    nb_proie_f = len(liste_proie)
    compte_proie.configure(text = nb_proie_f)
    
    # Mise à jour du compteur de Frames
    compte_frame.configure(text = frame)
    
    # On s'occupe de la courbe d'évolution des individus :
    demographie_pred(nb_pred_i, nb_pred_f, frame)
    demographie_proie(nb_proie_i, nb_proie_f, frame)
    
        
        
        
    

# Frame à  droie de la grille de jeu pour les compteurs
f1 = tk.Frame(fen)
# Champ pour l'affichage du décompte des Prédateurs
texte_pred = tk.Label (f1, text = "Nombre de Prédateurs :")
compte_pred = tk.Label (f1, text = len(liste_pred))
texte_pred.grid(row=4,column=1,sticky='NE')
compte_pred.grid(row=4,column=2,sticky='NW')
# Champ pour l'affichage du décompte des Proies
texte_proie = tk.Label (f1, text = "Nombre de Proies :")
compte_proie = tk.Label (f1, text = len(liste_proie))
texte_proie.grid(row=5,column=1,sticky='NW')
compte_proie.grid(row=5,column=2,sticky='NE')
f1.pack()
# Champ pour l'affichage du décompte des frames
texte_frame = tk.Label (f1, text = "Frame :")
compte_frame = tk.Label (f1, text = frame)
texte_frame.grid(row=6,column=1,sticky='NW')
compte_frame.grid(row=6,column=2,sticky='NW')

# Frame en bas de la grille pour disposer le bouton "Evolution"
f2 = tk.Frame(fen)
bou1 = tk.Button(f2, width=14, text="Evolution", font="Arial 10", command=evolution)
bou1.pack(side="bottom", padx=5, pady=5)
f2.pack(side="bottom")

# =============================================================================
# =============================================================================
# Frame à droite de la grille pour les courbes d'évolution des populations
f3 = tk.Frame(fen)
height1 = height* 0.8
width1 = width
cnv1 = Canvas(fen, width = width1, height = height1, bg = 'white')
cnv1.pack(side="left")
# Créer les bords du Canva :
cnv1.create_line((5,5),(5,height1),fill='grey', width = 1)
cnv1.create_line((5,height1),(width1,height1),fill='grey', width = 1)
cnv1.create_line((width1,height1),(width1,5),fill='grey', width = 1)
cnv1.create_line((width1,5),(5,5),fill='grey', width = 1)


# Axe y (Nombre d'individus)
gap1 = 20
(x0, y0) = (gap1, height1-gap1)  # Origine = (gap1,height1-gap1)
taille_fleche = gap1/4
cnv1.create_line((x0,gap1),(x0,y0),fill='black', width = 1.5)  # Axe y
cnv1.create_line((gap1,gap1),(gap1+taille_fleche,gap1+taille_fleche),fill='black', width = 1.5) #Flèche y
cnv1.create_line((gap1,gap1),(gap1-taille_fleche,gap1+taille_fleche),fill='black', width = 1.5) #Flèche y
cnv1.create_text(gap1+1.4*gap1, gap1-gap1/2.5, text ='Démographie', font=tkFont.Font(family="Arial", size=7))  # Titre axe y

# Axe x (Nombre de frames)
intervalle_frame = 0.7
cnv1.create_line((x0,y0),(width-gap1,y0),fill='black', width = 1.5)  # Axe x
cnv1.create_line((width-gap1,height1-gap1),(width-gap1-taille_fleche,height1-gap1-taille_fleche),fill='black', width = 1.5)  #Flèche x
cnv1.create_line((width-gap1,height1-gap1),(width-gap1-taille_fleche,height1-gap1+taille_fleche),fill='black', width = 1.5) #Flèche x
cnv1.create_text(width-gap1-gap1/2,height1-gap1+gap1/2, text ='Temps', font=tkFont.Font(family="Arial", size=7))  # Titre axe x

intervalle_indiv = 0.5

def demographie_pred(nb_pred_i, nb_pred_f, frame) :
    global x0, y0, intervalle_indiv, intervalle_frame
    cnv1.create_line((x0+(frame-1)*intervalle_frame,y0-nb_pred_i*intervalle_indiv), (x0+frame*intervalle_frame,y0-nb_pred_f*intervalle_indiv),fill='red', width = 1.5)

def demographie_proie(nb_proie_i, nb_proie_f, frame) :
    global x0, y0, intervalle_indiv, intervalle_frame
    cnv1.create_line((x0+(frame-1)*intervalle_frame,y0-nb_proie_i*intervalle_indiv), (x0+frame*intervalle_frame,y0-nb_proie_f*intervalle_indiv),fill='cyan', width = 1.5)

fen.mainloop()