# Trace — History Explorer

Double-cliquer sur `Lancer.cmd`, puis ouvrir http://127.0.0.1:8765 si nécessaire.
Python 3 est requis, sans dépendance supplémentaire. Garder la fenêtre du serveur ouverte ; Ctrl+C l’arrête.
Le fichier `History` doit rester dans le dossier parent. Pour une autre copie : `python server.py --database "C:\chemin\History"`.

- Graphique de toutes les visites, zoom à la molette, déplacement en glissant, curseurs accessibles et plein écran.
- Clic sur un point : recherche de son URL dans le tableau. Clic sur un site ou une case horaire : filtre global. « Réinitialiser » retire tous les filtres.
- Recherche textuelle, dates, recherches enregistrées, tableau paginé, tri chronologique et export CSV de la sélection.
- Les moyennes utilisent les jours calendaires de la période choisie, y compris les jours sans visite. La carte hebdomadaire montre les totaux cumulés. Horaires Europe/Paris, changement d’heure compris.
- Une recherche désigne une visite d’une URL associée à un terme dans `keyword_search_terms` ; ce n’est pas une garantie qu’une nouvelle recherche a été saisie à chaque visite. Les recherches absentes de cette table ne sont pas identifiables ici.
- Le classement compte les lignes de visites conservées, pas les compteurs historiques agrégés de `urls`. Il regroupe les noms d’hôte exacts (sous-domaines distincts).

La base est ouverte en lecture seule. L’application écoute uniquement sur 127.0.0.1, sans ressource externe ni télémétrie. Les données sont chargées au démarrage ; redémarrer le serveur pour lire une copie actualisée. Les liens de pages s’ouvrent seulement sur clic explicite. Les exports contiennent l’historique personnel.

Vérifications : `python -m unittest test_server.py` et `node --check app.js`.
