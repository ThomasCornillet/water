# water

Récupérer les informations importantes pour le brassage concernant l'eau du réseau public.

Les informations proviennent du site du ministère : https://orobnat.sante.gouv.fr/


## Origines

Projet issu d'un script : https://gist.github.com/ThomasCornillet/a26b6aa6f27aa2b1513afc11765b270b
lui même issu d'un premier script : https://gist.github.com/julienvaslet/ccfa2327bf2531eadc51cdab17300e03

Ce script ne fonctionne que pour la ville de Toulouse
L'idée est maintenant de l'opérationnaliser pour les autres villes de France métropolitaine et d'outre-mer.


## Description du projet
### Général
Le projet de base est développé avec python3 sous linux (fedora).
Pour les utilisateurs et utilisatrices de Windows, pensez à changer l'encodage de Utf-8 à Latin-1.

### water.py
La première version de water.py est celle du script mentionné précédemment.

### /villes
Le répertoire 'villes' contient pour l'instant le script utilisé pour récupérer les informations nécessaires à water.py pour chaque ville réportorié dans la base de données du site du ministère (trouver_villes.py).

Il contient également un sous-répertoire 'dpt' pour stocker les informations sur les villes et les réseaux, par département.


## Modules nécessaires
### water.py
requests
re
bs4

### /villes/trouver_villes.py
requests
re
os
bs4


## En cours
### water.py
Le développement est actuellement à l'arrêt pour se concentrer sur trouver_ville.py

### /villes/trouver_villes.py
La version actuelle génère un fichier .ini par département contenant, pour chaque ville, les données "brutes" issues du site du ministère.


## À faire
### water.py
Sélection de la ville pour récupérer les informations

### /villes/trouver_villes.py
Ne faire qu'un id par ville dans les .ini, et renseigné les différents réseaux dans l'id unique de la ville

Trouver le code de recherche dans l'url du site du ministère pour les réseaux

Repérer quelles informations sont disponibles pour chaque réseau de chaque ville


## Bugs connus
### water.py
Je ne suis pas complètement sur de mon calcul de mon calcul pour l'aclcalinité.

### /villes/trouver_villes.py
Certaines ville ont plusieurs réseaux. Pour l'instant, ces villes apparaissent à plusieur reprises dans le .ini, avec un id de ville différent.

Il semble que le nom du réseau soit différent selon que l'on soit dans la liste des villes ou dans la page des résultats. Dans cette dernière, le nom indique davantage les quartiers concernés.


/-----

English coming soon (more or less)...
