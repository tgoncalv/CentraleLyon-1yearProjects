// Création d'une carte dans la balise div "map", 
// et position de la vue sur un point donné et un niveau de zoom
var map = L.map('map').setView([45.775,4.83], 10);
var markers = {};
const station_selector = document.getElementById('station_selector');

// Ajout d'une couche de dalles OpenStreetMap
L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
     attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
     }).addTo(map);

// Fonction appelée au chargement de la page
function load_data () {

  // objet pour l'envoi d'une requête Ajax
  var xhr = new XMLHttpRequest();

  // fonction appelée lorsque la réponse à la requête (liste des lieux insolites) sera arrivée
  xhr.onload = function() {

    // transformation des données renvoyées par le serveur
    // responseText est du type string, data est une liste
    var data = JSON.parse(this.responseText);

    // boucle sur les lieux
    for ( n = 0; n < data.length; n++ ) {
      // insertion d'un marqueur à la position du lieu,
      // attachement d'une popup, capture de l'événement 'clic'
      // ajout d'une propriété personnalisée au marqueur
      idnum = data[n].id;
      markers[idnum] = L.marker([data[n].Y,data[n].X]);
      markers[idnum].addTo(map)
       .bindPopup('Station: '+data[n].nom_station)
       .addEventListener('click',ClickOnMarker)
       .idnum = data[n].id;

      //Insertion du nom de toutes les stations dans le sélecteur
      var station_selector_opt = document.createElement("option");
      station_selector_opt.value = data[n].id;
      station_selector_opt.text = data[n].nom_station;
      station_selector.add(station_selector_opt, null);
    }
  };

  // Envoi de la requête Ajax pour la récupération de la liste des lieux insolites
  xhr.open('GET','/location',true);
  xhr.send();
}

// Charge la page pour la carte de pollution
const nom_polluant_selector_page2 = document.getElementById('nom_polluant_selector_page2');
const nom_polluant_selector_page3 = document.getElementById('nom_polluant_selector_page3');
function load_data_page2 () {

  var xhr = new XMLHttpRequest();

  xhr.onload = function() {

    var data = JSON.parse(this.responseText);

    nom_polluant_selector_page2.length = 1;
    for(var i = 0; i < data.length; i++) {
      var opt = document.createElement("option");
      var opt_copy = document.createElement("option"); // fait la même chose que opt, pour le selecteur de la page3
      opt.value = data[i].nom_du_polluant;
      opt_copy.value = data[i].nom_du_polluant;
      opt.text = data[i].nom_du_polluant;
      opt_copy.text = data[i].nom_du_polluant;
      nom_polluant_selector_page2.add(opt, null);
      nom_polluant_selector_page3.add(opt_copy, null);
    }
  };

  xhr.open('GET','/selection/Tout',true);
  xhr.send();
}

//Affiche ou cache les marqueurs
function markers_unload() {
  for (const [key, value] of Object.entries(markers)) {
    value.remove();
  }};
  
  function markers_load() {
    for (const [key, value] of Object.entries(markers)) {
      value.addTo(map);
    }};

// Fonction appelée lorsqu'on sélectionne une station en cliquant sur la map
const nom_polluant_selector = document.getElementById('nom_polluant_selector');
function ClickOnMarker (e) {

  var xhr = new XMLHttpRequest();

  xhr.onload = function() {

    var data = JSON.parse(this.responseText);

    station_selector.value = idnum;

    nom_polluant_selector.length = 1;
    for(var i = 0; i < data.length; i++) {
      var nom_polluant_selector_opt = document.createElement("option");
      nom_polluant_selector_opt.value = data[i].nom_du_polluant;
      nom_polluant_selector_opt.text = data[i].nom_du_polluant;
      nom_polluant_selector.add(nom_polluant_selector_opt, null);
    }

    load_page1();
  };

  // Le numéro du lieu est récupéré via la propriété personnalisée du marqueur
  var idnum = e.target.idnum;

  xhr.open('GET','/selection/'+idnum,true); 
  xhr.send();
}

