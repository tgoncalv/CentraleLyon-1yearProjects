# -*- coding: utf-8 -*-
"""
Created on Tue Oct 13 08:00:27 2020

@author: taiga
"""

from tkinter import *
from tkinter import colorchooser
from seance5_4h_formes import *
from random import randint
import sqlite3

class ZoneAffichage(Canvas):
    def __init__(self, master, largeur, hauteur):
        Canvas.__init__(self, master, width=largeur, height=hauteur)
        self.__1=Rectangle(self,50,280,100,5,'black')
        self.__2=Rectangle(self,98,40,6,240,'black')
        self.__3=Rectangle(self,98,40,150,6,'black')
        self.__4=Rectangle(self,248,40,6,50,'black')
        self.__5=Ellipse(self,251,98,20,20,'black')
        self.__6=Rectangle(self,248,118,6,80,'black')
        self.__7=Rectangle(self,214,148,74,6,'black')
        self.__8=Rectangle(self,241,198,20,6,'black')
        self.__9=Rectangle(self,241,198,6,60,'black')
        self.__10=Rectangle(self,255,198,6,60,'black')
        
    
    def Dessin(self,nb_tentatives,s):
        if nb_tentatives==1:
            self.__1.setState(s)
        elif nb_tentatives==2:
            self.__2.setState(s)
        elif nb_tentatives==3:
            self.__3.setState(s)
        elif nb_tentatives==4:
            self.__4.setState(s)
        elif nb_tentatives==5:
            self.__5.setState(s)
        elif nb_tentatives==6:
            self.__6.setState(s)
        elif nb_tentatives==7:
            self.__7.setState(s)
        elif nb_tentatives==8:
            self.__8.setState(s)
        elif nb_tentatives==9:
            self.__9.setState(s)
        elif nb_tentatives==10:
            self.__10.setState(s)
            
        
        
class MonBoutonLettre(Button):
    def __init__(self, fenetre, frame,texte):
        Button.__init__(self, frame, text= texte, command=self.cliquer, padx=0, pady=5, width=8, borderwidth='3', state=DISABLED)
        self.__text=texte
        self.__fen=fenetre
                    
    def cliquer(self):
        self.config(state=DISABLED)
        self.__fen.traitement(self.__text)
                  

