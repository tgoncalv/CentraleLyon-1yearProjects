
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 07:50:32 2020

@author: taiga
"""

from PIL import Image # importation de la librairie d’image PILLOW
from math import sqrt, log10 # fonctions essentielles de la librairie math
from graphviz import Digraph
from graphviz import Source
g = Digraph('G', filename='graph.gv')
im = Image.open("lyon.bmp") # ouverture du fichier d’image que nous allons compresser
im_ori = Image.open("lyon.bmp") # image originale (que nous n'allons pas compresser)
px = im.load() # importation des pixels de l’image
px_ori = im_ori.load() 
W, H = im.size

### Exercice 1.1 ###
def SetColorRegion(x,y,w,h,c):
    """Création d'un rectangle d'origine (x,y), de dimension w*h et de couleur c"""
    for i in range(y,y+w):
        for j in range(x,x+h):
            px[i,j]= int(c[0]),int(c[1]),int(c[2])


### Test ###
# SetColorRegion(0,0,500,50,(256,256,256))
# im.show()
### Fin du test ###


### Exercice 1.2 ###            
def moy(x,y,w,h):
    """Caclule la moyenne des pixels d'une région rectangulaire"""
    r,g,b=0,0,0
    N=w*h
    for i in range(y,y+w):
        for j in range(x,x+h):
            c=px[i,j]
            r+=c[0]
            g+=c[1]
            b+=c[2]
    return (r/N,g/N,b/N)

### Exercice 1.3 ###
def ecart_type(x,y,w,h):
    """Calcule l'écart-type des pixels d'une région rectangulaire"""
    sigma=[0,0,0]
    n=w*h
    for i in range(y,y+w):
        for j in range(x,x+h):
            c=px[i,j]
            sigma[0]+=c[0]**2
            sigma[1]+=c[1]**2
            sigma[2]+=c[2]**2
    mu=moy(x,y,w,h)
    sigma[0]=sqrt(sigma[0]/n-mu[0]**2)
    sigma[1]=sqrt(sigma[1]/n-mu[1]**2)
    sigma[2]=sqrt(sigma[2]/n-mu[2]**2)
    return sigma


### Test ###
# print(ecart_type(0,0,W,H))
# print(ecart_type(0,0,10,10))
### Fin du test ###


### Exercice 1.4 ###
def homogeneite(x,y,w,h,seuil):
    """Estime l'homogénéité des pixels d'une région rectangulaire, en comparant l'ecart-type correspondant avec un certain seuil"""
    if w*h>0:
        sigma=ecart_type(x,y,w,h)
        for i in range(len(sigma)):
            if sigma[i]>seuil:
                return False
        return True
    
