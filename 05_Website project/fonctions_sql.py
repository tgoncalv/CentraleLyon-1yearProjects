
import sqlite3
conn = sqlite3.connect('2020.db')
c = conn.cursor()

#retourne la liste des noms des polluants (type string) pour une station donnée par son identifiant

def get_polluants(idnum):  #fonction 3
    if idnum=='Tout':
        c.execute(f"SELECT distinct nom_poll FROM 'moyennes-journalieres'")
    else:    
        idnum="'"+idnum+"'"
        c.execute(f"SELECT distinct nom_poll FROM 'moyennes-journalieres' WHERE code_station={idnum}")
    donnees = c.fetchall()
    
    polluants=[]
    for d in donnees:
        if idnum!='Tout':
            nom='"'+d[0]+'"'
            c.execute(f"SELECT distinct valeur FROM 'moyennes-journalieres' WHERE code_station={idnum} and nom_poll={nom}")
            val=c.fetchall()
            if val!=[(None,)]:
                polluants.append({'nom_du_polluant':d[0]})
        else:
            polluants.append({'nom_du_polluant':d[0]})
    return polluants

#print(get_polluants('Tout'))

#retourne la liste des dates (type string) et concentrations (type float) d'un polluant donné pour une station donnée par son id


def liste_dates(idnum,nom_du_polluant):
    nom_du_polluant='"'+nom_du_polluant+'"'

    if idnum=='Tout':
        c.execute(f"SELECT date_debut FROM 'moyennes-journalieres' WHERE nom_poll={nom_du_polluant} order by date_debut")
    else:
        idnum="'"+idnum+"'"
        c.execute(f"SELECT date_debut FROM 'moyennes-journalieres' WHERE code_station={idnum} AND nom_poll={nom_du_polluant} order by date_debut")
    donnees = c.fetchall()

    date_min=donnees[0][0][:10]
    date_max=donnees[-1][0][:10]
    date_min=date_min[:4]+"-"+date_min[5:7]+"-"+date_min[8:]
    date_max=date_max[:4]+"-"+date_max[5:7]+"-"+date_max[8:]
    return date_min,date_max

#print(liste_dates("Tout","benzène"))

def conversion_dates(date):
    return date[:4]+"/"+date[5:7]+"/"+date[8:]
   

def modif_date_fin(date):
    c.execute("SELECT date_debut FROM 'moyennes-journalieres' group by date_debut ")
    donnees = c.fetchall()
    dico={donnees[i][0][:10]:i for i in range(len(donnees))}   
    liste=[donnee[0][:10] for donnee in donnees]
    if date not in liste or date==liste[-1] or date==liste[-2] :
        return date
    return liste[dico[date]+1]

# print(modif_date_fin("2020/10/04"))
def liste_jours(date_deb,date_fin,pas_temps):
    c.execute(f"SELECT date_debut FROM 'moyennes-journalieres' WHERE date_debut >= {date_deb} and date_debut <= {date_fin} group by date_debut order by date_debut ")
    donnees = c.fetchall()
    
    dico={donnees[i][0][:10]:i for i in range(len(donnees))}   
    dates=list(dico.keys())
    jours=[]
   
    if pas_temps=='month':
        for date in dates:
            if date[8:10]=='01':
                jours.append(date)
                
    if pas_temps=='week':
        n=len(dates)
        for i in range(0,n-1,7):
            jours.append(dates[i])
           
    if pas_temps=='day':
        jours=dates
    return dico,jours    

#print(liste_jours('2019/12/28','2020/01/05','month'))      

def historique(idnum,nom_du_polluant,date_deb,date_fin,pas_temps):  #fonction1
    idnum="'"+idnum+"'"

    nom_du_polluant='"'+nom_du_polluant+'"'
    heure=" 00:00:00+00"
    date_deb="'"+conversion_dates(date_deb)+heure+"'"
    date_fin=modif_date_fin(conversion_dates(date_fin))
    date_fin="'"+date_fin+heure+"'"
    dico,jours=liste_jours(date_deb,date_fin,pas_temps)
    
    
    
    c.execute(f"SELECT date_debut,valeur,unite FROM 'moyennes-journalieres' WHERE code_station={idnum} \
              and nom_poll={nom_du_polluant} and date_debut>={date_deb} and date_debut<={date_fin} order by date_debut")
    donnees = c.fetchall()
    dates=[]
    j=0
    while dico[donnees[j][0][:10]]<dico[jours[0]]: #trouve indice dans donnees de la premiere date de jours
        j+=1
    for i in range(len(jours)-1):
        ind1,ind2=dico[jours[i]],dico[jours[i+1]]-1
        compteur=0
        somme=0 
        while j<len(donnees) and dico[donnees[j][0][:10]]<=ind2 :
            if donnees[j][1] is not None:
                unite=donnees[j][2]
                compteur+=1
                somme+=float(donnees[j][1])
            j+=1
        if compteur!=0 and somme!=0:
            dates.append({'date':jours[i],'concentration':round(somme/compteur,1),'unite':unite})    
    return dates

