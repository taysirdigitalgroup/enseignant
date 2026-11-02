## 2.2.0 — 31 octobre 2026

- Header : icône « Documentation & Référence » entre le dictionnaire et les réglages.
- Fonds Sénégal : 72 fiches originales (40 géographie, dont 14 profils régionaux ; 32 histoire), 64 références, 10 illustrations réutilisables, 59 repères et 90 notions.
- Lecteur avec sections, tableaux, objectifs, points à retenir, activités corrigées, références, images agrandissables et navigation précédente/suivante.
- Carte vectorielle des 14 régions, sélection tactile et ouverture du profil ; limites simplifiées 2019, CC BY 3.0 IGO.
- Recherche globale, filtres par dossier/favoris, marqueurs de lecture et options sur appui long ; clés `reference:` indépendantes des marqueurs existants.
- Données et images hors connexion, liens de provenance externes ; aucune dépendance ni modification Android native.
- Scripts reproductibles de construction et contrôle, tests de navigation, favoris et carte fournis. Contrôles de données et de syntaxe exécutés ; tests Flutter à exécuter sur le poste utilisateur.

## 2.1.0 — 31 octobre 2026

- Dictionnaire : 532 544 articles Wiktionnaire et 8 509 notices FranceTerme.
- 714 505 sens lexicaux contemporains et 5 401 141 accès normalisés modernes ; mots actuels, sciences et technologies disponibles hors connexion.
- Provenance, licences hors connexion, comparaison des sources, renvois et filtres grammaticaux/domaines.
- Identifiants modernes stables 64 bits ; anciens favoris, historique et signets préservés.
- Correction des deux diagnostics de la livraison 2.0.0 incluse (import inutile et utilisation de void dans le test).
- Contrôles réels des 541 053 articles modernes et 643 631 renvois ; tests Flutter fournis, non exécutés ici.

## 1.0.2 — 31 octobre 2026

- Agenda : détails dédiés des cours par jour ; tableaux chronologiques jour/semaine, couleurs stables par matière, légende, salles et horaires.
- Champ Matière ajouté aux cours ; les anciens créneaux utilisent leur titre comme repère de couleur et sont conservés.
- Classes : quatrième onglet Appréciation, filtres de période et de besoin, moyennes, états des appels et conseils factuels.
- Les repères automatiques exigent au moins deux notes pour un classement pédagogique ; ils n’affectent pas les notes et ne supposent pas les présences manquantes.
- Savoirs : 225 leçons, dont 174 ajouts ; tous les niveaux CI à CM2 et 18 leçons de pédagogie.
- Nouvel accueil des Savoirs avec parcours par classe, domaines, filtres de progression, recherche multi-mots et favoris.
- Nouveaux tests pour les appréciations, les données manquantes et la couverture de la bibliothèque ; à exécuter sur le poste utilisateur.
- Les tableaux, champs et contenus ajoutés ne changent pas la version du stockage utilisateur.

## Correctif interactif — 31 octobre 2026

- Rechargement au tirage vers le bas et rafraîchissement automatique après écriture dans les onglets.
- Détails au clic ; trois points et appui long pour modifier ou supprimer les enregistrements.
- Fiche élève avec historique des évaluations et des présences, absences, retards et coordonnées du parent ou tuteur.
- Navigation horizontale entre les pages du Grevisse, zoom et rotation conservés.
- Recherche de page : dialogue qui gère son propre contrôleur texte pour éviter l’erreur de contrôleur détruit.
- Pages scannées manquantes sur l’installation signalée : 38 images livrées séparément dans le correctif.
- Android : activation du rappel gestuel du système pour retirer l’avertissement du journal.
- Nouvel essai de widget sur l’ouverture/fermeture du dialogue de page.
- Structure de données inchangée : les nouveaux champs de parent/tuteur sont facultatifs, les données existantes sont conservées.

# Enseignant — Fiche technique

## 1.0.0 — 30 octobre 2026

- Application Android Flutter, `com.tdg.enseignant`, nom affiché Enseignant.
- Configuration Gradle/Kotlin/Java/API Android reprise de la référence TDG fournie.
- Agenda hebdomadaire, contrôle des chevauchements et tâches datées.
- Classes du CI au CM2, élèves, appel par date, évaluations et moyenne pondérée sur 20.
- Carnet avec lecture, modification, suppression, épinglage et recherche.
- 51 fiches originales, 8 domaines, explication/activité/question/correction.
- Grevisse fourni : 468 pages, 137 repères, index OCR français et lecteur d’images.
- Rotation dédiée à l’OCR des pages PDF 437 à 449 ; rotation manuelle disponible dans le lecteur.
- Logo TDG fourni ; icône Enseignant générée et intégrée ; splash avec marge propre.
- Persistance JSON version 1, AtomicFile Android et sérialisation des écritures Dart.
- Sauvegarde/restauration via Storage Access Framework ; pas de permission générale de stockage.
- Thèmes et taille de lecture persistants.

## Architecture

La logique métier et les données sont dans `core.dart`, l’interface métier dans `main.dart`, les ressources pédagogiques et le livre dans `library.dart`. Le canal `com.tdg.enseignant/storage` gère les fichiers privés, le sélecteur de documents et les liens externes.

Aucune dépendance tierce d’exécution Flutter : uniquement le SDK Flutter. Les outils Python sont réservés à la génération d’assets et ne sont pas requis pour lancer l’application. Le projet ne contient ni compte de service, ni clé de signature, ni configuration Firebase.

## Données personnelles

Collections versionnées : classes, élèves, évaluations, présences, créneaux, tâches et notes ; listes d’identifiants pour favoris, signets et fiches étudiées. Supprimer une classe supprime ses élèves, évaluations et appels ; supprimer un élève retire ses notes des évaluations. Ces suppressions nécessitent confirmation.

La restauration valide la structure puis demande confirmation. Les données sont locales et les exports non chiffrés. En cas d’évolution de schéma, ajouter une migration qui conserve les données ; ne pas réinitialiser les collections lors d’une simple mise à jour.

## Validation

Les sources et données ont été préparées et relues. Les commandes Flutter et la compilation Android ne sont pas exécutées ici : elles sont laissées à Aliou Mbengue, comme demandé. Les tests présents dans `test/` sont à lancer sur son poste.

## Périmètre éditorial

Le livre est fourni sous forme de pages intégrales et de navigation classée, avec un index OCR non corrigé. Il n’est pas converti en une édition numérique textuelle entièrement révisée. Les 51 fiches originales constituent un socle initial et ne couvrent pas exhaustivement les programmes de toutes les classes. Aucune validation institutionnelle n’est revendiquée.


## Ajout 2.1.0 : références contemporaines

Wiktionnaire français : 532 544 articles, contributeurs du Wiktionnaire sous CC BY-SA 4.0, extraction Wiktextract / Kaikki.org. FranceTerme : 8 509 notices, ministère de la Culture / Commission d’enrichissement de la langue française, Licence Ouverte 2.0. Voir [les sources, transformations, licences et limites](DICTIONNAIRE_MODERNE.md).
