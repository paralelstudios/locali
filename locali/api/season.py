# -*- coding: utf-8 -*-
"""
    locali.api.season
    ~~~~~~~~~~~~~~~~
    Season API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint
from flask_cors import CORS
from ..services import plants as _plants
from .base import add_resource
from datetime import datetime

bp = Blueprint('season', __name__, url_prefix="/season")
CORS(bp)
api = Api(bp)


class SeasonEndpoint(Resource):
    uri = "/<month_number>"

    def get(self, month_number=None):
        try:
            month_number = abs(int(month_number or datetime.today().month))
        except ValueError:
            abort(400, description="<month_number> needs to be a natural number")

        plants_in_season = _plants.get_plants_in_season_query(month_number).all()

        if not plants_in_season:
            abort(404, description="No plants in season! What has the world come to!")

        return [
            {"name": plant.primary_name}
            for plant in plants_in_season]


class ThisSeasonEndpoint(SeasonEndpoint):
    uri = "/"


add_resource(api, SeasonEndpoint)
add_resource(api, ThisSeasonEndpoint)
