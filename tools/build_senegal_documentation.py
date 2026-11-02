#!/usr/bin/env python3
"""Textes pédagogiques originaux, illustrations et références du fonds Sénégal.
Reconstruction locale : python3 tools/build_senegal_documentation.py
Les fichiers images.json et regions.json sont les instantanés documentés des sources.
"""
from pathlib import Path
import json,re,math,hashlib
ROOT=Path(__file__).resolve().parents[1];DEST=ROOT/'assets/documentation';sources={};articles=[]
def src(key,title,publisher,url,date,note):sources[key]={'title':title,'publisher':publisher,'url':url,'date':date,'note':note,'accessed':'2026-10-31'}
src('surface','Superficie du Sénégal','ANSD','https://www.ansd.sn/node/47','2023','Valeur de référence : 196 712 km². Les superficies issues de jeux cartographiques peuvent différer ; ne pas les mélanger.')
src('population','Données de population','ANSD','https://www.ansd.sn/Indicateur/donnees-de-population','RGPH-5 2023 et projections','Les chiffres d’un recensement et d’une projection ne sont pas interchangeables. La page reprend 18 126 390 habitants pour 2023.')
src('rgph','RGPH-5 : rapport global provisoire de juillet 2024','ANSD','https://www.ansd.sn/sites/default/files/2024-07/RGPH-5_Rapport%20global-Prov-juillet2024.pdf','Juillet 2024','Base statistique datée retenue pour le repère national de 2023 ; des résultats préliminaires antérieurs étaient différents.')
src('rgph-first','Résultats préliminaires : population du RGPH-5','ANSD','https://www.ansd.sn/flash-stat/resultats-du-rgph-5-une-population-tres-jeune-marquee-par-une-predominance-de-leffectif','Résultats préliminaires 2023','La valeur 18 032 473 appartient à la première publication. Elle est présentée comme repère de révision, pas comme une deuxième population à additionner.')
src('ses','Situation économique et sociale nationale, édition 2024','ANSD','https://www.ansd.sn/sites/default/files/2026-02/SESN%202024.pdf','2024 ; publication 2026','Référence nationale multisectorielle. Les données d’une édition ne décrivent pas automatiquement l’année de consultation.')
src('regions','Situations économiques et sociales régionales','ANSD','https://www.ansd.sn/ses-regionales','Éditions régionales 2023–2024','Portail des rapports régionaux : organisation territoriale, activités, population et équipements. Les profils de l’app privilégient des repères durables.')
src('geo','Géographie du Sénégal','Ministère sénégalais chargé de la Culture et du Tourisme','https://mcat.gouv.sn/geographie/','Page de présentation, consultée en 2026','Localisation, grands paysages et relief ; synthèse ancienne, non utilisée pour les statistiques actuelles.')
src('climat','Habitat et environnement : cadre climatique','ANSD','https://www.ansd.sn/Indicateur/sesnchapitre-habitat-et-environnement','SES nationales','Explique l’influence de l’océan et les circulations atmosphériques ; les saisons ont des dates variables selon les régions et les années.')
src('agri','Plan national d’adaptation du secteur de l’agriculture','République du Sénégal / CCNUCC','https://unfccc.int/sites/default/files/resource/PNA_du_Secteur_de_l%25E2%2580%2599Agriculture_2025_Senegal_FR.pdf','2025','Cadre des six grandes zones agroécologiques et des vulnérabilités agricoles ; les zonages peuvent varier selon l’objectif de la carte.')
src('fao','Contexte écologique et socioéconomique du Sénégal','FAO','https://www.fao.org/4/X6888F/x6888f03.htm','Document de contexte ancien','Description du réseau hydrographique, des sols et des formations végétales ; pas de reprise de ses anciens indicateurs économiques.')
src('saga','SAGA 2 au Sénégal : adaptation de l’agriculture','FAO','https://www.fao.org/in-action/saga/countries/senegal/fr','Programme consulté en 2026','Adaptation, sécurité alimentaire et collaboration avec les institutions et les communautés rurales.')
src('omvs','Conventions de base de l’OMVS','OMVS','https://www.omvs.org/conventions-de-base/','Conventions et présentation institutionnelle','Statut international du fleuve Sénégal et coopération entre États ; ouvrages communs et gestion partagée.')
src('diama','Fonctions des barrages et gestion de l’eau','SOGED / OMVS','https://soged-omvs.org/a-propos-de-soged/','Présentation institutionnelle','Diama, Manantali, eau douce et coordination des usages dans le bassin du Sénégal.')
src('omvg','Organisation pour la mise en valeur du fleuve Gambie','Géo Sénégal','https://www.geosenegal.gouv.sn/%2B-organisation-pour-la-mise-en-valeur-du-fleuve-gambie-%2B.html','Présentation institutionnelle','Coopération de la Gambie, de la Guinée, de la Guinée-Bissau et du Sénégal.')
src('water','Sécurité hydrique au Sénégal','Banque mondiale','https://www.banquemondiale.org/fr/topic/water/publication/water-security-in-senegal-challenges-and-recommendations','2022','Ressources, demande et risques ; les pourcentages d’un diagnostic daté ne sont pas présentés comme des constantes.')
src('ccdr','Rapport national sur le climat et le développement','Banque mondiale','https://www.banquemondiale.org/fr/country/senegal/publication/senegal-country-climate-and-development-report','2024','Vulnérabilité, villes, littoral, adaptation et transition énergétique. Les projections sont des scénarios, pas des événements acquis.')
src('oil','Projets stratégiques pétroliers et gaziers','COS-PETROGAZ','https://cospetrogaz.sn/projets-strategiques','Repères 2024–2025','Sangomar : pétrole depuis juin 2024. GTA : mise en production à fin 2024, premiers jalons commerciaux en 2025. Pas de promesse de revenus.')
src('patrimoine','Biens inscrits du Sénégal','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/etatsparties/sn/','Liste consultée le 31/10/2026','Sept biens : cinq culturels et deux naturels. Inscription internationale et conservation sont deux notions distinctes.')
src('goree','Île de Gorée','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/list/26/','Inscription 1978','Portée mémorielle et patrimoniale du lieu. Les controverses sur les volumes de traite ne sont pas remplacées par un chiffre sans preuve.')
src('saint-louis','Île de Saint-Louis','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/list/956/','Inscription 2000','Ville insulaire, comptoir, architecture et fonctions coloniales ; les différentes capitales administratives doivent être distinguées.')
src('saloum','Delta du Saloum','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/list/1359/','Inscription 2011','Paysage culturel, mangroves, amas coquilliers et longue histoire d’occupation humaine.')
src('djoudj','Parc national des oiseaux du Djoudj','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/list/25/','Inscription 1981','Zone humide du delta et oiseaux migrateurs. Les effectifs d’oiseaux varient selon les années et les comptages.')
src('niokolo','Parc national du Niokolo-Koba','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/list/153/','Inscription 1981','Savanes, forêts-galeries et conservation. Une liste d’espèces historiquement signalées n’est pas un inventaire actuel d’effectifs.')
src('megalithes','Cercles mégalithiques de Sénégambie','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/list/1226/','Inscription 2006','Bien transfrontalier : Sine Ngayène et Wanar au Sénégal ; Wassu et Kerbatch en Gambie. Datations de pratiques funéraires sur une longue période.')
src('bassari','Pays Bassari : paysages Bassari, Peul et Bédik','UNESCO, Centre du patrimoine mondial','https://whc.unesco.org/fr/list/1407/','Inscription 2012','Paysages culturels autour de Salémata, Bandafassi et Dindéfello ; ne pas confondre ces aires avec des régions administratives.')
src('immat','Patrimoine culturel immatériel du Sénégal','UNESCO','https://ich.unesco.org/fr/etat/senegal-SN','Liste consultée le 31/10/2026','Kankurang, xooy et ceebu jën ; les traditions sont vivantes et ne se réduisent pas à des spectacles.')
src('faleme','Projet Falémé : peuplements et paléoenvironnements','Université de Genève, laboratoire ARCAN','https://arcan.unige.ch/recherche/peuplement-humain-et-paleoenvironnement-en-afrique-projet-faleme','Recherches en cours','Archéologie du Paléolithique aux périodes récentes ; cadres chronologiques construits par les fouilles et les datations.')
src('prehistoire','Préhistoire et collections archéologiques','Musée historique du Sénégal / IFAN','https://musee-historiquedusenegal.sn/collection/prehistoire','Collections consultées en 2026','Outils, sites et indices matériels ; les objets archéologiques ne sont pas des fossiles par définition.')
src('royaumes','Histoire et royaumes du Sénégal','Musée historique du Sénégal / IFAN','https://musee-historiquedusenegal.sn/histoire','Parcours historique','Repérage des principaux États. Les récits de fondation mêlent traditions et données historiques ; certaines datations institutionnelles sont approximatives.')
src('jolof','Royaume du Djolof','Musée historique du Sénégal / IFAN','https://musee-historiquedusenegal.sn/collection/objet/royaume-du-djolof','Notice de collection','Tradition de Ndiadiane Ndiaye et organisation du Grand Jolof ; ne pas traiter la légende de fondation comme une biographie entièrement datée.')
src('resistances','Les résistances africaines','Musée historique du Sénégal / IFAN','https://musee-historiquedusenegal.sn/collection/periode/les-resistances-africaines','Parcours historique','Résistances armées, culturelles et religieuses ; trajectoires et alliances complexes.')
src('latdior','Lat Dior','Musée historique du Sénégal / IFAN','https://musee-historiquedusenegal.sn/collection/objet/lat-dior','Notice de collection','Damel du Cayor ; mort à Dékheulé le 26 octobre 1886.')
src('femmes','Trois figures historiques féminines','Direction des Archives du Sénégal','https://archivesdusenegal.gouv.sn/?page_id=3154','Dossier du 8 mars','Ndaté Yalla Mbodj, Aline Sitoe Diatta et Caroline Faye Diop. Les dates biographiques anciennes peuvent varier selon les travaux.')
src('islam','Islam et confréries dans le parcours du musée','Musée historique du Sénégal / IFAN','https://musee-historiquedusenegal.sn/collection/periode/lislam','Notice de collection','Identification des confréries ; la synthèse pédagogique évite de réduire l’islamisation à une conquête unique ou à une seule date.')
src('malick','Présentation du nouveau Dîwân d’El Hadji Malick Sy','Presses universitaires de Dakar / UCAD','https://editions.ucad.sn/ouvrages/103','2025','Atteste la dimension savante, littéraire et éducative de son œuvre ; aucun poème ni extrait du livre n’est reproduit.')
src('diagne','Blaise Diagne : notice parlementaire','Assemblée nationale française, Sycomore','https://www2.assemblee-nationale.fr/sycomore/fiche?num_dept=2496','Mandats 1914–1934','Mandats, action parlementaire et recrutement militaire. Une citoyenneté particulière ne signifie pas l’égalité de tous sous la colonisation.')
src('tirailleurs','Journée du tirailleur : repères historiques','Ministère sénégalais des Forces armées','https://www.forcesarmees.gouv.sn/discours/discours-ministre-des-forces-armees-celebration-de-la-journee-du-tirailleur-edition-2019','2019','Recrutement colonial et guerres mondiales ; le terme « sénégalais » recouvre des origines ouest-africaines diverses.')
src('thiaroye','Commémoration du massacre de Thiaroye','Gouvernement du Sénégal','https://www.primature.sn/publications/actualites/commemoration-du-80e-anniversaire-du-massacre-des-tirailleurs-senegalais','2024','Massacre du 1er décembre 1944 ; mémoire, archives et recherches. Le bilan humain n’est pas réduit à un chiffre définitif.')
src('rail','Exposition sur l’histoire ferroviaire','Agence de presse sénégalaise, reportage sur l’exposition','https://aps.sn/une-exposition-revisite-lhistoire-ferroviaire-du-senegal-en-inscriptions-et-cliches/','29 janvier 2026','Histoire des lignes et grève de 1947–1948. Les photographies de l’exposition ne sont pas reproduites sans licence.')
src('indep','Dossier diplomatique Sénégal : indépendance et institutions','Archives diplomatiques françaises','https://archivesdiplomatiques.diplomatie.gouv.fr/ark%3A/14366/5jfsg3w6z48h','Dossiers 1960–1972','Indépendance fédérale le 20 juin 1960 ; séparation le 20 août. Source d’archives à lire dans son contexte diplomatique.')
src('presidence','L’indépendance et les alternances','Présidence de la République du Sénégal','https://www.presidence.sn/fr/presidence/lindependance-4-avril-1960/','Repères jusqu’en 2024','Fête nationale du 4 avril et alternances électorales de 2000, 2012 et 2024 ; certaines dates sont détaillées dans les autres références.')
src('diouf','Abdou Diouf','Présidence de la République du Sénégal','https://www.presidence.sn/fr/presidence/abdou-diouf/','Présidence 1981–2000','Accession le 1er janvier 1981 et élections de 1983, 1988 et 1993.')
src('macky','Macky Sall','Présidence de la République du Sénégal','https://www.presidence.sn/fr/presidence/macky-sall/','Présidence 2012–2024','Élection du 25 mars 2012 ; cette notice est un document institutionnel, pas une évaluation indépendante du mandat.')
src('constitution','Constitution du Sénégal','Conseil constitutionnel du Sénégal','https://conseilconstitutionnel.sn/la-constitution/','Constitution de 2001, version du site consultée le 31/10/2026','État, souveraineté, symboles et institutions. Pas de consultation juridique ; vérifier toute modification avant d’en enseigner un détail technique.')
src('onu','Admission du Sénégal aux Nations Unies','Bibliothèque numérique des Nations Unies','https://digitallibrary.un.org/record/206140?ln=en','28 septembre 1960','Résolution 1490 (XV) de l’Assemblée générale : admission du Sénégal.')
src('map','Limites régionales du Sénégal — geoBoundaries ADM1','Gouvernement du Sénégal / OCHA ROWCA ; diffusion geoBoundaries','https://data.humdata.org/dataset/senegal-administrative-boundaries','Limites représentées : 2019 ; jeu consulté en 2026','CC BY 3.0 IGO. Carte simplifiée de repérage ; ne pas utiliser comme limite cadastrale ou document de délimitation juridique.')

def p(text):return {'type':'p','text':text}
def note(text):return {'type':'note','text':text}
def table(headers,rows):return {'type':'table','headers':headers,'rows':rows}
def fig(image,caption):return {'type':'image','image':image,'caption':caption}
def add(id,subject,group,title,summary,text,refs,retain,task,answer,*,image=None,related=(),questions=(),extra=()):
 blocks=[]
 if image:blocks.append(fig(*image))
 for part in text.strip().split('\n\n'):
  part=part.strip()
  if part.startswith('## '):blocks.append({'type':'h2','text':part[3:]})
  elif part.startswith('! '):blocks.append(note(part[2:]))
  elif part.startswith('• '):blocks.append({'type':'bullets','items':[s.removeprefix('• ') for s in part.split('\n')]})
  elif part:blocks.append(p(part))
 blocks+=list(extra)
 words=len(re.findall(r'\S+',text+' '+task+' '+answer))
 articles.append({'id':id,'subject':subject,'group':group,'title':title,'summary':summary,'objectives':['Situer et expliquer : '+title.lower()+'.','Employer le vocabulaire de la fiche et justifier une réponse avec un exemple.'],'blocks':blocks,'sources':refs,'takeaways':retain,'activity':{'task':task,'answer':answer},'questions':[{'q':q,'a':a} for q,a in questions],'related':list(related),'minutes':max(3,math.ceil(words/130))})

