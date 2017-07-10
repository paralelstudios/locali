# -*- coding: utf-8 -*-
"""
    locali.api.base
    ~~~~~~~~~~~~~~~~~~

    Locali base API
"""
from werkzeug.exceptions import ServiceUnavailable
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
        raise ServiceUnavailable


def add_resource(api, resource):
    api.add_resource(resource, resource.uri)
