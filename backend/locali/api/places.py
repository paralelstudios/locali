# -*- coding: utf-8 -*-
"""
    locali.api.places
    ~~~~~~~~~~~~~~~~
    Plant Quizes API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint
from flask_cors import CORS
from ..services import place_categories as _place_c, places as _places
from .base import add_resource

bp = Blueprint('places', __name__, url_prefix='/api/places')
CORS(bp)
api = Api(bp)


class PlaceCategoriesListEndpoint(Resource):
    uri = '/categories'

    def get(self):
        categories = _place_c.get_query_with_cols("name", "description")
        res = [
            cat.as_dict()
            for cat in categories]

        if not res:
            abort(404, description="There don't seem to be any place categories, hmmm")

        return res


class PlacesListEndpoint(Resource):
    uri = '/category/<category>'

    def get(self, category):
        category = _place_c.first_or_404(name=category)

        return [
            {"name": place.name, "description": place.description}
            for place in category.places
        ]


class PlaceEndpoint(Resource):
    uri = '/<place_name>'

    def get(self, place_name):
        if "_" in place_name:
            place_name = " ".join(place_name.split("_"))
        place = _places.first_or_404(name=place_name)
        payload = place.as_dict()
        payload["plants"] = [{"name": plant.primary_name} for plant in place.plants]
        return payload


add_resource(api, PlaceCategoriesListEndpoint)
add_resource(api, PlacesListEndpoint)
add_resource(api, PlaceEndpoint)