add('g01','geo','Repères et méthodes','Situer le Sénégal en Afrique','Position, voisins, océan et ordre de grandeur du territoire.', '''## Un pays d’Afrique de l’Ouest

Le Sénégal occupe la façade atlantique de l’Afrique de l’Ouest. Le fleuve Sénégal borde une partie du nord ; la presqu’île du Cap-Vert porte Dakar, la capitale. La pointe des Almadies est le point le plus occidental de l’Afrique continentale. Elle ne doit pas être confondue avec les îles de l’État du Cabo Verde, situées au large.

## Des frontières à lire sur la carte

La Mauritanie se trouve au nord, le Mali à l’est, la Guinée et la Guinée-Bissau au sud. La Gambie s’étire le long du fleuve Gambie et possède une ouverture sur l’Atlantique : elle n’est donc pas une enclave entièrement fermée. La Casamance est située au sud de cette bande territoriale.

L’ANSD retient une superficie nationale de 196 712 km². Une surface se mesure en kilomètres carrés ; ce n’est pas une distance à parcourir. Les légères différences entre atlas viennent notamment des méthodes de calcul et des délimitations utilisées. Dans un exercice, garder une même référence.

! Une carte actuelle montre des États et des frontières contemporaines. Elle ne doit pas servir à délimiter automatiquement les anciens royaumes.''',['surface','geo'],['Le Sénégal est à l’ouest du continent africain.','Ses cinq voisins terrestres sont Mauritanie, Mali, Guinée, Guinée-Bissau et Gambie.'],'Sur une carte muette, écrire les cinq voisins puis dessiner une flèche indiquant l’Atlantique.','Le nord doit être repéré avant de placer les noms. Vérifier en particulier les deux Guinées et l’ouverture maritime de la Gambie.',related=['g02','g04','h04'],questions=[('Pourquoi 196 712 km² n’est-il pas une longueur ?','Parce qu’il s’agit de la mesure d’une surface ; une longueur s’exprime en kilomètres.')])
add('g02','geo','Repères et méthodes','Lire une carte et construire un croquis','Titre, orientation, légende, échelle et localisation.', '''## Les informations indispensables

Une carte répond à une question : où sont les régions, comment se répartit la population, où se trouvent les cours d’eau ? Son titre doit annoncer cette question, son territoire et, pour une donnée changeante, sa date. L’orientation permet de lire nord, sud, est et ouest. La légende explique les signes ; une même couleur n’a pas de sens universel.

L’échelle relie une distance sur la carte à une distance réelle. À 1:1 000 000, un centimètre représente dix kilomètres sur le terrain. Une échelle graphique reste utilisable si une carte est agrandie avec toutes ses proportions ; une simple échelle numérique peut devenir fausse après redimensionnement.

## Passer de l’observation à l’explication

Pour un croquis scolaire, sélectionner peu d’informations, choisir des figurés distincts et organiser la légende. Une ville peut être un point, un axe une ligne et une zone agricole une surface. Faire apparaître les contrastes plutôt que recopier chaque détail. Les frontières de la carte interactive de l’app sont simplifiées ; elle n’est pas un document de mesure fine.

! Une carte de densité ne représente pas des quantités totales. Deux régions de même couleur peuvent avoir des populations très différentes si leurs superficies diffèrent.''',['map','rgph'],['Une carte doit être titrée, orientée et légendée.','L’échelle et la date déterminent ce que l’on peut comparer.'],'Construire un croquis du quartier de l’école avec cinq signes et une légende.','Partir d’observations locales et distinguer route, bâtiment, espace vert et cours d’eau éventuel. Évaluer la cohérence entre légende et dessin plutôt que la décoration.',related=['g01','g15'])
add('g03','geo','Repères et méthodes','Observer un paysage et mener une enquête','Une démarche pour apprendre à décrire avant d’expliquer.', '''## Décrire ce qui est visible

Un paysage associe relief, eau, végétation, bâtiments, voies de circulation et activités. Distinguer premier plan et arrière-plan, éléments naturels et aménagements humains. Une photographie n’est qu’un point de vue : elle peut masquer un quartier, une saison ou une activité. Noter le lieu, la date et l’auteur quand ils sont connus.

## Construire une explication prudente

Après la description, proposer des relations : un marché près d’un carrefour, des cultures près d’une source d’eau, des maisons sur une hauteur. Ces relations doivent être vérifiées par une carte, une seconde image ou un entretien. Ne pas conclure qu’une activité n’existe pas parce qu’elle n’apparaît pas sur une photo.

Pour une enquête de classe, préparer trois questions courtes, demander l’accord des personnes, consigner leurs réponses sans inventer de chiffres. Une petite enquête autour de l’école illustre une situation ; elle ne permet pas de calculer un taux valable pour tout le Sénégal. Les élèves peuvent croiser dessins, croquis et témoignages pour présenter une observation argumentée.''',['regions','map'],['Décrire et expliquer sont deux étapes différentes.','Toute image et toute enquête ont des limites.'],'Observer un marché, un puits ou une rue depuis un point sûr puis rédiger cinq constats et deux hypothèses.','Séparer les constats visibles des interprétations. Rechercher une preuve supplémentaire pour chaque hypothèse ; ne pas collecter de données personnelles inutiles.',related=['g02','h01'])
add('g04','geo','Milieux physiques','Relief et grandes structures géologiques','Un territoire surtout bas, avec des reliefs plus marqués au sud-est.', '''## Plaines, plateaux et collines

Une grande partie du Sénégal est formée de plaines et de plateaux de faible altitude. Cela ne signifie pas que le terrain est partout horizontal : dunes, vallées, falaises et petites hauteurs organisent les paysages. La région de Thiès possède des reliefs de plateau ; la presqu’île du Cap-Vert présente des héritages volcaniques.

Au sud-est, autour de Kédougou et vers la Guinée, les terrains sont plus accidentés et rattachés aux contreforts du Fouta-Djalon. Les cours d’eau y découpent des vallées ; la cascade de Dindéfello illustre ce contraste avec les vastes étendues basses de l’ouest et du centre.

## Comprendre le sous-sol

Le bassin sédimentaire couvre la majeure partie du pays. Des dépôts successifs y ont enregistré une histoire géologique longue. À l’est affleurent des terrains plus anciens, liés au socle. La géologie aide à comprendre les sols, l’eau souterraine et certaines ressources minières ; elle ne permet pas de déduire à elle seule les usages agricoles.

! Les altitudes maximales publiées dans les anciens atlas divergent selon les relevés et les noms de sommet. On privilégie ici le contraste régional plutôt qu’un record non harmonisé.''',['geo','fao'],['Le relief est généralement peu élevé, mais contrasté.','Le sud-est est plus accidenté que la majeure partie du territoire.'],'Comparer une image de Dindéfello et une image du lac de Guiers : relief, eau, végétation.','Relever par exemple paroi rocheuse et chute d’eau à Dindéfello, surface lacustre étendue et relief bas autour de Guiers. Ne pas comparer les pluies à partir des seules images.',image=('dindefelo','La cascade de Dindéfello : un relief du sud-est sénégalais.'),related=['g05','g26','r-kedougou'])
add('g05','geo','Milieux physiques','Le climat : saisons, vents et contrastes','Comprendre l’hivernage sans lui attribuer partout les mêmes dates.', '''## Deux grandes saisons, des calendriers variables

Le climat sénégalais se caractérise par l’alternance d’une saison sèche et d’une saison des pluies, souvent appelée hivernage. Les pluies sont généralement plus abondantes et la saison humide plus longue vers le sud ; le nord est plus sec. Les dates de début et de fin varient d’une région et d’une année à l’autre : juin à octobre constitue un repère large, pas une règle fixe.

L’océan atténue les contrastes thermiques près du littoral. L’intérieur connaît souvent des chaleurs plus fortes. L’harmattan est un vent continental sec qui peut transporter des poussières ; les flux de mousson apportent de l’humidité depuis l’Atlantique. L’alizé maritime participe aux conditions plus fraîches de la côte à certaines périodes.

## Météo et climat

La météo décrit une situation à court terme ; le climat repose sur des observations longues et des statistiques. Une journée très pluvieuse ne suffit pas à définir le climat d’un lieu. Pour suivre l’hivernage, examiner les dates, les cumuls et les pauses sèches. Pour les semis, utiliser les conseils météorologiques et agricoles locaux plutôt qu’un calendrier scolaire unique.''',['climat','agri'],['L’hivernage n’a pas partout les mêmes dates.','Les pluies augmentent globalement du nord vers le sud.'],'Relever pendant un mois les jours de pluie et comparer le relevé avec celui d’une autre école.','Conserver le même mois, les mêmes unités et une méthode identique. Distinguer nombre de jours pluvieux et quantité d’eau ; ne pas transformer un mois en normale climatique.',related=['g06','g24'],questions=[('Pourquoi une averse ne prouve-t-elle pas un changement du climat ?','Le climat s’étudie sur de longues séries, alors qu’une averse est un événement météorologique.')])
add('g06','geo','Milieux physiques','Les six grandes zones agroécologiques','Des milieux utiles pour comprendre les activités rurales.', '''## Un découpage selon les milieux

Un zonage agroécologique rassemble des espaces ayant des conditions proches : pluies, sols, eau, végétation et usages agricoles. Le Plan national d’adaptation agricole distingue six grands ensembles : Niayes, vallée du fleuve Sénégal, bassin arachidier, zone sylvopastorale, Sénégal oriental et Casamance. Ces ensembles ne sont ni des régions administratives ni des blocs aux limites parfaitement fixes.

Les Niayes sont associées aux cultures maraîchères ; la vallée combine crue, irrigation et agriculture. Dans le bassin arachidier, les cultures pluviales et l’élevage s’articulent. Le Ferlo illustre l’importance des parcours et de l’eau pour le pastoralisme. Le Sénégal oriental et la Casamance présentent d’autres combinaisons de pluies, de sols, de relief et de ressources.

## Éviter les déterminismes

Un milieu crée des possibilités et des contraintes, mais les décisions humaines comptent : équipements, marchés, accès à la terre, savoir-faire et politiques publiques. Une zone réputée pastorale comporte aussi des cultures et des villes ; une zone agricole accueille de nombreuses activités non agricoles. Pour enseigner, relier une carte de zonage à des exemples locaux, sans enfermer les habitants dans une activité unique.''',['agri','saga'],['Un zonage écologique et une région administrative répondent à des objectifs différents.','Les activités dépendent aussi des équipements et des choix humains.'],'Associer à chaque grande zone un usage possible et une contrainte, puis expliquer les exceptions.','Accepter plusieurs activités par zone. Exemples : maraîchage/eau dans les Niayes ; élevage/accès aux pâturages dans le Ferlo ; riziculture/gestion de la salinité en Casamance.',related=['g10','g11','g12','g18'])
add('g07','geo','Eaux et littoraux','Le fleuve Sénégal et son bassin','Un système partagé, de l’amont ouest-africain à l’Atlantique.', '''## Un bassin dépasse les frontières

Le bassin d’un fleuve regroupe les terrains dont les eaux convergent vers ce cours d’eau. Le fleuve Sénégal résulte notamment de la réunion du Bafing et du Bakoye ; la Falémé fait partie de ses grands affluents. Son parcours et ses tributaires relient des territoires de Guinée, du Mali, de Mauritanie et du Sénégal. En aval, il atteint l’Atlantique dans l’espace de Saint-Louis.

L’amont alimente l’aval, mais les usages se répartissent tout au long du bassin : agriculture, eau domestique, élevage, pêche, énergie et conservation. Les crues peuvent nourrir les sols et les zones humides tout en menaçant les habitations installées dans les secteurs inondables.

## Une coopération nécessaire

L’OMVS organise une gestion partagée. Diama limite la remontée d’eau salée et facilite le maintien d’eau douce ; Manantali, au Mali, contribue à la régulation et à la production électrique. Les barrages ne font pas disparaître tous les risques de crue ou de pénurie. Les décisions doivent articuler sécurité, production et besoins des écosystèmes.''',['omvs','diama'],['Le bassin du Sénégal est transfrontalier.','Un barrage modifie les usages et les rythmes de l’eau.'],'Dessiner un schéma amont–aval avec trois usages de l’eau et deux risques.','Faire apparaître la circulation vers l’aval et la coexistence des besoins. Ne pas dessiner le bassin comme une bande limitée aux berges du fleuve.',related=['g08','g09','r-saint-louis','r-matam'])
add('g08','geo','Eaux et littoraux','Gambie, Casamance et Saloum','Fleuves, estuaires et bras de mer : des fonctionnements différents.', '''## Le réseau du sud et du centre-ouest

Le fleuve Gambie naît dans les hautes terres guinéennes, traverse le Sénégal oriental puis la Gambie avant d’atteindre l’océan. Les ressources de son bassin impliquent plusieurs pays. L’OMVG s’inscrit dans cette coopération sous-régionale, aux côtés de la gestion d’autres bassins et des échanges énergétiques.

La Casamance désigne à la fois un cours d’eau et un grand espace du sud du Sénégal. Dans sa partie aval, les marées et le sel jouent un rôle important : on parle d’estuaire. Des bolongs, chenaux soumis à la marée, irriguent les paysages de mangrove. Le Saloum forme également un ensemble estuarien et insulaire où la mer intervient fortement.

## Ne pas confondre eau visible et eau douce disponible

La présence d’une grande étendue d’eau ne signifie pas qu’elle est potable ou utilisable directement pour les cultures. La salinité varie selon les lieux, les saisons et les échanges avec l’océan. Pour les habitants, les aménagements doivent tenir compte des ressources en eau douce, de la pêche, des sols salés et des circulations en pirogue.''',['omvg','fao','saloum'],['Fleuve, estuaire et bolong ne sont pas synonymes.','Les marées influencent les eaux du Saloum et de la basse Casamance.'],'Classer quatre photographies : rivière, estuaire, lac et bolong ; justifier chaque choix.','L’image seule peut être insuffisante : demander le lieu et une légende. Insister sur l’arrivée en mer, la présence de marées et la notion de plan d’eau fermé ou ouvert.',related=['g07','g09','g13'])
add('g09','geo','Eaux et littoraux','Lac de Guiers, nappes et eau potable','De la ressource naturelle au service d’alimentation en eau.', '''## Diverses réserves, divers usages

Le lac de Guiers est une importante réserve d’eau douce reliée au système du fleuve Sénégal. Les nappes souterraines stockent aussi de l’eau dans certaines formations géologiques. Cette eau peut circuler lentement et n’est pas une réserve inépuisable. Son accessibilité dépend de la profondeur, de la qualité et des équipements.

L’alimentation en eau potable suit une chaîne : captage, traitement éventuel, stockage, transport puis distribution. Une eau claire n’est pas nécessairement sûre à boire ; la qualité doit être contrôlée. Les réseaux alimentent les ménages mais la demande provient également des cultures, des industries et des services.

## Protéger et partager

La surexploitation peut abaisser les niveaux d’eau ; les pollutions et l’intrusion saline peuvent dégrader une ressource. La sécurité hydrique associe disponibilité, qualité, accès et résistance aux sécheresses ou aux inondations. Préserver un bassin, limiter les fuites et utiliser l’eau avec discernement sont des actions complémentaires, et non des solutions interchangeables.''',['water','diama'],['Une réserve d’eau et un réseau d’eau potable sont différents.','Quantité, qualité et accès doivent être étudiés ensemble.'],'Reconstituer le trajet de l’eau jusqu’à l’école et repérer deux lieux où elle peut être économisée.','Utiliser les informations du service d’eau ou d’un agent local ; ne pas ouvrir les installations. Distinguer gestes quotidiens, maintenance des réseaux et décisions collectives.',image=('lac-guiers','Le lac de Guiers, réserve d’eau douce du nord du Sénégal.'),related=['g07','g24'])
add('g10','geo','Milieux physiques','Sols et fertilité','Comprendre les possibilités agricoles sans réduire un sol à sa couleur.', '''## Ce qui compose un sol

Un sol associe éléments minéraux, matière organique, eau, air et êtres vivants. Sa texture, sa profondeur, sa structure et son drainage influencent ce qui peut y pousser. Les sols sableux laissent souvent infiltrer l’eau rapidement ; des sols plus argileux peuvent la retenir davantage, mais un engorgement prolongé gêne certaines cultures.

Au Sénégal, les ensembles sableux, les sols ferrugineux, les sols de bas-fonds et les sols salés sont des repères utiles. Les termes locaux dior et deck décrivent des expériences de terrain ; leurs usages ne remplacent pas partout une classification scientifique détaillée. Une parcelle peut présenter plusieurs états selon la saison et les pratiques.

## Préserver les terres cultivées

L’érosion emporte les particules ; l’exportation des récoltes et la baisse des apports organiques peuvent appauvrir les sols. Les rotations, la couverture du sol et des apports adaptés contribuent à la fertilité. Dans les zones salées, la gestion de l’eau est déterminante. Un choix de fertilisant doit s’appuyer sur les conseils agricoles et les caractéristiques réelles du sol.''',['fao','agri'],['La fertilité dépend de plusieurs propriétés du sol.','Érosion et salinisation sont des processus différents.'],'Comparer deux échantillons autorisés de sol : texture au toucher et infiltration d’eau dans des récipients identiques.','Employer une petite quantité de sols non contaminés. La démonstration compare des comportements ; elle ne remplace pas une analyse de fertilité ni un conseil agronomique.',related=['g18','g24'])
add('g11','geo','Paysages et écosystèmes','Les Niayes : dunes et maraîchage','Un espace littoral productif soumis à plusieurs pressions.', '''## Une mosaïque de dunes et de dépressions

Les Niayes se situent le long du littoral nord-ouest. Les dépressions entre les cordons dunaires et la présence d’eau souterraine ont favorisé des activités maraîchères. Le voisinage de grands marchés urbains et les conditions du littoral contribuent aussi à leur importance. La zone n’est pas une bande homogène de jardins.

Légumes, arboriculture et autres usages agricoles coexistent avec l’habitat, les infrastructures et certaines activités industrielles. Les calendriers de production dépendent des espèces cultivées, de l’accès à l’eau et des débouchés, et pas seulement de la saison des pluies.

## Préserver une ressource et une fonction alimentaire

L’urbanisation peut réduire les terres disponibles et morceler les parcelles. L’exploitation des nappes, la salinisation et les pollutions nécessitent une gestion attentive. La protection des Niayes pose une question d’aménagement : comment loger, circuler et développer l’économie tout en maintenant des terres nourricières et des milieux fragiles ? Cette question se traite avec les producteurs, les habitants et les autorités.''',['agri','water'],['Les Niayes associent conditions naturelles et proximité des marchés.','L’eau et le foncier y constituent des enjeux majeurs.'],'Construire un tableau « atouts / contraintes / décisions possibles » pour un périmètre maraîcher.','Faire figurer au moins un facteur naturel et un facteur humain dans chaque colonne. Une décision possible est d’améliorer l’efficience de l’arrosage ; elle n’autorise pas à ignorer les droits fonciers.',related=['g06','g09','g16','r-thies'])
add('g12','geo','Paysages et écosystèmes','Le Ferlo et le pastoralisme','Mobilités, pâturages, points d’eau et activités associées.', '''## Un espace sylvopastoral

Le Ferlo est un vaste espace du nord et du centre intérieur, associé aux milieux sahéliens et aux activités pastorales. La végétation, les pluies et les points d’eau conditionnent l’alimentation du bétail. Les forages ont modifié l’accès à l’eau et l’organisation de certains déplacements, sans supprimer la dépendance aux parcours et aux saisons.

La transhumance est une mobilité organisée des troupeaux pour accéder à l’eau et aux pâturages. Elle mobilise des savoirs, des accords et des itinéraires. Elle ne doit pas être assimilée à une errance. Des éleveurs pratiquent aussi l’agriculture, le commerce ou des activités urbaines ; les situations familiales sont diverses.

## Gérer les complémentarités

Les cultures fournissent parfois des résidus utilisés par les animaux ; l’élevage peut apporter des produits et de la matière organique. Les concurrences deviennent plus fortes quand l’eau, les parcours ou les accès sont restreints. Prévoir des couloirs de passage et des dispositifs de dialogue aide à prévenir des conflits. L’étude d’un paysage pastoral doit donc inclure les règles et les acteurs, en plus du climat.''',['agri','saga'],['Le pastoralisme repose sur une organisation des ressources.','Les activités rurales sont souvent combinées.'],'Tracer le parcours saisonnier fictif d’un troupeau entre trois points d’eau et deux zones de pâturage.','Demander d’argumenter le trajet et d’identifier les terres cultivées à respecter. Le dessin est un modèle pédagogique, pas un itinéraire réel à imposer aux éleveurs.',related=['g06','g19','r-louga','r-matam'])
add('g13','geo','Paysages et écosystèmes','Mangroves, bolongs et tannes','Un milieu entre terre et mer, essentiel aux sociétés littorales.', '''## La mangrove est une forêt particulière

Les palétuviers vivent dans des milieux côtiers soumis aux marées et à des eaux plus ou moins salées. Leurs racines contribuent à retenir les sédiments et offrent des habitats. Dans le Saloum et la basse Casamance, les chenaux appelés bolongs structurent les déplacements et les activités de pêche ou de collecte.

Les tannes sont des surfaces souvent très salées où la végétation est rare. Tous les espaces nus du littoral ne sont pas des tannes et toutes les mangroves ne présentent pas la même dynamique. Il faut observer la salinité, les échanges d’eau et les usages locaux pour comprendre leur évolution.

## Un paysage naturel et culturel

La récolte de coquillages, leur transformation et les déplacements en pirogue relient les communautés à ce milieu. Dans le delta du Saloum, des amas coquilliers témoignent d’occupations anciennes. Préserver la mangrove implique de maintenir les circulations d’eau, de réduire les dégradations et de respecter les pratiques et droits des populations ; planter des arbres ne suffit pas dans un site hydrologiquement défavorable.''',['saloum','fao'],['La marée et la salinité structurent ce milieu.','Les mangroves assurent plusieurs fonctions écologiques et sociales.'],'À partir de la photographie, identifier racines, eau et sol puis proposer deux fonctions de la mangrove.','Les racines sont visibles ; les fonctions de nurserie ou de protection se démontrent avec d’autres observations. Distinguer ce qui est observé de ce qui est expliqué.',image=('saloum','Palétuviers et racines dans un paysage du delta du Saloum.'),related=['g08','g20','h03'])
add('g14','geo','Paysages et écosystèmes','Parcs, biodiversité et patrimoine naturel','Djoudj, Niokolo-Koba et protection des habitats.', '''## Deux espaces, deux fonctionnements

Le Djoudj se situe dans le delta du fleuve Sénégal. Cette zone humide offre repos et alimentation à de nombreux oiseaux, dont des migrateurs. Sa conservation dépend notamment de l’eau, des habitats et de la maîtrise des perturbations. Le nombre d’oiseaux n’est pas identique chaque année.

Le Niokolo-Koba se situe dans le sud-est, autour du système de la Gambie. Il associe savanes, mares et forêts-galeries. La diversité des habitats permet celle de nombreuses espèces. Une ancienne liste d’animaux signalés dans le parc ne constitue pas un comptage de leur population actuelle.

## Protéger sans isoler la nature des habitants

Une aire protégée suppose des règles, des moyens et une coopération avec les populations voisines. Braconnage, feux mal maîtrisés, fragmentation des habitats et perturbations du régime de l’eau peuvent compromettre la conservation. Le tourisme doit respecter les règles du site. L’inscription au patrimoine mondial signale une valeur reconnue ; elle ne met pas automatiquement fin aux menaces.''',['djoudj','niokolo'],['La biodiversité dépend des habitats et de leur fonctionnement.','La protection demande une gestion continue.'],'Comparer le Djoudj et le Niokolo-Koba dans un tableau : localisation, habitat, exemple d’espèce, enjeu.','Accepter pélican et zone humide pour le Djoudj, par exemple élan de Derby et savane pour le Niokolo-Koba. Éviter de transformer une présence historique en promesse d’observation.',image=('djoudj','Un pélican photographié au Djoudj ; l’effectif des oiseaux varie dans le temps.'),related=['g07','g25','r-saint-louis','r-tambacounda'])
add('g15','geo','Population et territoires','Population : recensement, densité et croissance','Des chiffres datés à lire avec leur définition et leur statut.', '''## Compter et estimer

Un recensement dénombre une population à une date et selon une définition. Une projection utilise des hypothèses pour estimer une population future. Le rapport global provisoire du RGPH-5 publié en juillet 2024 retient 18 126 390 habitants pour 2023. Les premiers résultats annonçaient 18 032 473 : il s’agit de publications successives du même recensement, pas de deux populations différentes.

Le millésime 2023 doit accompagner ce repère. Il ne représente pas le nombre exact d’habitants en octobre 2026. Les changements de définition, les contrôles et les révisions expliquent pourquoi les chiffres d’un site ou d’un manuel peuvent différer.

## Lire une répartition

La densité est un rapport entre population et superficie. Une moyenne nationale masque des contrastes : l’ouest concentre des habitants et des activités, tandis que de vastes territoires de l’est sont moins densément peuplés. Une population jeune implique des besoins importants d’éducation, de santé, de formation et d’emploi, mais une pyramide des âges ne détermine pas à elle seule l’avenir d’un pays.

! Ne pas additionner une projection à un recensement ni comparer des régions avec des chiffres d’années différentes sans le signaler.''',['rgph','population','rgph-first'],['Un chiffre de population doit être daté et qualifié.','Densité = population divisée par superficie.'],'Calculer la densité d’un territoire fictif de 20 000 habitants sur 100 km², puis expliquer une limite de cette moyenne.','Le résultat est 200 habitants/km². Cela ne signifie pas que chaque kilomètre carré contient exactement 200 personnes.',related=['g02','g16','g17'],questions=[('18 126 390 habitants : quel millésime et quel statut ?','2023, selon le rapport global provisoire de juillet 2024 du RGPH-5 retenu dans cette fiche.')])
add('g16','geo','Population et territoires','Villes, métropolisation et réseaux urbains','Dakar et les autres pôles : concentration, connexions et défis.', '''## Des villes reliées entre elles

Une ville rassemble des habitants, des services et des activités. Une métropole exerce des fonctions de commandement et entretient des relations avec un territoire plus large. Dakar concentre des institutions, des entreprises, des équipements et des infrastructures de transport. Cette concentration participe à son attraction et aux déplacements quotidiens.

Thiès, Touba, Saint-Louis, Kaolack, Ziguinchor et d’autres villes jouent aussi des rôles régionaux, commerciaux, religieux, universitaires ou administratifs. Un réseau urbain ne se résume donc pas à la capitale. Les villes et leurs campagnes échangent des produits, du travail et des services.

## Aménager l’expansion

La croissance urbaine peut éloigner les logements des emplois, transformer les terres agricoles et augmenter les besoins en eau, assainissement, écoles et transport. L’installation dans des zones basses peut accroître l’exposition aux inondations. Décrire un quartier comme « informel » ou « périphérique » ne permet pas de déduire la situation de chaque habitant. Une analyse géographique doit croiser accessibilité, équipements, habitat et expériences des résidents.''',['ses','rgph','ccdr'],['Dakar domine le réseau urbain mais n’est pas le seul pôle.','La croissance d’une ville exige équipements et planification.'],'Dessiner les liens entre une ville, son marché et trois villages d’approvisionnement.','Utiliser des flèches différentes pour les produits, les personnes et les services. Montrer au moins un échange dans chaque sens.',image=('dakar','Vue d’une partie de Dakar : photographie d’illustration, non relevé urbain actuel.'),related=['g17','g22','r-dakar','r-diourbel'])
add('g17','geo','Population et territoires','Migrations et relations villes–campagnes','Des mobilités aux causes multiples et aux effets variés.', '''## Plusieurs formes de mobilité

Une migration change le lieu de résidence pour une certaine durée ; un trajet quotidien entre domicile et travail relève plutôt de la mobilité pendulaire. Les déplacements peuvent être ruraux, urbains, internes au pays ou internationaux. Les calendriers agricoles, les études, l’emploi, la famille, la sécurité et les conditions environnementales peuvent se combiner dans une décision.

Les villes ne reçoivent pas seulement des habitants des campagnes. Il existe aussi des circulations entre villes, des retours et des formes de résidence partagée. Les relations familiales et économiques peuvent maintenir des liens forts avec le lieu de départ.

## Décrire sans réduire les personnes à une catégorie

Les transferts d’argent, les investissements, les compétences et les réseaux influencent les territoires. Les migrations peuvent aussi créer des difficultés : séparation familiale, coût du déplacement ou accès incertain à l’emploi. Un solde migratoire mesure la différence entre entrées et sorties ; il ne mesure ni le nombre total de voyages ni la valeur des personnes. En classe, traiter ces sujets sans demander à un élève de révéler une histoire familiale sensible.''',['population','ses'],['Migration et déplacement quotidien sont différents.','Les causes et les effets des migrations sont multiples.'],'Classer six situations fictives : trajet scolaire, déménagement, transhumance, séjour touristique, retour durable et voyage familial.','Expliquer la durée et le changement éventuel de résidence. Certaines situations demandent une définition précise avant classement ; accepter une réponse argumentée.',related=['g12','g15','g16'])
add('g18','geo','Activités et échanges','Agriculture et sécurité alimentaire','Cultures pluviales, irrigation, marchés et systèmes alimentaires.', '''## Produire avec des techniques différentes

Le mil, le sorgho, le maïs, le riz, l’arachide, le niébé et les productions horticoles occupent des places différentes selon les territoires. Les cultures pluviales dépendent des pluies ; l’irrigation apporte de l’eau par un dispositif aménagé. Des ménages combinent plusieurs cultures et l’élevage pour diversifier leurs ressources.

La production ne dépend pas seulement du climat : semences, accès au foncier, équipement, financement, main-d’œuvre, conservation et marchés sont essentiels. Une hausse des surfaces ne garantit pas une hausse des rendements. Le rendement est une production rapportée à une surface, tandis que la production totale est une quantité.

## De la récolte à l’alimentation

La sécurité alimentaire repose sur la disponibilité, l’accès, la qualité de l’alimentation et leur stabilité. Elle concerne aussi la transformation, les prix, le transport et le stockage. Produire un aliment dans le pays et permettre à tous les ménages de l’acheter sont deux questions liées mais distinctes. L’adaptation agricole cherche à réduire les pertes et les risques tout en préservant les ressources.''',['agri','saga','ses'],['Production, surface et rendement sont trois indicateurs distincts.','La sécurité alimentaire ne dépend pas uniquement de la récolte.'],'Décrire le trajet d’un sac de riz ou de mil, du producteur au repas familial.','Inclure transformation, transport, vente, préparation et éventuelles pertes. Ne pas attribuer automatiquement la même origine à tous les produits vendus sur un marché.',related=['g06','g10','g19','g23'])
add('g19','geo','Activités et échanges','Élevage et complémentarités rurales','Viande, lait, travail, revenus et gestion des ressources.', '''## Des systèmes divers

Bovins, ovins, caprins et volailles ne sont pas élevés partout de la même façon. Certains systèmes reposent largement sur les parcours et la mobilité ; d’autres combinent cultures et animaux ou utilisent davantage des aliments achetés. Élevage extensif ne signifie pas absence de savoir-faire, et intensification ne signifie pas automatiquement durabilité.

Les animaux fournissent des produits alimentaires, des revenus et parfois du travail ou de la fumure. Les marchés, les fêtes et les besoins des ménages structurent la demande. Le suivi sanitaire, l’accès à l’eau et la qualité de l’alimentation influencent la production.

## Gérer les interactions

L’utilisation de résidus de cultures et les échanges entre agriculteurs et éleveurs peuvent être complémentaires. À l’inverse, des dommages aux cultures, l’enclosure d’un passage ou la saturation d’un point d’eau peuvent provoquer des tensions. Il faut donc étudier les règles d’accès et les accords locaux, pas seulement compter les troupeaux. Les activités de transformation et de vente, souvent peu visibles dans une carte de pâturages, font aussi partie de la filière.''',['ses','agri'],['Il existe plusieurs systèmes d’élevage.','Une filière inclut production, transformation et commercialisation.'],'Construire un schéma de la filière du lait : animaux, collecte, conservation, transformation et vente.','Identifier les moments où le respect de l’hygiène et de la chaîne de conservation est important. L’activité décrit une filière ; elle ne prescrit pas une méthode de soins vétérinaires.',related=['g12','g18','g23'])
add('g20','geo','Activités et échanges','Pêche et ressources aquatiques','De la capture à la transformation, une ressource à préserver.', '''## Plusieurs espaces et plusieurs métiers

Le littoral, les fleuves, les lacs et les estuaires accueillent des pratiques de pêche différentes. Pêche artisanale et pêche industrielle se distinguent par leurs équipements, leurs organisations et leurs zones d’activité, mais cette distinction ne suffit pas à juger chaque pratique. Les quais, les marchés, la transformation, le froid et le transport participent à la filière.

La disponibilité du poisson varie avec les espèces, les saisons, les conditions du milieu et la pression de capture. Une débarque abondante un jour ne prouve pas que la ressource augmente durablement. Les observations doivent être mises en série et comparées aux efforts de pêche.

## Conserver des ressources vivantes

La gestion peut associer réglementation, surveillance, protection des habitats et suivi scientifique. Les mangroves et les zones de reproduction jouent un rôle pour certaines espèces. La transformation et la commercialisation créent des emplois et réduisent certaines pertes, à condition de respecter qualité et hygiène. Pour enseigner, éviter de présenter la mer comme une réserve illimitée ou de réduire le métier de pêcheur à la seule sortie en pirogue.''',['ses','saloum','fao'],['La pêche forme une filière, pas seulement une capture.','Les ressources aquatiques demandent un suivi et une gestion.'],'Associer cinq métiers à une filière de pêche puis repérer deux risques de perte du produit.','Inclure par exemple capture, mareyage, transformation, transport et vente. Évoquer conservation et hygiène sans faire manipuler des produits à risque.',related=['g08','g13','g23'])
add('g21','geo','Activités et échanges','Mines, pétrole, gaz et énergie','Des ressources, des étapes de production et des choix collectifs.', '''## Des ressources localisées

L’or du Sénégal oriental, les phosphates et les matériaux de construction illustrent la diversité du sous-sol. Extraction et transformation ne se déroulent pas toujours au même endroit. Une ressource connue n’est pas nécessairement une réserve économiquement exploitable ; une découverte ne signifie pas qu’une production commerciale a commencé.

Le pétrole de Sangomar entre en production en juin 2024. Pour le gaz de Grand Tortue Ahmeyim, projet partagé avec la Mauritanie, la mise en production intervient à la fin de 2024, puis des jalons de liquéfaction et d’exportation sont franchis en 2025. Ces dates désignent des étapes différentes. Le Sénégal exploitait déjà du gaz à terre avant ces grands projets offshore.

## Comprendre les enjeux

La valeur créée dépend des prix, des coûts, des contrats, de la fiscalité et de l’usage des recettes. Les activités extractives posent aussi des enjeux de travail, d’eau, de déchets, de biodiversité et de transparence. Le système énergétique combine différentes sources ; l’électricité est un produit issu de leur conversion. Le solaire et les autres renouvelables demandent, eux aussi, des réseaux et une planification.''',['oil','ses','ccdr'],['Découverte, mise en production et exportation sont des étapes distinctes.','Une ressource ne garantit pas automatiquement un revenu partagé.'],'Classer les étapes d’un projet : découverte, études, investissement, production, transport, vente et recettes publiques.','Discuter les liens et les délais ; les recettes dépendent de règles et de coûts. Ne pas demander de prédire un enrichissement individuel à partir d’un gisement.',related=['g04','g24','r-kedougou'])
add('g22','geo','Activités et échanges','Transports et aménagement du territoire','Routes, rail, ports et déplacements du quotidien.', '''## Relier des lieux et des fonctions

Un réseau de transport associe des axes, des nœuds et des terminaux. Au Sénégal, routes, liaisons ferroviaires, ports et aéroports relient les régions et les pays voisins. Dakar joue un rôle majeur dans les échanges, mais les carrefours de Thiès, Kaolack ou Tambacounda et les passages vers la Casamance structurent aussi les circulations.

Le coût et le temps de trajet influencent l’accès à un marché, une école ou un centre de santé. Une distance courte à vol d’oiseau peut correspondre à un déplacement long en raison d’un obstacle, d’un détour ou d’une mauvaise desserte. L’accessibilité est donc plus riche que la simple distance.

## Des héritages et des transformations

Les anciens axes ferroviaires ont accompagné l’économie coloniale et la croissance de certaines villes. Aujourd’hui, les choix d’aménagement doivent articuler transport de voyageurs, marchandises, sécurité, entretien et environnement. Une infrastructure construite n’apporte pas les mêmes avantages à tous : examiner les tarifs, les horaires et les connexions avec les quartiers et les villages.''',['ses','rail'],['Un réseau comprend des axes et des nœuds.','L’accessibilité dépend du temps, du coût et de la desserte.'],'Comparer deux trajets vers une école : un trajet court avec un obstacle et un trajet plus long mais directement desservi.','Utiliser des temps fictifs clairement annoncés. Demander de justifier le trajet le plus accessible selon l’usager, sans considérer uniquement les kilomètres.',related=['g16','g23','h18'])
add('g23','geo','Activités et échanges','Commerce, services, artisanat et tourisme','Une économie d’échanges aux activités visibles et moins visibles.', '''## Des activités qui relient les territoires

Le commerce met en relation producteurs, intermédiaires et consommateurs. Un marché hebdomadaire, une boutique, un atelier et une grande entreprise n’ont pas la même organisation, mais participent tous à des échanges. L’artisanat combine savoir-faire, production et vente ; les services comprennent notamment transport, éducation, santé, finance et activités numériques.

Le terme secteur informel renvoie à des critères statistiques et institutionnels. Il n’est pas synonyme de travail sans compétence, et il ne permet pas de déclarer toute activité illégale. Pour comparer des emplois, il faut aussi regarder revenu, protection, durée et conditions de travail.

## Tourisme et ressources territoriales

Les paysages, les patrimoines et les cultures attirent des visiteurs. Le tourisme mobilise hébergement, restauration, guides, transport et artisanat. Ses effets dépendent de la saisonnalité, de l’emploi local, des conditions de visite et de la préservation des lieux. Un site ne doit pas être réduit à un décor ; ses habitants, ses usages et sa mémoire demeurent au centre du territoire.''',['ses','patrimoine'],['Le commerce et les services structurent les relations entre lieux.','Le tourisme peut créer des activités et exercer des pressions.'],'Imaginer une visite responsable d’un site : trajet, accueil, activité, achat local et règle de protection.','Relier chaque choix à un effet possible. Prévoir une règle de respect des habitants et une règle de préservation du lieu ; ne pas promettre un accès non autorisé.',related=['g18','g20','g25','h26'])
add('g24','geo','Environnement et développement','Risques, changement climatique et adaptation','Sécheresses, inondations, érosion et actions à plusieurs échelles.', '''## Un risque associe aléa, exposition et vulnérabilité

Une pluie forte est un aléa. Les dommages dépendent aussi de la localisation des personnes et des biens, de la qualité des ouvrages et de la capacité à se préparer. Une même quantité de pluie ne produit donc pas les mêmes conséquences dans tous les quartiers. De même, un déficit de pluies n’affecte pas toutes les cultures et toutes les familles de manière identique.

Le littoral subit des dynamiques d’érosion et de submersion ; les activités humaines peuvent accentuer l’exposition. La salinisation, la dégradation des sols et les tensions sur l’eau concernent d’autres espaces. Le changement climatique modifie certains paramètres et certains risques, mais chaque sinistre doit être analysé dans son contexte.

## Des actions complémentaires

Adapter les cultures, améliorer le drainage et l’entretien, préserver les zones humides et organiser l’urbanisation sont des leviers. Les gestes des ménages ne remplacent pas les décisions d’aménagement. L’atténuation réduit les émissions de gaz à effet de serre ; l’adaptation réduit les effets et les vulnérabilités. Les scénarios climatiques expriment des futurs possibles, pas des dates certaines de catastrophe.''',['ccdr','water','saga'],['Un aléa ne suffit pas à définir un risque.','Adaptation et atténuation sont complémentaires mais différentes.'],'Pour une école fictive en zone inondable, proposer une action avant la saison des pluies, une règle d’alerte et un aménagement collectif.','Prioriser les consignes locales de sécurité et le repérage des responsables. Ne pas faire traverser une zone inondée pour observer le phénomène. Distinguer prévention et intervention d’urgence.',related=['g05','g09','g16'])
add('g25','geo','Paysages et écosystèmes','Les sept biens du patrimoine mondial','Lire ensemble nature, histoire et paysages culturels.', '''## Une reconnaissance internationale

Au 31 octobre 2026, la liste du patrimoine mondial recense sept biens pour le Sénégal. Gorée, Saint-Louis, les cercles mégalithiques de Sénégambie, le delta du Saloum et le pays Bassari sont des biens culturels. Le Djoudj et le Niokolo-Koba sont des biens naturels. Certains biens traversent une frontière, comme les cercles partagés avec la Gambie.

## Un patrimoine n’est pas seulement un bâtiment

Un paysage culturel résulte de relations prolongées entre communautés et milieu : le Saloum associe milieux estuariens et amas coquilliers ; le pays Bassari réunit habitats, cultures et pratiques sociales. Une aire naturelle possède aussi une histoire humaine. La distinction culturel/naturel sert au classement international, pas à séparer totalement sociétés et environnement.

La reconnaissance impose de préserver les valeurs du bien et d’organiser sa gestion. Elle ne signifie pas que tous les sites importants du pays sont inscrits. Le patrimoine national, les mémoires locales et les traditions vivantes dépassent cette liste. Une visite scolaire doit préparer observation, contexte, règles et exploitation pédagogique après la sortie.''',['patrimoine','saloum','bassari'],['Sept biens sont inscrits pour le Sénégal à la date de cette édition.','Une inscription ne résume pas tout le patrimoine national.'],'Choisir un bien et proposer une question de géographe et une question d’historien.','Pour le Saloum : comment circulent eau et activités ? Que révèlent les amas coquilliers sur les occupations anciennes ? Les réponses attendues mobilisent des types de sources différents.',related=['g14','h03','h26'],extra=[table(['Bien','Type','Inscription'],[['Île de Gorée','Culturel','1978'],['Djoudj','Naturel','1981'],['Niokolo-Koba','Naturel','1981'],['Île de Saint-Louis','Culturel','2000'],['Cercles mégalithiques de Sénégambie','Culturel, avec la Gambie','2006'],['Delta du Saloum','Culturel','2011'],['Pays Bassari','Culturel','2012']])])
add('g26','geo','Paysages et écosystèmes','Casamance et Sénégal oriental : comparer les paysages','Des espaces méridionaux divers, à ne pas confondre.', '''## Des traits communs et des différences

La Casamance correspond à un grand ensemble du sud, réparti notamment entre Ziguinchor, Sédhiou et Kolda. La basse Casamance est fortement marquée par l’estuaire, les mangroves et certains paysages rizicoles. Vers l’intérieur, d’autres combinaisons de cultures, d’élevage, de villes et de formations végétales se rencontrent. Le mot Casamance ne désigne donc pas une région administrative unique.

Le Sénégal oriental inclut des territoires de l’est et du sud-est, notamment Tambacounda et Kédougou. Les vastes savanes, les cours d’eau et les reliefs du sud-est créent des paysages variés. Le pays Bassari, autour de Salémata, Bandafassi et Dindéfello, montre des adaptations culturelles particulières au milieu.

## Une comparaison raisonnée

Pour comparer deux paysages, retenir les mêmes critères : relief, eau, végétation, habitat, activités et circulations. Éviter les formules qui présentent une région comme uniquement « traditionnelle », uniquement agricole ou vide d’habitants. Les paysages changent avec les saisons et les choix sociaux. Une photographie peut servir de point de départ, mais une carte et une enquête complètent son interprétation.''',['bassari','fao','regions'],['Casamance et Sénégal oriental sont des ensembles géographiques, pas une seule région administrative.','Une comparaison exige les mêmes critères.'],'Comparer un paysage de bolong et la cascade de Dindéfello à l’aide de six critères communs.','Préciser ce que les images permettent de voir et ce qui nécessite des documents complémentaires. Ne pas attribuer une seule culture ou activité à toute une région.',image=('niokolo','Le fleuve Gambie dans le parc du Niokolo-Koba : eau et végétation du Sénégal oriental.'),related=['g03','g04','g13','r-kolda','r-kedougou'])

