# -*- coding: utf-8 -*-
"""
Created on Tue Sep 29 08:23:39 2020

@author: taiga
"""

import sqlite3, datetime, matplotlib.pyplot as plt

def trans_date(D):
    """Transforme la date écrite avec le format aaaa-mm-dd en objet de type datetime.date"""
    return datetime.date(int(D[0:4]),int(D[5:7]),int(D[8:10]))

def trans_periode(dd,df):
    """Créee une liste comprenant toutes les dates entre dd et df (dd et df sont de la forme année-mois-jour)"""
    dd2,df2 = trans_date(dd),trans_date(df)
    periode = [dd2]
    while periode[-1] < df2:
        D = periode[-1] + datetime.timedelta(days=1)
        periode+=[D]
    return periode

class HotelDB:
    def __init__(self,BDD):
        self.__BDD = BDD
        
    def __del__(self):
        # self.conn.close()
        pass
    
    def __str__(self):
        pass
    
    def get_name_hotel_etoile(self,n):
        conn = sqlite3.connect(self.__BDD)
        curseur = conn.cursor()
        liste=' Hôtels ayant {} étoile(s):'.format(n)+'\n     '
        try:
            hotels=curseur.execute("SELECT nom FROM hotel WHERE etoiles={}".format(n)).fetchall()
            if len(hotels)!=0:
                for ligne in hotels:
                    liste+=str(ligne[0])+'\n     '
            else:
                liste+="Aucun\n"
        except:
            liste=" Aucun résultat ne correspond à votre recherche. Modifiez l'argument '{}'.\n".format(n)
        conn.close()
        return liste
            
    
    def insert_client(self,nom,prenom):
        conn = sqlite3.connect(self.__BDD)
        curseur = conn.cursor()
        numclient = curseur.execute("SELECT * FROM client WHERE nom='{}' AND prenom='{}'".format(nom,prenom)).fetchall()
        if len(numclient)!=0:
            return "le client est déjà enregistré, son numéro est: "+str(numclient[0][0])
        liste_num = curseur.execute("SELECT numclient FROM client").fetchall()
        new_num = 1
        while (new_num,) in liste_num:
            new_num+=1
        curseur.execute("INSERT INTO client VALUES({},'{}','{}')".format(new_num,nom,prenom))
        conn.commit()
        return "Ce client est désormais enregistré. Son numéro est: "+str(new_num)        
        conn.close()
        

        
    def affluence(self,hotel,dd ,df, n=1):
        """Donne l'affluence d'un hôtel entre dd (date de début) et df (date de fin). Mettre hotel=* pour regarder l'affluence de tous les hôtels"""
        conn = sqlite3.connect(self.__BDD)
        curseur = conn.cursor()
        
        #Etape 1: On récupère toutes les dates durant lesquelles une chambre de l'hôtel ou des hôtels nous intéréssant était occupée.
        #do représente la liste de ces dates pour lequelles les chambres étaient effectivement occupées.
        #dr représente la liste de ces dates pour lesquelles les chambres seront probablement occupées (car réservées).
        if hotel == "*":
            num_hotel = curseur.execute("SELECT numhotel FROM hotel").fetchall()
            liste_num = tuple([num_hotel[i][0] for i in range(len(num_hotel))])
            do = curseur.execute("SELECT datedepart, datearrivee FROM occupation WHERE numhotel IN {}".format(liste_num)).fetchall()
            dr = curseur.execute("SELECT datedepart, datearrivee FROM reservation WHERE numhotel IN {}".format(liste_num)).fetchall()
        else:
            num_hotel = curseur.execute("SELECT numhotel FROM hotel WHERE nom='{}'".format(hotel)).fetchall()
            liste_num = num_hotel[0][0]
            do = curseur.execute("SELECT datedepart, datearrivee FROM occupation WHERE numhotel == {}".format(liste_num)).fetchall()
            dr = curseur.execute("SELECT datedepart, datearrivee FROM reservation WHERE numhotel == {}".format(liste_num)).fetchall()
            
        conn.close() #On n'a plus besoin de la BDD, donc on ferme l'accès dès la fin de cette étape.
        
        
        #Etape 2: Les dates étant de type str, on les transforme en type date à l'aide du module datetime.
        #On rajoute également les dates comprises entre la date d'arrivée du client et la date de départ.
        #Les conditions if type(...)==str existent car dans la base de donnée étudiée, certaines chambres sont occupées mais la date n'est pas mentionnée
        dates = []
        for D in do:
            if type(D[0])==str and type(D[1])==str:
                dates+=trans_periode(D[1],D[0])  #trans_periode() est une fonction permettant de créer une liste contenant toutes les dates entre deux dates (ici, entre D[1] et D[0]).
        for D in dr:    
            if type(D[0])==str and type(D[1])==str:
                dates+=trans_periode(D[1],D[0])
            
        
        #Etape 3: On prépare l'axe des absicces.
        date_debut = trans_date(dd) #♫trans_date() est une fonction permettant de transformée une date de type 'année-mois-jour' en un élément de type date
        date_fin = trans_date(df)
        periode = trans_periode(dd,df)
        periode_pas_n = [date_debut]

        while periode_pas_n[-1] < date_fin:
            D_pas_n = periode_pas_n[-1] + datetime.timedelta(days=n)
            periode_pas_n+=[D_pas_n]
        
            
                    
        
        #Etape 4: On trace l'histogramme
        plt.style.use('classic')
        plt.figure(figsize=(5,3))
        ax = plt.axes(facecolor='#E6E6E6')
        ax.set_axisbelow(True)
        plt.grid(color='w', linestyle='solid')
        ax.xaxis.tick_bottom()
        ax.yaxis.tick_left()
        if hotel == '*':
            ax.set_title("Nombre de clients dans tous les hôtels \n entre {} et {}".format(dd,df),fontsize=9, fontweight='bold', color='#EE6666')
        else:
            ax.set_title("Nombre de clients dans l'hôtel {} \n entre {} et {}".format(hotel,dd,df),fontsize=9, fontweight='bold', color='#EE6666')
        marqueurs = []
        labels = []
        for date in periode:
            if date.day == 1:
                marqueurs+=[date]
                date_str = date.strftime("%b %Y")
                labels+=[date_str]
        plt.xticks(marqueurs,labels)
        ax.tick_params(colors='gray', direction='out')
        for tick in ax.get_xticklabels():
            tick.set_color('gray')
        for tick in ax.get_yticklabels():
            tick.set_color('gray')
        ax.hist(dates, periode_pas_n, edgecolor='#E6E6E6', color='#EE6666')
        plt.savefig('affluence.png')
        plt.show()
        plt.close()
      
        
    def profits(self,dd,df,n):
        """Calcul l'argent récolté par chaque hôtel entre la date de début dd et la date de fin df"""
        conn = sqlite3.connect(self.__BDD)
        curseur = conn.cursor()
        
        #Etape 1: création d'une liste de liste nommée liste_hotel.
        #Chaque sous-liste est pour l'instant composée du numéro de l'hotel et de son nom.
        if n == "all":
            hotel = curseur.execute("SELECT numhotel,nom FROM hotel").fetchall()
            # liste_num = tuple([hotel[i][0] for i in range(len(hotel))])
            liste_hotel = [[hotel[i][0],hotel[i][1]] for i in range(len(hotel))]
        else:
            hotel = curseur.execute("SELECT numhotel,nom FROM hotel WHERE etoiles='{}'".format(n)).fetchall()
            # liste_num = tuple([hotel[i][0] for i in range(len(hotel))])
            liste_hotel = [[hotel[i][0],hotel[i][1]] for i in range(len(hotel))]
            
            
        #Etape 2: moidification de la liste liste_hotel
        #Dans chaque sous-liste, on rajoute l'entier 'profit' caractérisant la somme d'argent récupérée par l'hôtel de la sous-liste concernée entre dd et df.
        periode = trans_periode(dd,df)
        
        #La fonction ajout_profit est crée pour ne pas avoir à l'écrire deux fois (pour les listes do et dr).
        def ajout_profit(D,i):
            """ajoute la somme d'argent récolté par l'hôtel i (D=do ou D=dr)""" 
            profit = 0
            for hotel in D:
                datedepart,datearrivee=hotel[0],hotel[1]
                if type(datedepart)==str and type(datearrivee)==str and trans_date(datearrivee) in periode:
                    if trans_date(datedepart) in periode:
                        nb_jours = trans_date(datedepart)-trans_date(datearrivee)
                    else:
                        nb_jours = periode[-1]-trans_date(datearrivee)
                    profit+= nb_jours.days * hotel[3]
            liste_hotel[i].append(profit)
            

        for i in range(len(liste_hotel)):
            
            do = curseur.execute("SELECT datedepart, datearrivee, c.numhotel, prixnuitht FROM occupation as o JOIN chambre as c ON"
                                 " o.numchambre=c.numchambre AND o.numhotel=c.numhotel WHERE c.numhotel = {}".format(liste_hotel[i][0])).fetchall()
            
            dr = curseur.execute("SELECT datedepart, datearrivee, c.numhotel, prixnuitht FROM reservation as r JOIN chambre as c ON"
                                 " r.numchambre=c.numchambre AND r.numhotel=c.numhotel WHERE c.numhotel = {}".format(liste_hotel[i][0])).fetchall()
            ajout_profit(do,i)
            ajout_profit(dr,i)
              
            
        conn.close()
        
        
        #Etape 3: Tracé de la somme d'argent récupéré en fonction du nom de l'hôtel.

        
        nom_hotel = []
        profits = []
        #Cette section est faite car certains hôtels ont le même nom mais pas le même numéro d'identification (car le même hôtel existe dans plusieurs villes).
        #L'argent récolté par les hôtels de même nom sont alors fusionné (même entreprise). 
        for i in range(len(liste_hotel)):
            if liste_hotel[i][1] not in nom_hotel:
                nom_hotel+=[liste_hotel[i][1]]
                profits+=[liste_hotel[i][2]]
            else:
                #Ici, on fusionne le profit des deux hôtels de même nom.
                for j in range(len(nom_hotel)):
                    if liste_hotel[i][1]==nom_hotel[j]:
                        profits[j]+=liste_hotel[i][2]

        
        plt.style.use('classic')
        plt.figure(figsize=(8,3))
        ax = plt.axes(facecolor='#E6E6E6')
        ax.set_axisbelow(True)
        plt.grid(color='w', linestyle='solid')
        ax.xaxis.tick_bottom()
        ax.yaxis.tick_left()
        x=range(1,1+len(nom_hotel))
        if n == 'all':
            ax.set_title("Profit de chaque hôtel \n entre {} et {}".format(dd,df),fontsize=9, fontweight='bold', color='#EE6666')
        else:
            ax.set_title("Profit des hôtels {} étoile(s) \n entre {} et {}".format(n,dd,df),fontsize=9, fontweight='bold', color='#EE6666')
        plt.xticks(x,nom_hotel,ha='right',rotation=15,fontsize=8, fontweight='bold')
        ax.tick_params(colors='gray', direction='out')
        for tick in ax.get_xticklabels():
            tick.set_color('gray')
        for tick in ax.get_yticklabels():
            tick.set_color('gray')
        ax.set_ylabel('Profit en €', color ='gray')
        ax.bar(x,profits, edgecolor='#E6E6E6', color='#EE6666')
        plt.savefig('profits.png')
        plt.show()
        plt.close()
          
        
                        
        
        
        

if __name__ == '__main__':
    aHotelDB =  HotelDB('hotellerie.db')
    print(aHotelDB.get_name_hotel_etoile("2"))
    # print(aHotelDB.get_name_hotel_etoile("-1"))
    # print(aHotelDB.get_name_hotel_etoile("Hello"))
    # print(aHotelDB.insert_client("Goncalves","Taiga"))
    print(aHotelDB.affluence("Hotel chez soi","2014-03-01","2014-06-8",4))
    # print(aHotelDB.affluence("*","2014-03-01","2014-06-02",1))
    # print(aHotelDB.profits("2014-03-01","2014-05-05","all"))
    # print(aHotelDB.profits("2014-03-01","2014-05-05","2"))
    
    
    
