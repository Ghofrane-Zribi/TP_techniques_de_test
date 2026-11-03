"""Conversion entre les structures Python et les formats binaires.

Les formats `PointSet` et `Triangles` sont décrits dans `api/triangulator.yml`.
En interne, un point est un tuple `(x, y)` et un triangle un tuple de trois
indices `(i, j, k)` qui référencent des points.
"""


def encode_point_set(points: list[tuple[float, float]]) -> bytes:
    """Encode une liste de points au format binaire `PointSet`.

    Args:
        points: liste de points `(x, y)`.

    Returns:
        La représentation binaire du `PointSet`.

    """
    raise NotImplementedError


def decode_point_set(data: bytes) -> list[tuple[float, float]]:
    """Décode un `PointSet` binaire en liste de points.

    Args:
        data: la représentation binaire du `PointSet`.

    Returns:
        La liste des points `(x, y)`.

    Raises:
        ValueError: si les données sont tronquées ou incohérentes.

    """
    raise NotImplementedError


def encode_triangles(
    points: list[tuple[float, float]], triangles: list[tuple[int, int, int]]
) -> bytes:
    """Encode des sommets et des triangles au format binaire `Triangles`.

    Args:
        points: liste des sommets `(x, y)`.
        triangles: liste de triangles `(i, j, k)` (indices dans `points`).

    Returns:
        La représentation binaire de `Triangles`.

    """
    raise NotImplementedError


def decode_triangles(
    data: bytes,
) -> tuple[list[tuple[float, float]], list[tuple[int, int, int]]]:
    """Décode une structure `Triangles` binaire.

    Args:
        data: la représentation binaire de `Triangles`.

    Returns:
        Un tuple `(points, triangles)`.

    Raises:
        ValueError: si les données sont tronquées ou incohérentes.

    """
    raise NotImplementedError