# Les départements sont explicitement rattachés au découpage de référence du RGPH-5 (2023).
regional=[
('dakar','Dakar',['Dakar','Guédiawaye','Pikine','Rufisque','Keur Massar'],'À l’extrémité occidentale du pays, sur la presqu’île du Cap-Vert et ses prolongements, Dakar associe capitale nationale, espaces portuaires, habitat dense et périphéries en transformation. L’océan encadre fortement le territoire et les possibilités d’extension.','Les fonctions administratives, les services, les échanges et les activités industrielles y sont concentrés. L’agriculture et la pêche restent présentes dans certains secteurs. Les enjeux portent sur les déplacements, le logement, l’eau, l’assainissement, les terres agricoles et les risques littoraux.','Ne pas confondre la ville de Dakar avec toute la région, ni la capitale nationale avec chaque quartier de l’agglomération.','dakar',['g16','g22']),
('diourbel','Diourbel',['Bambey','Diourbel','Mbacké'],'Région intérieure du centre-ouest, Diourbel se rattache à l’histoire du Baol et à l’espace du bassin arachidier. Son chef-lieu est Diourbel ; Touba, située dans le département de Mbacké, constitue un pôle religieux, commercial et urbain majeur.','Les échanges, l’artisanat, les services, les cultures pluviales et l’élevage composent son économie. La croissance des espaces bâtis pose des questions de réseaux et d’équipements ; les activités rurales sont sensibles à l’accès à l’eau et à la fertilité des sols.','Une ville peut être plus peuplée ou plus influente dans un domaine sans être le chef-lieu régional.',None,['g16','g18','h09']),
('fatick','Fatick',['Fatick','Foundiougne','Gossas'],'Fatick associe espaces du centre-ouest, paysages du Sine et du Saloum et zones littorales ou estuariennes. Son chef-lieu est Fatick. L’insularité, les chenaux et les mangroves caractérisent certains secteurs, mais pas toute la région.','Agriculture, élevage, pêche, collecte et transformation de produits aquatiques, commerce et tourisme se combinent selon les lieux. La salinité des eaux et des sols, les transports entre îles et continent et la préservation du patrimoine constituent des enjeux importants.','Le delta du Saloum est un paysage culturel et écologique ; il ne se confond pas avec la totalité d’une région administrative.','saloum',['g13','g25','h06']),
('kaffrine','Kaffrine',['Birkelane','Kaffrine','Koungheul','Malem Hodar'],'Située au centre du Sénégal, Kaffrine appartient à un espace de transition entre des milieux agricoles et sylvopastoraux. Elle devient région en 2008. Son chef-lieu porte le même nom ; les axes vers l’est lui donnent une fonction de passage et d’échange.','Les cultures pluviales, notamment céréales et arachide, et l’élevage sont des repères de l’économie rurale. L’accès aux marchés et aux équipements, la variabilité des pluies et la préservation de la fertilité influencent les conditions de production. Les activités urbaines et commerciales complètent cet ensemble.','Une région agricole comprend aussi des villes, des services et des mobilités ; elle ne se réduit pas aux champs.',None,['g06','g18','g19']),
('kaolack','Kaolack',['Guinguinéo','Kaolack','Nioro du Rip'],'Kaolack est un carrefour du centre-ouest, relié aux espaces du bassin arachidier et aux axes vers la Gambie, la Casamance et l’est. Son chef-lieu est un centre de commerce et de services lié à l’histoire des échanges agricoles.','Les cultures pluviales, l’élevage, la transformation et les marchés structurent des relations entre villes et campagnes. Les paysages sont aussi marqués par le Saloum et, dans certains secteurs, des contraintes de salinité. Les enjeux concernent production, circulation, emplois, assainissement et restauration des terres.','Un carrefour se définit par les relations qu’il organise, et pas seulement par sa position sur une route.',None,['g18','g22','h06']),
('kedougou','Kédougou',['Kédougou','Salémata','Saraya'],'Au sud-est, près de la Guinée et du Mali, Kédougou présente des reliefs et des vallées plus marqués que la majeure partie du pays. Érigée en région en 2008, elle comprend des paysages liés à la Gambie et à la Falémé et le territoire du pays Bassari.','Agriculture, élevage, activités minières, commerce et tourisme y coexistent. Les mines d’or posent des enjeux d’emploi, de partage des revenus, de santé et de protection de l’eau. La conservation des habitats, l’accès aux équipements et les liaisons de transport sont également importants.','Ne pas confondre un potentiel minier avec un revenu assuré pour tous les habitants.','dindefelo',['g04','g21','g25']),
('kolda','Kolda',['Kolda','Médina Yoro Foulah','Vélingara'],'Kolda appartient à la haute Casamance, dans le sud intérieur. Elle se distingue de la basse Casamance estuarienne : les paysages et les activités ne s’organisent pas tous autour des mangroves. Le chef-lieu régional est Kolda.','L’agriculture et l’élevage occupent une place importante, avec des marchés, des circulations transfrontalières et des services urbains. La gestion des formations végétales, des terres et de l’eau, ainsi que l’accès aux transports et aux équipements, participent aux enjeux régionaux. Les usages des sols varient selon les localités.','La Casamance est un grand ensemble géographique ; ses différentes parties n’ont pas un paysage unique.',None,['g19','g26']),
('louga','Louga',['Kébémer','Linguère','Louga'],'Louga s’étend du littoral vers de vastes espaces intérieurs du nord-ouest. Cette extension met en relation des milieux côtiers, agricoles et pastoraux. Le chef-lieu est Louga, tandis que Linguère constitue un repère important pour l’étude du Ferlo.','Élevage, cultures, commerce, artisanat et services s’articulent aux mobilités des populations. Les disponibilités en eau et en pâturages, les liaisons entre localités et l’accès aux équipements sont des questions majeures. Il faut distinguer les situations littorales de celles de l’intérieur plutôt que généraliser à toute la région.','Un même territoire administratif peut rassembler plusieurs zones écologiques.',None,['g06','g12','g17']),
('matam','Matam',['Kanel','Matam','Ranérou Ferlo'],'Matam associe une partie de la vallée du fleuve Sénégal et de vastes territoires intérieurs du Ferlo. La frontière avec la Mauritanie et les relations à l’amont et à l’aval du fleuve contribuent à sa situation géographique. Son chef-lieu est Matam.','Les activités combinent agriculture de vallée, irrigation dans certains secteurs, élevage, commerce et services. Les mobilités et les liens avec les migrants ont une place dans les relations économiques et familiales. Les ressources en eau, les crues et la desserte des espaces intérieurs exigent des approches différentes selon les lieux.','Vallée irriguée et espaces pastoraux peuvent appartenir à la même région administrative.',None,['g07','g12','g17']),
('saint-louis','Saint-Louis',['Dagana','Podor','Saint-Louis'],'La région de Saint-Louis occupe une partie du nord du Sénégal, du littoral à la vallée du fleuve. Le chef-lieu se situe près de l’embouchure et comprend une île historique inscrite au patrimoine mondial. Le delta et le lac de Guiers fournissent d’autres repères essentiels.','Les activités associent agriculture irriguée, élevage, pêche, commerce, services et tourisme. L’eau doit être partagée entre usages productifs, alimentation et conservation. Les crues, l’érosion et la submersion littorale touchent certains secteurs ; elles ne concernent pas chaque localité de façon identique.','La région ne se limite ni à l’île historique ni à la ville du même nom.','saint-louis',['g07','g09','g14','h11']),
('sedhiou','Sédhiou',['Bounkiling','Goudomp','Sédhiou'],'Créée en 2008, la région de Sédhiou se situe dans la moyenne Casamance. Les cours d’eau et les relations avec les territoires voisins marquent l’organisation de l’habitat et des activités. Son chef-lieu est Sédhiou.','L’agriculture, notamment les productions vivrières et l’arboriculture selon les secteurs, l’élevage, la pêche et les échanges occupent une place importante. L’accessibilité des localités, la gestion des sols et de l’eau et l’accès aux services constituent des enjeux de développement. Les territoires proches des cours d’eau et ceux de plateau ont des conditions différentes.','La notion de moyenne Casamance aide à situer un espace mais ne suffit pas à décrire toutes ses activités.',None,['g08','g18','g26']),
('tambacounda','Tambacounda',['Bakel','Goudiry','Koumpentoum','Tambacounda'],'Tambacounda couvre un vaste espace de l’est du Sénégal. Son chef-lieu constitue un carrefour vers le Mali, Kédougou et les autres régions. La vallée et les affluents du Sénégal, les espaces de savane et le secteur du Niokolo-Koba fournissent des repères variés.','Agriculture, élevage, commerce, transport et conservation des milieux y coexistent. Les grandes distances entre certaines localités influencent l’accès aux écoles, aux soins et aux marchés. La gestion des ressources naturelles et des espaces protégés demande de tenir compte des besoins des populations et des relations transfrontalières.','Une faible densité moyenne ne signifie pas un territoire vide ou dépourvu d’activités.','niokolo',['g07','g14','g22']),
('thies','Thiès',['Mbour','Thiès','Tivaouane'],'Thiès relie Dakar à plusieurs grands axes nationaux. La région réunit des plateaux, des espaces agricoles, les Niayes et une façade littorale. Son chef-lieu possède une histoire ferroviaire importante ; Mbour et Tivaouane illustrent d’autres fonctions urbaines.','Pêche, horticulture, industrie, activités extractives, tourisme, artisanat et services forment une économie diversifiée. La concurrence pour l’espace et pour l’eau peut être forte. Les liens avec la métropole dakaroise, les circulations quotidiennes et la protection des espaces littoraux constituent des questions d’aménagement.','Ne pas attribuer une seule fonction à une région qui comprend des villes, des campagnes et plusieurs littoraux.',None,['g11','g20','g22','h18']),
('ziguinchor','Ziguinchor',['Bignona','Oussouye','Ziguinchor'],'Ziguinchor correspond à la basse Casamance et à une partie du littoral sud. L’estuaire, les bolongs, les mangroves et les terres rizicoles caractérisent plusieurs de ses paysages. La ville de Ziguinchor est le chef-lieu régional et un pôle de services et d’échanges.','Agriculture, pêche, tourisme, transformation et commerce se combinent à des pratiques sociales et culturelles diverses. Les relations avec la Gambie et la Guinée-Bissau, les transports, la préservation des milieux et la consolidation de la paix sont des enjeux territoriaux. Il ne faut ni réduire la région au conflit ni nier ses effets historiques.','Une fiche régionale doit montrer les habitants, les activités et les transformations, au-delà des seuls paysages touristiques.','saloum',['g08','g13','g26','h24']),
]
for key,name,depts,location,economy,caution,image,related in regional:
 blocks='## Situation et paysages\n\n'+location+'\n\n## Activités et enjeux\n\n'+economy+'\n\n! '+caution
 # L’image du Saloum n’est pas réutilisée pour représenter un paysage de Casamance.
 photo=(image,'Vue ancienne du pont Faidherbe à Saint-Louis ; document historique.') if key=='saint-louis' else (image,{'dakar':'Vue d’une partie de Dakar.','fatick':'Mangrove dans le delta du Saloum.','kedougou':'Cascade de Dindéfello, dans la région de Kédougou.','tambacounda':'Le fleuve Gambie au Niokolo-Koba.'}.get(key,'Paysage d’illustration.')) if image and key!='ziguinchor' else None
 add('r-'+key,'geo','Les 14 régions',name+' : profil régional','Chef-lieu : '+name+' · repères de localisation, activités et enjeux.',blocks,['regions','rgph','map'],['Chef-lieu régional : '+name+'.',caution],f'Situer {name} sur la carte puis comparer deux de ses traits avec ceux de la région de l’école.','Utiliser les mêmes critères : position, milieu, activités et accessibilité. Éviter un classement en région « meilleure » ou « moins bonne » ; justifier les différences.',image=photo,related=related,extra=[table(['Découpage de référence','Départements'],[['RGPH-5, 2023',' ; '.join(depts)]])])

