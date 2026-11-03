"""Fixtures pytest partagées par les tests de l'API.

pytest lit ce fichier automatiquement. Une fixture est un objet préparé par
pytest : un test le reçoit en mettant son nom dans ses paramètres, par
exemple `def test_x(client, mock_psm):`.
"""

from unittest.mock import MagicMock

import pytest

from triangulator.app import create_app


@pytest.fixture
def client():
    """Faux client HTTP pour envoyer des requêtes à l'application Flask."""
    app = create_app()
    return app.test_client()


@pytest.fixture
def mock_psm(monkeypatch):
    """Faux PointSetManager.

    La fonction `get_point_set` (qui appellerait le vrai PointSetManager sur
    le réseau) est remplacée par un MagicMock. Dans un test, on écrit :
    - `mock_psm.return_value = ...` : ce que le faux PointSetManager renvoie ;
    - `mock_psm.side_effect = UneErreur()` : l'erreur qu'il doit lever.
    `monkeypatch` remet la vraie fonction en place à la fin du test.

    Pour que ce remplacement fonctionne, `app.py` devra appeler
    `client.get_point_set(...)` après `from triangulator import client`.
    """
    fake = MagicMock()
    monkeypatch.setattr("triangulator.client.get_point_set", fake)
    return fake
