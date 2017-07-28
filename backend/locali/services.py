# -*- coding: utf-8 -*-
"""
    locali.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .places import PlaceService
from .plants import PlantService
from .users import UserService

plants = PlantService()
places = PlaceService()
users = UserService()
