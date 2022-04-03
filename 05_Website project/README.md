D1b - Groupe B
Mesure de la pollution atmosphérique en Auvergne Rhône-Alpes 

Membres:
Taiga GONCALVES --> CSS/HTML
Jonathan GUERIN --> Serveur
Timothee BARRY  --> SQL/BDD 


--> Démarrer le code SERVEUR.py
--> Accéder à http://localhost:8088/Projet_groupeB.html

==> Le site est constitué d'une carte intéractive et d'un menu en bas:

###############################################
# HISTORIQUE DES CONCENTRATIONS DES POLLUANTS #
###############################################
1. Choisir une station en cliquant sur un marqueur bleu ou en utilisant le sélecteur de station
2. Choisir le type de polluant
3. Choisir une date de début et de fin (par défaut, la date minimale et maximale)
4. Choisir un pas de temps (par défaut, le jour)

==> Un graphe apparaît, avec la concentration d'un polluant particulier pour une certaine station en fonction du temps

Remarque 1: Choisir "CHOISIR UNE STATION" pour ne plus afficher de graphes


######################
# Carte de pollution #
######################
1. Choisir un polluant
2. Choisir une date (par défaut, la date minimale)

==> La carte intéractive s'actualise, avec des cercles indiquant le niveau de pollution autour de chaque station

Remarque 1: Il n'y a aucun cercle pour les stations ne possédant pas les données voulues
Remarque 2: Utilisez la légende pour comprendre les codes couleurs (la légende change en fonction du polluant)
Remarque 3: Les boutons "<<<" et ">>>" permettent de sélectionner la date minimale ou maximale
Remarque 4: Les boutons "<<" et ">>" permettent de faire un bond de 10 jours dans les dates
Remarque 5: Les boutons "<" et ">" permettent de faire un bond de 1 jour dans les dates
Remarque 6: Choisir "CHOISIR UN POLLUANT" pour effacer les cercles
Remarque 7: Utiliser les bouttons "Afficher les marqueurs" et "Cacher les marqueurs" pour mieux visualiser la carte de pollution


##########################
# COMPARAISON DE DONNEES #
##########################
1. Choisir un polluant
2. Sélectionner au moins une stations
3. Choisir une date de début et de fin (par défaut, la date minimale et maximale)
4. Choisir un pas de temps (par défaut, le jour)

==> Plusieurs graphe apparaissent, avec des concentrations d'un polluant particulier pour plusieurs stations

Remarque 1: Déselectionner toutes les stations ou sélectionner "CHOISIR UN POLLUANT" pour ne plus afficher de graphes


########
# INFO #
########
Affiche des informations complémentaires
