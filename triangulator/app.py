"""Application Flask exposant l'API HTTP du Triangulator."""

from flask import Flask


def create_app() -> Flask:
    """Crée et configure l'application Flask du Triangulator.

    Returns:
        L'application Flask avec la route `/triangulation/<pointSetId>`.

    """
    app = Flask(__name__)

    @app.get("/triangulation/<point_set_id>")
    def get_triangulation(point_set_id: str):
        """Renvoie la triangulation du PointSet `point_set_id` en binaire."""
        raise NotImplementedError

    return app
