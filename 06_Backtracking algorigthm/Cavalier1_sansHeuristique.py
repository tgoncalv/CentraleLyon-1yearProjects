# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 14:45:12 2021

@author: taiga
"""

import numpy as np
import time


def AES_parcours_cavalier_un_succes_suffit(derniere_case_traitee, prochain_numero):
    if prochain_numero > taille**2:
        return True # Toutes les cases (au nombre de taille**2) ont été visitées
    else:
        x,y = derniere_case_traitee
        for i in range(8): # Etude de tous les déplacements possibles
            nextX = x + tabDeltaXY[i][0]
            nextY = y + tabDeltaXY[i][1]
            if prometteur(nextX,nextY):
                compteurs["compteurTentative"] += 1 # Tente de résoudre le problème en déplaçant le cavalier à la case (nextX,nextY)
                echiquier[nextX, nextY] = prochain_numero
                if AES_parcours_cavalier_un_succes_suffit((nextX, nextY), prochain_numero+1):
                    return True # Récursivité pour vérifier si toutes les cases non encore visitées sont accessibles en partant de (nextX,nextY)
                compteurs["compteurRetourArriere"] += 1 # On retourne en arrière pour tenter un autre déplacement
                echiquier[nextX, nextY] = -1
        return False # Retourne False si aucun deplacement n'aboutit a la resolustion du probleme


def prometteur(newX, newY):
    # Vérifie si la case choisie est dans l'échiquier et est non visitée
    return 0 <= newX < taille and 0<= newY < taille and echiquier[newX, newY] == -1

if __name__ == '__main__':
    while(True):
        try:
            taille = int(input("Donnez la taille de l'échiquier (>4): "))
            if taille>4:
                break
        except:
            continue
        
    tabDeltaXY=[[1,2], [1,-2], [-1,2], [-1,-2], [2,1], [2,-1], [-2,1], [-2,-1]] # Ensemble des déplacements que le cavalier peut réaliser
    echiquier = np.matrix([-1 for i in range(taille**2)]).reshape(taille,taille) # Matrice de taille*taille correspondant à l'échiquier, les cases -1 sont les cases non encore visitées
    
    while(True): #Choix de la position de départ
        try:
            x0 = int(input("Entrez x0 (Ligne de la case de départ): "))
            y0 = int(input("Entrez y0 (Colonne de la case de départ): "))
            if 0<=x0<taille and 0<=y0<taille:
                break
        except:
            continue
    echiquier[x0,y0] = 1 # La case de départ est la première case visitée
    prochain_numero = 2 # Numéro qui sera attribuée à la prochaine case visitée
    
    compteurs = {"compteurTentative":0, "compteurRetourArriere":0}
    
    start = time.time()
    if AES_parcours_cavalier_un_succes_suffit((x0, y0), prochain_numero):
        print('\n \n')
        print(echiquier)
    else:
        print("Echec")
    print('\n')
    print(compteurs)
    end = time.time()
    print("Temps écoulé : "+str(end-start)+" s")
    