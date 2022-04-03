# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 17:02:24 2021

@author: taiga
"""

import numpy as np
import time

def init_voisin():
    for i in range(2,taille+2): # Prend en compte le décalage dû à la bande interdite
        for j in range(2,taille+2):
            nbVoisinsLibres = 0 # Nombre de voisins libres pour la case(i,j)
            for k in range(8): # Vérifie l'accessibilité de chaque case voisine de (i,j)
                NX = i + tabDeltaXY[k][0]
                NY = j + tabDeltaXY[k][1]
                if prometteur(NX,NY) : 
                    nbVoisinsLibres += 1 # la case (NX,NY) est accessible depuis (i,j) et prometteur (i.e. non visitée), donc c'est un voisin libre
            echiquierVoisins[i,j] = nbVoisinsLibres # affecte le nombre de voisins libres de la case(i,j)
            
def trouverMeilleurVoisinsLibres(case):
    vecteurMeilleursVoisins = [] # Liste contenant tous les voisins de la case étudiée, dans l'ordre croissant de leur nombre de voisin libre
    
    def trouverLePremierVoisinDeDegreMinimalLibre(case):
        """Cherche le plus petit nombre de voisins libres parmi les voisins de la case étudiée"""
        X,Y = case[0], case[1]
        min_k = 9 # Valeur renvoyée par la fonction par défaut plus grande que 8 (max voisins)
        for k in range(8): # Parcours tous les voisins de la case étudiée
            Nx,Ny = X+tabDeltaXY[k][0], Y+tabDeltaXY[k][1]
            if not prometteur(Nx, Ny) : continue
        
            if min_k > echiquierVoisins[Nx,Ny] :
                min_k = echiquierVoisins[Nx,Ny] # Actualise le nombre minimal de voisins libres
        return min_k

    def trouverTousLesMeilleursVoisins(case, min_k):
        """Renvoie la liste de tout les voisins ayant le minimum de voisin libre (minimum connu grâce à la fonction trouverLePremierVoisinDeDegreMinimalLibre"""
        X,Y = case[0],case[1]
        for z in range(8): # Parcours tous les voisins de la case étudiée
            Nx, Ny = X+tabDeltaXY[z][0], Y+tabDeltaXY[z][1]
            if not prometteur(Nx,Ny) : continue
            if min_k == echiquierVoisins[Nx,Ny]:
                vecteurMeilleursVoisins.append((Nx,Ny)) # Ajoute le voisin si son nombre de voisins libres est minimal
        return vecteurMeilleursVoisins
    
    min_k = trouverLePremierVoisinDeDegreMinimalLibre(case)
    if min_k >= 0:
        vecteurMeilleursVoisins = trouverTousLesMeilleursVoisins(case, min_k)
    return vecteurMeilleursVoisins

def miseAJourVoisins(case):
    """La case étudiée est choisie, ses voisins ne doivent donc plus la considérer libre"""
    X,Y = case[0], case[1]
    for z in range(8): # Parcours tous les voisins de la case étudiée
        Nx,Ny = X + tabDeltaXY[z][0], Y+tabDeltaXY[z][1]
        if not prometteur(Nx, Ny) : continue
        if echiquierVoisins[Nx,Ny] > 0 : echiquierVoisins[Nx,Ny] -= 1 # Enlève un voisin libre
        
def remiseAJourVoisins(case):
    """La case étudiée n'est plus choisie (retour en arrière), ses voisins doivent donc la reconsidérer libre"""
    X,Y = case[0],case[1]
    for z in range(8): # Parcours tous les voisins de la case étudiée
        Nx,Ny = X + tabDeltaXY[z][0], Y+tabDeltaXY[z][1]
        if not prometteur(Nx, Ny) : continue
        echiquierVoisins[Nx,Ny] += 1 # Rajoute un voisin libre
    

def AES_parcours_cavalier_un_succes_suffit(derniere_case_traitee, prochain_numero):
    if prochain_numero > taille**2:
        return True # Toutes les cases (au nombre de taille**2) ont été visitées
    else:
        x,y = derniere_case_traitee
        for caseChoisie in trouverMeilleurVoisinsLibres(derniere_case_traitee): # Parcours seulement les cases possédant le plus petit nombre de voisins
            miseAJourVoisins(caseChoisie) # La case choisie n'est plus considérée comme libre du point de vue de ses voisins
            nextX,nextY = caseChoisie[0],caseChoisie[1]
            compteurs["compteurTentative"] = compteurs["compteurTentative"]+1 # Tente de résoudre le problème en déplaçant le cavalier à la case (nextX,nextY)
            echiquierBandes[nextX, nextY] = prochain_numero
            if AES_parcours_cavalier_un_succes_suffit((nextX, nextY), prochain_numero+1):
                return True # Récursivité pour vérifier si toutes les cases non encore visitées sont accessibles en partant de (nextX,nextY)
            compteurs["compteurRetourArriere"] = compteurs["compteurRetourArriere"]+1 # On retourne en arrière pour tenter un autre déplacement
            remiseAJourVoisins(caseChoisie) # La case qui était choisie redevient libre du point de vue de ses voisins
            echiquierBandes[nextX, nextY] = -1
        return False # Retourne False si aucun deplacement n'aboutit a la resolustion du probleme
    
def prometteur(newX, newY):
    return echiquierBandes[newX, newY] == -1

if __name__ == '__main__':
    while(True):
        try:
            taille = int(input("Donnez la taille de l'échiquier (>4): "))
            if taille>4:
                break
        except:
            continue
    tabDeltaXY=[[1,2], [1,-2], [-1,2], [-1,-2], [2,1], [2,-1], [-2,1], [-2,-1]] # Ensemble des déplacements que le cavalier peut réaliser
    echiquierBandes = np.matrix([-1 for i in range((taille+4)**2)]).reshape(taille+4,taille+4) # Matrice de (taille+4)*(taille+4) correspondant à l'échiquier entouré de deux bandes non accessibles par le cavalier
    for i in range(taille+4) :
        for j in range(taille+4) :
            if i<2 or j<2 or i>=taille+2 or j>=taille+2 :
                echiquierBandes[i,j] = taille**2+1 # Affectation d'un numéro >taille**2 dans la bande interdite pour rendre son accès impossible (grâce à la fonction prometteur(case))
                
    echiquierVoisins = np.matrix([9 for i in range((taille+4)**2)]).reshape(taille+4,taille+4) # Matrice de taille identique à la précédente, indiquant le nombre de voisins non visitées de chaque case. La valeur par défaut est 9 (soit plus que la maximum de voisins) pour distinguer les cases non accessibles (bande interdite)
    init_voisin() # Calcul le nombre de voisins dans chaque cases de l'échiquier (ne modifie pas la bande interdite)
    
    while(True): #Choix de la position de départ
        try:
            x0 = int(input("Entrez x0 (Ligne de la case de départ): "))
            y0 = int(input("Entrez y0 (Colonne de la case de départ): "))
            if 0<=x0<taille and 0<=y0<taille:
                break
        except:
            continue
    x0 += 2 # Ajuste le numéro de la case car les 2 premières lignes et colonnes de echiquierBandes correspondent à la bande interdite
    y0 += 2
    echiquierBandes[x0,y0] = 1 # La case de départ est la première case visitée
    prochain_numero = 2 # Numéro qui sera attribuée à la prochaine case visitée
    
    compteurs = {"compteurTentative":0, "compteurRetourArriere":0}
    
    start = time.time()
    if AES_parcours_cavalier_un_succes_suffit((x0, y0), prochain_numero):
        echiquier = echiquierBandes[2:taille+2,2:taille+2] # Création d'un échiquier sans les bandes pour améliorer la lisibilité 742
        print('\n \n')
        print(echiquierBandes)
        print('\n \n')
        print(echiquier)
    else:
        print("Echec")
    print('\n')
    print(compteurs)
    end = time.time()
    print("Temps écoulé : "+str(end-start)+" s")