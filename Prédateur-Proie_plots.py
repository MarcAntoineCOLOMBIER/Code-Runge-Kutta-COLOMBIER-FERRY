# Importation des modules
import tkinter as tk
from tkinter import Canvas
import random as rd
import tkinter.font as tkFont
import matplotlib.pyplot as plt
import numpy as np
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
nb_lig =int(30*0.8)
nb_col = nb_lig

#==============================================================================
# Input Proie / Prédateurs :
frame = 0
nb_pred = int(150*0.8**2)
nb_proie = int(150*0.8**2)
liste_pred = []
liste_proie = []
liste_tot = []

reproduction_proie = 0.5   
reproduction_pred = 0.24
mortalite = 0.2   
chasse = 0.9  

# Initialisation de la liste de Proies
def init_liste_proie(nb_proies) :
    global liste_tot,liste_pred,liste_proie
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
def init_liste_pred(nb_pred):
    global liste_tot,liste_proie,liste_pred
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

init_liste_proie(nb_proie) 
init_liste_pred(nb_proie) 
#==============================================================================
# Place les prédateurs sur la grille
for pred in liste_pred:
    coord = pred.coord
    
# Place les proies sur la grille
for proie in liste_proie:
    coord = proie.coord

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

demographie_pred = [nb_pred]
demographie_proie = [nb_proie]
liste_frame = []
liste_demographie_pred = []
liste_demographie_proie = []

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
        if indice_proie != -1 :   # S'il y a une Proie dans les parrages :
            tirage = rd.random()
            if tirage < pred.chasse :  # Si le prédateur tue la Proie :
                coord_proie = liste_proie[indice_proie].coord        
                if pred.reproduction < 0.8 :
                    pred.reproduction **=1/3
                del(liste_proie[indice_proie])     # On la retire de la liste des Proies
                # MODIFICATION DES PARAMETRES DU PREDATEUR QUI VIENT DE MANGER ?
            elif pred.reproduction > 0.1 :
                pred.reproduction **=3
        elif pred.reproduction > 0.1:
            pred.reproduction **=3
        # Déplacement du Prédateur :
        nv_coord = nv_coord_voisine((x,y),liste_proie+liste_pred)
        if nv_coord != -1 :
            pred.coord = nv_coord
        # Reproduction des Prédateurs restants :
        tirage = rd.random()
        if tirage < pred.reproduction:
            nv_coord = nv_coord_voisine((x,y), liste_pred+liste_proie+liste_pred_add)
            if nv_coord != -1 :
                liste_pred_add.append(Predateur(nv_coord, reproduction_pred, mortalite, chasse))
    for k in liste_pred_morts :
        (x,y) = liste_pred[k].coord
        del(liste_pred[k])   # On le retire de la liste des Prédateurs
        for i in range(len(liste_pred_morts)) :
            liste_pred_morts[i] -= 1    # On modifie la position des prédateurs morts car on a enlevé un élément antérieur
    # Mise à jour des Liste_pred et compteur Prédateurs
    liste_pred = liste_pred + liste_pred_add
    nb_pred_f = len(liste_pred)
    
    # On s'intéresse ensuite aux Proies:
    for k in range(len(liste_proie)):  
        proie = liste_proie[k]
        (x,y) = proie.coord
        # Déplacement de la Proie :
        nv_coord = nv_coord_voisine((x,y),liste_proie+liste_pred)
        if nv_coord != -1 :
            proie.coord = nv_coord
        # Reproduction des Proies restantes:
        tirage = rd.random()
        if tirage < proie.reproduction :  # Si la Proie peut se reproduire :
            nv_coord = nv_coord_voisine((x,y),liste_proie+liste_pred)
            if nv_coord != -1 :      
                liste_proie_add.append(Proie(nv_coord,reproduction_proie))  
    # Mise à jour des Liste_proie et compteur Proies
    liste_proie = liste_proie + liste_proie_add
    nb_proie_f = len(liste_proie)
    # On s'occupe de la courbe d'évolution des individus :
    demographie_pred.append(nb_pred_f)
    demographie_proie.append(nb_proie_f)

# Fonction pour faire la moyenne des éléments d'une colonne spécifique
def liste_moyenne(matrice): #matrice est une liste de listes de même taille
    matrice = np.array(matrice)
    moyenne = []
    # Transposition de la matrice pour obtenir les colonnes
    matrice = np.transpose(matrice)
    for colonne in matrice:
        # moyenne des éléments de la colonne
        moyenne.append(np.mean(colonne))
    return moyenne #Renvoie la liste moyenne

n_sample = 40
n_frame_max = 500
for i in range(n_sample):
    while frame<n_frame_max: #and len(liste_pred)>0 and len(liste_pred)>0 ?
        evolution()
    liste_demographie_proie.append(demographie_proie)
    liste_demographie_pred.append(demographie_pred)
    liste_frame.append([i for i in range(len(demographie_pred))])
    #Réinitialisation des listes
    demographie_proie = [nb_proie]
    demographie_pred = [nb_pred]
    liste_proie = []
    liste_pred = []
    liste_tot = []
    init_liste_proie(nb_proie)
    init_liste_pred(nb_pred)
    frame = 0
    
demographie_proie_moyenne = liste_moyenne(liste_demographie_proie)
demographie_pred_moyenne = liste_moyenne(liste_demographie_pred)

plt.plot(liste_frame[0],demographie_proie_moyenne,label='Proie',color='cyan')
plt.plot(liste_frame[0],demographie_pred_moyenne,label='Prédateur',color='red')
plt.legend()
plt.xlabel('Temps')
plt.ylabel('Démographie')
plt.show()