src('hga','Histoire générale de l’Afrique : collection et démarche','UNESCO','https://www.unesco.org/fr/general-history-africa','Collection scientifique, plusieurs volumes','Ouvrages de référence pour élargir le cadre africain ; l’app n’en reproduit pas les chapitres. Les synthèses anciennes se lisent avec les recherches récentes.')
src('sine','Histoire du Sine-Saloum','Fonds documentaire IRD / recherche historique','https://www.documentation.ird.fr/hor/fdi%3A35086','1986','Notice et ouvrage de recherche sur le Sine-Saloum ; les généalogies et traditions demandent une confrontation de sources.')
src('fouta','La révolution du Fouta et Abdoul Khadre Kane','APS, présentation d’un ouvrage universitaire','https://aps.sn/un-universitaire-revisite-les-enseignements-dabdoul-khadre-kane-premier-almamy-du-fouta/','2025','Repère de la révolution de 1776 et de l’almamat ; distinguer Thierno Souleymane Baal et Abdoul Khadre Kane.')
src('kaabu','Le Kaabu, patrimoine historique guinéo-séné-gambien','AfricaBib, notice de recherche','https://www.africabib.org/rec.php?DB=p&RID=108872173','Notice bibliographique','Rappel du caractère transfrontalier de cet espace et des liens avec Casamance et Guinée-Bissau ; ne pas tracer de frontières modernes sur cet ancien ensemble.')
src('maba','Contexte historique et politique de Maba Diakhou Ba','APS, présentation de travaux dirigés par Mor Ndao (UCAD)','https://aps.sn/un-ouvrage-revisite-le-contexte-historique-et-politique-du-jihad-de-maba-diakhou-ba/','2026','Renvoie à des travaux collectifs et à la pluralité des dimensions politiques, spirituelles et militaires.')
src('nder','Nder : mémoire d’une résistance','Agence de presse sénégalaise','https://aps.sn/nder-village-historique-de-dagana-reclame-plus-dinfrastructures/','9 mars 2025','Date commémorée : 7 mars 1820. Le récit de Nder relève aussi de traditions transmises, dont les variantes ne sont pas toutes des archives datées.')
src('senghor','Léopold Sédar Senghor','Présidence de la République du Sénégal','https://www.presidence.sn/fr/presidence/leopold-sedar-senghor/','Mandat 1960–1980','Poète et premier président. Les appréciations institutionnelles sont distinguées des repères factuels.')
src('dia','Les premières institutions et le gouvernement de Mamadou Dia','RTS, lecture des actes du Journal officiel','https://www.rts.sn/actualite/detail/a-la-une/17-septembre-1960-aux-origines-du-premier-gouvernement-du-senegal-independant','Septembre 2026','Sépare nomination, publication des textes et crise de 1962 ; aide à comprendre les différences de dates entre notices.')
src('senegambie','Textes instituant la Confédération de Sénégambie','Direction des Relations avec les Institutions du Sénégal','https://www.dri.gouv.sn/%C3%A9tiquettes/conf%C3%A9d%C3%A9ration-de-la-s%C3%A9n%C3%A9gambie','Pacte 1981 et lois 1982–1983','Signature en décembre 1981 et mise en place institutionnelle en 1982 ; ne pas confondre avec la Fédération du Mali de 1960.')
src('refugies','Retour de réfugiés mauritaniens depuis le Sénégal','HCR / UNHCR','https://www.unhcr.org/fr/actualites/briefing-notes/accord-tripartite-sur-le-retour-des-refugies-mauritaniens','2007','Crise de 1989, déplacements et retour volontaire ; ne pas attribuer collectivement une responsabilité à un peuple.')
src('paix','Accord de Bissau et développement de la Casamance','Présidence du Sénégal, Conseil des ministres','https://www.presidence.sn/fr/actualites/communique-du-conseil-des-ministres-du-mercredi-26-fevrier-2025/','26 février 2025','Mentionne l’accord du 23 février 2025. Un accord et sa mise en œuvre sont deux objets distincts ; aucune garantie de sécurité actuelle n’est formulée.')
src('joola','Commémoration du naufrage du Joola','Ministère sénégalais des Forces armées','https://forcesarmees.gouv.sn/actualites/20eme-anniversaire-du-naufrage-du-bateau-le-joola','2022','Date du naufrage : 26 septembre 2002 ; mémoire des victimes et responsabilité collective. Pas d’image de victimes.')
src('ifan','Recherche scientifique et laboratoire carbone 14','IFAN, Université Cheikh Anta Diop','https://ifan.ucad.sn/botanique-geologie/','Présentation de laboratoire','Rôle de Cheikh Anta Diop dans la recherche et la datation ; les dates de création et d’officialisation varient selon les notices, elles ne sont pas confondues.')

