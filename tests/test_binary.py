"""Tests de la conversion binaire (formats PointSet et Triangles).

Rappel du format PointSet (voir api/triangulator.yml) :
- 4 octets : le nombre de points ;
- puis 8 octets par point : X (float sur 4 octets) et Y (float sur 4 octets).

La spec ne dit pas dans quel ordre sont les octets : on suppose le
« little-endian » (l'octet de poids faible en premier).
"""

import pytest

from triangulator.binary import (
    decode_point_set,
    decode_triangles,
    encode_point_set,
    encode_triangles,
)


def test_point_set_round_trip():
    """Encoder puis décoder des points redonne exactement les mêmes points."""
    # Valeurs exactes en float 32 bits (0.1, par exemple, ne le serait pas).
    points = [(1.5, -2.25), (1000.0, 0.125), (-0.5, 3.0)]

    data = encode_point_set(points)
    result = decode_point_set(data)

    assert result == points


def test_point_set_byte_exact():
    """Les octets produits sont exactement ceux demandés par la spec."""
    # 01000000 = le nombre 1 (1 point)
    # 0000803f = le float 1.0 (X)
    # 00000040 = le float 2.0 (Y)
    expected = bytes.fromhex("01000000 0000803f 00000040")

    assert encode_point_set([(1.0, 2.0)]) == expected


def test_empty_point_set():
    """0 point donne un binaire minimal : juste le nombre 0 sur 4 octets."""
    assert encode_point_set([]) == bytes.fromhex("00000000")


def test_truncated_bytes():
    """Un binaire coupé (2 octets au lieu d'au moins 4) est refusé."""
    with pytest.raises(ValueError):
        decode_point_set(bytes.fromhex("0100"))


def test_inconsistent_count():
    """Le binaire annonce 5 points mais n'en contient que 2 : erreur."""
    header = bytes.fromhex("05000000")  # annonce 5 points
    one_point = bytes.fromhex("0000803f 00000040")  # le point (1.0, 2.0)
    data = header + one_point + one_point  # mais seulement 2 points

    with pytest.raises(ValueError):
        decode_point_set(data)


def test_triangles_round_trip():
    """Encoder puis décoder des Triangles redonne les mêmes points et triangles."""
    points = [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]
    triangles = [(0, 1, 2), (0, 2, 3)]

    data = encode_triangles(points, triangles)
    result_points, result_triangles = decode_triangles(data)

    assert result_points == points
    assert result_triangles == triangles
