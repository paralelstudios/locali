# -*- coding: utf-8 -*-
"""
    locali.plants
    ~~~~~~~~~~~~~~~~
    locali plants service module
"""

from ..core import Service
from .models import Plant
from datetime import datetime


class PlantService(Service):
    __model__ = Plant

    def get_plants_in_season_query(self, month=None):
        if not month:
            month = datetime.today().month

        return self.__model__.query.filter(
            Plant.months_available.any(month)).order_by(Plant.primary_name)
