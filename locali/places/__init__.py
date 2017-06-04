# -*- coding: utf-8 -*-
"""
    locali.places
    ~~~~~~~~~~~~~~~~
    locali places service module
"""

from ..core import Service
from .models import Places, PlaceCategory


class PlacesService(Service):
    __model__ = Places


class PlaceCategoryService(Service):
    __model__ = PlaceCategory
