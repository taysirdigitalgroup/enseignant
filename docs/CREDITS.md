# Sources, crédits et actifs

## Ouvrage fourni

Jean-Christophe Pellat et Stéphanie Fonvielle — **Le Grevisse de l’enseignant, Grammaire de référence**, Magnard. Le PDF utilisateur comporte 468 pages. Les images et la transcription OCR proviennent de cette copie. Les droits sur l’ouvrage restent à leurs titulaires ; l’application n’est ni un produit officiel de l’éditeur ni une nouvelle licence de diffusion.

Le classement est établi d’après le sommaire imprimé, vérifié sur les images des pages PDF 4 à 9. Les entrées de même page peuvent être regroupées. Les repères ne remplacent pas le sommaire original ni l’index alphabétique du livre.

## Fiches

225 leçons originales préparées pour TDG, dont les 51 fiches de la première édition. Elles expliquent les notions par des exemples et activités originaux. Elles demandent une relecture pédagogique et une adaptation au contexte de la classe ; ce ne sont pas des reproductions d’un manuel officiel sénégalais.

## Logo TDG

`assets/images/logo_tdg.png` : conversion PNG sans redessin du fichier `logo3.jpeg` fourni par l’utilisateur. Identité, contacts et slogan repris de son Dev Env.

## Icône Enseignant

Créée avec l’outil de génération d’images intégré, puis corrigée pour le nom exact **Enseignant**. Source retenue : `assets/images/icon.png`. Les tailles launcher et splash sont produites par `tools/prepare_icons.py`.

Direction créative : livre ivoire ouvert, crayon doré, jeune pousse verte, fond bleu royal, composition lisible et nom blanc. Instruction finale : corriger le nom en « Enseignant », conserver l’illustration et le fond, centrer les éléments avec des marges adaptées aux masques Android.

Le splash utilise `assets/images/splash.png`, un dérivé distinct de l’icône, centré sur canevas transparent. Ses coins transparents évitent un rectangle blanc sur le thème sombre ; le badge bleu reste volontairement visible.

## Gradle Wrapper

Scripts et JAR issus du dépôt officiel Gradle, tag v8.14.1, licence Apache 2.0. Ils servent uniquement à démarrer la version Gradle fixée dans le fichier de propriétés.

## Outils de préparation

Python, Pillow et PyMuPDF pour les images ; Tesseract, modèle français, pour l’OCR. Ces outils ne sont pas embarqués dans l’application et ne sont pas requis à l’exécution.

## Enrichissement 1.0.2

Les pages publiques PROMET du CI au CM2 ont servi au repérage de domaines. Les leçons intégrées sont rédigées pour Enseignant ; les vidéos et documents PROMET ne sont pas copiés. Voir SAVOIRS_COUVERTURE.md pour les liens consultés et la matrice par niveau.

## Ajout 2.1.0 : références contemporaines

Wiktionnaire français : 532 544 articles, contributeurs du Wiktionnaire sous CC BY-SA 4.0, extraction Wiktextract / Kaikki.org. FranceTerme : 8 509 notices, ministère de la Culture / Commission d’enrichissement de la langue française, Licence Ouverte 2.0. Voir [les sources, transformations, licences et limites](DICTIONNAIRE_MODERNE.md).


## Documentation & Référence · Sénégal · 2.2.0

72 synthèses pédagogiques originales préparées pour TDG. Le fonds ne reproduit pas intégralement un manuel ou une encyclopédie. Les faits sont documentés par 64 références : ANSD, IFAN / Musée historique, UCAD, ISRA, Archives du Sénégal, institutions sénégalaises, UNESCO, FAO, OMVS, HCR et autres références identifiées. Les textes sources restent soumis à leurs propres droits ; leur mention n’implique pas une validation de l’app par ces institutions.

Les dix images proviennent de Wikimedia Commons : les auteurs, licences, liens de provenance et transformations sont dans `assets/documentation/images.json` et dans l’interface. Les limites régionales proviennent du Gouvernement du Sénégal / OCHA ROWCA, via geoBoundaries, sous CC BY 3.0 IGO ; géométrie de référence 2019 simplifiée et coordonnées arrondies. Aucun cliché protégé de musée n’est reproduit sans licence de réutilisation identifiée.

Voir [le catalogue documentaire et ses crédits](DOCUMENTATION_SENEGAL.md).
