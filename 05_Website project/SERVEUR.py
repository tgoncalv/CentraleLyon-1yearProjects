# TD3-lieux-insolites.py

# Application exemple : affichage de mes lieux préférés à la Croix-Rousse 2018-10-24 coucou c taiga

import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, unquote
import json
import sqlite3
import fonctions_sql as sql_func

import matplotlib.pyplot as plt
import datetime as dt
import matplotlib.dates as pltd
import os.path

# définition du handler
class RequestHandler(http.server.SimpleHTTPRequestHandler):
    static_dir = '/client'
    server_version = 'Projet_groupeB.py/0.1'
    
    def do_GET(self):
        self.init_params()
        
        if self.path_info[0] == "location":
            #HTML
            #send_locationsHTML()
            
            #JSON
            self.send_locationsJSON()
            
        elif self.path_info[0] == "selection":
            self.send_selection()
                
        elif self.path_info[0] == "polluant":
            self.send_polluant()
            
        elif self.path_info[0] == "carte_pollution":
            self.send_carte_pollution()
            
        elif self.path_info[0] == "polluant_date":
            self.send_polluant_date()
            #self.send_test()
        
        elif self.path_info[0] == "comparaison":
            self.send_comparaison()
            
        elif self.path_info[0] == "dates_intersect":
            self.send_dates_intersect()
        
        elif self.path_info[0] == "stations_polluant":
            self.send_stations_polluant()
            
        elif self.path_info[0] == "service":
            self.send_html('<p>Path info : <code>{}</p><p>Chaîne de requête : <code>{}</code></p>' \
                           .format('/'.join(self.path_info),self.query_string));
        
        else:
            self.send_static()
            
    def do_HEAD(self):
        self.send_static()
        
    def do_POST(self):
        self.init_params()
        if self.path_info[0] == "service":
            self.send_html(('<p>Path info : <code>{}</code></p><p>Chaîne de requête : <code>{}</code></p>' \
                            + '<p>Corps :</p><pre>{}</pre>').format('/'.join(self.path_info),self.query_string,self.body));
        else:
            self.send_error(405)
            
            
            
    def send_static(self):
        self.path = self.static_dir + self.path
        if (self.command=='HEAD'):
            http.server.SimpleHTTPRequestHandler.do_HEAD(self)
        else:
            http.server.SimpleHTTPRequestHandler.do_GET(self)
            
    
      
          
    # on appelle la méthode parent (do_GET ou do_HEAD)
    # à partir du verbe HTTP (GET ou HEAD)
    
    # on envoie un document html dynamique
    def send_html(self,content):
        headers = [('Content-Type','text/html;charset=utf-8')]
        html = '<!DOCTYPE html><title>{}</title><meta charset="utf-8">{}' \
            .format(self.path_info[0],content)
        self.send(html,headers)
        
    def send_json(self,data,headers=[]):
        body = bytes(json.dumps(data),'utf-8') # encodage en json et UTF-8
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',int(len(body)))
        [self.send_header(*t) for t in headers]
        self.end_headers()
        self.wfile.write(body)
    
    def send(self,body,headers=[]):
        encoded = bytes(body, 'UTF-8')
        self.send_response(200)
        [self.send_header(*t) for t in headers]
        self.send_header('Content-Length',int(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)
        
        
    def init_params(self):
        info = urlparse(self.path)
        self.path_info = [unquote(v) for v in info.path.split('/')[1:]]
        self.query_string = info.query
        self.params = parse_qs(info.query)
        length = self.headers.get('Content-Length')
        ctype = self.headers.get('Content-Type')
        if length:
            self.body = str(self.rfile.read(int(length)),'utf-8')
            if ctype == 'application/x-www-form-urlencoded' : 
                self.params = parse_qs(self.body)
        else:
            self.body = ''
        print('info_path =',self.path_info)
        print('body =',length,ctype,self.body)
        print('params =', self.params)
        
    def send_locationsHTML(self):
        conn = sqlite3.connect('2020.db')
        c = conn.cursor()
        
        c.execute("SELECT id,X,Y,label FROM 'Stations-2020'")
        r = c.fetchall()
        
        txt = 'Liste des {} locations :\n'.format(len(r))
        txt = txt + '{}\n'.format(r[0])
    
        headers = [('Content-Type','text/plain;charset=utf-8')]
        self.send(txt,headers)
        
    def send_locationsJSON(self):
        data_test=[{'id':1,'Y':45.76843,'X':4.82667,'nom_station':"Rue Couverte"},\
                  {'id':2,'Y':45.77128,'X':4.83251,'nom_station':"Rue Caponi"}]
        data = sql_func.location()
        self.send_json(data)
        
    def send_polluant(self):
        idnum = self.path_info[1]   #FR0011-FR0130-
        nom_du_polluant = self.path_info[2]
        nom_du_polluant = self.conversion_espace(nom_du_polluant)
        nom_du_polluant = self.conversion_accent(nom_du_polluant)
        date_deb = self.path_info[3]
        date_fin = self.path_info[4]
        pas_temps = self.path_info[5]
        
        #On teste si le ficher existe déjà
        fichier = 'courbes/polluant_'+idnum+'_'+nom_du_polluant+'_'+date_deb+'_'+date_fin+'_'+pas_temps+'.png'
        if os.path.exists(fichier):
            body = json.dumps({
                'title': 'Concentration du polluant '+nom_du_polluant, \
                'img': '/'+fichier \
                });
            headers = [('Content-Type','application/json')];
            self.send(body,headers)
            return
            
        
        
        data = sql_func.historique(idnum,nom_du_polluant,date_deb,date_fin,pas_temps)
        
        unite_concentration = data[0]['unite']
        
        fig1 = plt.figure(figsize=(10,5))
        ax = fig1.add_subplot(111)
        # ax.set_ylim(bottom=80,top=100)
        ax.grid(which='major', color='#888888', linestyle='-')
        ax.grid(which='minor',axis='x', color='#888888', linestyle=':')
        
        #ax.xaxis.set_major_locator(pltd.YearLocator())
        #ax.xaxis.set_minor_locator(pltd.MonthLocator())
        if pas_temps == 'day':
            ann_deb = int(date_deb[:4])
            ann_fin = int(date_fin[:4])
            mon_deb = int(date_deb[5:7])
            mon_fin = int(date_fin[5:7])
            day_deb = int(date_deb[8:10])
            day_fin = int(date_fin[8:10])
            ecart_day = 365*(ann_fin-ann_deb)+30*(mon_fin-mon_deb)+day_fin-day_deb
            if ecart_day <= 16:
                ax.xaxis.set_major_locator(pltd.DayLocator())
                ax.xaxis.set_minor_locator(pltd.HourLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 0.8
                
            if ecart_day >= 17 and ecart_day <= 112:
                ax.xaxis.set_major_locator(pltd.WeekdayLocator())
                ax.xaxis.set_minor_locator(pltd.DayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 0.8
                
            if ecart_day >= 113 and ecart_day <= 480:
                ax.xaxis.set_major_locator(pltd.MonthLocator())
                ax.xaxis.set_minor_locator(pltd.WeekdayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 0.8
                
            if ecart_day >= 481:
                ax.xaxis.set_major_locator(pltd.YearLocator())
                ax.xaxis.set_minor_locator(pltd.MonthLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m'))
                ax.xaxis.set_tick_params(labelsize=10)  
                largeur_requise = 0.8
                
            
        elif pas_temps == 'week':
            ann_deb = int(date_deb[:4])
            ann_fin = int(date_fin[:4])
            mon_deb = int(date_deb[5:7])
            mon_fin = int(date_fin[5:7])
            day_deb = int(date_deb[8:10])
            day_fin = int(date_fin[8:10])
            ecart_week = (12*(ann_fin-ann_deb)+mon_fin-mon_deb)*4
            if ecart_week <= 12:
                ax.xaxis.set_major_locator(pltd.WeekdayLocator())
                ax.xaxis.set_minor_locator(pltd.DayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 4
            if ecart_week >= 13 and ecart_week <= 48:
                ax.xaxis.set_major_locator(pltd.MonthLocator())
                ax.xaxis.set_minor_locator(pltd.WeekdayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m'))
                ax.xaxis.set_tick_params(labelsize=8)  
                largeur_requise = 4
            if ecart_week >= 49:
                ax.xaxis.set_major_locator(pltd.YearLocator())
                ax.xaxis.set_minor_locator(pltd.MonthLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 4
        
        elif pas_temps == 'month':
            ann_deb = int(date_deb[:4])
            ann_fin = int(date_fin[:4])
            mon_deb = int(date_deb[5:7])
            mon_fin = int(date_fin[5:7])
            ecart_mon = 12*(ann_fin-ann_deb)+mon_fin-mon_deb
            if ecart_mon <=15:
                ax.xaxis.set_major_locator(pltd.MonthLocator())
                ax.xaxis.set_minor_locator(pltd.WeekdayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8)  
                largeur_requise = 16
            if ecart_mon >=16:
                ax.xaxis.set_major_locator(pltd.YearLocator())
                ax.xaxis.set_minor_locator(pltd.MonthLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 16
        
        else:
            ax.xaxis.set_major_locator(pltd.YearLocator())
            ax.xaxis.set_minor_locator(pltd.MonthLocator())
            ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
            ax.xaxis.set_tick_params(labelsize=8) 
            largeur_requise = 0.8
        
                                                            
        
        
        
        
        ax.xaxis.set_label_text("Date")
        ax.yaxis.set_label_text("concentration du polluant en {}".format(unite_concentration))
        
        ### historique(idnum,nom_du_polluant)
        """
        idnum="'"+idnum+"'"
        nom_du_polluant="'"+nom_du_polluant+"'"
        c.execute(f"SELECT date_debut,valeur FROM 'moyennes-journalieres' WHERE code_station={idnum} and nom_poll={nom_du_polluant} order by date_debut")
        donnees = c.fetchall()
        dates=[]
        for donnee in donnees:
            if donnee[1] is not None:
                dates.append({'date':donnee[0][:10],'concentration':float(donnee[1])})
        """
        
        x = [pltd.date2num(dt.date(int(a["date"][:4]),int(a["date"][5:7]),int(a["date"][8:10]))) for a in data]
        y = [float(a["concentration"]) for a in data]
        #plt.plot(x,y,linewidth=1, linestyle='-', marker='o', color='red')
        plt.bar(x,y,color='red',width=largeur_requise)
        
        
        #plt.legend(loc='lower left')
        #plt.title('Concentration du polluant {} en {}'.format(nom_du_polluant,unite_concentration),fontsize=16)
        
        #Obligation de créer un nouveau fichier à chaque fois, sinon ça coince
        fichier = 'courbes/polluant_'+idnum+'_'+nom_du_polluant+'_'+date_deb+'_'+date_fin+'_'+pas_temps+'.png'
        #fichier = 'courbes/img_graph.png'
        plt.savefig('client/{}'.format(fichier))
        plt.close()
        
        body = json.dumps({
            'title': 'Concentration du polluant '+nom_du_polluant, \
            'img': '/'+fichier \
            });
        
        headers = [('Content-Type','application/json')];
        self.send(body,headers)
        
    def send_comparaison(self):
        
        nom_du_polluant = self.path_info[1]
        nom_du_polluant = self.conversion_espace(nom_du_polluant)
        nom_du_polluant = self.conversion_accent(nom_du_polluant)
        list_idnum = self.path_info[2]
        list_idnum = self.creation_list_idnum(list_idnum)
        #list_idnum= "[FR0011,..]"
        date_deb = self.path_info[3]
        date_fin = self.path_info[4]
        pas_temps = self.path_info[5]
        
        #On teste si le ficher existe déjà
        list_idnum_txt = "{}".format(list_idnum)
        fichier = 'courbes/comparaison_'+nom_du_polluant+'_'+list_idnum_txt+'_'+date_deb+'_'+date_fin+'_'+pas_temps+'.png'
        if os.path.exists(fichier):
            body = json.dumps({
                'title': 'Comparaison du polluant '+nom_du_polluant, \
                'img': '/'+fichier \
                });
            headers = [('Content-Type','application/json')];
            self.send(body,headers)
            return
            
        
        DATA = []
        for id_num in list_idnum:
            data = sql_func.historique(id_num,nom_du_polluant,date_deb,date_fin,pas_temps)
            DATA.append(data)
        
        
        unite_concentration = DATA[0][0]['unite']
        
        fig1 = plt.figure(figsize=(10,5))
        ax = fig1.add_subplot(111)
        # ax.set_ylim(bottom=80,top=100)
        ax.grid(which='major', color='#888888', linestyle='-')
        ax.grid(which='minor',axis='x', color='#888888', linestyle=':')
        
        #ax.xaxis.set_major_locator(pltd.YearLocator())
        #ax.xaxis.set_minor_locator(pltd.MonthLocator())
        if pas_temps == 'day':
            ann_deb = int(date_deb[:4])
            ann_fin = int(date_fin[:4])
            mon_deb = int(date_deb[5:7])
            mon_fin = int(date_fin[5:7])
            day_deb = int(date_deb[8:10])
            day_fin = int(date_fin[8:10])
            ecart_day = 365*(ann_fin-ann_deb)+30*(mon_fin-mon_deb)+day_fin-day_deb
            if ecart_day <= 16:
                ax.xaxis.set_major_locator(pltd.DayLocator())
                ax.xaxis.set_minor_locator(pltd.HourLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 0.8
                
            if ecart_day >= 17 and ecart_day <= 112:
                ax.xaxis.set_major_locator(pltd.WeekdayLocator())
                ax.xaxis.set_minor_locator(pltd.DayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 0.8
                
            if ecart_day >= 113 and ecart_day <= 480:
                ax.xaxis.set_major_locator(pltd.MonthLocator())
                ax.xaxis.set_minor_locator(pltd.WeekdayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 0.8
                
            if ecart_day >= 481:
                ax.xaxis.set_major_locator(pltd.YearLocator())
                ax.xaxis.set_minor_locator(pltd.MonthLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m'))
                ax.xaxis.set_tick_params(labelsize=10)  
                largeur_requise = 0.8
                
            
        elif pas_temps == 'week':
            ann_deb = int(date_deb[:4])
            ann_fin = int(date_fin[:4])
            mon_deb = int(date_deb[5:7])
            mon_fin = int(date_fin[5:7])
            day_deb = int(date_deb[8:10])
            day_fin = int(date_fin[8:10])
            ecart_week = (12*(ann_fin-ann_deb)+mon_fin-mon_deb)*4
            if ecart_week <= 12:
                ax.xaxis.set_major_locator(pltd.WeekdayLocator())
                ax.xaxis.set_minor_locator(pltd.DayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 4
            if ecart_week >= 13 and ecart_week <= 48:
                ax.xaxis.set_major_locator(pltd.MonthLocator())
                ax.xaxis.set_minor_locator(pltd.WeekdayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m'))
                ax.xaxis.set_tick_params(labelsize=8)  
                largeur_requise = 4
            if ecart_week >= 49:
                ax.xaxis.set_major_locator(pltd.YearLocator())
                ax.xaxis.set_minor_locator(pltd.MonthLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 4
        
        elif pas_temps == 'month':
            ann_deb = int(date_deb[:4])
            ann_fin = int(date_fin[:4])
            mon_deb = int(date_deb[5:7])
            mon_fin = int(date_fin[5:7])
            ecart_mon = 12*(ann_fin-ann_deb)+mon_fin-mon_deb
            if ecart_mon <=15:
                ax.xaxis.set_major_locator(pltd.MonthLocator())
                ax.xaxis.set_minor_locator(pltd.WeekdayLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8)  
                largeur_requise = 16
            if ecart_mon >=16:
                ax.xaxis.set_major_locator(pltd.YearLocator())
                ax.xaxis.set_minor_locator(pltd.MonthLocator())
                ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
                ax.xaxis.set_tick_params(labelsize=8) 
                largeur_requise = 16
        
        else:
            ax.xaxis.set_major_locator(pltd.YearLocator())
            ax.xaxis.set_minor_locator(pltd.MonthLocator())
            ax.xaxis.set_major_formatter(pltd.DateFormatter('%Y %m %d'))
            ax.xaxis.set_tick_params(labelsize=8) 
            largeur_requise = 0.8
        
                                                            
        
        
        
        
        ax.xaxis.set_label_text("Date")
        ax.yaxis.set_label_text("concentration du polluant en {}".format(unite_concentration))
        
        ### historique(idnum,nom_du_polluant)
        """
        idnum="'"+idnum+"'"
        nom_du_polluant="'"+nom_du_polluant+"'"
        c.execute(f"SELECT date_debut,valeur FROM 'moyennes-journalieres' WHERE code_station={idnum} and nom_poll={nom_du_polluant} order by date_debut")
        donnees = c.fetchall()
        dates=[]
        for donnee in donnees:
            if donnee[1] is not None:
                dates.append({'date':donnee[0][:10],'concentration':float(donnee[1])})
        """
        
        #datax=DATA[0]
        #x = [pltd.date2num(dt.date(int(a["date"][:4]),int(a["date"][5:7]),int(a["date"][8:10]))) for a in datax]
        Y=[]
        X=[]
        for i in range(len(list_idnum)):
            data = DATA[i]
            y = [float(a["concentration"]) for a in data]
            x = [pltd.date2num(dt.date(int(a["date"][:4]),int(a["date"][5:7]),int(a["date"][8:10]))) for a in data]
            X.append(x)
            Y.append(y)
        
        
        #plt.plot(x,y,linewidth=1, linestyle='-', marker='o', color='red')
        #list_noms = [sql_func.liste_stations(nom_du_polluant)[i]['nom_station'] for i in range(len(list_idnum))]
        list_noms = sql_func.nom_station(list_idnum)
        lines=[]
        i=0
        for k in range(len(Y)):
            #plt.plot(x,y)
            x=X[k]
            y=Y[k]
            local_line, = plt.plot(x,y, label='{}'.format(list_noms[i]))
            lines.append(local_line)
            i+=1
        
        
        
        #plt.legend(loc='lower left')
        plt.legend(handles=lines)
        #plt.title('Concentration du polluant {} en {}'.format(nom_du_polluant,unite_concentration),fontsize=16)
        
        #Obligation de créer un nouveau fichier à chaque fois, sinon ça coince
        fichier = 'courbes/comparaison_'+nom_du_polluant+'_'+list_idnum_txt+'_'+date_deb+'_'+date_fin+'_'+pas_temps+'.png'
        #fichier = 'courbes/img_graph.png'
        plt.savefig('client/{}'.format(fichier))
        plt.close()
        
        body = json.dumps({
            'title': 'Comparaison du polluant '+nom_du_polluant, \
            'img': '/'+fichier \
            });
        
        headers = [('Content-Type','application/json')];
        self.send(body,headers)
        
        
    def send_selection(self):
        idnum = self.path_info[1]
        data = sql_func.get_polluants(idnum)
        self.send_json(data)
        
        
        """
        data=[{'id':1,'desc':"Il ne faut pas être <b>trop grand</b> pour marcher dans cette rue qui passe sous une maison"},\
                  {'id':2,'desc':"Cette rue est <b>si étroite</b> qu'on touche les 2 côtés en tendant les bras !"}]
        for c in data:
            if c['id'] == int(self.path_info[1]):
                self.send_json(c)
                break
        """
        
    def send_carte_pollution(self):
        nom_du_polluant = self.path_info[1]
        nom_du_polluant = self.conversion_espace(nom_du_polluant)
        nom_du_polluant = self.conversion_accent(nom_du_polluant)
        date = self.path_info[2]
        data = sql_func.carte_pollution(nom_du_polluant,date)
        
        self.send_json(data)

        
    def send_polluant_date(self):
        idnum = self.path_info[1]
        nom_du_polluant = self.path_info[2]
        nom_du_polluant = self.conversion_espace(nom_du_polluant)
        nom_du_polluant = self.conversion_accent(nom_du_polluant)
        data = sql_func.liste_dates(idnum,nom_du_polluant)
        self.send_json(data)
        
    def send_test(self):
        data = self.path_info[1]
        self.send_json(data)
        
    def conversion_espace(self,mot):
        for i in range(len(mot)):
            if mot[i] == "%" and mot[i+1] == "2":
                mot1=mot[:i]
                mot2=mot[(i+3):]
                maus=mot1+' '+mot2
                return maus
        return mot
    
    def conversion_datetonum(self,date):
        ann = int(date[:4])*365
        mon = int(date[5:7])*30
        day = int(date[8:10])
        num = ann+mon+day
        return num
    
    def conversion_accent(self,mot):
        for i in range(len(mot)):
            if mot[i] == "%" and mot[i+1] == "C":
                mot1=mot[:i]
                mot2=mot[(i+6):]
                maus=mot1+'è'+mot2
                return maus
        return mot
    
    def send_dates_intersect(self):
        list_idnum = self.path_info[1]
        list_idnum = self.creation_list_idnum(list_idnum)
        nom_du_polluant = self.path_info[2]
        nom_du_polluant = self.conversion_espace(nom_du_polluant)
        nom_du_polluant = self.conversion_accent(nom_du_polluant)
        data = sql_func.intersection_dates(nom_du_polluant,list_idnum)
        self.send_json(data)
        
    def send_stations_polluant(self):
        nom_du_polluant = self.path_info[1]
        nom_du_polluant = self.conversion_espace(nom_du_polluant)
        nom_du_polluant = self.conversion_accent(nom_du_polluant)
        data = sql_func.liste_stations(nom_du_polluant)
        self.send_json(data)
        
    def creation_list_idnum(self,chaine):
        cpt = 0
        pos_virgule = []
        chaine = ","+chaine
        chaine = chaine+","
        for i in range(len(chaine)):
            if chaine[i] == ",":
                cpt+=1
                pos_virgule.append(i)
        longueur = cpt-1
        list_idnum = []
        for i in range(longueur):
            list_idnum.append("{}".format(chaine[(pos_virgule[i]+1):pos_virgule[i+1]]))
        return list_idnum









# instanciation et lancement du serveur
PORT = 8088
httpd = socketserver.TCPServer(("", PORT), RequestHandler)
print ("serveur sur port : {}".format(PORT))
httpd.serve_forever()