add('h01','history','Sources et temps historique','Comment connaît-on l’histoire du Sénégal ?','Archéologie, traditions orales, écrits et critique des sources.', '''## Une histoire construite à partir de traces

Les objets, les sites, les récits transmis, les manuscrits, les photographies et les archives permettent d’étudier le passé. Chaque source a un auteur ou un contexte de production, une date et une fonction. Un document administratif colonial ne décrit pas nécessairement le point de vue des populations ; un récit familial ne raconte pas toutes les expériences d’une période.

Les traditions orales conservent des généalogies, des valeurs et des événements. Elles ne doivent ni être rejetées parce qu’elles sont orales ni être transformées sans examen en chronologies exactes. Les comparer aux données archéologiques et aux écrits permet de préciser ce qui est établi et ce qui reste discuté.

## Faire travailler les sources ensemble

L’archéologie étudie les traces matérielles et leur contexte. Les méthodes de datation fournissent des fourchettes, pas toujours une année précise. Les photographies et les témoignages récents doivent aussi être confrontés. Une synthèse honnête indique ses limites et peut être corrigée par une découverte.

! Dire « nous ne savons pas précisément » constitue parfois une réponse scientifique plus juste qu’une date inventée. L’histoire et la mémoire se complètent, mais elles ne répondent pas exactement aux mêmes questions.''',['hga','faleme','prehistoire'],['Les sources se lisent en fonction de leur contexte.','Une tradition de fondation n’a pas le même statut qu’un acte daté.'],'Comparer un récit oral local et une photographie ancienne : auteur, date, intention, informations et limites.','Accueillir le témoignage avec respect puis demander ce qu’il permet réellement d’établir. Ne pas noter un récit comme faux parce qu’une variante existe ; chercher les convergences et les différences.',related=['h02','h26','g03'],questions=[('Pourquoi croiser plusieurs sources ?','Parce qu’elles éclairent des aspects différents et permettent de repérer oublis, contradictions ou points de vue.')])
add('h02','history','Premiers peuplements','Préhistoire et premiers peuplements','Des occupations anciennes étudiées grâce aux vestiges et aux datations.', '''## Avant les sources écrites locales

La préhistoire se connaît surtout par l’archéologie. Dans l’actuel Sénégal, des outils de pierre et d’autres vestiges témoignent de longues histoires de peuplement. La vallée de la Falémé, le littoral et plusieurs espaces intérieurs ont livré des indices. Les recherches de la Falémé associent étude des outils, des sédiments et des milieux anciens.

Le Paléolithique renvoie à des sociétés et des techniques très diverses sur de longues durées. Au Néolithique, l’étude de la pierre polie, de la céramique et d’autres indices renseigne sur des transformations des modes de vie. Les changements ne se produisent pas simultanément dans toutes les régions.

## Observer sans inventer

Un outil de pierre ne permet pas, à lui seul, de connaître la langue, le nom d’un peuple ou la forme exacte de sa société. Son emplacement et ses relations avec les autres vestiges comptent. Un objet archéologique n’est pas nécessairement un fossile : les fossiles sont des traces ou restes d’êtres vivants anciens.

Les recherches actuelles peuvent modifier les chronologies. On évite donc d’attribuer aux premières populations des identités contemporaines ou de raconter une migration unique à partir d’un seul objet.''',['faleme','prehistoire'],['L’archéologie permet d’étudier des périodes sans écrits locaux.','Les chronologies sont régionales et peuvent être révisées.'],'Décrire le dessin d’un outil : matière, forme, traces possibles et questions encore ouvertes.','Distinguer observation et interprétation. On peut formuler une hypothèse d’usage, mais pas déduire automatiquement le nom du fabricant, son peuple ou sa langue.',related=['h01','h03'])
add('h03','history','Premiers peuplements','Protohistoire, mégalithes et amas coquilliers','Des sociétés organisées avant les chroniques abondantes.', '''## Des monuments qui demandent une organisation

Les cercles mégalithiques de Sénégambie sont des ensembles de pierres dressées, souvent associés à des pratiques funéraires. Le bien inscrit comprend Sine Ngayène et Wanar au Sénégal, Wassu et Kerbatch en Gambie. Les fouilles révèlent des usages sur une très longue période, et non un événement unique ayant la même date partout.

Extraire, tailler et déplacer des blocs de latérite suppose des savoir-faire et une organisation collective. Les vestiges permettent d’interroger les techniques, les échanges et les rites ; ils ne livrent pas directement tous les noms des populations concernées.

## Les amas coquilliers du Saloum

Des accumulations de coquilles témoignent d’activités humaines répétées. Certaines sont associées à des sépultures et à d’autres objets. Leur étude renseigne sur l’alimentation, les milieux, les déplacements et les occupations anciennes. Un paysage peut donc être à la fois un milieu vivant et une archive du passé.

! Un grand monument n’est pas automatiquement une œuvre étrangère ou mystérieuse. Commencer par les preuves archéologiques et les techniques documentées plutôt que par une légende présentée comme certitude.''',['megalithes','saloum'],['Les mégalithes sont liés à des sociétés et à des pratiques funéraires anciennes.','Les amas coquilliers constituent aussi des archives archéologiques.'],'Comparer une photographie de mégalithes et une description d’amas coquillier : matériaux, activités et informations possibles.','Relever pierre dressée et coquilles accumulées. Distinguer l’activité à l’origine du vestige et les questions que les fouilles peuvent résoudre.',image=('megalithes','Cercles de pierres à Sine Ngayène, un des sites du bien transfrontalier de Sénégambie.'),related=['g13','g25','h02'])
add('h04','history','Royaumes et sociétés','Sénégambie et grands ensembles ouest-africains','Relier l’histoire locale aux échanges et aux pouvoirs de la région.', '''## Un espace historique plus large que les frontières actuelles

La Sénégambie est un espace historique de relations entre les bassins du Sénégal et de la Gambie, le littoral et leurs arrière-pays. Les États actuels n’existaient pas sous cette forme. Des réseaux reliaient ces territoires aux mondes sahariens, sahéliens et guinéens.

Les ensembles du Ghana, du Mali puis du Songhaï ont structuré une partie de l’histoire ouest-africaine. Leurs zones d’influence ont changé ; il ne faut pas colorier tout le Sénégal actuel comme une province permanente d’un même empire. L’or, le sel, les produits agricoles, les techniques et les savoirs circulaient par des réseaux aux acteurs multiples.

## Pouvoir, commerce et sociétés

Un empire peut associer un centre politique, des territoires tributaires et des autorités locales. Les relations ne se limitent pas à une conquête : alliances, échanges et concurrences interviennent aussi. Les villes et les campagnes ont leurs organisations propres. L’histoire d’un royaume ne doit pas effacer les cultivateurs, les artisans, les pasteurs, les femmes et les personnes privées de liberté qui participaient à ces sociétés.''',['hga','royaumes'],['Les frontières et les influences ont changé dans le temps.','La Sénégambie désigne un espace historique de relations.'],'Comparer une carte politique actuelle et un schéma d’anciens réseaux d’échanges.','Demander ce que chaque document représente. Ne pas chercher une correspondance exacte entre les limites d’un empire et celles des États contemporains.',related=['g01','h05','h06','h10'])
add('h05','history','Royaumes et sociétés','Tekrur, Fouta-Toro et révolution de 1776','Des États et des transformations dans la vallée du Sénégal.', '''## Une vallée ancienne de peuplement et d’échanges

Le Tekrur apparaît dans les écrits médiévaux concernant la vallée du fleuve Sénégal. Il est associé aux échanges et à une islamisation ancienne des élites. Les textes n’emploient pas toujours ce nom avec le même sens : lieu, État et désignation de populations doivent être distingués.

Le Fouta-Toro connaît ensuite plusieurs configurations politiques. La dynastie des Denianké, liée à Koli Tenguella, précède l’almamat instauré à la fin du XVIIIe siècle. Les changements politiques s’accompagnent de relations entre groupes sociaux, pouvoirs locaux et réseaux religieux.

## Le repère de 1776

La révolution torodo de 1776 est associée à Thierno Souleymane Baal. Abdoul Khadre Kane devient une figure majeure de l’almamat. L’événement porte des enjeux religieux, sociaux et politiques ; il ne résume pas l’introduction de l’islam, beaucoup plus ancienne, et ne transforme pas toutes les relations sociales en une seule journée.

! Le titre almamy appartient à un contexte politique et religieux précis. Il ne doit pas être attribué indistinctement à tous les souverains de la vallée depuis les origines.''',['royaumes','fouta','hga'],['Tekrur et Fouta-Toro désignent des histoires liées mais non identiques.','1776 marque une transformation politique, pas le début de toute présence musulmane.'],'Organiser quatre repères sans leur inventer une date : Tekrur médiéval, Denianké, révolution de 1776, almamat.','Faire préciser que l’ordre des grandes étapes est plus certain que toutes les dates de fondation. Relier les étapes à la vallée du fleuve Sénégal.',related=['g07','h04','h08'])
add('h06','history','Royaumes et sociétés','Grand Jolof, Cayor, Baol et Waalo','Un pouvoir régional puis des royaumes aux trajectoires propres.', '''## La formation du Grand Jolof

La tradition associe Ndiadiane Ndiaye à la fondation du Jolof. Les récits présentent des variantes et ne constituent pas une biographie entièrement datée. Le Grand Jolof organise, à certaines périodes, des relations de domination et de tribut avec plusieurs territoires du centre-ouest et du nord.

Au XVIe siècle, cet ensemble se fragmente et des pouvoirs locaux affirment leur autonomie. Les trajectoires du Cayor, du Baol, du Waalo, du Sine et du Saloum ne sont pas identiques. Le Jolof subsiste comme royaume dans un espace plus réduit.

## Des titres, des institutions et des populations

Le bourba est associé au Jolof, le damel au Cayor, le teigne au Baol et le brak au Waalo. Ces titres facilitent le repérage ; ils ne suffisent pas à expliquer les modes de succession, les alliances et l’autorité des différents acteurs. Les linguères occupent une place politique importante dans certains royaumes.

Les populations échangeaient et se déplaçaient. Il faut éviter d’imaginer des royaumes fermés correspondant chacun à une ethnie homogène ou à une région administrative actuelle.''',['jolof','royaumes'],['Le Grand Jolof et le royaume du Jolof après fragmentation ne sont pas identiques.','Les titres de souverains dépendent des royaumes.'],'Associer royaume et titre, puis situer approximativement les ensembles sur un schéma.','Jolof/bourba ; Cayor/damel ; Baol/teigne ; Waalo/brak. Noter que le schéma représente un repérage historique, pas des frontières cadastrales.',related=['h04','h07','h13','r-diourbel'])
add('h07','history','Royaumes et sociétés','Sine, Saloum, Kaabu et sociétés méridionales','Des histoires reliées par les échanges, les lignages et les migrations.', '''## Sine et Saloum

Le Sine et le Saloum possèdent des institutions et des traditions politiques anciennes. L’histoire des lignages, notamment les références guelwar, relie ces espaces aux circulations de la Sénégambie méridionale. Les généalogies et les récits de fondation doivent être confrontés aux travaux historiques ; ils ne se réduisent pas à une origine unique et certaine.

Les pouvoirs royaux coexistent avec des autorités locales, des institutions sociales et des pratiques religieuses diverses. Les relations avec les mouvements de réforme islamique du XIXe siècle comprennent des conflits et des alliances ; il serait trompeur de les lire comme une opposition uniforme et permanente entre deux populations.

## Le Kaabu et les espaces du sud

Le Kaabu est un grand ensemble de l’histoire mandingue, lié aux territoires aujourd’hui répartis entre plusieurs États, dont la Guinée-Bissau, la Gambie et le sud du Sénégal. Il ne correspond pas à toute la Casamance. Dans les espaces méridionaux, les formes d’autorité et les organisations villageoises sont diverses. Toutes les sociétés ne se résument pas au modèle d’un royaume centralisé.''',['sine','kaabu','hga'],['Les sociétés de Sénégambie ont des organisations politiques diverses.','Le Kaabu dépasse les frontières d’un État actuel.'],'Comparer un royaume centralisé et une organisation villageoise à partir de deux descriptions.','Rechercher comment sont prises les décisions et comment s’exerce l’autorité. Ne pas classer une société comme « sans histoire » parce qu’elle ne possède pas de roi.',related=['g26','h04','h08','r-fatick'])
add('h08','history','Royaumes et sociétés','Islamisation, savoirs et diversité religieuse','Une histoire longue de circulations, de pratiques et de transformations.', '''## Une diffusion sur la durée

L’islam est présent dans les réseaux de commerce et de savoir de la vallée et du Sahel depuis le Moyen Âge. Son adoption par des souverains et des lettrés précède une diffusion plus large dans les sociétés. Cette histoire ne tient pas à une conquête unique ni à une date identique pour toutes les régions.

Enseignement, déplacements de savants, échanges, réformes et transformations politiques interviennent à des moments différents. Les États musulmans, les confréries et les écoles coraniques ne sont pas des institutions identiques. L’histoire du Fouta-Toro de 1776 illustre une réorganisation politique ; les réseaux confrériques des XIXe et XXe siècles renvoient à d’autres dynamiques.

## Étudier avec respect et précision

Le Sénégal connaît aussi des traditions religieuses locales, une histoire chrétienne et des situations de pratiques combinées. Les identités et les convictions ne se déduisent pas automatiquement d’une langue, d’une région ou d’un nom de famille. Une approche historique décrit les acteurs et les transformations sans demander aux élèves de justifier leur croyance ou celle de leur famille.''',['islam','hga','fouta'],['L’islamisation est un processus long et différencié.','Histoire religieuse, conviction personnelle et statut des institutions sont des questions distinctes.'],'Placer sur une frise trois grandes périodes : présence médiévale, transformations des États, développement de réseaux confrériques.','Ne pas chercher une année unique de conversion de toute la population. Faire distinguer les niveaux : personnes, institutions, enseignement et pratiques sociales.',related=['h05','h09','h25'])
add('h09','history','Royaumes et sociétés','Confréries, centres de savoir et figures savantes','Transmission, écriture et rayonnements spirituels.', '''## Des réseaux organisés

Les confréries soufies relient des maîtres, des disciples, des lieux d’enseignement et des pratiques spirituelles. La Qadiriyya et la Tijaniyya ont une histoire plus large que le Sénégal. La Mouridiyya est associée à Cheikh Ahmadou Bamba ; la communauté layène à Seydina Limamou Laye. Les noms des fondateurs d’une voie et ceux des grands acteurs de son implantation locale ne doivent pas être confondus.

Au Sénégal, El Hadji Malick Sy et d’autres savants développent des foyers majeurs de transmission. Son œuvre écrite illustre la place de la langue arabe, de la poésie et de l’enseignement. La circulation des textes, les écoles et les liens entre localités contribuent à former de vastes réseaux de savoir.

## Une place dans l’histoire sociale

Les centres religieux jouent des rôles éducatifs, économiques et sociaux qui évoluent dans le temps. Ils participent aussi à l’organisation des mobilités et de certaines villes. Les relations avec l’ordre colonial puis avec l’État indépendant ne sont ni uniformes ni immuables. Une fiche de référence ne remplace pas l’étude des œuvres et ne présente pas une tradition particulière comme la seule histoire de la société.''',['islam','malick','resistances'],['Fondateur d’une voie et acteur de son rayonnement local sont deux rôles possibles.','Les écrits et les écoles font partie du patrimoine intellectuel.'],'Choisir un centre de savoir et rechercher lieu, figure, type d’enseignement et source écrite vérifiable.','Privilégier une bibliothèque, une publication universitaire ou une institution du centre concerné. Distinguer les informations historiques des récits de dévotion sans les dénigrer.',related=['h08','h25','r-diourbel','r-thies'])
add('h10','history','Échanges et domination coloniale','Contacts atlantiques et traite esclavagiste','Échanges côtiers, violences et systèmes de domination.', '''## De nouveaux réseaux à partir du XVe siècle

Les navigateurs portugais fréquentent les côtes de Sénégambie au XVe siècle. D’autres puissances européennes s’y implantent ensuite. Les contacts concernent commerce, navigation, rivalités et relations avec les autorités africaines. Les échanges de l’intérieur ne disparaissent pas : plusieurs réseaux se croisent.

La traite atlantique arrache des personnes à leurs sociétés et alimente des systèmes esclavagistes outre-Atlantique. Elle implique captures, contraintes, ventes et transports. Des acteurs européens et africains y participent selon des positions et des rapports de force différents. Cela ne justifie aucune responsabilité collective attribuée aux descendants actuels.

## Comprendre un système sans banaliser la violence

La traite est liée à des marchés, à des États et à des économies fondées sur l’exploitation humaine. Les personnes asservies ne doivent pas être réduites à des marchandises : elles ont des histoires, des résistances et des familles. Gorée constitue un lieu majeur de mémoire ; son rôle symbolique ne permet pas d’inventer un volume local de déportations. Les chiffres doivent venir de recherches identifiées et porter sur un espace défini.''',['goree','saint-louis','hga'],['Les contacts atlantiques ne marquent pas le début de l’histoire locale.','L’esclavage est un système de privation de liberté et d’exploitation humaine.'],'À partir d’un document choisi par l’enseignant, identifier trajet, acteurs et informations manquantes.','Employer un vocabulaire respectueux et adapté à l’âge. Ne pas organiser de jeu de rôle où des élèves incarnent une vente de personnes.',related=['h11','h14','h26'])
add('h11','history','Échanges et domination coloniale','Gorée, Saint-Louis et l’époque des comptoirs','Des positions stratégiques devenues lieux de mémoire.', '''## Qu’est-ce qu’un comptoir ?

Un comptoir est un établissement destiné aux échanges et au contrôle d’une présence commerciale. Posséder un point côtier ne signifie pas dominer immédiatement l’ensemble de l’intérieur. Les autorités locales, les taxes, les routes et les alliances déterminent les relations entre littoral et arrière-pays.

Saint-Louis est fondée comme établissement français au XVIIe siècle, sur une île proche de l’embouchure du Sénégal. Le fleuve permet des relations vers l’intérieur. Gorée, en face de Dakar, fait l’objet de rivalités entre puissances européennes. L’architecture et la disposition des lieux témoignent de ces histoires, tout en ayant connu des transformations ultérieures.

## Une lecture critique du patrimoine

Les quais, les maisons, les bâtiments administratifs et les forts révèlent des fonctions différentes. Une construction restaurée n’est pas nécessairement identique à son état ancien. La visite doit articuler commerce, coercition, vie quotidienne et mémoire des personnes. Préserver un bâtiment colonial ne signifie pas approuver la domination qu’il a servie ; c’est aussi conserver une trace à expliquer et à discuter.''',['saint-louis','goree'],['Un comptoir n’est pas l’équivalent d’une conquête de tout le territoire.','Les bâtiments sont des sources à contextualiser.'],'Observer une vue ancienne du pont Faidherbe : matériau, fonction, légende et informations impossibles à déduire.','Le pont relie des espaces et facilite des circulations. L’image ne suffit pas à connaître tous les usagers, les échanges ni les rapports sociaux.',image=('saint-louis','Vue ancienne du pont Faidherbe à Saint-Louis : une source visuelle à dater et à contextualiser.'),related=['g22','h10','h12'])
add('h12','history','Échanges et domination coloniale','La conquête coloniale du XIXe siècle','De points commerciaux à une domination territoriale et administrative.', '''## Une extension progressive

Au XIXe siècle, la France transforme sa présence côtière et fluviale en un projet de domination territoriale. Les campagnes militaires, les traités inégaux et les postes permettent d’étendre le contrôle. Sous Faidherbe et ses successeurs, le pouvoir colonial cherche à sécuriser routes, commerce et accès à l’intérieur ouest-africain.

La conquête se heurte à des résistances ; elle s’appuie aussi sur des alliances, des négociations et des rivalités locales. Son calendrier varie selon les espaces. Un traité présenté comme protectorat ne doit pas être confondu avec une décision libre et égale de tous les habitants.

## Des effets politiques et économiques

La domination réduit ou transforme les pouvoirs locaux, impose des administrations et oriente des productions vers des marchés coloniaux. Les infrastructures ont plusieurs fonctions : circulation commerciale, contrôle politique et transport militaire. Les présenter uniquement comme des progrès techniques effacerait ces rapports de pouvoir. Les populations réagissent par des formes diverses d’action, et ne sont pas de simples spectatrices de la conquête.''',['hga','resistances','latdior'],['La conquête est un processus inégal selon les territoires.','Techniques, intérêts économiques et contrôle politique sont liés.'],'Comparer les expressions « route construite », « route de commerce » et « axe de conquête » pour une même infrastructure.','Les trois peuvent désigner des aspects du même objet. Rechercher qui décide, qui travaille, qui circule et qui bénéficie de l’infrastructure.',related=['h13','h15','h18'])
add('h13','history','Résistances et transformations','Résistances armées : acteurs, alliances et territoires','Lat Dior, Alboury Ndiaye, El Hadj Omar et d’autres trajectoires.', '''## Des résistances dans plusieurs espaces

Lat Dior, damel du Cayor, s’oppose à l’expansion coloniale et meurt à Dékheulé le 26 octobre 1886. Les enjeux du chemin de fer, du contrôle du territoire et des alliances se croisent dans sa trajectoire. Alboury Ndiaye au Jolof et Mamadou Lamine Dramé dans l’est illustrent d’autres résistances à la pénétration française.

El Hadj Omar Tall mène un mouvement religieux et politique dans un vaste espace ouest-africain ; ses relations avec les pouvoirs français et africains sont complexes. Maba Diakhou Ba agit dans le Rip et les espaces sénégambiens, dans un contexte mêlant réforme religieuse, conflits régionaux et opposition coloniale.

## Ne pas simplifier les parcours

Ces figures n’agissent pas toutes au même moment, avec les mêmes objectifs ou les mêmes alliés. Les traités, les retournements et les rivalités font partie de leur histoire. La résistance ne se réduit pas à une bataille finale : elle peut inclure négociation, déplacement, refus et maintien d’institutions. Une mémoire nationale rassemble des figures diverses, sans effacer les conflits entre acteurs africains.''',['latdior','resistances','maba','hga'],['Il n’existe pas une résistance unique et parfaitement coordonnée.','Lat Dior meurt à Dékheulé en 1886.'],'Établir pour deux figures un tableau : territoire, époque, enjeu et source consultée.','Comparer les objectifs plutôt que classer les héros par valeur. Éviter de présenter une alliance ponctuelle comme une identité politique immuable.',related=['h06','h12','h14'])
add('h14','history','Résistances et transformations','Nder et les figures féminines de la résistance','Des femmes au centre de l’histoire, pas en marge.', '''## Nder et la mémoire du Waalo

Le récit de Nder évoque des femmes refusant la capture lors d’un raid esclavagiste dans le Waalo. La commémoration retient couramment le 7 mars 1820. Les traditions et les récits demandent un travail de confrontation ; cette mémoire ne doit pas être confondue avec la conquête française du Waalo au milieu du XIXe siècle.

Ndaté Yalla Mbodj exerce une autorité importante et résiste aux pressions françaises. Son parcours montre la place politique des linguères et la nécessité de ne pas réserver l’histoire des pouvoirs aux seuls rois.

## Aline Sitoe Diatta et d’autres engagements

En Casamance, Aline Sitoe Diatta devient une figure de mobilisation religieuse et sociale face à l’ordre colonial. Son arrestation et son éloignement illustrent la répression exercée contre des formes d’autorité que l’administration juge menaçantes. Sa mémoire dépasse une simple biographie héroïque et reste liée à des communautés et des pratiques locales.

Les femmes participent également à la production, aux réseaux de solidarité et aux luttes sociales. Les retrouver dans les sources demande parfois d’élargir le regard au-delà des actes officiels et des seuls récits militaires.''',['femmes','nder','resistances'],['Les femmes exercent des rôles politiques, sociaux et religieux.','Nder et la conquête française du Waalo renvoient à des événements distincts.'],'Choisir une figure féminine et préparer une notice : lieu, rôle, type de source et point restant à vérifier.','Privilégier un portrait historique sobre. Pour les jeunes élèves, expliquer la privation de liberté et le courage sans description dramatique ni mise en scène de la mort.',related=['h06','h10','h25'])
add('h15','history','Échanges et domination coloniale','L’ordre colonial et les Quatre Communes','AOF, administrations, citoyenneté et inégalités.', '''## Organiser une domination

L’Afrique-Occidentale française est créée à la fin du XIXe siècle. Elle réunit des colonies sous une administration fédérale dont Dakar devient le siège au début du XXe siècle. Les limites, les fonctions et les statuts des territoires évoluent ; l’AOF n’est pas un État indépendant choisi par ses habitants.

L’administration coloniale s’appuie sur une hiérarchie, des impôts, des intermédiaires et des formes de contrainte. La production et les infrastructures sont orientées par les priorités de la domination et des marchés. Les habitants ne disposent pas tous des mêmes droits.

## Le cas particulier des Quatre Communes

Saint-Louis, Gorée, Rufisque et Dakar possèdent des statuts politiques particuliers. Les originaires ont une histoire spécifique de représentation et de citoyenneté. Ce statut ne s’étend pas automatiquement à toute la population de la colonie. L’élection de Blaise Diagne comme député en 1914 et son action sur la citoyenneté constituent des repères majeurs, à replacer dans un régime où les inégalités persistent.''',['diagne','hga','saint-louis'],['Les Quatre Communes ne représentent pas toute la colonie.','Statut, droits et conditions de vie doivent être distingués.'],'Nommer les Quatre Communes puis expliquer pourquoi leur statut ne prouve pas l’égalité de tous les habitants.','Localiser les communes sur la côte. Insister sur le périmètre particulier des droits plutôt que sur une opposition entre habitants supposés « évolués » et « non évolués ».',related=['h16','h19'])
add('h16','history','Résistances et transformations','Blaise Diagne, tirailleurs et Première Guerre mondiale','Représentation politique, recrutements et expériences de guerre.', '''## Un député et des attentes de droits

Blaise Diagne est élu député du Sénégal en 1914. Son action parlementaire est liée à la défense du statut des originaires des Quatre Communes et à la question de la citoyenneté. Pendant la guerre, il joue aussi un rôle dans le recrutement de soldats africains. Ces dimensions doivent être étudiées ensemble, sans transformer son parcours en récit uniquement glorieux ou uniquement accusateur.

## Qui sont les tirailleurs dits « sénégalais » ?

Le nom désigne des unités coloniales qui recrutent dans plusieurs territoires d’Afrique occidentale, et pas uniquement dans l’actuel Sénégal. Les situations de recrutement associent engagements, contraintes et pressions diverses. Les soldats vivent des expériences de combat, de déplacement, de maladie et de discrimination.

La participation à la guerre nourrit des attentes de reconnaissance et de droits. Une promesse ne vaut pas une égalité effectivement réalisée. Pour lire une lettre ou une photographie militaire, demander date, unité, lieu et auteur de la légende, sans déduire automatiquement la nationalité actuelle de chaque personne du seul terme « sénégalais ».''',['diagne','tirailleurs'],['Les tirailleurs dits sénégalais viennent de plusieurs territoires.','La participation militaire ne supprime pas les inégalités coloniales.'],'Analyser une photographie de soldat et une notice parlementaire : quelles questions chacune permet-elle d’étudier ?','La photo renseigne certains éléments visibles ; la notice renseigne une carrière institutionnelle. Aucune des deux ne raconte seule l’expérience de tous les combattants.',image=('blaise-diagne','Blaise Diagne en 1933 : portrait d’archive, postérieur à son élection de 1914.'),related=['h15','h17'])
add('h17','history','Résistances et transformations','Seconde Guerre mondiale et massacre de Thiaroye','Une tragédie historique étudiée à travers archives et mémoires.', '''## Des soldats dans un conflit mondial

Des soldats africains participent à la Seconde Guerre mondiale et subissent combats, captivité, déplacements et traitements inégaux. Le retour ne met pas fin aux rapports de domination. Les questions de soldes et de droits nourrissent des revendications.

Le 1er décembre 1944, l’armée française tue des tirailleurs rassemblés au camp de Thiaroye. Cet événement est un massacre. Les revendications des soldats et les décisions des autorités doivent être étudiées avec les archives, les témoignages et les recherches, plutôt qu’en reprenant sans examen le vocabulaire de « mutinerie » utilisé pour justifier la répression.

## Établir les faits et respecter les mémoires

Le nombre de victimes, certaines circonstances et les lieux d’inhumation ont fait l’objet de débats et d’enquêtes. La commémoration de 2024 et les recherches poursuivent le travail de reconnaissance. La fiche n’impose pas un bilan humain présenté comme définitivement établi.

L’enseignement peut montrer comment une version officielle est discutée à partir de nouvelles preuves. La mémoire des victimes, l’analyse scientifique et la responsabilité des institutions sont des dimensions liées mais distinctes.''',['thiaroye','tirailleurs'],['Le massacre de Thiaroye a lieu le 1er décembre 1944.','Certains aspects du bilan et des circonstances restent des objets de recherche.'],'Comparer deux légendes d’un événement, dont une emploie un terme justificatif : auteur, intention et preuves.','L’objectif est d’apprendre la critique des sources, sans relativiser la réalité du massacre. Adapter les documents à l’âge et ne pas utiliser d’images violentes.',related=['h01','h16','h26'],questions=[('Pourquoi ne donne-t-on pas ici un chiffre unique de victimes ?','Parce que les bilans et les circonstances demeurent discutés et étudiés ; une précision apparente ne doit pas masquer les incertitudes documentaires.')])
add('h18','history','Résistances et transformations','Travail, chemin de fer et luttes sociales','Le rail comme infrastructure, lieu de travail et espace de mobilisation.', '''## Des infrastructures et des travailleurs

Le chemin de fer relie des lieux, facilite des échanges et sert aussi les objectifs de l’économie coloniale. Thiès devient un nœud ferroviaire majeur. Derrière les locomotives se trouvent des métiers, des ateliers, des horaires et des conditions de travail souvent inégales.

La grève des cheminots de 1947–1948 marque l’histoire sociale de l’Afrique occidentale. Les revendications portent notamment sur les conditions de travail et l’égalité de traitement. Les solidarités concernent aussi les familles et les villes traversées par le réseau. L’événement dépasse donc la seule histoire technique du rail.

## Lire l’histoire sociale

Les journaux, archives syndicales, photographies et témoignages permettent de comprendre les mobilisations. Une œuvre littéraire inspirée d’une grève n’est pas un procès-verbal ; elle peut éclairer une expérience tout en transformant personnages et situations. Les deux types de documents ont un intérêt différent.

Les luttes sociales participent aux transformations politiques, mais ne doivent pas être présentées comme la cause unique et mécanique de l’indépendance.''',['rail','hga'],['Un réseau de transport est aussi un espace de travail.','La grève de 1947–1948 constitue un repère de l’histoire sociale.'],'Construire une frise de la mobilisation en distinguant revendications, acteurs et formes de solidarité.','Utiliser une chronologie documentée. Éviter de transformer les personnages d’un roman en témoins historiques réels sans vérification.',related=['g22','r-thies','h19'])
add('h19','history','Indépendance et République','De l’après-guerre à l’indépendance de 1960','Distinguer autonomies, accords et séparation de la Fédération du Mali.', '''## Une évolution politique accélérée

Après la Seconde Guerre mondiale, les revendications de droits, l’activité des partis et les transformations de l’empire colonial ouvrent une nouvelle période. Les élections et les assemblées se développent, tandis que des responsables sénégalais discutent les formes d’autonomie et de coopération africaine. L’indépendance n’est pas le produit d’un seul acteur.

Le Sénégal et le Soudan français s’associent dans la Fédération du Mali. Le nom de cette fédération ne doit pas être confondu avec celui du seul État du Mali qui se constitue ensuite. Les dirigeants défendent des projets politiques et institutionnels qui finissent par diverger.

## Les trois repères de 1960

Le 4 avril 1960 correspond aux accords ouvrant la voie à l’indépendance ; cette date est retenue pour la fête nationale sénégalaise. Le 20 juin, la Fédération du Mali accède effectivement à l’indépendance. Le 20 août, le Sénégal s’en sépare et poursuit son existence comme État indépendant distinct. Son admission à l’ONU intervient le 28 septembre 1960.

! Ces dates décrivent des étapes différentes ; il ne faut ni en choisir une au hasard ni présenter les trois comme un même événement.''',['indep','presidence','onu'],['4 avril : accords et fête nationale.','20 juin : indépendance fédérale ; 20 août : séparation du Sénégal.'],'Associer quatre cartes-date à quatre événements : 4 avril, 20 juin, 20 août et 28 septembre 1960.','Attendre accords, indépendance fédérale, séparation et admission à l’ONU. Faire expliquer pourquoi plusieurs dates importantes peuvent appartenir à un même processus.',related=['h20','h21','h28'],questions=[('Pourquoi la fête du 4 avril ne rend-elle pas inutiles les dates du 20 juin et du 20 août ?','Parce qu’une fête nationale commémore un repère choisi tandis que les autres dates décrivent les étapes institutionnelles du processus.')])
add('h20','history','Indépendance et République','Les débuts de la République : Senghor et Mamadou Dia','Institutions, projets de développement et crise de 1962.', '''## Construire un nouvel État

Après la séparation de la Fédération, Léopold Sédar Senghor est président de la République et Mamadou Dia président du Conseil. La répartition des responsabilités organise un exécutif à deux pôles. Les institutions, les services publics et les choix économiques s’inscrivent dans la construction d’un État indépendant, avec des héritages coloniaux persistants.

La crise de décembre 1962 oppose les deux responsables et leurs soutiens. Mamadou Dia est écarté, arrêté puis condamné. Les interprétations politiques de la crise ont été débattues ; il faut distinguer les actes établis des qualifications employées par les acteurs. La Constitution de 1963 renforce la place de la présidence.

## Une période de transformations et de tensions

La présidence de Senghor est marquée par la construction institutionnelle, des politiques éducatives et culturelles, mais aussi par une forte concentration politique et des contestations. L’ouverture au pluralisme se développe progressivement à la fin de la période. Senghor quitte la présidence à la fin de 1980 ; Abdou Diouf lui succède le 1er janvier 1981. Le bilan d’un mandat ne se réduit pas à une notice commémorative.''',['dia','senghor','diouf','constitution'],['Les premières institutions distinguent président et président du Conseil.','La crise de 1962 conduit à une réorganisation du pouvoir.'],'Comparer un texte de nomination et une synthèse historique sur la crise : quelles informations sont de nature différente ?','Le texte établit une fonction à une date ; la synthèse explique des relations et des interprétations. Vérifier si la date désigne signature, entrée en fonction ou publication.',related=['h19','h21','h28'])
add('h21','history','Indépendance et République','Abdou Diouf et la Confédération de Sénégambie','1981–2000 : pluralisme, coopération et défis sociaux.', '''## Une succession institutionnelle

Abdou Diouf devient président le 1er janvier 1981 après le départ de Senghor. Il dirige le pays jusqu’à l’alternance de 2000. Les transformations de la vie partisane, les réformes économiques et les demandes sociales marquent cette période. Une stabilité institutionnelle n’exclut ni tensions, ni contestations, ni difficultés économiques.

## Une coopération avec la Gambie

Le pacte instituant la Confédération de Sénégambie est signé en décembre 1981. La mise en place institutionnelle intervient en 1982. Le projet associe Sénégal et Gambie dans certains domaines tout en maintenant deux États. Il prend fin en 1989. Une confédération ne correspond donc ni à une fusion complète ni à la Fédération du Mali de 1960.

La coopération entre pays ne s’arrête pas à la fin d’une formule institutionnelle. Les échanges, les mobilités et les enjeux de bassin continuent à relier les territoires. Comparer les expériences fédérale et confédérale permet de comprendre que les formes d’intégration peuvent changer sans que disparaissent les relations entre populations.''',['diouf','senegambie','presidence'],['Abdou Diouf exerce la présidence de 1981 à 2000.','La Confédération est mise en place en 1982, après le pacte de 1981.'],'Comparer Fédération du Mali et Confédération de Sénégambie : partenaires, période et devenir.','Mali fédéral : Sénégal et Soudan français, 1959–1960. Sénégambie : Sénégal et Gambie, pacte 1981, fonctionnement à partir de 1982, fin 1989. Éviter une simple confusion de noms.',related=['h19','h22','g08'])
add('h22','history','Indépendance et République','L’alternance de 2000 et la période Abdoulaye Wade','Le changement de majorité et les transformations institutionnelles.', '''## Une alternance électorale

En 2000, Abdoulaye Wade remporte l’élection présidentielle face à Abdou Diouf. Le transfert du pouvoir marque une alternance : la présidence change de camp politique par l’élection. Cet événement ne signifie ni que toute contestation disparaît ni que toutes les politiques antérieures sont immédiatement remplacées.

La période 2000–2012 comprend des changements institutionnels, des investissements, des transformations économiques et des débats sur le pouvoir. La Constitution adoptée en 2001 devient un texte central, ensuite modifié à plusieurs reprises. Pour présenter une règle constitutionnelle, il faut donc préciser la version du texte.

## Étudier une alternance sans faire campagne

Comparer programmes, décisions, résultats et critiques demande des documents de nature différente. Une infrastructure visible n’épuise pas le bilan d’une politique ; un discours d’opposition n’est pas à lui seul une mesure statistique. L’enseignement peut se concentrer sur les mécanismes de l’élection, de la représentation et du contrôle, sans demander aux élèves de choisir un parti ni attribuer une opinion politique à leur famille.''',['presidence','constitution'],['2000 marque une alternance à la présidence.','La Constitution de 2001 a été modifiée : sa date d’origine ne suffit pas à connaître sa version.'],'Définir élection, alternance et opposition à partir d’une situation fictive d’association scolaire.','Faire distinguer une règle de vote et le choix personnel d’un candidat. L’analogie aide à comprendre un mécanisme mais ne résume pas les institutions d’un État.',related=['h21','h23','h28'])
add('h23','history','Indépendance et République','Les alternances de 2012 et de 2024','Des repères récents à replacer dans une histoire encore en cours.', '''## Deux nouveaux changements à la présidence

Macky Sall remporte le second tour de l’élection présidentielle le 25 mars 2012 face à Abdoulaye Wade. Il exerce ensuite la présidence jusqu’en 2024. Le 24 mars 2024, Bassirou Diomaye Faye est élu président. Ces repères s’ajoutent à l’alternance de 2000, sans rendre les contextes identiques.

Les périodes récentes associent transformations économiques, projets d’infrastructure, revendications sociales et controverses politiques. L’histoire immédiate utilise des documents abondants mais parfois partiels ou engagés. Une promesse de campagne, une décision annoncée et une réalisation évaluée sont trois objets différents.

## Dater le récit

Cette édition fournit des repères électoraux vérifiés, pas un suivi quotidien de l’action gouvernementale. Les institutions, les lois et les indicateurs doivent être actualisés à partir de leurs publications officielles. Pour les élèves, les grandes compétences sont de situer un événement, vérifier sa source et distinguer fait, commentaire et jugement.

! La pluralité des points de vue n’oblige pas à présenter une rumeur non vérifiée comme une information équivalente à un résultat électoral établi.''',['macky','presidence','constitution'],['2012 et 2024 sont deux repères d’alternance présidentielle.','L’histoire récente exige datation et vérification des documents.'],'Classer des énoncés fictifs : résultat officiel, promesse, opinion et rumeur non vérifiée.','Demander quel document permettrait de vérifier chaque énoncé. Ne pas utiliser l’exercice pour étiqueter politiquement les élèves.',related=['h22','h28'])
add('h24','history','Sociétés, mémoires et culture','Casamance, conflit et construction de la paix','Des expériences territoriales et humaines à traiter sans généralisation.', '''## Un conflit et ses effets sur les populations

Le conflit en Casamance se développe à partir de 1982 autour de revendications du MFDC et de la réponse de l’État. Sa durée et ses épisodes ont affecté déplacements, activités économiques, familles et accès aux terres. Les acteurs et les positions évoluent ; la Casamance n’est ni une population uniforme ni un territoire défini uniquement par la violence.

## Accords et mise en œuvre

Plusieurs initiatives cherchent à consolider la paix. L’accord signé à Bissau le 23 février 2025 constitue un repère récent mentionné par les autorités sénégalaises. La signature d’un accord ne prouve pas à elle seule que chaque difficulté est résolue : retour des personnes déplacées, confiance, activité économique et traitement des conséquences du conflit demandent un travail durable.

La coopération avec les pays voisins et les organisations locales compte dans ces dynamiques. Pour enseigner, privilégier des textes adaptés à l’âge, ne pas assigner une opinion aux habitants d’une région et distinguer récit historique et conseil de sécurité actuel. Cette fiche ne donne pas de consignes de déplacement sur le terrain.''',['paix','regions'],['La Casamance ne se réduit pas au conflit.','Un accord doit être distingué de son application.'],'Construire un schéma des besoins d’une paix durable : sécurité, droits, retour, services et dialogue.','Utiliser une situation fictive et éviter de demander un témoignage personnel à un enfant. Faire apparaître les dimensions humaines et territoriales de la reconstruction.',related=['g26','r-ziguinchor','r-sedhiou','r-kolda'])
add('h25','history','Sociétés, mémoires et culture','Éducation, culture et place des femmes','Des savoirs et des créations au-delà des seuls pouvoirs politiques.', '''## Une histoire des transmissions

L’enseignement familial, les apprentissages professionnels, les écoles coraniques, l’école publique et l’université participent à des histoires différentes de formation. Les langues nationales, l’arabe et le français sont associés à des usages et à des productions variés. Aucune langue ne permet, à elle seule, de mesurer la valeur d’un savoir.

La poésie, les récits, la musique, les arts visuels et le cinéma conservent et transforment des expériences sociales. Senghor associe une œuvre littéraire à une carrière politique ; Cheikh Anta Diop occupe une place majeure dans les débats sur l’histoire africaine et la recherche scientifique, notamment au sein de l’IFAN. Une œuvre se lit et se discute : le prestige d’un auteur ne remplace pas l’examen des preuves.

## Des actrices de la vie publique

Caroline Faye Diop, institutrice puis femme politique, devient députée en 1963. Son parcours rappelle le rôle des femmes dans l’éducation et la représentation. Les figures connues ne doivent pas effacer les engagements ordinaires : associations, production, commerce, soins et transmission. Une histoire plus complète recherche aussi ces expériences dans les archives et les témoignages.''',['femmes','senghor','ifan','malick'],['L’histoire culturelle et scientifique fait partie de l’histoire nationale.','Les femmes sont des actrices de la transmission et de la vie publique.'],'Préparer une petite exposition de classe : une œuvre, un savoir-faire, une institution de recherche et un parcours féminin.','Citer les auteurs et les sources. Une courte présentation originale est préférable à la copie d’un livre ; demander l’autorisation pour photographier les personnes ou leurs productions.',related=['h09','h14','h26'])
add('h26','history','Sociétés, mémoires et culture','Patrimoine et mémoire : transmettre sans figer','Monuments, lieux, pratiques et récit national.', '''## Plusieurs formes de patrimoine

Le patrimoine matériel comprend des sites, des bâtiments et des objets ; le patrimoine immatériel concerne des pratiques et des savoir-faire vivants. Au Sénégal, le Kankurang, le xooy et le ceebu jën figurent sur les listes de l’UNESCO. Une inscription reconnaît une valeur et une nécessité de sauvegarde ; elle ne transforme pas une pratique en objet immuable.

Gorée, Saint-Louis, les mégalithes, le Saloum et le pays Bassari éclairent des périodes et des expériences différentes. La mémoire d’un lieu peut changer avec les générations, les recherches et les décisions de conservation. Les musées choisissent aussi ce qu’ils exposent et comment ils le racontent.

## Une transmission active

Une visite scolaire se prépare par une question, des documents et un objectif d’observation. Au retour, une synthèse distingue ce qui a été vu, entendu et vérifié. Les enfants peuvent contribuer à une mémoire locale par un carnet de lieux et de récits, en respectant les personnes et les objets. Préserver ne signifie pas tout idéaliser : les traces de domination ou de souffrance doivent être expliquées avec rigueur et humanité.''',['immat','patrimoine','goree'],['Patrimoine matériel et immatériel se complètent.','La mémoire est vivante ; l’histoire examine ses sources.'],'Choisir un objet ou une pratique locale et rédiger une notice : qui transmet, comment, à qui et avec quels changements ?','Ne pas limiter la notice à une date ou à un costume. Respecter les usages qui ne peuvent pas être montrés publiquement et distinguer information accessible et savoir réservé.',image=('goree','L’île de Gorée : un lieu habité, historique et mémoriel.'),related=['h01','h03','g25'])
add('h27','history','Sociétés, mémoires et culture','Crises et solidarités : 1989 et le Joola','Des événements marquants et leurs conséquences humaines.', '''## La crise sénégalo-mauritanienne de 1989

En 1989, des tensions frontalières dégénèrent en violences intercommunautaires et en déplacements de populations entre Mauritanie et Sénégal. Les conséquences se prolongent au-delà des premiers événements : familles séparées, pertes de biens, refuge et questions de retour. Les opérations de rapatriement volontaire, notamment accompagnées par le HCR, témoignent de cette durée.

Il faut distinguer les responsabilités d’acteurs et de décisions de toute accusation collective envers une nationalité ou une communauté. Les témoignages des personnes déplacées sont des sources précieuses, à recueillir avec leur accord et sans leur imposer de revivre une expérience douloureuse.

## Le naufrage du Joola

Le 26 septembre 2002, le ferry Le Joola, qui relie la Casamance à Dakar, fait naufrage au large de la Gambie. La catastrophe bouleverse le pays et de nombreuses familles. Les commémorations entretiennent la mémoire des victimes et rappellent les enjeux de responsabilité et de sécurité des transports.

L’histoire des crises ne consiste pas à accumuler des images choquantes ou des records de victimes. Elle étudie les faits, les causes documentées, les effets et les réponses collectives.''',['refugies','joola'],['Les conséquences d’une crise peuvent durer plusieurs décennies.','La mémoire des victimes demande respect et exactitude.'],'Distinguer dans une commémoration : événement rappelé, personnes honorées, documents utilisés et message pour l’avenir.','Proposer un document sobre. Aucune enquête personnelle sur une famille touchée n’est nécessaire pour réussir l’activité.',related=['g17','g22','h24','h26'])
add('h28','history','Indépendance et République','République, symboles et citoyenneté','Des repères civiques à lire à la lumière des textes.', '''## Les symboles de la République

Le drapeau sénégalais comporte trois bandes verticales verte, or et rouge, avec une étoile verte au centre de la bande or. La devise est « Un Peuple – Un But – Une Foi ». Ces symboles accompagnent l’histoire de l’État et de l’indépendance ; leurs usages doivent être expliqués avec respect.

## Institutions et souveraineté

Une Constitution organise les pouvoirs et les droits fondamentaux. Le président, le gouvernement, l’Assemblée nationale et les institutions de justice ont des fonctions différentes. Représenter, décider, mettre en œuvre et contrôler ne sont pas des rôles interchangeables. La citoyenneté implique aussi participation, respect des droits d’autrui et attention au bien commun.

La Constitution de 2001 a été modifiée à plusieurs reprises. Les durées de mandat, les procédures et les formulations précises doivent être vérifiées dans la version applicable. Cette fiche présente des notions et ne remplace pas un texte juridique consolidé.

! Dans un travail scolaire, distinguer un symbole national, une institution de l’État et un parti politique. Ils n’ont ni la même fonction ni le même statut.''',['constitution','presidence','onu'],['Le drapeau et la devise sont des symboles nationaux.','La Constitution organise pouvoirs et droits ; sa version compte.'],'Classer des cartes illustrées : drapeau, Assemblée, école publique, association et parti politique.','Faire justifier les catégories. L’école est un service et une institution éducative ; elle n’est pas un parti. L’exercice vise les fonctions, pas les préférences politiques.',related=['h19','h22','h23'])

