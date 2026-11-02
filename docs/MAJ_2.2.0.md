# Mise à jour Enseignant 2.2.0 depuis 2.1.0

Cette archive contient uniquement les fichiers modifiés ou nouveaux. Elle complète un **projet 2.1.0 existant** et n’est pas autonome.

1. Conserver une copie du projet.
2. Extraire le contenu de l’archive à la racine de `enseignant/`, là où se trouve `pubspec.yaml`, en acceptant les remplacements.
3. Les chemins `lib/`, `assets/`, `test/`, `tools/` et `docs/` rejoignent les dossiers existants.
4. Redémarrer complètement l’application après la compilation, pour charger les nouveaux assets.

```bash
flutter pub get && flutter analyze && flutter test && flutter run
```

La nouvelle icône de livre se trouve à côté de celle du dictionnaire. Le fonds contient 72 fiches, une carte des 14 régions, 59 repères chronologiques, 90 notions et 10 illustrations.

Les données personnelles, les favoris antérieurs, le Grevisse et les dictionnaires existants restent en place. Aucun changement de schéma personnel ni nouvelle dépendance n’est nécessaire. Les marqueurs documentaires utilisent le préfixe `reference:` dans les listes existantes et sont inclus dans les sauvegardes habituelles.

Le fonds est un instantané daté, pas un fil d’actualité ni une encyclopédie exhaustive. Le rapport de validation précise les contrôles exécutés et ceux restant à lancer avec Flutter.
