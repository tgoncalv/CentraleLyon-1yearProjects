# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:27:19 2021

@author: taiga
"""

import numpy as np
import time
import random
import math

class Labyrinthe:
    

    def __init__(self, taille, num_case_debut=None, num_case_fin=None):
        self.__taille = taille
        if num_case_debut != None:
            assert (0 <= num_case_debut < taille * taille)
        if num_case_fin != None:
            assert (0 <= num_case_fin < taille * taille)
        self.__num_case_debut = num_case_debut  # un No case, pas (L,C)
        self.__num_case_fin = num_case_fin
        self.__matrice = []
        self.__voisins = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        self.__matriceDesNumeros = []
        # print('Init : labyrinth créé')

    # -----------------------------------
    def remplir(self, nb_murs):
        # Tirage aléatoire de k  '1' (mur)
        assert (nb_murs > 0 and nb_murs < self.__taille * self.__taille)
        # On met des 0 partout d'abord
        for i in range(0, self.__taille):
            lig = [-1 for i in range(self.__taille)]
            self.__matrice.append(lig)
        for i in range(0, self.__taille):
            lig = [math.inf for i in range(self.__taille)] 
            self.__matriceDesNumeros.append(lig)

        # On met qq murs
        for i in range(nb_murs):
            case = random.randint(0, self.__taille * self.__taille - 1)
            ligne = case // self.__taille
            col = case % self.__taille
            self.__matrice[ligne][col] = 1
            self.__matriceDesNumeros[ligne][col] = 1

        # Fixer les cases début et num_case_fin (peuvent être données
        N = self.__taille  # Pour simplifier les écritures
        num_case_debut = self.__num_case_debut;
        num_case_fin = self.__num_case_fin
        if num_case_debut not in range(N * N) and num_case_fin not in range(N * N):
            # Si non définis, mettre début (2) et cible (3) sur le contour extérieur
            Top_bande = list(range(N))  # [0.. taille]
            Bottom_bande = list(range(N * N - N, N * N))
            Left_bande = list(range(0, N * N, N))
            Right_bande = list(range(N - 1, N * N, N))
            # cases_contour=Top_bande+Bottom_bande+Left_bande+Right_bande
            # taille_controur=len(cases_contour)
            Les_4_listes = [Top_bande, Bottom_bande, Left_bande, Right_bande]
            # Tirage du début : on choisit l'un de ces 4 liste de contours pour y mettre le début
            quelle_liste_debut = random.randint(0, 3)  # On a 4 listes de contours 0..3
            # On sait que chaucun des 4 listes est de taille N  : len(Les_4_listes[quelle_liste])=N
            num_case_debut = Les_4_listes[quelle_liste_debut][random.randint(0, N - 1)]
            # Tirage de num_case_fin != num_case_debut
            quelle_liste_fin = random.randint(0, 3)

            # Moi : il se peut que debut=Fin car les 4 contours ont 4 cases en commun. Il arrive
            # Que debut=(0,0) dans la bande haute et num_case_fin = la mm chose dans la bande gauche !
            while True:
                while quelle_liste_debut == quelle_liste_fin:
                    quelle_liste_fin = random.randint(0, 3)
                num_case_fin = Les_4_listes[quelle_liste_fin][random.randint(0, N - 1)]
                if num_case_fin != num_case_debut: break

            self.__num_case_debut = num_case_debut
            self.__num_case_fin = num_case_fin
            # if self.__num_case_debut not in range(N*N-1) : print("Pb num_case_debut = ", self.__num_case_debut)
        # On écrite 'début' et 'num_case_fin'
        ligne = num_case_debut // N
        col = num_case_debut % N
        self.__matrice[ligne][col] = 2
        self.__matriceDesNumeros[ligne][col] = 2
        ligne = num_case_fin // N
        col = num_case_fin % N
        self.__matrice[ligne][col] = 3
        self.__matriceDesNumeros[ligne][col] = 3

        
    def getStartCase(self):
        """Permet d'obtenir le numéro de la ligne et de la colonne de la case de départ, sous le forme d'un tuple"""
        N = self.__taille
        num_case_debut = self.__num_case_debut
        ligne = num_case_debut // N
        col = num_case_debut % N
        return (ligne,col)
        
    def show(self):
        """"Affiche le labyrinthe ainsi que la matrice des numéros, sous la forme de tableau de la forme taille*taille"""
        print(np.matrix(self.__matrice).reshape(self.__taille,self.__taille))
        print("\n")
        print(np.matrix(self.__matriceDesNumeros).reshape(self.__taille,self.__taille))
        
    def AES_un_chemin(self,derniereCaseTraitee):
        """"Algorithme permettant d'obtenir un chemin possible pour arriver jusqu'à la case d'arrivée"""
        x,y = derniereCaseTraitee
        if self.__matrice[x][y] == 3:
            return True # Le point d'arrivé a été atteint
        else:
            for caseChoisie in self.__voisins: # Essaye tout les déplacements possibles
                nextX,nextY = x+caseChoisie[0],y+caseChoisie[1] # Ligne et colonne de la nouvelle case
                if self.prometteur(nextX,nextY): #Vérifie que la case n'est pas un mur ou dans la bordure du labyrinthe
                    if self.__matrice[nextX][nextY] == 3:
                        return True # Le point d'arrivé a été atteint
                    if self.__matrice[nextX][nextY] == -1: # Le point d'arrivé n'est pas atteint, on met donc un "4" sur la nouvelle case
                        self.__matrice[nextX][nextY] = 4
                        compteurs["compteurTentative"] = compteurs["compteurTentative"]+1 # Tente de résoudre le problème en déplaçant le personnage à la case (nextX,nextY)
                        if self.AES_un_chemin((nextX, nextY)):
                            return True # Récursivité pour atteindre le point d'arrivé
                        compteurs["compteurRetourArriere"] = compteurs["compteurRetourArriere"]+1 # On retourne en arrière pour tenter un autre déplacement
                        self.__matrice[nextX][nextY] = -1
            return False # Retourne False si aucun deplacement n'aboutit a la resolustion du probleme
        
    def prometteur(self, newX, newY):
        return  0 <= newX < self.__taille and 0<= newY < self.__taille and self.__matrice[newX][newY] != 1
    
    def numerotationDesCases(self, noeudCourrant):
        """"Complète de la matrice des numéros"""
        x,y = noeudCourrant
        if self.__matrice[x][y] == 3:
            return
        else:
            if self.__matrice[x][y] != 2:
                # Le numéro de la case actuelle (>=100)
                numeroDeCetteCase = self.__matriceDesNumeros[x][y]
            else:
                # Si la case actuelle est 2, il faut initialiser ses cases voisines à 100
                numeroDeCetteCase = 99;
            for caseChoisie in self.__voisins: # Essaye tout les déplacements
                nextX,nextY = x+caseChoisie[0],y+caseChoisie[1] # Nouvelle case
                if self.prometteur(nextX,nextY): # Vérifie que la nouvelle case n'est ni un mur ni à l'extérieur du labyrinthe
                    if self.__matrice[nextX][nextY] == 3 or self.__matrice[nextX][nextY] == 2:
                        # Vérifie que la case n'est ni le point de départ ni le point d'arrivée
                        continue
                    if self.__matriceDesNumeros[nextX][nextY] <= numeroDeCetteCase:
                        # Evite de faire une récursion sans améliorer les numéros déjà affectés
                        continue
                    self.__matriceDesNumeros[nextX][nextY] = min(self.__matriceDesNumeros[nextX][nextY], numeroDeCetteCase+1)
                    self.numerotationDesCases((nextX,nextY)) # Récursion pour essayer les cases suivantes
    
    def unDesPCCs(self,noeudCourrant):
        """Obtient une liste de tuple correspondant aux coordonnées d'un des chemins les plus courts (renvoie [] si le point d'arrivée n'est pas atteignable)"""
        x,y = noeudCourrant
        if self.__matrice[x][y] == 3:
            #Point d'arrivée atteint
            return [noeudCourrant]
        else:
            for caseChoisie in self.__voisins: # Essaye tout les déplacements
                nextX,nextY = x+caseChoisie[0], y+caseChoisie[1] # Nouvelle case
                if self.prometteur(nextX,nextY):
                    if self.__matriceDesNumeros[nextX][nextY] == 3:
                        #Point d'arrivee atteint
                        return [(nextX,nextY)]
                    if self.__matriceDesNumeros[x][y] == 2 or self.__matriceDesNumeros[nextX][nextY] == self.__matriceDesNumeros[x][y]+1:
                        # Vérifie si le déplacement effectué correspond au chemin le plus court pour aller du point de départ jusqu'à la case actuelle
                        trajetRestant = self.unDesPCCs((nextX,nextY))
                        if trajetRestant != []:
                           return [(nextX,nextY)] + trajetRestant
        return []
    
    def utiliserPCC(self):
        """Remplie l'échiquier en plaçant des 4 là où le personnage s'est déplacé, le chemin étant trouvé par la méthode unDesPCCs"""
        trajet = self.unDesPCCs(self.getStartCase())
        if trajet == []:
            return False
        for noeud in trajet[:-1]: # Ne prend pas en compte le dernier élement qui correpond à la case d'arrivée (pour laisser le chiffre 3 dans cette case)
            x,y = noeud
            self.__matrice[x][y] = 4
        return True
                
        
if __name__ == '__main__':
    # libre = -1 ; murs = 1 ; arrivée = 3 ; départ = 2 ; occupé = 4
    taille = 10
    laby = Labyrinthe(taille)
    laby.remplir(30)
    compteurs = {"compteurTentative":0, "compteurRetourArriere":0}
    start = time.time()
    startCase = laby.getStartCase()
    laby.numerotationDesCases(startCase)
    print('\n')
    #if laby.AES_un_chemin(startCase):
    if laby.utiliserPCC():
        print("Succès")
    else:
        print("Echec")
    print('\n')
    laby.show()
    print('\n')
    print(compteurs)
    end = time.time()
    print("Temps écoulé : "+str(end-start)+" s")
    
    
