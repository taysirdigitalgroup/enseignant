# Mise à jour Enseignant 2.1.0 depuis 2.0.0

Cette archive est un **correctif cumulatif pour le projet 2.0.0 existant**, avec ou sans le petit correctif d'analyse déjà appliqué. Ce n'est pas un projet autonome. Fermer l'app, conserver une sauvegarde du projet, puis extraire le contenu **à la racine du projet `enseignant/`**, là où se trouve `pubspec.yaml`, en autorisant le remplacement des fichiers.

Les chemins `lib/`, `assets/`, `android/`, `test/`, `tools/` et `docs/` doivent rejoindre les dossiers existants. Aucun fichier de données personnelles du téléphone n'est inclus. Garder le même identifiant Android `com.tdg.enseignant` et la même clé de signature afin de mettre à jour l'app existante.

```bash
flutter pub get && flutter analyze && flutter test && flutter run
```

Un redémarrage complet est nécessaire : les modifications du moteur Android et les nouveaux assets ne sont pas chargés par un simple hot reload. Les paquets signalés comme ayant une version plus récente ne nécessitent pas de mise à jour pour ce correctif.

Le dictionnaire moderne fonctionne hors connexion et se prépare au premier accès, sans remplacer les favoris ou l'historique. Prévoir environ **3 Go d'espace libre** pour le pack, le cache SQLite et l'installation. Ne pas supprimer le PDF ou la base historique : ils restent utilisés par la recherche commune.

Les contrôles de données et de syntaxe ont été exécutés pendant la préparation. Les tests Flutter et le build Android n'ont pas été exécutés ici, faute de SDK Flutter. Si votre poste signale une erreur, conserver le message complet et la commande utilisée pour permettre une correction précise.
