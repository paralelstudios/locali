# -*- coding: utf-8 -*-
"""
    locali.users.models
    ~~~~~~

"""
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy import func
from flask_bcrypt import generate_password_hash, check_password_hash
from flask import current_app
from ..core import db
from ..helpers import Dictable


class User(db.Model, Dictable):
    __tablename__ = 'users'
    _private = ["_password"]
    id = db.Column(UUID, primary_key=True, default=lambda: str(uuid4()))
    email = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime,
                          server_default=func.now())
    _password = db.Column(db.Binary, nullable=False)

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def _set_password(self, password):
        self._password = generate_password_hash(
            password, current_app.config['BCRYPT_LOG_ROUNDS'])

    def verify_password(self, password):
        return check_password_hash(self._password, password)

    def __str__(self):
        return "User(id='%s')" % self.id
