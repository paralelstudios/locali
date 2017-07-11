# -*- coding: utf-8 -*-
"""
    locali.helpers
    ~~~~~~~~~~~~~~~~
    Matchme Helpers
"""
import pkgutil
import importlib
from werkzeug import exceptions as e
from jsonschema import validate, ValidationError
from flask import Blueprint, abort
from flask.json import JSONEncoder as BaseJSONEncoder
from flask_jwt import jwt_required
from flask_restful import Resource


def register_blueprints(app, package_name, package_path):
    """Register all Blueprint instances on the specified Flask application found
    in all modules for the specified package.

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    """
    rv = []
    for _, name, _ in pkgutil.iter_modules(package_path):
        m = importlib.import_module('%s.%s' % (package_name, name))
        for item in dir(m):
            item = getattr(m, item)
            if isinstance(item, Blueprint):
                app.register_blueprint(item)
            rv.append(item)
    return rv


class Dictable(object):
    __private__ = None

    def get_field_names(self):
        for p in self.__mapper__.iterate_properties:
            yield p.key

    def as_dict(self, with_secrets=False):
        return {
            col: getattr(self, col) for col in self.get_field_names()
            if col in self.__dict__ and (
                    not with_secrets or col not in self.__private__)
        }


class LocaliJSONEncoder(BaseJSONEncoder):
    def default(self, o):
        if isinstance(o, Dictable):
            return o.as_dict()
        return BaseJSONEncoder.default(self, o)


def try_committing(connection_reference):
    """
    Pass a scoped session or connection (anything with commit and rollback methods)
    to this function, and it will try committing, with rollback on failure.
    """
    try:
        connection_reference.commit()
    except Exception as e:
        connection_reference.rollback()
        raise e


class Validatable(object):
    schema = None

    def validate_query(self, query_keys, *required_keys):
        diff = set(required_keys or self.schema["required"]) - set(query_keys)
        if diff:
            abort(400, description="Query keys {} missing {}".format(query_keys, diff))

    def validate_form(self, data):
        try:
            validate(data, self.schema)
        except ValidationError as ve:
            raise e.BadRequest('{}: {}'.format(self.uri, ve.message))


class SchemaEndpoint(Validatable, Resource):
    pass


class JWTEndpoint(SchemaEndpoint):
    method_decorators = [jwt_required()]