def taux_pollution(taux,nom_du_polluant,valeur):

    ind=sorted(taux[nom_du_polluant]+[valeur])
    j=0
    couleur=["green","yellow","orange","red"]
    while ind[j]!=valeur:
        j+=1
    return couleur[j]
        
#d1,d2=liste_dates('FR07004','ozone')

#print(historique('FR20065','particules PM10','2019/10/23','2020/10/22','day'))

# retourne la liste des stations (id et nom) et leurs coordonnées X et Y (type float)
def location():  #fonction2
    c.execute("SELECT distinct code_station,X,Y,nom_station FROM 'moyennes-journalieres'")
    donnees = c.fetchall()
    coord=[{'id':d[0],'X':d[1],'Y':d[2],'nom_station':d[3]} for d in donnees]
    return coord


def carte_pollution(nom_du_polluant,date):
    #nom_du_polluant="'"+nom_du_polluant+"'"
    nom_du_polluant='"'+nom_du_polluant+'"'
    date = conversion_dates(date)
    heure=" 00:00:00+00"
    date="'"+date+heure+"'"
    c.execute(f"SELECT code_station,valeur,unite FROM 'moyennes-journalieres' WHERE nom_poll = {nom_du_polluant} AND date_debut = {date}")
    liste_concentrations = c.fetchall()
    taux={"dioxyde d'azote":[40,90,230],"ozone":[50,100,240],"particules PM10":[20,40,100],"monoxyde de carbone":[2,7.5,10],"dioxyde de soufre":[100,300,500],"particules PM2,5":[10,25,50],"benzène":[3,5,10],"oxydes d'azote":[40,90,230],"monoxyde d'azote":[40,90,230]}
    unite=liste_concentrations[0][2]
    data=[]
    for d in liste_concentrations:
        if d[1] is not None:
            data.append({'id':d[0],'couleur':taux_pollution(taux,nom_du_polluant[1:-1],float(d[1]))})
    return data,taux[nom_du_polluant[1:-1]],unite

#print(carte_pollution("dioxyde d'azote", "2019/11/23"))

def get_tout_polluants():
    c.execute("SELECT distinct nom_poll FROM 'moyennes-journalieres' ")
    donnees = c.fetchall()
    nom_poll=[{'nom_du_polluant':donnee[0]} for donnee in donnees]
    return nom_poll




def liste_stations(nom_du_polluant):
    nom_du_polluant='"'+nom_du_polluant+'"'
    c.execute(f"SELECT distinct nom_station,code_station FROM 'moyennes-journalieres' where nom_poll={nom_du_polluant}")
    donnees = c.fetchall()
    stations=[{'id':donnee[1],'nom_station':donnee[0]} for donnee in donnees]
    return stations
    

#print(liste_stations('ozone'))


def intersection_dates(nom_du_polluant,liste_idnum): #stations est une liste de stations
    dates_min=[liste_dates(idnum,nom_du_polluant)[0] for idnum in liste_idnum]
    dates_max=[liste_dates(idnum,nom_du_polluant)[1] for idnum in liste_idnum]
    return(max(dates_min),min(dates_max))  #en format tirets

#print(intersection_dates('ozone',['FR07004','FR07009']))  

def comparaison(liste_idnum,nom_du_polluant,date_deb,date_fin,pas_temps,):
    return [historique(idnum, nom_du_polluant, date_deb, date_fin, pas_temps) for idnum in liste_idnum]
 

def nom_station(liste_idnum):
    noms=[]
    for idnum in liste_idnum:
        idnum='"'+idnum+'"'
        c.execute(f"SELECT distinct nom_station FROM 'moyennes-journalieres' where code_station={idnum}")
        donnees = c.fetchall()
        noms.append(donnees[0][0])
    return noms
        
#print(nom_station(['FR07004','FR07009']))    

#print(comparaison(['FR07004','FR07009'],'ozone','2010/01/01','2020/10/24','month'))

import numpy as np
import matplotlib.pyplot as pl

def trace(donnees):
    pl.close()
   
    courbes=[]
    for donnee in donnees:
        n=len(donnee)
        abcisse=np.linspace(1,n,n)
        pl.plot(abcisse,[d['concentration'] for d in donnee])

    pl.show()
    
#trace(comparaison(['FR07004','FR07009'],'ozone','2020/09/01','2020/10/24','day'))    
        
        
    