// Fonction appelée lorsqu'on sélectionne une station en utilisant le sélectionneur
station_selector.addEventListener('change', (e) => {
  var idnum = e.target.value;
  if (idnum=='None') {
    map.closePopup();
    unload_page1();
  }

  else {

    var xhr = new XMLHttpRequest();
    
    xhr.onload = function() {

      var data = JSON.parse(this.responseText);
      marker = markers[idnum] // selectionne le marqueur de la station correspondante
      var zoom = map.getZoom();
      var LatLng = marker.getLatLng();
      map.setView([LatLng.lat,LatLng.lng], zoom); // repositionne la map en la centrant sur le marqueur
      marker.openPopup(); // Affiche le marqueur

      // test.innerHTML =  'Station sélectionnée: ' + marker.getPopup().getContent() ;

      nom_polluant_selector.length = 1;
      for(var i = 0; i < data.length; i++) {
        var nom_polluant_selector_opt = document.createElement("option");
        nom_polluant_selector_opt.value = data[i].nom_du_polluant;
        nom_polluant_selector_opt.text = data[i].nom_du_polluant;
        nom_polluant_selector.add(nom_polluant_selector_opt, null);
      }

      load_page1();
    };

    xhr.open('GET','/selection/'+idnum,true); 
    xhr.send();
  }});

// show the given page, hide the rest
function show(elementID) {
  // try to find the requested page and alert if it's not found
  var ele = document.getElementById(elementID);
  var ele_menu = document.getElementById(elementID+'_menu');
  if (!ele) {
      alert('no such element');
      return;
  }

  // get all pages, loop through them and hide them
  var pages = document.getElementsByClassName('page');
  for(var i = 0; i < pages.length; i++) {
      pages[i].style.display = 'none';
  }
  var pages_menu = document.getElementsByClassName('tab_menu_on');
  for(var i = 0; i < pages_menu.length; i++) {
    pages_menu[i].className = 'tab_menu';
}

  // then show the requested page
  ele.style.display = 'block';
  ele_menu.className = 'tab_menu_on';
}

// Obtenir l'identifiant de la station sélectionnée
function GetIDNUM() {
  return station_selector.value;
}

// affiche la page 1
function load_page1() {
document.getElementById('page1_graph').style.display = 'block';
document.getElementById('page1_none').style.display= 'none';
}
function unload_page1() {
document.getElementById('page1_graph').style.display = 'none';
document.getElementById('page1_none').style.display= 'block';
const img_graph = document.getElementById('img_graph');
img_graph.src = "";
img_graph.alt = "";
document.getElementById('title_graph').innerHTML = ""
}




// Le graphe est actualisé dès qu'un paramètre du graphe est modifié
const date_deb_hist = document.getElementById('Date_deb_hist');
const date_fin_hist = document.getElementById('Date_fin_hist');
const date_pas_hist = document.getElementById('Date_pas_hist');
nom_polluant_selector.addEventListener('change', update_graph_polluant);
date_deb_hist.addEventListener('change', update_graph);
date_fin_hist.addEventListener('change', update_graph);
date_pas_hist.addEventListener('change', update_graph);

// Actualise le graphe quand on sélectionne un nouveau polluant (et affiche les dates qu'on a le droit de choisir)
function update_graph_polluant() {
  idnum = GetIDNUM();
  var nom_du_polluant = nom_polluant_selector.value; // Selectionne le polluant

  if (nom_du_polluant == 'None') {
    const img_graph = document.getElementById('img_graph');
    img_graph.src = "";
    img_graph.alt = "";
    document.getElementById('title_graph').innerHTML = ""
    }
    
  else {

    var xhr = new XMLHttpRequest();
    
    xhr.onload = function() {

      var data = JSON.parse(this.responseText);
      let date_deb = data[0];
      let date_fin = data[1];
      date_deb_hist.value = date_deb;
      date_deb_hist.min = date_deb;
      date_deb_hist.max = date_fin;
      date_fin_hist.value = date_fin;
      date_fin_hist.min = date_deb;
      date_fin_hist.max = date_fin;
      update_graph();
    };

    xhr.open('GET','/polluant_date/'+idnum+'/'+nom_du_polluant,true); 
    xhr.send();
}};

