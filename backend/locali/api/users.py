# -*- coding: utf-8 -*-
"""
    locali.api.users
    ~~~~~~~~~~~~~~~~
    Users API resources
"""
from flask_restful import Api
from flask import Blueprint, request
from flask_cors import CORS
from .base import add_resource, SchemaEndpoint
from ..services import users as _users

bp = Blueprint('users', __name__, url_prefix='/api/users')
CORS(bp)
api = Api(bp)


class UsersEndpoint(SchemaEndpoint):
    uri = ""
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "title": "user",
        "type": "object",
        "properties": {
            "email": {"type": "string"},
            "password": {"type": "string"}},
        "required": ["email", "password"]
    }

    def post(self):
        self.validate_form(request.json)

        _users.get_and_409(email=request.json['email'])

        new_user = _users.create(email=request.json['email'],
                                 password=request.json['password'])

        return {"user_id": new_user.id}, 201


add_resource(api, UsersEndpoint)
