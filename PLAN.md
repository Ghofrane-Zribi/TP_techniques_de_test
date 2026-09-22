# Plan de tests 

## Tests de sérialisation binaire

**Round-trip** : j'encode des points, puis je décode → je dois retrouver exactement les mêmes points.
**Byte-exact** : je vérifie que les bytes produits sont exactement ceux que la spec demande .
**PointSet vide** : si je donne 0 points, ça doit donner un fichier binaire minimal (juste le nombre 0).
**Bytes tronqués** : si quelqu'un envoie un fichier binaire coupé/incomplet, le décodeur doit dire "erreur".
**Count incohérent** : si le fichier dit "il y a 5 points" mais qu'il n'y a pas assez de bytes pour 5 points, il faut détecter l'erreur.
**Round-trip Triangles** : même logique que PointSet, mais pour le format Triangles qui est plus complexe (points + indices de triangles).

## Tests de l'algorithme de triangulation

### Cas normaux

* **3 points non colinéaires** : doit produire 1 triangle avec les 3 points.

* **4 points formant un carré** : doit produire 2 triangles qui couvrent tout le carré.

* **N points aléatoires** : utiliser une seed fixe et vérifier les règles ci-dessous sans avoir besoin de connaître le résultat exact.

### Cas limites

* **0 point** : doit retourner une erreur car une triangulation n'est pas possible.

* **1 ou 2 points** : doit retourner une erreur car il n'y a pas assez de points pour créer un triangle.

* **Points colinéaires** : le comportement doit être défini (erreur ou triangulation vide), puis testé.

* **Points dupliqués** : le comportement doit être défini, puis testé.

## Tests de l'API HTTP

- **Cas normal** : le `PointSetManager` renvoie un `PointSet` valide. La réponse doit être 200 avec les triangles en binaire et le `Content-Type` `application/octet-stream`.

- **pointSetId invalide** : le `PointSetManager` ne doit pas être appelé. La réponse doit être 400 avec un JSON `{code, message}`.

- **PointSet introuvable** : si le `PointSetManager` renvoie un 404, le `Triangulator` doit aussi renvoyer un 404 avec un JSON `{code, message}`.

- **PointSetManager indisponible** : simuler une erreur réseau ou un timeout. La réponse doit être 503 avec un JSON `{code, message}`.

- **Pas assez de points** : si le `PointSet` contient moins de 3 points, la réponse doit être 500 avec un JSON `{code, message}`.

- **Appel du PointSetManager** : vérifier qu'il est appelé avec le bon `pointSetId`.

## Tests de performance

- Vérifier le temps d'encodage et de décodage pour N = 100 / 10 000 / 100 000 points.

- Vérifier le temps de triangulation.

Remarque: Chaque mesure doit être répétée plusieurs fois afin d'avoir des résultats plus fiables et de voir la variation des temps.

