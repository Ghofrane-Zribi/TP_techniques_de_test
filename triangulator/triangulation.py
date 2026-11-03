"""Algorithme de triangulation d'un ensemble de points 2D."""


def triangulate(points: list[tuple[float, float]]) -> list[tuple[int, int, int]]:
    """Renvoie une triangulation de l'ensemble de points.

    Args:
        points: liste de points `(x, y)`.

    Returns:
        La liste des triangles, chacun étant un tuple de trois indices
        dans `points`.

    Raises:
        ValueError: si aucune triangulation n'est possible (moins de 3
            points distincts, ou tous les points sont colinéaires).

    """
    raise NotImplementedError
