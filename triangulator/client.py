"""Client HTTP permettant de récupérer un `PointSet` auprès du PointSetManager."""

import os

POINT_SET_MANAGER_URL = os.environ.get(
    "POINT_SET_MANAGER_URL", "http://localhost:5000"
)
"""URL de base du PointSetManager (configurable par variable d'environnement)."""

TIMEOUT_SECONDS = 5
"""Délai maximal d'attente d'une réponse du PointSetManager."""


class PointSetNotFoundError(Exception):
    """Le PointSetManager ne connaît pas le PointSetID demandé (404)."""


class PointSetManagerUnavailableError(Exception):
    """Le PointSetManager est injoignable, en timeout ou indisponible (503)."""


def get_point_set(point_set_id: str) -> bytes:
    """Récupère le `PointSet` binaire correspondant à `point_set_id`.

    Appelle `GET {POINT_SET_MANAGER_URL}/pointset/{point_set_id}`
    via `urllib.request.urlopen`.

    Args:
        point_set_id: l'identifiant (UUID) du PointSet.

    Returns:
        Le contenu binaire du `PointSet`.

    Raises:
        PointSetNotFoundError: si le PointSetManager répond 404.
        PointSetManagerUnavailableError: en cas d'erreur réseau, de timeout
            ou de réponse 503.

    """
    raise NotImplementedError