src('boundou','Le royaume du Boundou','Musée historique du Sénégal / IFAN','https://musee-historiquedusenegal.sn/collection/periode/les-royaumes-du-senegal','Notice de collection','Fondation associée à Malick Sy Daouda ; liens avec les territoires du Galam et du Bambouk. Ne pas confondre ce fondateur avec El Hadji Malick Sy de Tivaouane.')
src('arachide','Histoire de la recherche agricole au Sénégal','Institut sénégalais de recherches agricoles','https://isra.sn/historique-de-lisra/','Présentation historique','Expansion de l’arachide, station de Bambey et recherches agricoles ; les appréciations anciennes sont à contextualiser.')
src('droits1946','Suppression du travail forcé dans les territoires d’outre-mer','Journal officiel français / Légifrance','https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000874642','Loi du 11 avril 1946','Texte historique, pas droit du travail actuel : distinguer abolition juridique, application et indépendance.')
src('citoyens1946','Textes d’extension des droits et de la citoyenneté','Digithèque de matériaux juridiques et politiques, Université de Perpignan','https://mjp.univ-perp.fr/france/1945outremer.htm','Textes de 1945–1947','Reproduction de textes historiques, dont la loi du 7 mai 1946 ; le contexte colonial demeure après leur adoption.')
src('festival','Premier Festival mondial des arts à Dakar','Archives audiovisuelles de l’UNESCO','https://www.unesco.org/archives/multimedia/document-5104','1966','Notice d’un documentaire sur le festival ; ni film ni musique de cette archive ne sont intégrés dans l’application.')
add('h29','history','Royaumes et sociétés','Boundou, Galam et Bambouk : pouvoirs et échanges','L’histoire des territoires de l’est dans les réseaux sénégambiens.', '''## Un carrefour intérieur

Le Boundou, dans l’est de l’espace sénégambien, se forme autour d’une autorité musulmane associée à Malick Sy Daouda. Il faut distinguer ce nom de celui d’El Hadji Malick Sy, grande figure de Tivaouane à une époque ultérieure. Les relations avec le Fouta-Toro, le Jolof et les espaces mandingues contribuent à son histoire.

Les noms Galam et Bambouk renvoient à des territoires historiques et à des réseaux, notamment ceux des échanges et de l’or. Ils ne correspondent pas directement à des départements actuels. Le fleuve Sénégal et la Falémé relient ces espaces à d’autres centres de production et de commerce.

## Étudier la circulation plutôt qu’une carte figée

Les autorités cherchent à contrôler des routes, des ressources et des prélèvements. Les commerçants, les artisans, les cultivateurs et les lettrés contribuent aussi aux relations régionales. L’histoire de l’est ne se réduit donc ni à une zone vide entre royaumes ni à la seule arrivée de l’administration coloniale. Un schéma historique doit représenter des relations et des incertitudes, pas fabriquer des frontières précises.''',['boundou','royaumes','hga'],['Les territoires de l’est participent à d’importants réseaux intérieurs.','Des noms proches peuvent désigner des figures de périodes différentes.'],'Sur un schéma, relier vallée du Sénégal, Falémé et territoires d’échanges ; ajouter deux types de circulation.','Accepter produits et savoirs, routes et migrations. Un schéma relationnel ne prétend pas fixer les limites exactes d’un royaume.',related=['h04','h05','g07','r-tambacounda'])
add('h30','history','Échanges et domination coloniale','L’arachide et les transformations des campagnes','Une histoire économique faite de contraintes et d’initiatives paysannes.', '''## Une culture commerciale en expansion

L’extension de la production arachidière au XIXe et au XXe siècle transforme une partie des campagnes sénégalaises. Les besoins des industries huilières, les réseaux commerciaux, la fiscalité et les infrastructures coloniales favorisent cette orientation. Les producteurs restent des acteurs : ils adaptent les cultures, les outils et les organisations du travail à leurs conditions.

Les axes ferroviaires, les centres de collecte et les marchés relient des zones de production aux ports. Les déplacements et les défrichements accompagnent l’expansion vers certains territoires de l’intérieur. Cette histoire ne supprime pas les cultures alimentaires ni les activités pastorales, même lorsque l’arachide domine le commerce extérieur.

## Savoirs, sols et politiques agricoles

La station de Bambey illustre le développement de recherches d’abord fortement tournées vers l’arachide, avant diversification. Les rendements, la fertilité et les débouchés dépendent aussi de choix techniques et institutionnels. Comprendre cet héritage aide à étudier les politiques agricoles et les paysages actuels sans expliquer tous les problèmes par une cause unique.''',['arachide','hga','agri'],['Une culture commerciale relie les campagnes à des marchés éloignés.','Les transformations résultent de contraintes et d’initiatives multiples.'],'Dessiner une chaîne historique : producteur, collecte, rail, port, industrie ; ajouter deux questions sur les rapports de pouvoir.','Demander qui fixe les conditions d’achat et qui supporte les risques. Ne pas reprendre un vocabulaire colonial présentant les producteurs comme dépourvus de savoir.',related=['g18','h12','h18','r-diourbel'])
add('h31','history','Indépendance et République','1946 : droits, travail et citoyenneté','Des ruptures juridiques qui précèdent l’indépendance.', '''## Deux lois, deux objets

La loi du 11 avril 1946 supprime le travail forcé dans les territoires d’outre-mer. La loi du 7 mai 1946, associée à Lamine Guèye, proclame citoyens les ressortissants de ces territoires. Ces textes constituent des repères majeurs dans la transformation de l’ordre colonial après la guerre.

Le travail forcé prive une personne du choix de son travail par la contrainte. Sa suppression juridique n’est pas identique à une amélioration instantanée de toutes les conditions d’emploi. De même, une extension de citoyenneté ne signifie pas que toutes les inégalités de représentation et de pouvoir disparaissent immédiatement.

## Relier sans confondre

Les mobilisations sociales, l’action parlementaire et les changements internationaux contribuent à cette évolution. Le territoire reste dans le cadre colonial avant l’indépendance de 1960. Pour comprendre la chronologie, séparer extension des droits, autonomie et souveraineté. Cette distinction permet d’éviter l’erreur consistant à dater l’indépendance du Sénégal de l’une des lois de 1946.

! Un texte de loi historique explique une règle et une intention à une date. L’étude de son application nécessite d’autres documents.''',['droits1946','citoyens1946','diagne'],['11 avril 1946 : suppression juridique du travail forcé.','7 mai 1946 : extension de la citoyenneté ; l’indépendance vient plus tard.'],'Associer trois événements aux notions de travail libre, citoyenneté et souveraineté.','11 avril et 7 mai 1946 se distinguent ; les étapes de 1960 relèvent de l’indépendance. Demander ce qui change juridiquement et ce qui demande une enquête sur l’application.',related=['h15','h18','h19'])
add('h32','history','Sociétés, mémoires et culture','Création artistique, Négritude et rayonnement culturel','Une histoire d’œuvres, de débats et de rencontres.', '''## Des œuvres et des projets intellectuels

Le XXe siècle voit se développer des débats sur les cultures africaines, la colonisation et les relations au monde. La Négritude, à laquelle Senghor participe, affirme la valeur des héritages noirs face aux hiérarchies coloniales. Elle est aussi discutée par d’autres intellectuels : un mouvement culturel n’impose pas une opinion unique à tous les artistes africains.

Les langues nationales, le français et l’arabe portent des récits, des poèmes et des réflexions. Les pratiques orales continuent à vivre avec les livres, la radio, les images et le cinéma. La transmission peut donc associer fidélité à un héritage et invention, plutôt qu’opposer automatiquement tradition et modernité.

## Dakar, espace de rencontre

Le premier Festival mondial des arts nègres se tient à Dakar en 1966. Le titre historique doit être expliqué dans son contexte. Le festival met en relation création, représentation et projets politiques. D’autres manifestations et institutions prolongent le rôle culturel de la ville. Pour étudier une œuvre, présenter auteur, date, support et contexte, puis distinguer ce qu’elle montre de l’interprétation qu’on en propose.''',['festival','senghor','malick'],['La création culturelle comprend des débats et des transformations.','1966 est un repère du rayonnement culturel de Dakar.'],'Préparer une notice de vingt lignes sur une œuvre choisie légalement : auteur, contexte, support, observation et question.','Ne pas recopier intégralement une œuvre protégée. Une description originale et une courte citation autorisée ou un lien permettent de respecter le travail des créateurs.',related=['h25','h26','r-dakar'])
# Ordre de lecture : insérer les approfondissements à leur place dans le parcours.
for extra_id,before in [('h29','h06'),('h30','h15'),('h31','h19'),('h32','h26')]:
 item=next(a for a in articles if a['id']==extra_id);articles.remove(item);articles.insert(next(i for i,a in enumerate(articles) if a['id']==before),item)

