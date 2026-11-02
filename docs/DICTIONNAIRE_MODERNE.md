# Dictionnaire moderne · Enseignant 2.1.0

## Corpus réellement intégré

| Référence | Contenu | Licence et attribution |
|---|---|---|
| Wiktionnaire français | 532 544 graphies ; 714 505 sens lexicaux ; définitions, prononciations écrites, étymologies, synonymes, antonymes, hyperonymes, hyponymes et autres relations disponibles | Contributeurs du Wiktionnaire, CC BY-SA 4.0 ; extraction Wiktextract, Tatu Ylonen / Kaikki.org |
| FranceTerme | Les 8 509 notices publiées du fichier fourni, domaines, notes, variantes, équivalents et renvois | Ministère de la Culture / Commission d’enrichissement de la langue française ; Licence Ouverte 2.0 |

Les données Wiktionnaire proviennent de l'édition **française**, et non de définitions anglaises de mots français. Source : <https://kaikki.org/frwiktionary/> ; dump du 01/10/2026, extraction du 29/10/2026. Téléchargement brut : <https://kaikki.org/dictionary/downloads/fr/fr-extract.jsonl.gz>.

FranceTerme : <https://www.franceterme.culture.gouv.fr/public/FranceTerme.xml>. La provenance de chaque notice utilise son identifiant officiel, par exemple <https://www.culture.fr/franceterme/terme/INFO948>. La date affichée dans un article est celle de sa publication au Journal officiel ; elle ne date pas tout le corpus.

## Périmètre et transformations

Les 2 112 393 enregistrements français du dump ont été parcourus. Les emplois lexicaux d'une graphie sont regroupés dans un article, avec conservation des définitions et des marques de registre/domaines. Les graphies différentes restent distinctes. La recherche ignore casse et accents ; les comparaisons entre sources conservent les accents. Les homographies et les variantes ne sont pas fusionnées par simple ressemblance.

Les 1 547 949 enregistrements exclusivement flexionnels sont utilisés comme accès vers les lemmes quand ceux-ci existent, avec les formes données par les articles. **3 744 relations flexionnelles n'ont pas de lemme exact présent dans cette extraction** ; elles ne peuvent donc pas conduire à une définition autonome et ne sont pas inventées. Les lignes sans sens lexical exploitable ne constituent pas des articles. Les 5 401 141 accès sont des couples forme normalisée/article et ne représentent pas autant de mots distincts.

Les citations d'auteurs et les fichiers multimédias ne sont pas redistribués ; la prononciation est écrite, sans audio. Il ne s'agit pas d'une copie intégrale de toutes les sections des pages web : traductions multilingues, bibliographies, tableaux de conjugaison et exemples cités sont exclus. Les relations lexicales servent à créer des renvois cliquables lorsque leur cible exacte existe ; le texte conserve aussi les autres relations.

**731 notices FranceTerme n'ont pas de définition dans le XML officiel.** Elles restent consultables, avec leurs équivalents et renvois disponibles, et un message explicite. Aucune définition n'a été inventée pour les compléter. Les domaines et sous-domaines restent visibles ; le filtre regroupe les domaines principaux.

Le corpus couvre des usages familiers, vieillis, régionaux et spécialisés : un mot figurant dans une extraction récente n'est pas nécessairement un néologisme ni une recommandation pédagogique. FranceTerme fournit une terminologie française spécialisée, pas le programme scolaire officiel du Sénégal. Aucun corpus ne garantit tous les mots du français.

## Licences et redistribution

La base dérivée `assets/dictionary/modern.sqlite`, pour sa partie Wiktionnaire et sa diffusion combinée, est distribuée sous **CC BY-SA 4.0**. Les notices FranceTerme restent aussi disponibles sous **Licence Ouverte 2.0**, avec leur attribution. Conserver les crédits, les liens d'origine, les licences et l'indication des transformations lors d'une redistribution. Ces licences sont distinctes du code de l'application.

- Wiktionnaire : <https://fr.wiktionary.org/wiki/Wiktionnaire:Licence>.
- CC BY-SA 4.0 : <https://creativecommons.org/licenses/by-sa/4.0/> ; texte français hors connexion dans `assets/dictionary/licenses/CC-BY-SA-4.0-fr.txt`.
- Licence Ouverte 2.0 : <https://www.etalab.gouv.fr/licence-ouverte-open-licence/> ; copie dans `assets/dictionary/licenses/Licence-Ouverte.md`, issue du dépôt officiel <https://github.com/etalab/licence-ouverte>.
- Extraction : Tatu Ylonen, *Wiktextract: Wiktionary as Machine-Readable Structured Data*, LREC 2022 ; <https://kaikki.org/>.

Les pages du Wiktionnaire liées par chaque article donnent accès aux contributeurs et à l'historique de la page. Les sources, leurs empreintes SHA-256, dates et transformations sont aussi consignées dans `modern_metadata.json` et dans la base.

## Fonctionnement et reconstruction

SQLite FTS4 assure la recherche des définitions sur Android, sans dépendance Dart supplémentaire ni accès réseau. Les recherches et la préparation initiale du cache s'exécutent sur un worker natif. Les données personnelles ne sont pas migrées ni remplacées. Les identifiants sont dérivés du SHA-256 de la source et de sa graphie ou de son identifiant officiel, sur 56 bits, avec contrôle des collisions à l'import. Le codec Android/Flutter conserve les entiers 64 bits ; cette intégration vise Android.

Reconstruction avec Python 3.11+ et les deux fichiers sources locaux :

```bash
python3 tools/build_modern_dictionary.py /chemin/vers/dictionary_sources
python3 tools/check_modern_dictionary.py
```

Le script reconstruit la base à partir de zéro, sans modifier les données personnelles. Télécharger explicitement une nouvelle version des sources avant de reconstruire, mettre à jour les dates des métadonnées, la version de l'application et le nom de cache `modern_v210.sqlite` dans `DictionaryEngine.kt`, puis relancer les contrôles. Il n'existe pas de téléchargement automatique de pack dans cette livraison.

## Validation

Contrôle d'intégrité SQLite, correspondance de tous les textes riches et simples, intégrité des renvois, absence d'alias orphelin et de collision avec les identifiants historiques, essais des requêtes communes par mot/préfixe/définitions, mots technologiques et flexions. Les tests Flutter supplémentaires vérifient la transmission des filtres et des identifiants 64 bits, la provenance des articles et les sauvegardes. Ils restent à exécuter sur un poste disposant du SDK Flutter ; aucune compilation APK n'est revendiquée ici.