### Exercice 1.5 ###
def Create(x,y,w,h,seuil):
    """Divise le rectangle d'entrée en quatre rectangles plus petits"""
    if w < 1 or h < 1:
        # Le paramètre d'entrée n'est pas un rectangle de dimension convenable, on ne renvoie donc rien
        return None
    else:
        hg = (x, y, w//2, h//2, seuil) # rectangle en haut à gauche
        bg = (x+h//2, y, w//2, h-h//2, seuil) # rectangle en bas à gauche, de hauteur potentiellement impair (h-h//2)
        hd = (x, y+w//2, w-w//2, h//2, seuil) # rectangle en haut à droite, de largeur potentiellement impair (w-w//2)
        bd = (x+h//2, y+w//2, w-w//2, h-h//2,seuil) # rectangle en bas à droite, de dimensions potentiellement impaires
        return [hg,bg,hd,bd]


### Test ###
# Create(300,0,256,256,50)
# im.show()
### Fin du test ###    
    

### Exercice 2 ###

# Exercice 2.3
def terminal(x,y,w,h,seuil):
    """Créee des noeuds terminaux de manière récursive de sorte à ce qu'elles vérifient le critère d'homogénéité"""
    if homogeneite(x, y, w, h, seuil) or w<=1 or h<=1:
        color = moy(x,y,w,h)
        return Node(x,y,w,h,color,None,None,None,None)
    else:
        hg = terminal(x, y, w//2 , h//2, seuil)
        hd = terminal(x, y+w//2 , w-w//2 , h//2, seuil)
        bg = terminal(x+h//2, y, w//2 , h-h//2, seuil)
        bd = terminal(x+h//2, y+w//2, w-w//2 , h-h//2, seuil)
        return Node(x ,y, w, h, None, hg, hd, bg, bd)
    
class Node:
    """Classe permettant de créer un noeud contenant une région rectangulaire (x,y,w,h) de couleur color, et ayant pour enfants [hg,hd,bg,bd]"""
    # Exercice 2.1
    def __init__(self,x,y,w,h,color,hg,hd,bg,bd):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.enfants = [hg,bg,hd,bd]
        self.hg = hg
        if hg is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (hg.x, hg.y, hg.h, hg.w))))
        self.hd = hd
        if hd is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (hd.x, hd.y, hd.h, hd.w))))
        self.bg= bg
        if bg is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (bg.x, bg.y, bg.h, bg.w))))
        self.bd = bd
        if bd is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (bd.x, bd.y, bd.h, bd.w))))
            
    def __str__(self):
        return str(self.nb_noeuds())

    # Exercice 3.6
    def schema(self):
        """Affiche le schéma du noeud et de ses enfants"""
        g.render(filename='img')
        g.view()

    # Exercice 2.4
    def peindre(self):
        """Peint les rectangles de chaque noeud terminal selon la couleur moyenne de tous ses pixels dans la région"""
        if self.enfants == [None,None,None,None]: #Vérifie si le noeud est terminal
            SetColorRegion(self.x, self.y, self.w, self.h, self.color) #On réutilise la fonction de l'exercice 1.1
        # Utilisation d'une méthode récursive pour atteindre chaque noeud terminal
        if self.hg != None:
            self.hg.peindre()
        if self.hd != None:
            self.hd.peindre()
        if self.bg != None:
            self.bg.peindre()
        if self.bd != None:
            self.bd.peindre()
            
    # Exercice 2.5    
    def peindre_profondeur(self,profondeur=0):
        """Peint les noeuds terminaux d'un arbre d'une couleur proportionnelle à la profondeur dans l'arbre"""
        self.__profondeur = 0 #profondeur du noeud maximal
        def profondeur_max(noeud,profondeur):
                """Calcule la profondeur maximale dans l'arbre, en prenant comme argument la profondeur initiale"""
                if self.enfants == [None,None,None,None]:
                    self.__profondeur = max(self.__profondeur,profondeur)
                # méthode récursive pour aller trouver la plus grande profondeur
                # à chaque nouvel appel de cette fonction, la profondeur augmente de 1
                if self.hg != None:
                    profondeur_max(self.hg,profondeur+1)
                if self.hd != None:
                    profondeur_max(self.hd,profondeur+1)
                if self.bg != None:
                    profondeur_max(self.bg,profondeur+1)
                if self.bd != None:
                    profondeur_max(self.bd,profondeur+1)
        if profondeur==0:
            # la fonction peindre_profondeur est appelée de manière récursive
            # cette condition permet donc de ne calculer la profondeur maximale qu'au premier appel
            profondeur_max(self,0)
        if self.hg == None and self.hd == None and self.bg == None and self.bd == None:
            r = 255*profondeur/self.__profondeur # Crée un niveau de gris proportionnel à la profondeur du noeud dans l'arbre
            SetColorRegion(self.x, self.y, self.w, self.h, [r,r,r])
        if self.hg != None:
            self.hg.peindre_profondeur(profondeur+1)
        if self.hd != None:
            self.hd.peindre_profondeur(profondeur+1)
        if self.bg != None:
            self.bg.peindre_profondeur(profondeur+1)
        if self.bd != None:
            self.bd.peindre_profondeur(profondeur+1)
        
    # Exercice 2.6
    def EQ(self):
        """Calcule l'erreur quadratique"""
        if self.color is not None: # Seul les noeuds terminaux ont une couleur
            R,G,B = self.color
            eq = 0
            
            for i in range(self.y, self.y+self.w):
                for j in range(self.x, self.x+self.h):
                    r,g,b = px[i,j]
                    eq += (R-r)**2 + (G-g)**2 + (B-b)**2
            return eq
        else: # Si le noeud n'est pas terminal, on appelle la fonction sur ses enfants
            s=0
            for n in self.enfants:
                s+= n.EQ()
            return s
    
    
    def PSNR(self):
        """Calcule la mesure Peak Signal to Noise Ratio"""
        return 20*log10(255)-10*log10(self.EQ()/(3*W*H))
    
    def get_PSNR(self):
        print(self.PSNR())
    
    # Quelle valeur du seuil donne un nombre de noeuds le plus proche de 10000 en moyenne ?
    def nb_noeuds(self,n=0):
        nb_noeuds = n+1 #stock le nombre de noeuds. La valeur par défaut est 0
        if self.enfants == [None,None,None,None]:
            return nb_noeuds # Il n'y a plus de noeuds à compter
        else : 
            # On compte par récurrence
            noeuds_hg = self.hg.nb_noeuds(n)
            noeuds_hd = self.hd.nb_noeuds(n)
            noeuds_bg = self.bg.nb_noeuds(n)
            noeuds_bd = self.bd.nb_noeuds(n)
            return noeuds_hg+noeuds_hd+noeuds_bg+noeuds_bd
        
        
