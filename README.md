# Enseignant — TDG

Application Flutter Android pour apprendre, préparer ses leçons et gérer une classe du primaire. Nom affiché **Enseignant**, identifiant **com.tdg.enseignant**, version **2.2.0+6**.

## Démarrer

Extraire l’archive puis ouvrir un terminal dans `enseignant/`, le dossier contenant `pubspec.yaml` :

```bash
flutter pub get && flutter analyze && flutter test && flutter run
```

Le wrapper Gradle 8.14.1 est fourni. Java 17, Flutter récent (3.35 ou supérieur recommandé), un SDK Android avec API 36 et un téléphone en débogage USB sont nécessaires. Flutter prépare `android/local.properties` selon le SDK installé sur votre poste. Aucun chemin du poste de développement TDG n’est enregistré dans le projet.

Si les fichiers du wrapper ont été supprimés, `bash tools/setup.sh` permet de les régénérer dans un projet temporaire, sans remplacer la configuration Gradle TDG ni le code de l’application. Ce script ne lance pas les tests.

**État de validation :** sources et assets préparés ; ni `flutter analyze`, ni `flutter test`, ni compilation APK, ni essai sur téléphone n’ont été exécutés dans l’environnement de préparation. Les tests Flutter sont fournis pour exécution sur votre poste. L’absence de SDK Flutter ici ne permet pas de garantir un build avant votre vérification.

## Fonctionnalités de cette première version

| Onglet | Fonctions implémentées |
| --- | --- |
| Agenda | Jour sélectionnable, cours hebdomadaires modifiables, tableaux jour/semaine colorés avec horaires, salles et détails au clic ; contrôle des chevauchements, salle, tâches datées et priorités, tâches en retard, vue des jours de la semaine ; détails au clic et actions via trois points ou appui long. |
| Classes | Appréciations automatiques avec période, besoins, assiduité et conseils ; classes CI à CM2, élèves, matricule facultatif, appel daté, absent/présent/retard/excusé, bilan des absences renseignées, évaluations et moyennes générales, fiches individuelles avec notes, appels, retards et coordonnées du parent ou tuteur. |
| Carnet | Notes, préparations, cahier de textes et réunions ; objectif, matière, niveau, déroulement et évaluation ; lecture au clic, modification, suppression et épinglage via trois points ou appui long ; recherche et filtres. |
| Savoirs | 225 leçons originales en français, mathématiques, sciences, histoire, géographie, éducation civique, éducation artistique, EPS, arabe, éducation religieuse et pédagogie. Recherche, matière, niveau, favoris, suivi personnel et copie vers une préparation. |
| Grevisse | Les 468 pages du document fourni, 137 repères classés, recherche OCR dans tout le livre, tous les mots ou expression exacte, filtre par partie, signets, zoom, rotation, navigation horizontale par glissement ou boutons et texte OCR sélectionnable. |

Les réglages comprennent les thèmes système/clair/sombre, la taille de lecture et l’export/restauration des données. Le logo TDG fourni est intégré à la page « Infos & À propos ». L’icône avec le texte **Enseignant** est intégrée dans l’app, au launcher Android et au splash, avec un dérivé distinct pour le splash.

### Moyennes scolaires

Chaque évaluation possède un barème et un coefficient strictement positifs. Les notes sont comprises entre zéro et le barème. Une case vide représente une note non renseignée et n’est pas comptée comme zéro.

```text
Moyenne générale /20 = Σ [(note / barème) × 20 × coefficient]
                      ÷ Σ [coefficients des notes renseignées]
```

Exemple : 8/10 coefficient 2 et 10/20 coefficient 1 donnent (16×2 + 10×1)/3 = **14/20**. Il s’agit d’une moyenne générale calculée par l’app, pas d’une formule de bulletin officiellement homologuée. Les évaluations portent un intitulé libre ; cette édition ne gère pas de moyennes par matière, trimestre ou semestre.

### Appel

Une ligne non renseignée reste **Non pointé**. Le programme ne suppose jamais que tous les élèves sont présents. Le bilan d’absences comptabilise les statuts « Absent » de toutes les dates enregistrées ; les retards et absences excusées sont conservés avec leur propre statut.

### Grevisse : organisation et recherche

Livre fourni : **Jean-Christophe Pellat et Stéphanie Fonvielle, Le Grevisse de l’enseignant — Grammaire de référence, Magnard**. Cette référence est distincte du *Petit Grevisse* évoqué avant la réception du PDF.

Le PDF est un scan sans couche texte exploitable. Les 468 pages ont été rendues en JPEG ; l’index OCR est une transcription automatique séparée. L’application charge l’index mais affiche seulement l’image de la page consultée, et non toutes les pages en mémoire.

