# -*- coding: utf-8 -*-
"""
    locali.api
    ~~~~~~~~~~~~~

    locali api application package
"""
from flask import jsonify

from ..core import LocaliException
from ..helpers import LocaliJSONEncoder
from .. import factory  # noqa
from .base import ping


def create_app(settings_override=None):
    """Returns the Locali API application instance"""
    app = factory.create_app(__name__, __path__, settings_override)  # noqa

    # Set the default JSON encoder
    app.json_encoder = LocaliJSONEncoder

    # Register custom error handlers
    app.errorhandler(LocaliException)(on_locali_error)
    app.errorhandler(404)(on_404)
    if 'ping' not in app.view_functions:
        app.add_url_rule('/_ping', 'ping', ping)

    return app


def on_locali_error(e):
    return jsonify(dict(error=e.msg)), 400


def on_404(e):
    return jsonify(dict(error='Not found')), 404
