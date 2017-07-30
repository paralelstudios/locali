# -*- coding: utf-8 -*-
"""
    locali.factory
    ~~~~~~~~~~~~

"""
import sys
import logging
from flask import Flask
from .core import db
from .helpers import register_blueprints
from .middleware import HTTPMethodOverrideMiddleware
from flask_jwt import JWT
from .services import users as _users


def create_app(package_name, package_path, settings_override=None):
    app = Flask(package_name, instance_relative_config=True)
    app.config.from_object('locali.settings')
    app.config.from_pyfile('settings.cfg', silent=True)
    app.config.from_object(settings_override)

    # if we're in debug mode and databases are not localhost, show a warning
    if app.config['DEBUG'] or app.config['TESTING']:
        warnings = [
            key + " is not localhost"
            for key in {'SQLALCHEMY_DATABASE_URI'}
            if app.config.get(key) and 'localhost' not in app.config[key]]
        map(app.logger.warn, warnings)
        if app.config['TESTING'] and warnings:
            raise Exception(
                'RUNNING TESTS ON A NONLOCAL DATABASE IS A DESTRUCTIVE ACTION')

    # component initiation
    db.init_app(app)
    jwt = JWT(app, _users.authenticate, _users.identity)  # noqa

    if not app.debug:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        handler.setLevel(logging.INFO)
        app.logger.addHandler(handler)

    register_blueprints(app, package_name, package_path)
    app.wsgi_app = HTTPMethodOverrideMiddleware(app.wsgi_app)

    return app