L’organisation comporte :

- Repères et préliminaires.
- Oral et écrit : sons, syllabes, liaisons, graphèmes, orthographe et ponctuation.
- Lexique : dérivation, composition, emprunts, familles, relations de sens.
- Classes de mots : noms, déterminants, adjectifs, pronoms, verbes, adverbes, prépositions, conjonctions et interjections.
- Phrase simple : fonctions, sujets, compléments, types, formes et accords.
- Phrase complexe : juxtaposition, coordination, subordination et concordance.
- Texte et discours : cohérence, cohésion, progression, types de textes, énonciation et poésie.
- Annexes : API, orthographe, féminisation, conjugaisons, homophones, glossaire et index.

Les repères renvoient à la pagination imprimée. Dans le fichier fourni, après la couverture, **page PDF = page imprimée + 2**. Le lecteur permet de saisir une page PDF précise. Les entrées proches peuvent partager une page du livre ; cette édition regroupe les sous-notions partageant une même page pour conserver des plages continues.

Par défaut, tous les mots de la requête doivent figurer sur une même page, dans un ordre quelconque. Le mode « Expression exacte » exige leur succession. La recherche ignore la casse et les accents ; elle n’est pas une recherche sémantique et ne corrige pas automatiquement les fautes de frappe. Les titres de notions sont recherchés en parallèle. Les résultats ouvrent toujours la page scannée.

**Limites OCR :** erreurs possibles, notamment dans les petits caractères, les tableaux, les noms propres et les pages orientées. Un mot absent des résultats ne prouve pas son absence du livre. Le lecteur permet de tourner l’image et de consulter le sommaire original. Le texte OCR n’est pas une édition corrigée ni un découpage réécrit en articles indépendants.

Le document a été transformé à partir de la copie fournie pour ce projet. Les droits du livre restent à leurs titulaires. L’application n’est pas affiliée à Magnard. Avant toute publication publique de l’app ou du dépôt avec ces assets, vérifier les autorisations de diffusion. Le code et les leçons originales ne confèrent aucun droit supplémentaire sur le livre.

### Savoirs : apprendre puis enseigner

Chaque fiche contient un objectif, une explication, un exemple, une proposition d’activité de classe, un point de vigilance et une question avec correction à dévoiler. Le bouton « Copier dans mes préparations » crée une note modifiable ; il ne remplace pas automatiquement les préparations existantes.

Les 225 leçons constituent une **bibliothèque progressive**, pas une encyclopédie exhaustive du primaire. 174 leçons ont été ajoutées aux 51 fiches précédentes ; les identifiants historiques sont conservés. Les niveaux indiquent des repères de travail et doivent être adaptés aux acquis réels des élèves et au programme de l’établissement. Ces contenus ne sont pas annoncés comme un curriculum sénégalais homologué. Les langues nationales ne sont pas traduites automatiquement ; leur enseignement demande des contenus validés.

## Stockage et sauvegardes

Aucun compte, publicité ou service Firebase n’est utilisé. Les fonctions pédagogiques sont disponibles hors connexion. Les liens téléphone, courriel et site TDG ouvrent une application externe sur demande de l’utilisateur.

Les données personnelles sont enregistrées en JSON versionné dans le répertoire privé Android, via un canal natif et `AtomicFile`. Le fichier est remplacé atomiquement. Côté Dart, les modifications sont sérialisées et le nouvel état n’est publié qu’après réussite de l’écriture. Une erreur de lecture ne déclenche pas un écrasement automatique des données.

- Export : « Infos & À propos » → « Exporter une sauvegarde », puis choix du dossier avec le sélecteur Android.
- Restauration : sélection d’un JSON, validation de sa version et de sa structure, puis confirmation du remplacement.
- L’export inclut classes, élèves, évaluations, présences, carnet, agenda, favoris, signets et réglages.
- Il n’inclut pas les pages du livre, déjà livrées dans les assets.
- Le tirage vers le bas recharge les données enregistrées dans les listes principales. La restauration est limitée à 10 Mo. Les sauvegardes ne sont pas chiffrées : les conserver de manière privée.
- Une désinstallation ou l’effacement des données Android peut supprimer les informations locales. Exporter avant ces opérations.
- Aucun moteur SQLite ni service de synchronisation n’est mis en place dans cette édition.

## Environnement TDG respecté

| Élément | Version / choix |
| --- | --- |
| Gradle | 8.14.1 |
| AGP | 8.11.1 |
| Kotlin | 2.2.20 |
| Java source/cible | 17 |
| compileSdk / targetSdk | 36 |
| Désucrage Java | desugar_jdk_libs 2.1.4 |
| Namespace / applicationId | com.tdg.enseignant |
| Configuration | Kotlin DSL |
| Firebase | Désactivé, aucun google-services.json requis |

