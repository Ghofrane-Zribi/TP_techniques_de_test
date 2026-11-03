"""Tests de l'API HTTP du Triangulator (spec : api/triangulator.yml).

Chaque test reçoit deux fixtures (définies dans conftest.py) :
- `client` : un faux client HTTP qui envoie des requêtes à l'application ;
- `mock_psm` : un faux PointSetManager dont on choisit la réponse.
"""

from triangulator.binary import decode_triangles, encode_point_set
from triangulator.client import PointSetManagerUnavailableError, PointSetNotFoundError

VALID_ID = "123e4567-e89b-12d3-a456-426614174000"
URL = "/triangulation/" + VALID_ID


def check_json_error(response, expected_status):
    """Vérifie le code HTTP et que la réponse est un JSON {code, message}."""
    assert response.status_code == expected_status
    assert response.mimetype == "application/json"
    body = response.get_json()
    assert "code" in body
    assert "message" in body


def test_triangulation_ok(client, mock_psm):
    """Cas normal : 200 et les triangles au format binaire."""
    points = [(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)]
    mock_psm.return_value = encode_point_set(points)

    response = client.get(URL)

    assert response.status_code == 200
    assert response.mimetype == "application/octet-stream"
    result_points, result_triangles = decode_triangles(response.data)
    assert result_points == points
    assert len(result_triangles) == 1


def test_invalid_point_set_id(client, mock_psm):
    """Un id qui n'est pas un UUID : 400, et le PointSetManager n'est pas appelé."""
    response = client.get("/triangulation/abc")

    check_json_error(response, 400)
    mock_psm.assert_not_called()


def test_point_set_not_found(client, mock_psm):
    """Le PointSetManager répond 404 : le Triangulator répond aussi 404."""
    mock_psm.side_effect = PointSetNotFoundError()

    response = client.get(URL)

    check_json_error(response, 404)


def test_point_set_manager_unavailable(client, mock_psm):
    """Le PointSetManager ne répond pas (réseau, timeout) : 503."""
    mock_psm.side_effect = PointSetManagerUnavailableError()

    response = client.get(URL)

    check_json_error(response, 503)


def test_not_enough_points(client, mock_psm):
    """Le PointSet n'a que 2 points : la triangulation échoue, 500."""
    mock_psm.return_value = encode_point_set([(0.0, 0.0), (1.0, 1.0)])

    response = client.get(URL)

    check_json_error(response, 500)


def test_collinear_points(client, mock_psm):
    """Les points sont colinéaires : la triangulation échoue, 500."""
    mock_psm.return_value = encode_point_set([(0.0, 0.0), (1.0, 1.0), (2.0, 2.0)])

    response = client.get(URL)

    check_json_error(response, 500)


def test_point_set_manager_called_with_id(client, mock_psm):
    """Le PointSetManager est appelé une seule fois, avec le bon id."""
    mock_psm.return_value = encode_point_set([(0.0, 0.0), (1.0, 0.0), (0.0, 1.0)])

    client.get(URL)

    mock_psm.assert_called_once_with(VALID_ID)
