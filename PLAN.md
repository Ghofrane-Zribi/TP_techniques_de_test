# Plan de tests 

## Tests de sérialisation binaire
**Round-trip** : j'encode des points, puis je décode → je dois retrouver exactement les mêmes points.
**Byte-exact** : je vérifie que les bytes produits sont exactement ceux que la spec demande . La spec ne dit pas dans quel ordre sont les octets, donc je choisis le **little-endian** (le plus courant sur nos machines). Les bytes attendus sont écrits en dur dans les tests.
**PointSet vide** : si je donne 0 points, ça doit donner un fichier binaire minimal (juste le nombre 0).
**Bytes tronqués** : si quelqu'un envoie un fichier binaire coupé/incomplet, le décodeur doit dire "erreur".
**Count incohérent** : si le fichier dit "il y a 5 points" mais qu'il n'y a pas assez de bytes pour 5 points, il faut détecter l'erreur.
**Round-trip Triangles** : même logique que PointSet, mais pour le format Triangles qui est plus complexe (points + indices de triangles).

## Tests de l'algorithme de triangulation

### Cas normaux

* **3 points non colinéaires** : doit produire 1 triangle avec les 3 points.

* **4 points formant un carré** : doit produire 2 triangles qui couvrent tout le carré.

* **N points aléatoires** : utiliser une seed fixe et vérifier les règles ci-dessous sans avoir besoin de connaître le résultat exact. Je place 4 points aux coins d'un carré et les autres points au hasard à l'intérieur. Comme ça, je connais la forme extérieure (le carré) sans avoir à la calculer. Ensuite je vérifie que :
  * chaque triangle est valide : 3 indices différents qui existent, et un triangle qui n'est pas plat ;
  * aucun triangle n'apparaît deux fois ;
  * tous les points sont utilisés ;
  * la somme des aires des triangles est égale à l'aire du carré (les triangles couvrent tout, sans trou ni chevauchement) ;
  * le nombre de triangles est `2n - h - 2`, avec `n` le nombre de points et `h` le nombre de points sur le bord (ici `h = 4`). C'est une formule connue qui marche pour toute triangulation.

### Cas limites

* **0 point** : doit retourner une erreur car une triangulation n'est pas possible.

* **1 ou 2 points** : doit retourner une erreur car il n'y a pas assez de points pour créer un triangle.

* **Points colinéaires** : si tous les points sont sur une même droite, on ne peut former aucun triangle. J'ai choisi de renvoyer une **erreur** (plutôt qu'une liste vide), comme pour 0, 1 ou 2 points. Dans l'API, ça donne donc une réponse 500.

* **Points dupliqués** : un point en double est simplement **ignoré**. Il ne provoque pas d'erreur et ne crée pas de triangle plat. Par exemple, un triangle dont un sommet est répété donne toujours 1 seul triangle.

## Tests de l'API HTTP

- **Cas normal** : le `PointSetManager` renvoie un `PointSet` valide. La réponse doit être 200 avec les triangles en binaire et le `Content-Type` `application/octet-stream`.

- **pointSetId invalide** : le `PointSetManager` ne doit pas être appelé. La réponse doit être 400 avec un JSON `{code, message}`.

- **PointSet introuvable** : si le `PointSetManager` renvoie un 404, le `Triangulator` doit aussi renvoyer un 404 avec un JSON `{code, message}`.

- **PointSetManager indisponible** : simuler une erreur réseau ou un timeout. La réponse doit être 503 avec un JSON `{code, message}`.

- **Pas assez de points** : si le `PointSet` contient moins de 3 points, la réponse doit être 500 avec un JSON `{code, message}`.

- **Points colinéaires** : même chose, la triangulation est impossible, donc la réponse est 500 avec un JSON `{code, message}`.

- **Appel du PointSetManager** : vérifier qu'il est appelé avec le bon `pointSetId`.

## Tests de performance

- Vérifier le temps d'encodage et de décodage pour N = 100 / 10 000 / 100 000 points.

- Vérifier le temps de triangulation pour N = 100 / 1 000 points. Je ne vais pas jusqu'à 100 000 car un algorithme simple serait beaucoup trop lent.

- Pour que le test échoue si c'est trop lent, je fixe un temps maximum : **1 seconde** pour l'encodage et le décodage, **5 secondes** pour la triangulation. Ces valeurs sont choisies un peu au hasard et je les ajusterai une fois l'implémentation faite.

Remarque: Chaque mesure doit être répétée plusieurs fois afin d'avoir des résultats plus fiables et de voir la variation des temps.

## Hypothèses et limites

- **Adresse du PointSetManager** : par défaut `http://localhost:5000`. On peut la changer avec la variable d'environnement `POINT_SET_MANAGER_URL`.

- **Cas que je ne teste pas pour l'instant**, parce que ni la spec ni ce plan ne disent quoi faire :
  - le `PointSetManager` renvoie un `PointSet` mal formé ;
  - le `PointSetManager` répond 400 ou 500 ;
  - il y a des octets en trop à la fin d'un message binaire.

  Je déciderai du comportement voulu pendant l'implémentation, puis j'ajouterai les tests correspondants.