# Lexique : définitions originales de repérage, avec renvoi vers une fiche.
glossary_data=[
('Accessibilité','Facilité d’atteindre un lieu, selon le temps, le coût, les moyens et les conditions du déplacement.','g22'),
('Adaptation climatique','Actions réduisant la vulnérabilité aux effets présents ou attendus du climat.','g24'),
('Affluent','Cours d’eau qui rejoint un autre cours d’eau.','g07'),
('Aire protégée','Espace bénéficiant de règles et d’une gestion visant à préserver ses milieux et ses valeurs.','g14'),
('Aléa','Phénomène pouvant causer des dommages : pluie intense, crue ou autre événement.','g24'),
('Alizé maritime','Flux d’air lié aux circulations atmosphériques au-dessus de l’océan et influençant le littoral.','g05'),
('Almamy','Titre d’un dirigeant dans certains États musulmans ouest-africains ; son sens dépend du contexte.','h05'),
('Alternance','Changement de camp ou de majorité à la tête du pouvoir par un processus électoral.','h22'),
('Aménagement','Action organisée sur un territoire pour répondre à des besoins : habitat, transport, production ou protection.','g22'),
('Amas coquillier','Accumulation de coquilles liée à des activités humaines anciennes, parfois associée à des sépultures.','h03'),
('Amont et aval','L’amont est du côté de la source ; l’aval est dans le sens de l’écoulement vers la partie basse.','g07'),
('Archéologie','Étude des sociétés à partir de leurs traces matérielles et de leur contexte.','h02'),
('Archive','Document conservé comme trace d’une activité ou d’un événement, à lire selon son contexte.','h01'),
('Atténuation','Actions visant à réduire les émissions de gaz à effet de serre ou à renforcer leur absorption.','g24'),
('Bassin versant','Ensemble des terrains dont les eaux convergent vers un même cours d’eau ou un même exutoire.','g07'),
('Biodiversité','Diversité des êtres vivants, de leurs variations et des écosystèmes auxquels ils appartiennent.','g14'),
('Bolong','Chen al estuarien soumis à la marée, fréquent dans les paysages de mangrove du Saloum et de Casamance.'.replace('Chen al','Chenal'),'g13'),
('Bourba','Titre associé au souverain du Jolof.','h06'),
('Brak','Titre associé au souverain du Waalo.','h06'),
('Capitale et chef-lieu','La capitale porte des fonctions nationales ; le chef-lieu est le centre administratif d’une subdivision.','r-dakar'),
('Carte thématique','Carte consacrée à un sujet précis, comme les pluies, les cultures ou la population.','g02'),
('Citoyenneté','Lien à une communauté politique, avec des droits, des devoirs et des possibilités de participation.','h28'),
('Climat','Caractéristiques statistiques du temps sur une durée longue, dans un espace donné.','g05'),
('Colonie','Territoire placé sous la domination d’un pouvoir extérieur, selon des institutions et des rapports inégaux.','h15'),
('Comptoir','Établissement destiné aux échanges et au contrôle d’une présence commerciale.','h11'),
('Confédération','Association d’États conservant leur existence et coopérant dans certains domaines selon un accord.','h21'),
('Confrérie soufie','Réseau spirituel associant maîtres, disciples, enseignements et pratiques dans l’islam.','h09'),
('Conservation','Protection et gestion dans la durée d’un milieu, d’un objet ou d’un patrimoine.','g25'),
('Constitution','Texte fondamental organisant les pouvoirs et les droits dans un État.','h28'),
('Crue','Élévation du niveau ou du débit d’un cours d’eau. Elle ne produit pas toujours une inondation dommageable.','g07'),
('Damel','Titre associé au souverain du Cayor.','h06'),
('Densité de population','Rapport entre le nombre d’habitants et la superficie d’un territoire.','g15'),
('Dior et deck','Termes locaux employés pour distinguer certains types de sols ; leur correspondance précise dépend du contexte.','g10'),
('Échelle cartographique','Relation entre une distance sur la carte et la distance correspondante sur le terrain.','g02'),
('Écosystème','Ensemble des êtres vivants, de leur milieu et des relations qu’ils entretiennent.','g14'),
('Embouchure','Lieu où un cours d’eau atteint une mer, un lac ou un autre milieu récepteur.','g07'),
('Érosion','Usure et déplacement de matériaux par l’eau, le vent ou d’autres processus.','g24'),
('Estuaire','Partie aval d’un cours d’eau en relation avec la mer et généralement influencée par les marées.','g08'),
('Exposition','Présence de personnes, de biens ou d’activités dans un espace susceptible d’être touché par un aléa.','g24'),
('Fédération','Organisation politique réunissant des entités avec une répartition de compétences entre niveau commun et niveaux membres.','h19'),
('Filière','Ensemble des étapes et des acteurs reliant une production à ses usages ou à sa consommation.','g20'),
('Fossile','Reste ou trace d’un être vivant ancien conservé dans un contexte géologique.','h02'),
('Harmattan','Vent continental sec pouvant transporter des poussières en Afrique de l’Ouest.','g05'),
('Hivernage','Nom couramment donné à la saison des pluies dans la région sahélo-soudanienne.','g05'),
('Hypothèse','Explication proposée qui demande à être confrontée à des observations ou à des preuves.','g03'),
('Indépendance','Exercice de la souveraineté d’un État, à distinguer des différentes étapes et formes d’autonomie.','h19'),
('Irrigation','Apport d’eau organisé aux cultures par des aménagements et des techniques.','g18'),
('Latérite','Matériau ou formation riche en oxydes de fer et d’aluminium, utilisé notamment pour certains mégalithes.','h03'),
('Légende cartographique','Ensemble des explications des couleurs, signes et figurés d’une carte.','g02'),
('Linguère','Titre féminin associé à une autorité politique ou dynastique dans certains royaumes sénégambiens.','h14'),
('Mangrove','Formation végétale de milieux côtiers soumis aux marées, notamment composée de palétuviers.','g13'),
('Mégalithe','Grand élément de pierre dressé ou assemblé par des sociétés humaines, dans un contexte à étudier.','h03'),
('Mémoire','Manière dont des personnes ou des groupes se souviennent du passé et lui donnent sens.','h26'),
('Métropole','Grande ville exerçant des fonctions de commandement et des relations à une large échelle.','g16'),
('Météo','État et évolution de l’atmosphère à court terme dans un lieu ou une région.','g05'),
('Migration','Changement de lieu de résidence, interne ou international, selon une durée et une définition précisées.','g17'),
('Mousson','Circulation saisonnière de l’air qui apporte notamment de l’humidité depuis l’Atlantique en Afrique de l’Ouest.','g05'),
('Nappe souterraine','Eau contenue dans une formation du sous-sol permettant son stockage et sa circulation.','g09'),
('Néolithique','Ensemble de transformations techniques et sociales, dont la chronologie diffère selon les régions.','h02'),
('Offshore','Situé en mer ; le terme est utilisé notamment pour certaines activités pétrolières et gazières.','g21'),
('Paléolithique','Longue période préhistorique étudiée notamment à travers les techniques de pierre taillée.','h02'),
('Pastoralisme','Organisation de l’élevage reposant largement sur l’usage de pâturages et de ressources naturelles.','g12'),
('Patrimoine immatériel','Pratiques, expressions et savoir-faire reconnus et transmis par des communautés.','h26'),
('Paysage culturel','Paysage façonné par des relations prolongées entre des sociétés et leur environnement.','g25'),
('Projection démographique','Estimation d’une population future fondée sur des hypothèses et un point de départ statistique.','g15'),
('Recensement','Opération de dénombrement d’une population à une date et selon des définitions explicites.','g15'),
('Rendement agricole','Quantité produite rapportée à une surface, par exemple en tonnes par hectare.','g18'),
('Réseau','Ensemble de lieux ou de nœuds reliés par des axes, des flux ou des relations.','g22'),
('Risque','Possibilité de dommages résultant d’un aléa, de l’exposition et de la vulnérabilité.','g24'),
('Salinisation','Augmentation de la quantité de sels dans un sol ou une eau, pouvant limiter certains usages.','g10'),
('Savane','Formation végétale où les herbes occupent une place importante, avec une densité variable d’arbres et d’arbustes.','g14'),
('Sécurité alimentaire','Situation associant disponibilité, accès, qualité et stabilité de l’alimentation.','g18'),
('Sénégambie','Espace historique de relations autour des bassins du Sénégal et de la Gambie ; aussi nom d’une ancienne confédération.','h04'),
('Source historique','Trace, document ou témoignage utilisé pour connaître un aspect du passé.','h01'),
('Souveraineté','Autorité politique et capacité de décision d’une communauté ou d’un État, selon un cadre institutionnel.','h28'),
('Tanne','Surface souvent très salée, peu ou pas végétalisée, dans certains milieux côtiers et estuariens.','g13'),
('Teigne','Titre associé au souverain du Baol.','h06'),
('Traite esclavagiste','Système de capture, de vente et de transport de personnes privées de liberté.','h10'),
('Tradition orale','Savoirs et récits transmis oralement, à étudier dans leurs contextes et leurs variantes.','h01'),
('Transhumance','Déplacement organisé des troupeaux pour accéder saisonnièrement à l’eau et aux pâturages.','g12'),
('Tribut','Prélèvement ou obligation versé à une autorité dans une relation politique donnée.','h06'),
('Vulnérabilité','Fragilité et capacité limitée à faire face à des dommages possibles, selon des conditions sociales et matérielles.','g24'),
('Zone humide','Milieu où la présence durable ou temporaire d’eau façonne les sols, les êtres vivants et les usages.','g14'),
]
glossary_data.extend([
('Autonomie','Possibilité d’exercer certaines compétences propres, sans équivaloir nécessairement à la souveraineté d’un État indépendant.','h19'),
('Culture de rente','Culture destinée surtout à la commercialisation, à distinguer d’une destination uniquement alimentaire du ménage.','h30'),
('Indigénat','Ensemble historique de règles et de sanctions d’exception imposées à des populations sous domination coloniale.','h15'),
('Négritude','Mouvement intellectuel et culturel affirmant la valeur des héritages noirs face aux hiérarchies coloniales, lui-même objet de débats.','h32'),
('Protectorat','Forme de domination où un pouvoir extérieur impose un contrôle tout en maintenant certaines autorités locales.','h12'),
('Travail forcé','Travail imposé à une personne par la contrainte, sans libre consentement.','h31'),
('Tributaire','Qui se trouve dans une relation de versement d’un tribut ou d’obligation envers une autorité.','h06'),
])
glossary=[{'term':t,'definition':d,'article':a} for t,d,a in sorted(glossary_data,key=lambda v:v[0].casefold())]
events=[
(-100000,0,'Préhistoire','Longues occupations et techniques étudiées par l’archéologie ; pas de date unique pour tous les sites.','h02'),
(-300,0,'IIIe siècle av. J.-C. – XVIe siècle','Longue fourchette des pratiques funéraires documentées dans les ensembles mégalithiques de Sénégambie.','h03'),
(1000,0,'XIe siècle et Moyen Âge','Le Tekrur est mentionné dans des écrits médiévaux ; la vallée participe aux réseaux de commerce et de savoir.','h05'),
(1200,0,'XIIIe–XVIe siècles','Le Mali et d’autres ensembles ouest-africains structurent des réseaux d’influence et d’échanges.','h04'),
(1350,0,'XIVe–XVIe siècles environ','Le Grand Jolof organise un vaste ensemble avant sa fragmentation. Les traditions de fondation présentent des variantes.','h06'),
(1440,0,'XVe siècle','Les contacts avec les navigateurs portugais développent de nouvelles relations atlantiques.','h10'),
(1550,0,'XVIe siècle','Fragmentation du Grand Jolof et affirmation d’autonomies régionales.','h06'),
(1659,0,'1659','Fondation du comptoir français de Saint-Louis selon la notice patrimoniale de l’UNESCO.','h11'),
(1776,0,'1776','Révolution torodo dans le Fouta-Toro, associée à Thierno Souleymane Baal et à l’almamat.','h05'),
(1820,307,'7 mars 1820, date commémorée','Nder : mémoire d’une résistance de femmes à un raid esclavagiste dans le Waalo.','h14'),
(1850,0,'Seconde moitié du XIXe siècle','Extension de la conquête territoriale française ; résistances, traités et affrontements.','h12'),
(1886,1026,'26 octobre 1886','Mort de Lat Dior à Dékheulé.','h13'),
(1890,0,'Fin du XIXe – début du XXe siècle','Rayonnement de réseaux confrériques et de foyers d’enseignement.','h09'),
(1895,0,'1895','Création de l’Afrique-Occidentale française.','h15'),
(1902,0,'1902','Dakar devient siège de l’administration fédérale de l’AOF, auparavant à Saint-Louis.','h15'),
(1914,0,'1914','Élection de Blaise Diagne comme député du Sénégal ; début de la Première Guerre mondiale.','h16'),
(1916,929,'29 septembre 1916','Loi liée au statut et à la citoyenneté des originaires des Quatre Communes.','h15'),
(1939,0,'1939–1945','Seconde Guerre mondiale et participation de soldats africains.','h17'),
(1944,1201,'1er décembre 1944','Massacre de Thiaroye. Le bilan et certaines circonstances restent des objets de recherche.','h17'),
(1947,0,'1947–1948','Grande grève des cheminots de l’Afrique occidentale, dont ceux du Dakar-Niger.','h18'),
(1950,0,'Années 1950','Accélération des transformations politiques et des projets d’autonomie et d’indépendance.','h19'),
(1959,0,'1959','Association du Sénégal et du Soudan français dans la Fédération du Mali.','h19'),
(1960,404,'4 avril 1960','Accords ouvrant la voie à l’indépendance ; date retenue pour la fête nationale sénégalaise.','h19'),
(1960,620,'20 juin 1960','Indépendance de la Fédération du Mali.','h19'),
(1960,820,'20 août 1960','Séparation du Sénégal de la Fédération du Mali.','h19'),
(1960,928,'28 septembre 1960','Admission du Sénégal à l’ONU.','h19'),
(1962,1200,'Décembre 1962','Crise entre Senghor et Mamadou Dia ; réorganisation du pouvoir.','h20'),
(1963,0,'1963','Nouvelle Constitution renforçant la fonction présidentielle.','h20'),
(1963,1,'1963','Caroline Faye Diop devient députée.','h25'),
(1978,0,'1978','Inscription de Gorée au patrimoine mondial.','g25'),
(1980,1231,'Fin 1980','Départ de Senghor de la présidence.','h20'),
(1981,101,'1er janvier 1981','Abdou Diouf devient président.','h21'),
(1981,200,'1981','Inscription du Djoudj et du Niokolo-Koba au patrimoine mondial.','g25'),
(1981,1217,'17 décembre 1981','Signature du pacte instituant la Confédération de Sénégambie.','h21'),
(1982,0,'1982','Mise en place de la Confédération de Sénégambie.','h21'),
(1982,1,'À partir de 1982','Développement du conflit en Casamance.','h24'),
(1989,0,'1989','Crise entre Sénégal et Mauritanie, violences et déplacements.','h27'),
(1989,1,'1989','Fin de la Confédération de Sénégambie.','h21'),
(2000,0,'2000','Élection d’Abdoulaye Wade et première alternance présidentielle.','h22'),
(2000,1,'2000','Inscription de l’île de Saint-Louis au patrimoine mondial.','g25'),
(2001,122,'2001','Adoption de la Constitution de 2001, modifiée par la suite.','h22'),
(2002,926,'26 septembre 2002','Naufrage du ferry Le Joola.','h27'),
(2006,0,'2006','Inscription des cercles mégalithiques de Sénégambie au patrimoine mondial.','g25'),
(2008,0,'2008','Création des régions de Kaffrine, Kédougou et Sédhiou.','r-kaffrine'),
(2008,1,'2008','Kankurang : inscription sur la Liste représentative du patrimoine culturel immatériel.','h26'),
(2011,0,'2011','Inscription du delta du Saloum au patrimoine mondial.','g25'),
(2012,325,'25 mars 2012','Élection de Macky Sall à la présidence.','h23'),
(2012,700,'2012','Inscription du pays Bassari au patrimoine mondial.','g25'),
(2013,0,'2013','Inscription du xooy sur la Liste représentative du patrimoine culturel immatériel.','h26'),
(2021,0,'2021','Inscription du ceebu jën sur la Liste représentative du patrimoine culturel immatériel.','h26'),
(2024,324,'24 mars 2024','Élection de Bassirou Diomaye Faye à la présidence.','h23'),
(2024,611,'Juin 2024','Début de la production pétrolière du champ de Sangomar.','g21'),
(2024,1231,'Fin décembre 2024','Mise en production du projet gazier GTA ; les jalons de commercialisation suivent en 2025.','g21'),
(2025,223,'23 février 2025','Accord de Bissau dans le processus de paix en Casamance.','h24'),
]
events.extend([
(1700,0,'Époque moderne','Développement du Boundou et des relations entre espaces de la vallée et de l’est.','h29'),
(1850,1,'XIXe–XXe siècles','Expansion de l’arachide et transformation d’une partie des campagnes.','h30'),
(1946,411,'11 avril 1946','Loi de suppression du travail forcé dans les territoires d’outre-mer.','h31'),
(1946,507,'7 mai 1946','Loi Lamine Guèye étendant la citoyenneté.','h31'),
(1966,400,'1966','Premier Festival mondial des arts nègres à Dakar.','h32'),
])
timeline=[{'date':d,'text':t,'article':a} for _,_,d,t,a in sorted(events)]