La configuration fournie est conservée dans `docs/FLUTTER_DEV_ENV_CONFIGS.md`. Les paramètres de signature release proviennent de cette référence. Aucune clé ni aucun secret n’est livré.

### APK et publication

Le débogage utilise `flutter run`. Pour une release, créer votre keystore, puis un fichier **android/key.properties**, exclu de Git :

```properties
storePassword=VOTRE_MOT_DE_PASSE
keyPassword=VOTRE_MOT_DE_PASSE
keyAlias=VOTRE_ALIAS
storeFile=/chemin/absolu/vers/votre-cle.jks
```

Puis lancer `flutter build apk --release` ou `flutter build appbundle --release`. Une release nécessite une signature correctement configurée ; elle n’utilise pas silencieusement la clé debug.

## Structure du projet

```text
lib/
  main.dart         Interface, agenda, classes, carnet et réglages
  core.dart         Données, validation, persistance et calcul des moyennes
  library.dart      Parcours pédagogiques et lecteur/recherche Grevisse
  teacher_tools.dart Tableaux des cours et appréciations automatiques
android/            Configuration TDG, bridge Kotlin et ressources natives
assets/data/        Fiches pédagogiques JSON
assets/grevisse/    Images des 468 pages, index OCR et classement
assets/images/      Icône, splash et logo TDG fourni
test/               Tests des règles de données, sauvegarde et assets
tools/              Régénération du wrapper, des icônes et de l’OCR
docs/               Configuration, fiche technique et crédits
```

Le fichier `assets/grevisse/chapters.json` est la source du classement ; `lessons.json` est la source des fiches. Les données utilisateur n’y sont jamais enregistrées. Pour les prochaines versions, maintenir un chemin de migration explicite si `version` change ; ne jamais réinitialiser automatiquement les données.

## Vérifications à effectuer sur le téléphone

1. Créer une classe, ajouter deux élèves et saisir un appel.
2. Saisir 8/10 coef. 2 et 10/20 coef. 1 pour le même élève : moyenne attendue 14/20.
3. Créer une préparation, l’épingler, fermer et relancer l’app.
4. Tester une recherche Grevisse, les filtres, le zoom et la rotation.
5. Exporter une sauvegarde, ajouter une donnée temporaire, restaurer et vérifier le remplacement.
6. Contrôler le clavier sur petit écran, le mode sombre, la taille de lecture et le splash Android 12+.

Les tests fournis vérifient notamment le calcul pondéré, la distinction note absente/zéro, le rejet d’une sauvegarde incohérente et le comportement lors d’un échec d’écriture. Ils sont **à exécuter sur votre poste**.

## Limites fonctionnelles connues

Pas encore de notifications Android, de pièces jointes, d’éditeur de texte enrichi, de bulletins PDF, d’export CSV, de vacances dans les récurrences, de groupes multi-établissements ou de synchronisation cloud. L’agenda affiche les échéances dans l’app et ne prétend pas déclencher d’alarme lorsque celle-ci est fermée. Les formulaires du carnet utilisent du texte simple.

Les données locales conviennent à un usage personnel initial ; une base indexée deviendra préférable pour un volume important. Les 468 pages scannées augmentent la taille de l’application. Le contenu du livre et les fiches doivent faire l’objet d’une relecture pédagogique avant une diffusion large.

## Développeur

**Taysir Digital Group (TDG)** — « Vos rêves, nos défis »  
Aliou Mbengue — PDG / Développeur  
Téléphone : +221 76 455 03 58  
E-mail : taysirdigitalgroup@gmail.com  
Site : https://taysirdigitalgroup.github.io/

## Références techniques

