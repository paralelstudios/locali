# -*- coding: utf-8 -*-
"""
    locali.places
    ~~~~~~~~~~~~~~~~
    locali places service module
"""

from ..core import Service
from .models import Place, PlaceCategory


class PlaceService(Service):
    __model__ = Place


class PlaceCategoryService(Service):
    __model__ = PlaceCategory
