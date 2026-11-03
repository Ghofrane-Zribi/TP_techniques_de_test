"""Tests de l'algorithme de triangulation.

`triangulate(points)` reçoit une liste de points (x, y) et renvoie une liste
de triangles. Un triangle est un tuple de 3 indices dans la liste de points :
par exemple (0, 1, 2) est le triangle formé par points[0], points[1], points[2].
"""

import random

import pytest

from triangulator.triangulation import triangulate

# ---------- Fonctions de vérification utilisées par plusieurs tests ----------


def triangle_area(p, q, r):
    """Renvoie l'aire du triangle de sommets p, q et r."""
    # Formule du produit en croix : sa valeur absolue divisée par 2 = l'aire.
    cross = (q[0] - p[0]) * (r[1] - p[1]) - (r[0] - p[0]) * (q[1] - p[1])
    return abs(cross) / 2


def total_area(points, triangles):
    """Renvoie la somme des aires de tous les triangles."""
    area = 0
    for a, b, c in triangles:
        area += triangle_area(points[a], points[b], points[c])
    return area


def check_triangles_are_valid(points, triangles):
    """Vérifie que chaque triangle est valide et qu'il n'y a pas de doublon."""
    already_seen = []
    for triangle in triangles:
        a, b, c = triangle

        # Les 3 indices sont différents.
        assert a != b and b != c and a != c

        # Les 3 indices existent dans la liste de points.
        for index in triangle:
            assert 0 <= index < len(points)

        # Le triangle n'est pas plat (son aire n'est pas nulle).
        assert triangle_area(points[a], points[b], points[c]) > 0

        # Le triangle n'a pas déjà été vu (on trie les indices pour que
        # (0, 1, 2) et (2, 0, 1) soient considérés comme le même triangle).
        sorted_indices = sorted(triangle)
        assert sorted_indices not in already_seen
        already_seen.append(sorted_indices)


# ---------- Cas normaux ----------


def test_three_points():
    """3 points non colinéaires donnent 1 triangle qui utilise les 3 points."""
    points = [(0.0, 0.0), (4.0, 0.0), (0.0, 3.0)]

    triangles = triangulate(points)

    assert len(triangles) == 1
    assert sorted(triangles[0]) == [0, 1, 2]


def test_square():
    """Un carré donne 2 triangles qui couvrent tout le carré."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]

    triangles = triangulate(points)

    assert len(triangles) == 2
    check_triangles_are_valid(points, triangles)
    # pytest.approx : compare des nombres à virgule avec une petite tolérance.
    assert total_area(points, triangles) == pytest.approx(1.0)


def test_random_points():
    """Points aléatoires : on vérifie des règles, pas un résultat exact."""
    # Les 4 coins d'un carré 100 x 100...
    points = [(0.0, 0.0), (100.0, 0.0), (100.0, 100.0), (0.0, 100.0)]
    # ... plus 50 points au hasard à l'intérieur. La seed 42 fait que le
    # « hasard » donne toujours les mêmes points d'une exécution à l'autre.
    generator = random.Random(42)
    for _ in range(50):
        x = generator.uniform(1, 99)
        y = generator.uniform(1, 99)
        points.append((x, y))

    triangles = triangulate(points)

    # Règle 1 : triangles valides et sans doublon.
    check_triangles_are_valid(points, triangles)

    # Règle 2 : tous les points sont utilisés.
    used_indices = set()
    for triangle in triangles:
        for index in triangle:
            used_indices.add(index)
    assert len(used_indices) == len(points)

    # Règle 3 : les triangles couvrent exactement le carré.
    assert total_area(points, triangles) == pytest.approx(100.0 * 100.0)

    # Règle 4 : n points dont h sur le bord donnent 2n - h - 2 triangles.
    n = len(points)
    h = 4
    assert len(triangles) == 2 * n - h - 2


# ---------- Cas limites ----------


def test_zero_point():
    """0 point : aucune triangulation possible, erreur."""
    with pytest.raises(ValueError):
        triangulate([])


def test_one_or_two_points():
    """1 ou 2 points : pas assez pour un triangle, erreur."""
    with pytest.raises(ValueError):
        triangulate([(0.0, 0.0)])

    with pytest.raises(ValueError):
        triangulate([(0.0, 0.0), (1.0, 1.0)])


def test_collinear_points():
    """Points tous sur une même droite : aucun triangle possible, erreur."""
    with pytest.raises(ValueError):
        triangulate([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)])


def test_duplicate_points():
    """Un point en double est ignoré : pas d'erreur et pas de triangle plat."""
    # Un triangle dont le point (0, 0) est répété à la fin.
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0), (0.0, 0.0)]

    triangles = triangulate(points)

    assert len(triangles) == 1
    check_triangles_are_valid(points, triangles)
