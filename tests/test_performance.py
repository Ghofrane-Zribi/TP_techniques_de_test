"""Tests de performance (marqueur `perf`, lancés avec `make perf_test`).

Chaque mesure est répétée REPEAT fois. On affiche les temps min / moyen / max
(visibles avec `pytest -s`) et on vérifie que le pire temps reste sous une
limite. Les limites sont provisoires : à ajuster après l'implémentation.
"""

import random
import time

import pytest

from triangulator.binary import decode_point_set, encode_point_set
from triangulator.triangulation import triangulate

REPEAT = 5
BINARY_MAX_SECONDS = 1.0
TRIANGULATION_MAX_SECONDS = 5.0


def random_points(n):
    """Renvoie n points au hasard (toujours les mêmes grâce à la seed 42)."""
    generator = random.Random(42)
    points = []
    for _ in range(n):
        points.append((generator.uniform(0, 1000), generator.uniform(0, 1000)))
    return points


def measure(name, function, argument):
    """Lance function(argument) REPEAT fois, affiche les temps, renvoie le pire."""
    durations = []
    for _ in range(REPEAT):
        start = time.perf_counter()
        function(argument)
        end = time.perf_counter()
        durations.append(end - start)

    average = sum(durations) / REPEAT
    # :.4f = afficher le nombre avec 4 chiffres après la virgule.
    print(
        f"{name} : min={min(durations):.4f}s "
        f"moyenne={average:.4f}s max={max(durations):.4f}s"
    )
    return max(durations)


@pytest.mark.perf
def test_encode_decode_performance():
    """Temps d'encodage et de décodage pour 100, 10 000 et 100 000 points."""
    for n in [100, 10000, 100000]:
        points = random_points(n)
        worst_encode = measure(f"encodage n={n}", encode_point_set, points)

        data = encode_point_set(points)
        worst_decode = measure(f"décodage n={n}", decode_point_set, data)

        assert worst_encode < BINARY_MAX_SECONDS
        assert worst_decode < BINARY_MAX_SECONDS


@pytest.mark.perf
def test_triangulation_performance():
    """Temps de triangulation pour 100 et 1 000 points."""
    for n in [100, 1000]:
        points = random_points(n)
        worst = measure(f"triangulation n={n}", triangulate, points)

        assert worst < TRIANGULATION_MAX_SECONDS
