# -*- coding: utf-8 -*-
"""
    locali.services
    ~~~~~~~~~~~~~~~~~

    services module
"""

from .places import PlacesService, PlaceCategoryService
from .plants import PlantService

plants = PlantService()
places = PlacesService()
place_categories = PlaceCategoryService()