// Actualise le graphe (quand on modifie la date de début/fin, ou quand on modifie le pas de temps)
function update_graph() {
  idnum = GetIDNUM();
  if (idnum != "None") {
    var nom_du_polluant = nom_polluant_selector.value; // Selectionne le polluant
    var date_deb = date_deb_hist.value; // Date du type yyyy-mm-dd
    var date_fin = date_fin_hist.value;
    var pas_temps = date_pas_hist.value; // type de pas (jour,semaine,mois ou année)

    const title_graph = document.getElementById('title_graph');
    const img_graph = document.getElementById('img_graph');

    if (date_deb>= date_fin) {
      title_graph.style.color = 'red';
      title_graph.style.textDecoration = 'none';
      title_graph.innerHTML = "Veuillez vous assurer que avez bien choisi des dates de début et de fin cohérentes !"
    }

    else {
    title_graph.style.color = 'black';
    title_graph.style.textDecoration = 'underline';

    var xhr = new XMLHttpRequest();
    
    xhr.onload = function() {

      var data = JSON.parse(this.responseText);
      img_graph.src = data.img;
      img_graph.alt = data.title;
      title_graph.innerHTML = data.title+' pour la '+markers[idnum].getPopup().getContent();
    };

    xhr.open('GET','/polluant/'+idnum+'/'+nom_du_polluant+'/'+date_deb+'/'+date_fin+'/'+pas_temps,true); 
    xhr.send();
}}};

// Configuration des boutons de raccourci pour la carte de pollution
date_carte = document.getElementById('date_carte');
function change_date(date_value) {
  let date = new Date(date_carte.value);
  
  if (nom_polluant_selector_page2.value == 'None') { // à compléter (changer 'nioooone' par 'None')
    console.log("ne rien afficher");
  }
  else {
  if (date_value=='min') {
    date_carte.value = date_carte.min;
  }
  else if (date_value=='max') {
    date_carte.value = date_carte.max;
  }
  else {
    let new_date = date.getDate() + date_value;
    date.setDate(new_date);
    date_carte.value = date.toJSON().slice(0,10);

    if (date_carte.value > date_carte.max) {
      date_carte.value = date_carte.max;
    }

    else if (date_carte.value < date_carte.min) {
      date_carte.value = date_carte.min;
}}
update_carte_pollution();
}};

// Fonction s'ativant lorsque qu'on choisit un polluant pour la carte de pollution
var circles = L.featureGroup(); // Stock les cercles crées sur la map pour pouvoir les modifier/supprimer
const Legend = document.getElementById('Legend');
nom_polluant_selector_page2.addEventListener('change', (e) => {
  var nom_du_polluant = nom_polluant_selector_page2.value; // Selectionne le polluant
  
  circles.remove();
  circles = L.featureGroup(); // Vide la liste des cercles

  if (nom_du_polluant == 'None') {
    Legend.style.display = 'none';
  }
    
  else { // Sinon, il faut initialiser le calendrier permettant de choisir la date de la carte de pollution
    Legend.style.display = 'block';

    var xhr = new XMLHttpRequest();
    
    xhr.onload = function() {

      var data = JSON.parse(this.responseText);
      let date_deb = data[0];
      let date_fin = data[1];
      date_carte.value = date_deb;
      date_carte.min = date_deb;
      date_carte.max = date_fin;
      update_carte_pollution();
    };

    xhr.open('GET','/polluant_date/'+'Tout'+'/'+nom_du_polluant,true); 
    xhr.send();
}});
var carte_pollution_radius=1000;
// Fonction s'activant lorque qu'on choisit la date pour la carte de pollution
date_carte.addEventListener('change', update_carte_pollution);
document.getElementById('select_radius').addEventListener('change', update_carte_pollution);
function update_carte_pollution() {
  //Créer ou actualise la carte de pollution selon le polluant et la date choisi
  var nom_du_polluant = nom_polluant_selector_page2.value; // Selectionne le polluant
  var date = date_carte.value; // Date du type yyyy-mm-dd

  circles.remove();
  circles = L.featureGroup(); // Vide la liste des cercles

  var xhr = new XMLHttpRequest();
  
  xhr.onload = function() {

    var data = JSON.parse(this.responseText);

    let color= "";
    let LatLng = [0,0];

    //Sélectionne la taille des cercles
    carte_pollution_radius = document.getElementById('select_radius').value;
    if(carte_pollution_radius>10000) {
      carte_pollution_radius=10000;
      document.getElementById('select_radius').value = 10000;
    }
    else if(carte_pollution_radius<100) {
      carte_pollution_radius=100;
      document.getElementById('select_radius').value = 100;
    }

    for(var i = 0; i < data[0].length; i++) { // boucle for pour placer un cercle de couleur au milieu de chaque station
      idnum = data[0][i].id
      color = data[0][i].couleur
      LatLng = markers[idnum].getLatLng();
      new_circle = L.circle(LatLng, {radius: carte_pollution_radius, color: color});
      new_circle.addTo(circles);
    };
      map.addLayer(circles);

      let unite = data[2];
      let val0 = data[1][0].toString();
      let val1 = data[1][1].toString();
      let val2 = data[1][2].toString();

      document.getElementById("green").innerHTML = "taux de pollution faible (inférieur à"+val0+unite+")";
      document.getElementById("yellow").innerHTML = "taux de pollution moyen (compris entre "+val0+" et "+val1+unite+")";
      document.getElementById("orange").innerHTML = "taux de pollution élevé (compris entre "+val1+" et "+val2+unite+")";
      document.getElementById("red").innerHTML = "taux de pollution très élevé (supérieur à "+val2+unite+")";
    
};

  xhr.open('GET','/carte_pollution/'+nom_du_polluant+'/'+date,true); 
  xhr.send();
};

