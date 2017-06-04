# -*- coding: utf-8 -*-
"""
    locali.plants
    ~~~~~~~~~~~~~~~~
    locali plants service module
"""

from ..core import Service
from .models import Plant


class PlantService(Service):
    __model__ = Plant