def build():
 images_list=json.loads((DEST/'images.json').read_text());images={r['id']:r for r in images_list if 'asset' in r}
 mapping=json.loads((DEST/'regions.json').read_text())
 variants={
 'h05':['Tekrour','Fuuta Tooro','Fouta Toro','Souleymane Bal','Abdoul Kader Kane'],
 'h06':['Djolof','Walo','Oualo','Kayor','Kajoor','Bawol','Ndiadiagne Ndiaye'],
 'h07':['Gabou','Gabu','Saalum','Saaluum','Siin','Guélowar','Sine-Saloum'],
 'h09':['Mouridisme','Tijanisme','Tidjaniyya','Qadiriyya','Layeniyya'],
 'h19':['fête nationale','Soudan français','Fédération du Mali','accords de Paris'],
 'g15':['démographie','RGPH-5','recensement','densité'],
 }
 for a in articles:a['keywords']=variants.get(a['id'],[])
 # Vocabulaire et renvois explicitement attachés aux fiches ; pas de contenu téléchargé à l’ouverture.
 ids={a['id'] for a in articles}
 for a in articles:
  assert all(s in sources for s in a['sources']),a['id']
  assert all(r in ids for r in a['related']),a['id']
  assert all(b['image'] in images for b in a['blocks'] if b['type']=='image'),a['id']
 pack={'schemaVersion':1,'version':'2.2.0','reviewedAt':'2026-10-31','displayDate':'31 octobre 2026','subjects':[
 {'id':'geo','title':'Géographie du Sénégal','image':'saloum','description':'Territoires, milieux, eau, population, activités, environnement et profils des 14 régions.'},
 {'id':'history','title':'Histoire du Sénégal','image':'goree','description':'Des premiers peuplements aux repères contemporains : royaumes, échanges, résistances, indépendance et mémoires.'}],
 'scope':'Un fonds national de référence pour l’enseignant : 72 fiches de synthèse, 14 profils régionaux inclus, une carte de repérage, une chronologie, un lexique et des activités avec pistes de correction. Ce n’est pas une encyclopédie exhaustive ni une validation officielle du programme scolaire.',
 'method':'Textes originaux préparés pour TDG à partir de références publiques identifiées. Les statistiques portent leur millésime et leur statut ; les témoignages, traditions et archives sont distingués. Les incertitudes sont signalées. La chronologie récente n’est pas un fil d’actualité. Adapter les activités à la classe, au contexte et aux manuels. Les liens externes nécessitent Internet, les contenus intégrés restent consultables hors connexion.',
 'articles':articles,'sources':sources,'images':images,'map':mapping,'timeline':timeline,'glossary':glossary}
 raw=json.dumps(pack,ensure_ascii=False,indent=2)+'\n';(DEST/'senegal.json').write_text(raw)
 words=len(re.findall(r'\S+',' '.join(str(b.get('text','')) for a in articles for b in a['blocks'])))
 print(json.dumps({'articles':len(articles),'geography':sum(a['subject']=='geo' for a in articles),'history':sum(a['subject']=='history' for a in articles),'sources':len(sources),'images':len(images),'timeline':len(timeline),'glossary':len(glossary),'paragraphWords':words,'bytes':len(raw.encode())},ensure_ascii=False))
if __name__=='__main__':build()