// // Fonction s'activant lorque qu'on choisit la date pour la carte de pollution
// date_carte.addEventListener('change', update_carte_pollution);
// function update_carte_pollution() {
//   //Créer ou actualise la carte de pollution selon le polluant et la date choisi
//   var nom_du_polluant = nom_polluant_selector_page2.value; // Selectionne le polluant
//   var date = date_carte.value; // Date du type yyyy-mm-dd

//   circles.remove();
//   circles = L.featureGroup(); // Vide la liste des cercles

//   var xhr = new XMLHttpRequest();
  
//   xhr.onload = function() {

//     var data = JSON.parse(this.responseText);
//     var concentration_max = data[0].concentration;
//     var concentration = 0;
//     for(var i = 0; i < data.length; i++) { // boucle for pour trouver la concentration maximale
//       concentration = data[i].concentration;
//       if (concentration>concentration_max) {
//         concentration_max = concentration;
//       };
//     };

//     let pollution_rate = 0;
//     let color= "";
//     let LatLng = [0,0];
//     for(var i = 0; i < data.length; i++) { // boucle for pour placer un cercle de couleur au milieu de chaque station
//       idnum = data[i].id
//       pollution_rate = data[i].concentration/concentration_max;
//       color = set_color(pollution_rate);
//       LatLng = markers[idnum].getLatLng();
//       new_circle = L.circle(LatLng, {radius: 10000, color: color});
//       new_circle.addTo(circles);
//     };
//       map.addLayer(circles);
// };

//   xhr.open('GET','/carte_pollution/'+nom_du_polluant+'/'+date,true); 
//   xhr.send();
// };

// // Définit la couleur des différents cercles de la carte de pollution en fonction du taux de pollution
// function set_color(pollution_rate) {
//   if (pollution_rate <= 0.2) {
//     return "green";
//   }
//   else if (pollution_rate<=0.75) {
//     return "yellow";
//   }
//   else if (pollution_rate <=0.9) {
//     return "orange";
//   }
//   else {
//     return "red";
//   }
// };
// Sélectionne ou déselectionne une station pour la comparaison de données
const list_idnum_box = document.getElementById('list_idnum_box');
const list_choix_box = document.getElementById('list_choix_box');
function Move(l1,l2) {
  if (l1.options.selectedIndex>=0) {
    idnum = l1.options[l1.options.selectedIndex].value;
    o=new Option(l1.options[l1.options.selectedIndex].text,idnum);
    l2.options[l2.options.length]=o;
    l1.options[l1.options.selectedIndex]=null;
    update_page3_dates();
}}

