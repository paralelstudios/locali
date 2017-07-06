# -*- coding: utf-8 -*-
"""
    locali.api.plant_quiz
    ~~~~~~~~~~~~~~~~
    Plant Quizes API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint
from flask_cors import CORS
from ..services import plants as _plants
from .base import add_resource

bp = Blueprint('quizzes', __name__, url_prefix="/quizzes")
CORS(bp)
api = Api(bp)


class PlantsQuizEndpoint(Resource):
    uri = "/plants"

    def get(self):
        plants = _plants.get_query_with_cols("primary_name", "image_urls")
        res = [
            {"name": plant.primary_name, "image_url": image}
            for plant in plants
            for image in plant.image_urls
        ]
        if not res:
            abort(404,
                  description="For some reason, there are no plants. Hmmm...")

        return res


add_resource(api, PlantsQuizEndpoint)
