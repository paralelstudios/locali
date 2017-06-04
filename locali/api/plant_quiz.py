# -*- coding: utf-8 -*-
"""
    locali.api.plant_quiz
    ~~~~~~~~~~~~~~~~
    Item API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint
from ..services import plants as _plants
from .base import add_resource

bp = Blueprint('quizzes', __name__, url_prefix="/quizzes")
api = Api(bp)


class PlantsQuizEndpoint(Resource):
    uri = "/plants"

    def get(self):
        plants = _plants.get_all_with_cols("primary_name", "image_urls")

        if not plants:
            abort(404,
                  description="For some reason, there are no plants. Hmmm...")

        return [
            {"name": plant.primary_name, "image_url": image}
            for plant in plants
            for image in plant.image_urls
        ], 200, {'Access-Control-Allow-Origin': "*"}


add_resource(api, PlantsQuizEndpoint)