class FenPrincipale(Tk):
    def __init__(self):
        Tk.__init__(self)
        
        #Couleurs
        self.__color_bg='dodgerblue'
        self.__color_canvas='darkorange'
        self.__end_text='red'
        self.__color_contour_bouttons='white'
        self.__color_buttonNewParty_bg='SystemButtonFace'
        self.__color_buttonNewParty_fg='black'
        self.__color_buttonNewParty_active='SystemButtonFace'
        self.__color_buttonQuit_bg='SystemButtonFace'
        self.__color_buttonQuit_fg='black'
        self.__color_buttonQuit_active='SystemButtonFace'
        self.__color_buttonColor_bg='SystemButtonFace'
        self.__color_buttonColor_fg='black'
        self.__color_buttonColor_active='SystemButtonFace'
        self.__color_buttonTriche_bg='SystemButtonFace'
        self.__color_buttonTriche_fg='black'
        self.__color_buttonTriche_active='SystemButtonFace'
        
        #arbre de scène
        self.configure(bg=self.__color_bg)
        self.title('Jeu du pendu')
        self.__barreOutils = Frame(self,bg=self.__color_contour_bouttons)
        self.__barreOutils.pack(side=TOP,pady=5)
        self.__buttonNewParty = Button(self.__barreOutils, text='Nouvelle partie', width=15, borderwidth='2',
                                bg=self.__color_buttonNewParty_bg,fg=self.__color_buttonNewParty_fg,activebackground=self.__color_buttonNewParty_active)
        self.__buttonNewParty.pack(side=LEFT, padx=3,pady=3)
        self.__buttonQuit = Button(self.__barreOutils, text='Quitter', width=15, borderwidth='2',
                            bg=self.__color_buttonQuit_bg,fg=self.__color_buttonQuit_fg,activebackground=self.__color_buttonQuit_active)
        self.__buttonQuit.pack(side=LEFT, padx=3,pady=3)
        
        self.__barreOptions = Frame(self)
        self.__barreOptions.pack(side=BOTTOM,pady=2)
        self.__buttonColor = Button(self.__barreOptions, text='Couleurs', width=10, borderwidth='2',
                             bg=self.__color_buttonColor_bg,fg=self.__color_buttonColor_fg,activebackground=self.__color_buttonColor_active)
        self.__buttonColor.pack(side=LEFT,padx=1,pady=1)
        self.__buttonTriche = Button(self.__barreOptions, text='Tricher', width=10, borderwidth='2',
                              bg=self.__color_buttonTriche_bg,fg=self.__color_buttonTriche_fg,activebackground=self.__color_buttonTriche_active)
        self.__buttonTriche.pack(side=LEFT,padx=1,pady=1)

        self.__buttonColor.config(command=self.color)
        self.__buttonTriche.config(command=self.triche)
        
        self.__score = Frame(self)
        self.__score.pack(side=TOP,pady=4,padx=10)
        self.__afficher_score = Label(self.__score)
        self.__afficher_score.grid(row=0,column=0,padx=5)
        self.__buttonUsername = Button(self.__score, text="Changer d'utilisateur",borderwidth=2,width=18)
        self.__buttonUsername.grid(row=0,column=1,pady=1)
        
        
        self.__UsernameID=0 #Utilisateur par défaut
        self.__score_user=self.LoadScore()
        
        self.__buttonUsername.config(command=self.ChooseUsername)
        




        self.__canvas = ZoneAffichage(self,400,300)
        self.__canvas.pack(side=TOP, padx=8, pady=2)
        self.__canvas.configure(bg=self.__color_canvas)
        self.__mot= Label(self, text = 'Mot: ')
        self.__mot.pack(side=TOP, padx=2, pady=7)
        self.__clavier = Frame(self,bg=self.__color_contour_bouttons)
        self.__clavier.pack(side=TOP)
        
        self.__perdu=self.__canvas.create_text(200,130,fill=self.__end_text,font=('calibri',30),
                        text="Vous avez perdu....",state='hidden')
        self.__gagne=self.__canvas.create_text(200,130,fill=self.__end_text,font=('calibri',30),
                        text="Vous avez gagné !!",state='hidden')
        

        
        self.__buttonQuit.config(command=self.destroy)
        
        
        
        self.__buttons = [MonBoutonLettre(self, self.__clavier, chr(ord('A')+i)) for i in range(26)]
        for i in range(26):
            self.__buttons[i].grid(row=i//7+1, column=i%7)
            if i in range(21,26):
                self.__buttons[i].grid(row=4, column=i%7+1)
        
        
                
        self.__buttonNewParty.config(command=self.NewParty)
        
        self.__essais=[] #Mémorise les lettres qu'on sélectionne dans l'ordre
        
    def chargeMots(self):
    	f = open('seance5_4h_mots.txt','r')
    	s = f.read()
    	self.__mots = s.split('\n')
    	f.close()

        
    def NewParty(self):
        self.__essais=[]
        self.__canvas.itemconfig(self.__gagne,state='hidden')
        self.__canvas.itemconfig(self.__perdu,state='hidden')
        for i in range(1,11):
            self.__canvas.Dessin(i,'hidden') #Cache toutes les figures
        self.__win=False
        self.__fautes=0
        self.chargeMots()
        self.__reponse=self.__mots[randint(0,len(self.__mots)-1)] #On met -1 car le dernier element de la liste n'est pas un mot
        self.__motAffiche='*'*len(self.__reponse)
        self.__mot.config(text='Mot: '+self.__motAffiche)
        for i in range(26):
            self.__buttons[i].config(state=NORMAL)

        
    def traitement(self,lettre):
        trouve=False #indique si la lettre est utilisée dans la mot à trouver
        self.__essais+=[lettre]
        for i in range(len(self.__reponse)):
            if lettre==self.__reponse[i]:
                motAffiche=self.__motAffiche[:i]+lettre+self.__motAffiche[i+1:]
                self.__motAffiche=motAffiche
                self.__mot.config(text='Mot: '+self.__motAffiche)
                trouve=True
        if not trouve:
            self.__fautes+=1
            self.__canvas.Dessin(self.__fautes,"normal")
        if self.__motAffiche==self.__reponse:
            self.__win=True
        if self.__win==True or self.__fautes==10:
            for i in range(26):
                self.__buttons[i].config(state=DISABLED)
            if self.__win==True:
                self.__canvas.itemconfig(self.__gagne,state='normal')
            else:
                self.__canvas.itemconfig(self.__perdu,state='normal')
            conn = sqlite3.connect('pendu.db')
            curseur = conn.cursor()
            idpartie = curseur.execute("SELECT COUNT(idpartie) FROM Partie").fetchall()[0][0]
            curseur.execute("INSERT INTO Partie VALUES({},{},'{}',{})".format(idpartie,self.__UsernameID,self.__reponse,int(self.__win)))
            conn.commit()
            conn.close()
            self.LoadScore()
                
            
    def color(self):
        self.__buttonColor.config(state="disabled")
        self.__ColorBox=Toplevel(self)
        self.__ColorBox.title("Choix des couleurs")
        Choix=[('Arrière plan',1),('Fenêtre principale',2),('texte de fin',3),('contour des boutons',4),('Bouton "Nouvelle partie"',5),
               ('Texte "Nouvelle Partie"',6),('Bouton "Quitter"',7),('Texte "Quitter"',8),('Bouton "Couleur"',9),
               ('Texte "Couleur"',10),('Bouton "Triche"',11),('Texte "Triche"',12)]
        self.__var=IntVar()
        for text,choix in Choix:
            b = Radiobutton(self.__ColorBox,text=text,value=choix,variable=self.__var,command=self.changer_couleur,indicatoron=0)
            b.deselect()
            b.pack(anchor=W)
        self.__Button_Valider=Button(self.__ColorBox,text="Ok",width=10)
        self.__Button_Valider.pack(anchor=S)
        self.__Button_Valider.config(command=self.__ColorBox.destroy)
        self.__ColorBox.bind('<Destroy>', self.refresh)
        
    def changer_couleur(self):
        choix=self.__var.get()
        color=colorchooser.askcolor()[1]
        if choix==1:
            self.__color_bg=color
        elif choix==2:
            self.__color_canvas=color
        elif choix==3:
            self.__end_text=color
        elif choix==4:
            self.__color_contour_bouttons=color
        elif choix==5:
            self.__color_buttonNewParty_bg=color
            self.__color_buttonNewParty_active=color
        elif choix==6:
            self.__color_buttonNewParty_fg=color
        elif choix==7:
            self.__color_buttonQuit_bg=color
            self.__color_buttonQuit_active=color
        elif choix==8:
            self.__color_buttonQuit_fg=color
        elif choix==9:
            self.__color_buttonColor_bg=color
            self.__color_buttonColor_active=color
        elif choix==10:
            self.__color_buttonColor_fg=color
        elif choix==11:
            self.__color_buttonTriche_bg=color
            self.__color_buttonTriche_active=color
        elif choix==12:
            self.__color_buttonTriche_fg=color
    
        
    def refresh(self,event):
        self.__buttonColor.config(state="normal")
        self.__ColorBox.destroy()
        self.configure(bg=self.__color_bg)
        self.__canvas.configure(bg=self.__color_canvas)
        self.__canvas.itemconfig(self.__perdu,fill=self.__end_text)
        self.__canvas.itemconfig(self.__gagne,fill=self.__end_text)
        self.__barreOutils.configure(bg=self.__color_contour_bouttons)
        self.__clavier.configure(bg=self.__color_contour_bouttons)
        self.__buttonNewParty.config(bg=self.__color_buttonNewParty_bg,fg=self.__color_buttonNewParty_fg,activebackground=self.__color_buttonNewParty_active)
        self.__buttonQuit.config(bg=self.__color_buttonQuit_bg,fg=self.__color_buttonQuit_fg,activebackground=self.__color_buttonQuit_active)
        self.__buttonColor.config(bg=self.__color_buttonColor_bg,fg=self.__color_buttonColor_fg,activebackground=self.__color_buttonColor_active)
        self.__buttonTriche.config(bg=self.__color_buttonTriche_bg,fg=self.__color_buttonTriche_fg,activebackground=self.__color_buttonTriche_active)
            
                    
        
    def triche(self):
        if len(self.__essais)>0:
            
            if self.__win==True or self.__fautes==10:
                for i in range(26):
                    self.__buttons[i].config(state=NORMAL)
                    if self.__win==True:
                        self.__canvas.itemconfig(self.__gagne,state='hidden')
                    else:
                        self.__canvas.itemconfig(self.__perdu,state='hidden')
                conn = sqlite3.connect('pendu.db')
                curseur = conn.cursor()
                idpartie = curseur.execute("SELECT COUNT(idpartie) FROM Partie").fetchall()[0][0]-1
                curseur.execute("DELETE FROM Partie WHERE idpartie={}".format(idpartie))
                conn.commit()
                conn.close()
                self.LoadScore()
            
            if self.__motAffiche==self.__reponse:
                self.__win=FALSE
            
            lettre=self.__essais.pop()
            trouve=False
            for i in range(len(self.__reponse)):
                if lettre==self.__reponse[i]:
                    motAffiche=self.__motAffiche[:i]+"*"+self.__motAffiche[i+1:]
                    self.__motAffiche=motAffiche
                    self.__mot.config(text='Mot: '+self.__motAffiche)
                    trouve=True
                
            if not trouve:
                self.__canvas.Dessin(self.__fautes,"hidden")
                self.__fautes+=-1
                
            ###Réactiver la dernière lettre (attention: toutes les lettres se retrouvent désactivé si la partie était terminée)
            for i in range(26):
                lettre=chr(ord('A')+i)
                if lettre in self.__essais:
                    self.__buttons[i].config(state="disabled")
                else:
                    self.__buttons[i].config(state="normal")
    
    def ChooseUsername(self):
        self.__Choose_Username = Toplevel(self)
        self.__Choose_Username.title("Choix de l'utilisateur")
        conn = sqlite3.connect('pendu.db')
        curseur = conn.cursor()
        self.__UsernameList = curseur.execute("SELECT * FROM Joueur").fetchall()
        conn.close()
        self.__id=IntVar()
        for idjoueur,nom,prenom in self.__UsernameList:
            u = Radiobutton(self.__Choose_Username,text=nom+" "+prenom,value=idjoueur,variable=self.__id,command=self.ChangeUsername,indicatoron=0)
            u.deselect()
            u.grid(sticky=W,padx=2)
        row=len(self.__UsernameList)+2
        Label(self.__Choose_Username).grid()
        self.__Button_annuler = Button(self.__Choose_Username, text="Annuler",command=self.__Choose_Username.destroy)
        self.__Button_annuler.grid(row=row,column=1,padx=2)
        self.__Button_creerID = Button(self.__Choose_Username, text="Créer un nouvel identifiant",command=self.CreateUsername)
        self.__Button_creerID.grid(row=row,column=0,padx=2)
        
        
    def ChangeUsername(self):
        self.__UsernameID = self.__id.get()
        self.LoadScore()
        self.__Choose_Username.destroy()
    
    def CreateUsername(self):
        self.__Choose_Username.destroy()
        self.__Create_Username = Toplevel(self)
        self.__Create_Username.title("Création d'un nouvel identifiant")
        Label(self.__Create_Username,text="Nom: ").grid(row=0)
        Label(self.__Create_Username,text="Prenom: ").grid(row=1)
        self.__nom = StringVar()
        Entry(self.__Create_Username,textvariable=self.__nom).grid(row=0,column=1,pady=2)
        self.__prenom = StringVar()
        Entry(self.__Create_Username,textvariable=self.__prenom).grid(row=1,column=1,pady=2)
        self.__Button_ValiderID = Button(self.__Create_Username, text="Valider",command=self.CreateUsernameValidate)
        self.__Button_ValiderID.grid(row=2)
        self.__Button_AnnulerID = Button(self.__Create_Username, text="Annuler",command=self.CreateUsernameCancel)
        self.__Button_AnnulerID.grid(row=2,column=1,sticky=W,pady=4)

    def CreateUsernameValidate(self):
        self.__Create_Username.destroy()
        conn = sqlite3.connect('pendu.db')
        curseur = conn.cursor()
        idjoueur = curseur.execute("SELECT COUNT(idjoueur) FROM Joueur").fetchall()[0][0]
        nom = self.__nom.get()
        prenom = self.__prenom.get()
        curseur.execute("INSERT INTO Joueur VALUES({},'{}','{}')".format(idjoueur,nom,prenom))
        conn.commit()
        conn.close()
        self.ChangeUsername()
        self.ChooseUsername()
        
    def CreateUsernameCancel(self):
        self.__Create_Username.destroy()
        self.ChooseUsername()
    
    def LoadScore(self):
        conn = sqlite3.connect('pendu.db')
        curseur = conn.cursor()
        self.__Username= curseur.execute("SELECT nom,prenom FROM Joueur WHERE idjoueur={}".format(self.__UsernameID)).fetchall()[0]
        self.__UsernameScore = curseur.execute("SELECT COUNT(succes) FROM Partie WHERE idjoueur={} AND succes=1".format(self.__UsernameID)).fetchall()[0]
        self.__score_text = "Score de "+self.__Username[0]+" "+self.__Username[1]+": "+str(self.__UsernameScore[0])
        self.__afficher_score.config(text=self.__score_text)
        conn.close()
                
            
            
            
            
    
        
    
    
    
        
if __name__ == '__main__':
    fen = FenPrincipale()
    fen.mainloop()
