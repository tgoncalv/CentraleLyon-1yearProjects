# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 07:59:28 2020

@author: taiga
"""

import numpy as np,math


# Exercice 1.1
def Monnaie_Gloutonne(S,M):
    T=[0]*len(S)
    Q=0
    while M != 0:
        p_max = 0
        for p in range(len(S)):
            if S[p]<=M:
                p_max=p # S est ordonné dans l'ordre croissant
        if S[p_max] == 0:
            print("impossible")
            return
        nb = M//S[p_max]
        M = M%S[p_max]
        T[p_max]+= nb
        Q+=nb
    return (T,Q)

print("\n  Tests exercice 1.1")
S = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000]
print(Monnaie_Gloutonne(S,23665))
S = [1,7,23]
print(Monnaie_Gloutonne(S,28))

# Exercice 1.3
def Monnaie_Gloutonne_D(S,M,D):
    T=[0]*len(S)
    Q=0
    while M != 0:
        p_max = 0
        for p in range(len(S)):
            if S[p]<=M and T[p]<D[p]: # ajout d'une condition
                p_max=p # S est ordonné dans l'ordre croissant
        if S[p_max] == 0 or D[p_max]==0: #condition D[p] à vérifier car p_max=0 dans le pire des cas
            print("impossible")
            return
        nb = M//S[p_max]
        M = M%S[p_max]
        if nb>D[p_max]: # si on a besoin de plus de pièces de type p_max que ce qu'on dispose,
            M+= S[p_max]*(nb-D[p_max]) # alors on s'arrête dès qu'on les a toutes utilisées, et donc on corrige la valeur de M
            nb=D[p_max]
        T[p_max]+= nb
        Q+=nb
    return (T,Q)

print("\n  Tests exercice 1.3")
S = [1 ,2 ,5 ,10,20,50,100,200,500,1000,2000,5000,10000]
D = [10,10,10,10,10,10,10 ,10 ,10 ,10  ,10  ,10  ,1    ]
print(Monnaie_Gloutonne_D(S,23665,D))
S = [1 ,7 ,23]
D = [10,10,10]
print(Monnaie_Gloutonne_D(S,28,D))

# Exercice 2.1
# def Monnaie_graphe(S,M):
#     F = []
#     A = {M:{}}
#     F.append(M)
#     trouve = False
#     while len(F)>0 and not trouve :
#         m = F.pop(0)
#         for p in S:
#             if p <= m:
#                 if m-p in A:
#                     A[m-p][m]=p # ajout d'un arc dans un noeud existant
#                 else:
#                     A[m-p]={} # ajout d'un noeud et d'un arc
#                     A[m-p][m]=p
#                 F.append(m-p)
#                 if m-p == 0:
#                     trouve = True
#     if len(F)==0 and not trouve:
#         print("Il y a un problème dans les calculs !")
#         return
#     else:
#         noeud = 0
#         T = [0]*len(S)
#         Q = 0
#         while noeud != M:
#             parents = list(A[noeud].items())
#             noeud,p = parents[0][0],parents[0][1]
#             for i in range(len(T)):
#                 if S[i]==p:
#                     T[i]+=1
#             Q+=1
#     return (T,Q)
def Monnaie_arbre(S,M):
    F = []
    A = {M:{}}
    F.append(M)
    while len(F)>0:
        m = F.pop(0)
        for p in S:
            if p <= m:
                if m-p in A:
                    A[m-p][m]=p # ajout d'un arc dans un noeud existant
                else:
                    A[m-p]={} # ajout d'un noeud et d'un arc
                    A[m-p][m]=p
                F.append(m-p)
    return A

# print("\n  Tests exercice 2.1")
# S = [1,7,23]
# print(Monnaie_arbre(S,28)) 

# Exercice 2.2
def Monnaie_parcours_largeur(S,M):
    F = []
    A = {M:{}}
    F.append(M)
    trouve = False
    while len(F)>0 and not trouve :
        m = F.pop(0)
        for p in S:
            if p <= m:
                if m-p not in A: # Le premier parent crée pour chaque noeud est le chemin le plus court
                    A[m-p]={} # ajout d'un noeud et d'un arc
                    A[m-p][m]=p
                F.append(m-p)
                if m-p == 0:
                    trouve = True
    if len(F)==0 and not trouve:
        print("Il y a un problème dans les calculs !")
        return
    else:
        noeud = 0
        T = [0]*len(S)
        Q = 0
        while noeud != M:
            parents = list(A[noeud].items())
            noeud,p = parents[0][0],parents[0][1]
            for i in range(len(T)):
                if S[i]==p:
                    T[i]+=1
            Q+=1
    return (T,Q)   
print("\n  Tests exercice 2.2")
S = [1,7,23]
print(Monnaie_parcours_largeur(S,28))   

# Exercice 3.1
def Monnaie_v1(S,M):
    mat = np.zeros((len(S)+1,M+1))
    for i in range(len(S)+1):
        for m in range(M+1):
            if m==0:
                mat[i][m]=0
            elif i==0:
                mat[i][m]=math.inf
            else:
                a,b=math.inf,math.inf
                if m-S[i-1]>=0: # on utilise la pièce de type i
                    a = 1+mat[i][m-S[i-1]]
                if i>=1: # on n'utilise pas la pièce de type i
                    b = mat[i-1][m]
                mat[i][m] = min(a,b)
    return mat[-1][-1]

print("\n  Tests exercice 3.1")
S = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000]
print(Monnaie_v1(S,23665))
S = [1,7,23]
print(Monnaie_v1(S,28))

# # Exercice 3.2  (version 1)
# def Monnaie_v2(S,M):
#     mat = np.zeros((len(S)+1,M+1))
#     for i in range(len(S)+1):
#         for m in range(M+1):
#             if m==0:
#                 mat[i][m]=0
#             elif i==0:
#                 mat[i][m]=math.inf
#             else:
#                 a,b=math.inf,math.inf
#                 if m-S[i-1]>=0: # on utilise la pièce de type i
#                     a = 1+mat[i][m-S[i-1]]
#                 if i>=1: # on n'utilise pas la pièce de type i
#                     b = mat[i-1][m]
#                 mat[i][m] = min(a,b)
#     Q=mat[-1][-1]
#     T = [0]*len(S)
#     m=M
#     while m!=0:
#         i=0;trouve=False
#         while i<=len(S) and not trouve:
#             if Q-1 == mat[-1][m-S[i]]: # On cherche la pièce à utiliser pour qu'on puisse payer le montant restant avec Q-1 pièces
#                 m=m-S[i] # le montant restant à payer
#                 Q=Q-1 # pièces restantes à utiliser
#                 trouve = True # On a trouvé la pièce qu'on voulait, on arrête donc la boucle
#                 T[i]+=1
#             else:
#                 i+=1
#         if not trouve:
#             print("Stooop !! Il y a un problème !")
#             return
#     return(T,mat[-1][-1])

# Exercice 3.2  (version 2)
def Monnaie_v2(S,M):
    s=len(S)
    mat = np.zeros((s+1,M+1))
    mat_T = [[[0]*s]*(M+1)]*(s+1) # pièces à utiliser
    for i in range(s+1):
        for m in range(M+1):
            if m==0:
                mat[i][m]=0
            elif i==0:
                mat[i][m]=math.inf
            else:
                a,b=math.inf,math.inf
                if m-S[i-1]>=0: # on utilise la pièce de type i
                    a = 1+mat[i][m-S[i-1]]
                if i>=1: # on n'utilise pas la pièce de type i
                    b = mat[i-1][m]
                if a<b: # c'est plus efficace d'utiliser la pièce de type i
                    mat[i][m] = a
                    mat_T[i][m] = mat_T[i][m-S[i-1]][:]
                    mat_T[i][m][i-1]+= 1
                else:
                    mat[i][m] = b
                    mat_T[i][m] = mat_T[i-1][m][:]
    return (mat_T[-1][-1],mat[-1][-1])

print("\n  Tests exercice 3.2")
S = [1,2,5,10,20,50,100,200,500,1000,2000,5000,10000]
print(Monnaie_v2(S,23665))
S = [1,7,23]
print(Monnaie_v2(S,28))

# # Exercice 3.3  (version non fonctionnelle)
# def Monnaie_v3(S,M,D):
#     s=len(S)
#     mat = np.zeros((s+1,M+1))
#     mat_T = [[[0]*s]*(M+1)]*(s+1) # pièces à utiliser  
#     for i in range(s+1):
#         for m in range(M+1):
#             if m==0:
#                 mat[i][m]=0
#             elif i==0:
#                 mat[i][m]=math.inf
#             else:
#                 a,b=math.inf,math.inf

#                 if i>=1: # on n'utilise pas la pièce de type i
#                     b = mat[i-1][m]
#                 if m-S[i-1]>=0 and  mat_T[i][m-S[i-1]][i-1]<D[i-1]: # on utilise la pièce de type i, si on en dispose
#                     a = 1+mat[i][m-S[i-1]]
#                 if a<b: # c'est plus efficace d'utiliser la pièce de type i
#                     mat[i][m] = a
#                     mat_T[i][m] = mat_T[i][m-S[i-1]][:]
#                     mat_T[i][m][i-1]+= 1
#                 else:
#                     mat[i][m] = b
#                     mat_T[i][m] = mat_T[i-1][m][:]
#     return (mat_T[-1][-1],mat[-1][-1])

# Ecercice 3.3  (version fonctionnelle)
def Monnaie_v3(S,M,D):
    s=len(S)
    mat = np.zeros((s+1,M+1))
    mat_T = [[[0]*s]*(M+1)]*(s+1) # pièces à utiliser  
    for i in range(s+1):
        for m in range(M+1):
            if m==0:
                mat[i][m]=0
            elif i==0:
                mat[i][m]=math.inf
            else:
                a,b=math.inf,math.inf

                if i>=1: # on n'utilise pas la pièce de type i
                    b = mat[i-1][m]
                if m-S[i-1]>=0 and  mat_T[i][m-S[i-1]][i-1]<D[i-1]: # on utilise la pièce de type i, si on en dispose
                    a = 1+mat[i][m-S[i-1]]
                    p=i # on mémorise l'indice de la pièce
                else: # on cherche une solution optimale dans la ligne i en excluant la colonne m-S[i-1] (pas assez de pièces)
                    for i2 in range(s+1):
                        if m-S[i2-1]>=0 and mat_T[i][m-S[i2-1]][i2-1]<D[i2-1] and mat[i][m-S[i2-1]]+1<a: # la dernière condition correspond à la condition d'optimalité
                            a=mat[i][m-S[i2-1]]+1
                            p=i2 # on mémorise l'indice de la pièce
                if a<b: # c'est plus efficace d'utiliser la pièce de type i
                    mat[i][m] = a
                    mat_T[i][m] = mat_T[i][m-S[p-1]][:]
                    mat_T[i][m][p-1]+= 1
                else:
                    mat[i][m] = b
                    mat_T[i][m] = mat_T[i-1][m][:]
    return (mat_T[-1][-1],mat[-1][-1])
                        
print("\n  Tests exercice 3.3")

S = [1 , 2, 5,10,20,50,100,200,500,1000,2000,5000,10000]
D = [10, 0, 2,1 ,0 ,10,10 ,10 ,10 ,10  ,10  ,1   ,1    ]
print(Monnaie_v3(S,23665,D))
S = [1 , 2, 5,10,20,50,100,200,500,1000,2000,5000,10000]
D = [10, 0, 2,1 ,0 ,10,10 ,10 ,10 ,10  ,10  ,2   ,1    ]
print(Monnaie_v3(S,23665,D))

# Ecercice 3.5
def Monnaie_poids(S,M,D,P):
    s=len(S)
    mat = np.zeros((s+1,M+1))
    mat_P = np.zeros((s+1,M+1)) # poids total des pièces
    mat_T = [[[0]*s]*(M+1)]*(s+1) # pièces à utiliser  
    for i in range(s+1):
        for m in range(M+1):
            if m==0:
                mat[i][m]=0
            elif i==0:
                mat[i][m]=math.inf
                mat_P[i][m]=math.inf
            else:
                a,b=math.inf,math.inf
                aP,bP=math.inf,math.inf
                if i>=1: # on n'utilise pas la pièce de type i
                    b = mat[i-1][m]
                    bP = mat_P[i-1][m]
                if m-S[i-1]>=0 and mat_T[i][m-S[i-1]][i-1]<D[i-1]: # on utilise la pièce de type i, si on en dispose
                    a = mat[i][m-S[i-1]]+1
                    aP = mat_P[i][m-S[i-1]]+P[i-1]
                    p=i # on mémorise l'indice de la pièce
                else: # on cherche une solution optimale dans la ligne i en excluant la colonne m-S[i-1] (pas assez de pièces)
                    for i2 in range(s+1):
                        if m-S[i2-1]>=0 and mat_T[i][m-S[i2-1]][i2-1]<D[i2-1] and mat[i][m-S[i2-1]]+1<a: # la dernière condition correspond à la condition d'optimalité
                            a =  mat[i][m-S[i2-1]]+1   
                            aP = mat_P[i][m-S[i2-1]]+P[i2-1]
                            p=i2 # on mémorise l'indice de la pièce
                if aP<bP: # c'est plus efficace d'utiliser la pièce de type i
                    mat_P[i][m] = aP
                    mat[i][m] = a
                    mat_T[i][m] = mat_T[i][m-S[p-1]][:]
                    mat_T[i][m][p-1]+= 1
                else:
                    mat[i][m] = b
                    mat_P[i][m] = bP
                    mat_T[i][m] = mat_T[i-1][m][:]
    return (mat_T[-1][-1],mat[-1][-1],mat_P[-1][-1])

print("\n Résultat exercice 3.4")
S = [1 , 2, 5,10,20,50,100,200,500,1000,2000,5000,10000]
D = [10, 0, 2,1 ,0 ,10,10 ,10 ,10 ,10  ,10  ,1   ,1    ]
P = [2.30,3.06,3.92,4.10,5.74,7.80,7.50,8.50,0.6,0.7,0.8,0.9,1]
print(Monnaie_v3(S,7,D))
print(Monnaie_poids(S,7,D,P))
                        
print("\n  Tests exercice 3.5")
S = [1 , 2, 5,10,20,50,100,200,500,1000,2000,5000,10000]
D = [10, 0, 2,1 ,0 ,10,10 ,10 ,10 ,10  ,10  ,1   ,1    ]
P = [2.30,3.06,3.92,4.10,5.74,7.80,7.50,8.50,0.6,0.7,0.8,0.9,1]
print(Monnaie_poids(S,23665,D,P))
S = [1,3,4,7]
D = [10,10,10,10]
P = [10,27,32,55]
print(Monnaie_poids(S,28,D,P))

# Exercice 3.6
def Poids_Gloutonne(S,P,M):
    L=[]
    for i in range(len(S)):
        L+=[(P[i]/S[i], S[i], P[i])]
    sorted(L)
    M2 = M
    res = 0
    while M2!=0:
        for triplet in L:
            if triplet[1] <= M2:
                res+= triplet[2]*(M2//triplet[1])
                M2 = M2%triplet[1]
    return res

print("\n Résultat exercice 3.6")
S = [1,3,4,7]
D = [100,100,100,100]
P = [10,27,32,55]
M=20
for m in range(1,M+1):
    meth_dyn = Monnaie_poids(S,m,D,P)[-1]
    meth_glou = Poids_Gloutonne(S,P,m)
    if meth_dyn != meth_glou:
        print(m)








