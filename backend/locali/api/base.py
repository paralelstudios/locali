# -*- coding: utf-8 -*-
"""
    locali.api.base
    ~~~~~~~~~~~~~~~~~~

    Locali base API
"""
from jsonschema import validate, ValidationError
from flask import abort
from flask_jwt import jwt_required
from flask_restful import Resource
from werkzeug import exceptions as e
from sqlalchemy.exc import OperationalError
from ..services import plants
from ..core import db


def _test_db():
    try:
        plants.first()
        return True
    except OperationalError:
        db.sesion.rollback()
        return False


def ping():
    if _test_db():
        return 'OK'
    else:
        raise e.ServiceUnavailable


def add_resource(api, resource):
    api.add_resource(resource, resource.uri)


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
