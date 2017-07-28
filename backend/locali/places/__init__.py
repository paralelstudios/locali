# -*- coding: utf-8 -*-
"""
    locali.places
    ~~~~~~~~~~~~~~~~
    locali places service module
"""

from ..core import Service
from .models import Place


class PlaceService(Service):
    __model__ = Place

    def get_root_places_query(self):
        return self.__model__.query.filter_by(superplace_id=None)