// Affiche la liste des stations disponibles lorsqu'on choisit un polluant particulier
nom_polluant_selector_page3.addEventListener('change', (e) => {
  var nom_du_polluant = nom_polluant_selector_page3.value; // Selectionne le polluant
  list_idnum_box.length = 0;
  list_choix_box.length = 0;

  if (nom_du_polluant == 'None') {
    const img_graph_page3 = document.getElementById('img_graph_page3');
    img_graph_page3.src = "";
    img_graph_page3.alt = "";
    document.getElementById('title_graph_page3').innerHTML = ""
    }
    
  else {

    var xhr = new XMLHttpRequest();
    
    xhr.onload = function() {

      var data = JSON.parse(this.responseText);

      for(var i = 0; i < data.length; i++) {
        var opt = document.createElement("option");
        opt.value = data[i].id;
        opt.text = data[i].nom_station;
        list_choix_box.add(opt, null);
      }
    };

    xhr.open('GET','/stations_polluant/'+nom_du_polluant,true); 
    xhr.send();
}});

//Actualise le choix des dates pour la page des comparaisons
var list_idnum = []
const date_deb_page3 = document.getElementById('Date_deb_page3');
const date_fin_page3 = document.getElementById('Date_fin_page3');
function update_page3_dates() {

  var nom_du_polluant = nom_polluant_selector_page3.value

  if(nom_du_polluant!='None') {
    list_idnum = [];
    for(var i = 0; i < list_idnum_box.options.length; i++) {
      list_idnum.push(list_idnum_box.options[i].value);
      };

    if(list_idnum.length==0) {
      const img_graph_page3 = document.getElementById('img_graph_page3');
      img_graph_page3.src = "";
      img_graph_page3.alt = "";
      document.getElementById('title_graph_page3').innerHTML = ""
    }

    else {

    var xhr = new XMLHttpRequest();

    xhr.onload = function() {


      var data = JSON.parse(this.responseText);

      let date_deb = data[0];
      let date_fin = data[1];
      date_deb_page3.value = date_deb;
      date_deb_page3.min = date_deb;
      date_deb_page3.max = date_fin;
      date_fin_page3.value = date_fin;
      date_fin_page3.min = date_deb;
      date_fin_page3.max = date_fin;
      update_graph_comparaisons();
    };

    xhr.open('GET','/dates_intersect/'+list_idnum+'/'+nom_du_polluant,true);
    xhr.send();
}}};

//Actualise le graphe des comparaisons
const date_pas_page3 = document.getElementById('Date_pas_page3');
date_deb_page3.addEventListener('change', update_graph_comparaisons);
date_fin_page3.addEventListener('change', update_graph_comparaisons);
date_pas_page3.addEventListener('change', update_graph_comparaisons);

function update_graph_comparaisons() {
  const title_graph_page3 = document.getElementById('title_graph_page3');
  const img_graph_page3 = document.getElementById('img_graph_page3');
  if(list_idnum.length==0) {
    title_graph.innerHTML = "";
    img_graph_page3.src = "";
    img_graph_page3.alt = "";
    
  }

  else {
    var nom_du_polluant = nom_polluant_selector_page3.value; // Selectionne le polluant
    var date_deb = date_deb_page3.value; // Date du type yyyy-mm-dd
    var date_fin = date_fin_page3.value;
    var pas_temps = date_pas_page3.value; // type de pas (jour,semaine,mois ou année)



    if (date_deb>= date_fin) {
      title_graph.style.color = 'red';
      title_graph.style.textDecoration = 'none';
      title_graph.innerHTML = "Veuillez vous assurer que avez bien choisi des dates de début et de fin cohérentes !"
    }

    else {
    title_graph.style.color = 'black';
    title_graph.style.textDecoration = 'underline';

    var xhr = new XMLHttpRequest();
    
    xhr.onload = function() {

      var data = JSON.parse(this.responseText);
      img_graph_page3.src = data.img;
      img_graph_page3.alt = data.title;
      title_graph_page3.innerHTML = data.title;
    };

  xhr.open('GET','/comparaison/'+nom_du_polluant+'/'+list_idnum+'/'+date_deb+'/'+date_fin+'/'+pas_temps,true);
  xhr.send();

}}};