#Exercice 3

# Exercice 3.3 (fonction terminal de l'exercice 2.3 adaptée pour inclure les types)
def quadripartition_type(x,y,w,h,seuil):            
    h_carre_hg = homogeneite(x, y, w//2, h//2, seuil) # carré en haut à gauche
    h_carre_hd = homogeneite(x, y+w//2 , w-w//2 , h//2 , seuil) # carré en haut à droite
    h_carre_bg = homogeneite(x+h//2, y, w//2 , h-h//2 , seuil) # carré en bas à gauche
    h_carre_bd = homogeneite(x+h//2, y+w//2, w-w//2 , h-h//2 , seuil) # carré en bas à droite
    h_rect_gd_g = homogeneite(x, y, w//2, h, seuil) # grand rectangle à gauche
    h_rect_gd_d = homogeneite(x, y+w//2, w-w//2, h, seuil) # grand rectangle à droite
    h_rect_pt_gg = homogeneite(x, y, w//4, h, seuil) # petit rectangle tout à gauche
    h_rect_pt_g = homogeneite(x, y+w//4 , w//4, h, seuil) # petit rectangle centre gauche
    h_rect_pt_d = homogeneite(x, y+2*w//4, w//4, h, seuil) # petit rectangle centre droite
    h_rect_pt_dd = homogeneite(x, y+3*w//4, w-3*w//4, h, seuil) # petit recntre tout à droite
    h_rect_gd_h = homogeneite(x, y, w, h//2, seuil) # grand rectangle en haut
    h_rect_gd_b = homogeneite(x+h//2, y, w, h-h//2, seuil) # grand rectangle en bas
    h_rect_pt_hh = homogeneite(x, y, w, h//4, seuil) # petit rectangle tout en haut
    h_rect_pt_h = homogeneite(x+h//4, y, w, h//4, seuil) # petit rectangle centre haut
    h_rect_pt_b = homogeneite(x+2*h//4, y, w, h//4, seuil) # petit rectangle centre bas
    h_rect_pt_bb = homogeneite(x+3*h//4, y, w, h-3*h//4, seuil) # petit rectangle tout en bas
    ho = homogeneite(x,y,w,h,seuil) # tout
    if ho or w<=1 or h<=1:
        #type 3
        r,g,b = moy(x, y, w, h)
        return Node2(x, y, w, h, None, None, None, None, 3, [r,g,b])
    elif h_carre_hg and h_carre_hd and h_carre_bg and h_carre_bd:
        # type 0
        rhg,ghg,bhg = moy(x, y, w//2, h//2)
        rhd,ghd,bhd = moy(x, y+w//2 , w-w//2 , h//2)
        rbg,gbg,bbg = moy(x+h//2, y, w//2 , h-h//2)
        rbd,gbd,bbd = moy(x+h//2, y+w//2, w-w//2 , h-h//2)
        return Node2(x,y,w,h, None, None, None, None, 0, [rhg,ghg,bhg,rhd,ghd,bhd,rbg,gbg,bbg,rbd,gbd,bbd])
    elif h_rect_gd_g and h_rect_gd_d:
        # type 1
        rg,gg,bg = moy(x, y,w//2, h)
        rd,gd,bd = moy(x, y+w//2, w-w//2, h)
        return Node2(x, y, w, h, None,None, None, None, 1, [rg,gg,bg,rd,gd,bd])
    elif h_rect_gd_h and h_rect_gd_b:
        #type 2
        rh,gh,bh = moy(x, y, w, h//2)
        rb,gb,bb = moy(x+h//2, y, w, h-h//2)
        return Node2(x, y, w, h, None,None, None, None, 2, [rh,gh,bh,rb,gb,bb])

    elif h_rect_gd_h and h_carre_bg and h_carre_bd:
        #type 4
        rh,gh,bh = moy(x, y, w, h//2)
        rbg,gbg,bbg = moy(x+h//2, y, w//2, h-h//2)
        rbd,gbd,bbd = moy(x+h//2, y+w//2, w-w//2, h-h//2)
        return Node2(x, y, w, h, None,None, None, None, 4, [rh,gh,bh,rbg,gbg,bbg,rbd,gbd,bbd])
    elif h_carre_hg and h_carre_hd and h_rect_gd_b:
        #type 5
        rhg,ghg,bhg = moy(x, y, w//2, h//2)
        rhd,ghd,bhd = moy(x, y+w//2 , w-w//2 , h//2)
        rb,gb,bb = moy(x+h//2, y, w, h-h//2)
        return Node2(x,y,w,h, None, None,None, None, 5, [rhg,ghg,bhg,rhd,ghd,bhd,rb,gb,bb])
    elif h_carre_hg and h_rect_gd_d and h_carre_bg:
        #type 6
        rhg,ghg,bhg = moy(x, y, w//2, h//2)
        rd,gd,bd = moy(x, y+w//2, w-w//2, h)
        rbg,gbg,bbg = moy(x+h//2, y, w//2 , h-h//2)
        return Node2(x,y,w,h, None, None,None, None, 6, [rhg,ghg,bhg,rd,gd,bd,rbg,gbg,bbg])
    elif h_rect_gd_g and h_carre_hd and h_carre_bd:
        #type 7
        rg,gg,bg = moy(x, y,w//2, h)
        rhd,ghd,bhd = moy(x, y+w//2 , w-w//2 , h//2)
        rbd,gbd,bbd = moy(x+h//2, y+w//2, w-w//2 , h-h//2)
        return Node2(x, y, w, h, None, None,None, None, 7, [rg,gg,bg,rhd,ghd,bhd,rbd,gbd,bbd])
    elif h_rect_pt_gg and h_rect_pt_g and h_rect_pt_d and h_rect_pt_dd:
        #type 8
        rgg,ggg,bgg = moy(x, y, w//4, h)
        rg,gg,bg = moy(x, y+w//4 , w//4, h)
        rd,gd,bd = moy(x, y+2*w//4, w//4, h)
        rdd,gdd,bdd = moy(x, y+3*w//4, w-3*w//4, h)
        return Node2(x, y, w, h, None, None, None, None, 8, [rgg,ggg,bgg,rg,gg,bg,rd,gd,bg,rdd,gdd,bdd])
    elif h_rect_pt_hh and h_rect_pt_h and h_rect_pt_b and h_rect_pt_bb:
        #type 9
        rhh,ghh,bhh = moy(x, y, w, h//4)
        rh,gh,bh = moy(x+h//4, y, w, h//4)
        rb,gb,bb = moy(x+2*h//4, y, w, h//4)
        rbb,gbb,bbb = moy(x+3*h//4, y, w, h-3*h//4)
        return Node2(x, y, w, h, None, None, None, None, 9, [rhh,ghh,bhh,rh,gh,bh,rb,gb,bb,rbb,gbb,bbb])
    else:
        # Si aucun de ces critères n'est vérifié, on découpe la région en 4 et on appelle la même méthode sur ces 4 régions
        hg = quadripartition_type(x, y, w//2 , h//2 , seuil)
        hd = quadripartition_type(x, y+w//2 , w-w//2 , h//2 , seuil)
        bg = quadripartition_type(x+h//2, y, w//2 , h-h//2 , seuil)
        bd = quadripartition_type(x+h//2, y+w//2, w-w//2 , h-h//2 , seuil)
        return Node2(x ,y, w, h, hg, hd, bg, bd, None, None)

class Node2:
    """Classe permettant de créer un noeud contenant une région rectangulaire (x,y,w,h) de couleur color, et ayant pour enfants [hg,hd,bg,bd]"""
    # Exercice 3.1
    def __init__(self,x,y,w,h,hg,hd,bg,bd, type_partition, colors):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.enfants = [hg,bg,hd,bd]
        self.type = type_partition
        self.colors = colors
        self.hg = hg
        if hg is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (hg.x, hg.y, hg.h, hg.w))))
        self.hd = hd
        if hd is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (hd.x, hd.y, hd.h, hd.w))))
        self.bg= bg
        if bg is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (bg.x, bg.y, bg.h, bg.w))))
        self.bd = bd
        if bd is not None:
            g.edge("-".join(map(str, (x,y,w,h))), "-".join(map(str, (bd.x, bd.y, bd.h, bd.w)))) 
            
    # Exercice 3.6
    def schema(self):
        """Affiche le schéma du noeud et de ses enfants"""
        g.render(filename='img')
        g.view()
            
    # Exercice 3.2
    def type_partition(self):
        """Renvoie le type de partition, les coordonnées du points d'origine de la région, ses dimensions, et les
        couleurs de chaque sous régions de haut en bas, de gauche à droite..."""
        if self.colors == None:
            self.hg.type_partition()
            self.hd.type_partition()
            self.bg.type_partition()
            self.bd.type_partition()
        else:
            s = str(self.type)+" "+str(self.x)+" "+str(self.y)+" "+str(self.w)+" "+str(self.h)
            for c in self.colors:
                s+=" "+str(c)
            print(s)
                
    def peindre(self):
        """Peint les rectangles de chaque noeud terminal selon la couleur moyenne de tous ses pixels dans la région"""
        if self.enfants == [None,None,None,None]: #Vérifie si le noeud est terminal
            x,y,w,h,c = self.x,self.y,self.w,self.h,self.colors
            if self.type==3:
                SetColorRegion(x, y, w, h, c) #On réutilise la fonction de l'exercice 1.1
            elif self.type==0:
                SetColorRegion(x, y, w//2, h//2,c[0:3])
                SetColorRegion(x, y+w//2 , w-w//2 , h//2,c[3:6])
                SetColorRegion(x+h//2, y, w//2 , h-h//2,c[6:9])
                SetColorRegion(x+h//2, y+w//2, w-w//2 , h-h//2,c[9:12])
            elif self.type==1:
                SetColorRegion(x, y,w//2, h,c[0:3])
                SetColorRegion(x, y+w//2, w-w//2, h,c[3:6])
            elif self.type==2:
                SetColorRegion(x, y, w, h//2,c[0:3])
                SetColorRegion(x+h//2, y, w, h-h//2,c[3:6])
            elif self.type==4:
                SetColorRegion(x, y, w, h//2,c[0:3])
                SetColorRegion(x+h//2, y, w//2, h-h//2,c[:6])
                SetColorRegion(x+h//2, y+w//2, w-w//2, h-h//2,c[6:9])
            elif self.type==5:
                SetColorRegion(x, y, w//2, h//2,c[0:3])
                SetColorRegion(x, y+w//2 , w-w//2 , h//2,c[3:6])
                SetColorRegion(x+h//2, y, w, h-h//2,c[6:9])
            elif self.type==6:
                SetColorRegion(x, y, w//2, h//2,c[0:3])
                SetColorRegion(x, y+w//2, w-w//2, h,c[3:6])
                SetColorRegion(x+h//2, y, w//2 , h-h//2,c[6:9])
            elif self.type==7:
                SetColorRegion(x, y,w//2, h,c[0:3])
                SetColorRegion(x, y+w//2 , w-w//2 , h//2,c[3:6])
                SetColorRegion(x+h//2, y+w//2, w-w//2 , h-h//2,c[6:9])
            elif self.type==8:
                SetColorRegion(x, y, w//4, h,c[0:3])
                SetColorRegion(x, y+w//4 , w//4, h,c[3:6])
                SetColorRegion(x, y+2*w//4, w//4, h,c[6:9])
                SetColorRegion(x, y+3*w//4, w-3*w//4, h,c[9:12])
            elif self.type==9:
                SetColorRegion(x, y, w, h//4,c[0:3])
                SetColorRegion(x+h//4, y, w, h//4,c[3:6])
                SetColorRegion(x+2*h//4, y, w, h//4,c[6:9])
                SetColorRegion(x+3*h//4, y, w, h-3*h//4,c[9:12])
        # Utilisation d'une méthode récursive pour atteindre chaque noeud terminal
        if self.hg != None:
            self.hg.peindre()
        if self.hd != None:
            self.hd.peindre()
        if self.bg != None:
            self.bg.peindre()
        if self.bd != None:
            self.bd.peindre()
    
    def nb_noeuds(self,n=0):
        nb_noeuds = n+1 #stock le nombre de noeuds. La valeur par défaut est 0
        if self.enfants == [None,None,None,None]:
            return nb_noeuds # Il n'y a plus de noeuds à compter
        else : 
            # On compte par récurrence
            noeuds_hg = self.hg.nb_noeuds(n)
            noeuds_hd = self.hd.nb_noeuds(n)
            noeuds_bg = self.bg.nb_noeuds(n)
            noeuds_bd = self.bd.nb_noeuds(n)
            return noeuds_hg+noeuds_hd+noeuds_bg+noeuds_bd
        
    def get_noeuds(self):
        print(self.nb_noeuds())
        
    # Exercice 3.4
    def SSIM(self):
        """Evalue la qualité de l'image en prenant en compte les caractéristiques de l'oeil humain"""
        L = 255 # dynamique des valeurs des pixels, soit 255
        c1,c2 = (0.01*L)**2, (0.03*L)**2 # variables destinées à stabiliser la division quand le dénominateur est très faible
        c3 = c2/2
        x,y,w,h = self.x,self.y,self.w,self.h
        rm,gm,bm = moy(x,y,w,h) # moyenne de l'image non compressée
        rv,gv,bv = ecart_type(x,y,w,h) # ecart-type de l'image non compresséex
        self.peindre()
        Rm,Gm,Bm = moy(x,y,w,h) # moyenne de l'image compressée
        Rv,Gv,Bv = ecart_type(x,y,w,h) # ecart-type de l'image compressée
        Rc,Gc,Bc = 0,0,0 #Covariance
        for i in range(self.y, self.y+self.w):
                for j in range(self.x, self.x+self.h):
                    r,g,b = px_ori[i,j] # couleurs de l'image initiale
                    R,G,B = px[i,j] # couleurs de l'image compressée
                    Rc+= (r-rm)*(R-Rm)
                    Gc+= (g-gm)*(G-Gm)
                    Bc+= (b-bm)*(B-Bm)
        n = h*w-1
        if n>0:
            Rc,Gc,Bc = Rc/n,Gc/n,Bc/n
        SSIM_R = ((2*Rm*rm+c1)*(2*Rv*rv+c2)*(Rc+c3))/((Rm**2+rm**2+c1)*(Rv**2+rv**2+c2)*(Rv*rv+c3))
        SSIM_G = ((2*Gm*gm+c1)*(2*Gv*gv+c2)*(Gc+c3))/((Gm**2+gm**2+c1)*(Gv**2+gv**2+c2)*(Gv*gv+c3))
        SSIM_B = ((2*Bm*bm+c1)*(2*Bv*bv+c2)*(Bc+c3))/((Bm**2+bm**2+c1)*(Bv**2+bv**2+c2)*(Bv*bv+c3))
        return sqrt((SSIM_R**2+SSIM_G**2+SSIM_B**2)/3)
        
    def get_SSIM(self):
        print(self.SSIM())
            
        
# Exercice 3.5
# Mesure du PSNR et de la SSIM
import matplotlib.pyplot as plt

def PSNR_graph():
    seuils=[0,6,12,
            18,24,30,
            36,42,48,
            54,60,66,
            72,78,84]
    PSNR=[28.573093996292513,28.157342033004987,27.729626451315063,
          27.03835826412918,25.50400068573657,24.491242664378753,
          23.35210127310573,21.229245662077314,19.555910573645136,
          17.57880433298135,16.441166304606604,14.560143066366358,
          14.059925531101129,11.018706007196215,11.018706007196215]
    plt.scatter(seuils, PSNR, marker='+')
    plt.xlabel('seuil')
    plt.ylabel('PSNR')
    plt.title("PSNR de l'image en fonction du seuil d'homogénéité")
    plt.xticks(seuils)
    plt.show()
    
PSNR_graph()
    
def SSIM_graph():
    seuils=[0,6,12,
            18,24,30,
            36,42,48,
            54,60,66,
            72]
    SSIM=[0.9910913735321284,0.9894904207837918,0.9881984682022541,
          0.9863336002621672,0.9810738975498168,0.9763315477047565,
          0.9689503261644314,0.9488425308575664,0.9232189972535227,
          0.8738293633476155,0.8302514501460321,0.7144507327257331,
          0.6602917207625764]
    plt.scatter(seuils, SSIM, marker='+')
    plt.xlabel('seuil')
    plt.ylabel('SSIM')
    plt.title("SSIM de l'image en fonction du seuil d'homogénéité")
    plt.xticks(seuils)
    plt.show()
    
SSIM_graph()

        
# Exercice 2.2

# if __name__ == '__main__':       
#     racine = Node(0, 0, 4, 4, 'grey',
#                   Node(0, 0, 2, 2, 'white', None, None, None, None),
#                   Node(2, 0, 2, 2, 'grey',
#                         Node(2, 0, 1, 1, 'grey', None, None, None, None),
#                         Node(3, 0, 1, 1, 'black', None, None, None, None),
#                         Node(2, 1, 1, 1, 'black', None, None, None, None),
#                         Node(3, 1, 1, 1, 'grey', None, None, None, None)),
#                   Node(0, 2, 2, 2, 'black', None, None, None, None),
#                   Node(2, 2, 2, 2, 'grey',
#                         Node(2, 2, 1, 1, 'white', None, None, None, None),
#                         Node(3, 2, 1, 1, 'white', None, None, None, None),
#                         Node(2, 3, 1, 1, 'grey', None, None, None, None),
#                         Node(3, 3, 1, 1, 'grey', None, None, None, None)))
#     racine.schema()




# Compression de l'image selon la première méthode (Classe Node)
# B=terminal(0,0,W,H,74)
# print(B.nb_noeuds())
# B.peindre()
# B.get_PSNR()


# Compression de l'image selon la deuxième méthode (Classe Node2)
A=quadripartition_type(0, 0, W, H, 66)
# A.get_noeuds()
A.peindre()
# A.get_SSIM()    


im.show()
im_ori.show()
# im.save("Node2_seuil=66.bmp")



    
 
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    