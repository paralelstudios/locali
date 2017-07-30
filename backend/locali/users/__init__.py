# -*- coding: utf-8 -*-
"""
    locali.plants
    ~~~~~~~~~~~~~~~~
    locali plants service module
"""

from ..core import Service
from .models import User


class UserService(Service):
    __model__ = User

    def authenticate(self, email, password):
        u = self.first(email=email)
        if u and u.verify_password(password):
            return u

    def identity(self, payload):
        user_id = payload["identity"]
        return User.query.get(user_id)
