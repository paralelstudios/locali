# -*- coding: utf-8 -*-
"""
    locali.api.plants
    ~~~~~~~~~~~~~~~~
    Plants API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint
from flask_cors import CORS
from ..services import plants as _plants
from .base import add_resource

bp = Blueprint('plants', __name__, url_prefix="/plants")
CORS(bp)
api = Api(bp)


class PlantsListEndpoint(Resource):
    uri = "/"

    def get(self):
        plants = _plants.get_query_with_cols("primary_name").order_by("primary_name")

        if not plants:
            abort(404,
                  description="For some reason, there are no plants. Hmmm...")

        return [
            {"name": plant.primary_name}
            for plant in plants
        ], 200


class PlantEndpoint(Resource):
    uri = "/<plant_name>"

    def get(self, plant_name):
        plant = _plants.first_or_404(primary_name=plant_name)

        return plant.as_dict(), 200


add_resource(api, PlantsListEndpoint)
add_resource(api, PlantEndpoint)