- [Canaux de plateforme Flutter](https://docs.flutter.dev/platform-integration/platform-channels)
- [API CardThemeData](https://api.flutter.dev/flutter/material/CardThemeData-class.html)
- [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html)

© 2026 Taysir Digital Group. Les crédits et droits du livre sont distincts de ceux de l’application.

## Tableaux et appréciations — version 1.0.2

Dans Agenda, le clic sur un jour de « Cette semaine » ouvre ses cours. Les icônes à droite de « Emploi du temps » et « Cette semaine » ouvrent les tableaux jour/semaine. Le champ Matière détermine une couleur stable ; un ancien créneau sans ce champ utilise son titre. Les tableaux se parcourent horizontalement et verticalement, les cours ouvrent leurs détails.

Dans une classe, l’onglet Appréciation calcule des repères sur une période choisie. À partir de deux notes : moyenne <10 → accompagnement ; de 10 à moins de 14 → consolidation ; ≥14 → encouragement. Avec zéro ou une note, les données sont indiquées comme limitées. Ces seuils internes sont des aides à la lecture, pas un barème officiel ni une décision automatique.

Les présences, absences, retards et absences excusées sont comptés séparément à partir des seuls appels renseignés. Un appel manquant n’est pas une absence. L’assiduité ne modifie pas les notes. Les conseils sont à valider par l’enseignant au regard du contexte. La moyenne de classe affichée est la moyenne des moyennes des élèves ayant au moins une note sur la période ; elle n’inclut pas les élèves non notés.

La matrice des 225 leçons et les liens de repérage PROMET figurent dans docs/SAVOIRS_COUVERTURE.md.

## Dictionnaire actuel — version 2.1.0

Le dictionnaire réunit **532 544 articles du Wiktionnaire** et **8 509 notices FranceTerme**, soit **541 053 articles au total**. Les **714 505 sens lexicaux** du corpus français extrait sont regroupés par graphie, avec prononciations écrites, étymologies et relations lexicales lorsqu'elles sont renseignées. Plus de **5,4 millions d'accès indexés** couvrent aussi les flexions, variantes et équivalents techniques : ce nombre n'est pas un nombre de mots distincts.

- Recherche commune par mot, expression, forme fléchie ou mots de définition ; filtres de provenance, lettre, emploi grammatical ou domaine.
- Une section permet de comparer Wiktionnaire et FranceTerme pour une même graphie, en conservant les accents.
- Chaque article indique sa source, sa licence, sa date ou son édition, avec lien de provenance et copie de citation. Les licences sont consultables hors connexion.
- Favoris et historique existants conservés ; identifiants modernes stables sur 64 bits.

Le Wiktionnaire utilise le dump français du **1er octobre 2026**, extrait par Wiktextract / Kaikki.org le **29 octobre 2026**. Les données modernes sont un instantané daté, sans mise à jour automatique ni serveur requis. Une nouvelle édition du pack nécessite une livraison de l'application ; les scripts de reconstruction et les empreintes sources sont fournis. Voir [le détail des sources et limites](docs/DICTIONNAIRE_MODERNE.md).

**Volume :** le pack complet occupe environ **1,1 Go décompressé**. Android le conserve également dans le cache de l'application pour SQLite : prévoir environ **3 Go libres**, en plus des autres données de l'app. La première ouverture prépare ce cache en arrière-plan et peut prendre plusieurs secondes. Il sera recréé si Android l'efface. Cette taille résulte du choix d'une consultation complète hors connexion.


## Documentation & Référence — version 2.2.0

Une nouvelle icône de livre, **à côté du dictionnaire dans le header**, ouvre un fonds sur le Sénégal :

- **Géographie : 40 fiches**, dont les profils des **14 régions** : milieux, relief, climat, eau, population, villes, activités, transports, patrimoine et risques.
- **Histoire : 32 fiches**, des premiers peuplements aux repères contemporains : royaumes, réseaux d’échanges, religions et savoirs, domination coloniale, résistances, luttes sociales, indépendance, République, culture et mémoire.
- **59 repères chronologiques**, **90 notions de vocabulaire**, une carte interactive des régions et **10 illustrations** avec crédits et licences.
- **72 activités avec pistes de correction**, objectifs et points à retenir ; **64 références** identifiées et accessibles depuis les fiches.

La recherche porte sur les textes, le lexique lié aux fiches et la chronologie, avec prise en charge des accents et de variantes de noms. Les favoris sont réactifs et distincts de ceux du dictionnaire et des leçons. On peut marquer les fiches lues, filtrer par dossier et favoris, ouvrir les options par les trois points ou un appui long, puis consulter les détails au toucher. Les photographies sont agrandissables et la carte permet de sélectionner une région puis d’ouvrir son profil. Le rafraîchissement au tirage recharge les marqueurs personnels ; les textes intégrés sont un instantané de l’édition.

Les textes et les images fonctionnent **hors connexion**. Seuls les liens externes vers les sources et les licences demandent Internet. Ce fonds est une synthèse pédagogique nationale étendue, **pas une encyclopédie exhaustive ni un programme officiel homologué** ; les activités restent à adapter à la classe. Les chiffres, limites cartographiques et événements portent leurs dates et leurs limites d’interprétation.

Les nouvelles ressources représentent environ **6 Mo décompressés** et n’ajoutent aucune dépendance Flutter. La mise à jour depuis 2.1.0 conserve les données personnelles, les livres et les deux bases du dictionnaire. Voir [la couverture et les crédits détaillés](docs/DOCUMENTATION_SENEGAL.md) et [les instructions de mise à jour](docs/MAJ_2.2.0.md).
