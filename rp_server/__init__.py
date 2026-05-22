"""RP Server package exposing the Flask app factory."""

from .app import create_app

__all__ = ["create_app"]
