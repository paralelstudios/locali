# -*- coding: utf-8 -*-
"""
    locali.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .places import PlaceService, PlaceCategoryService
from .plants import PlantService

plants = PlantService()
places = PlaceService()
place_categories = PlaceCategoryService()
