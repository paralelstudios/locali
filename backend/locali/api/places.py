# -*- coding: utf-8 -*-
"""
    locali.api.places
    ~~~~~~~~~~~~~~~~
    Plant Quizes API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint
from flask_cors import CORS
from ..services import places as _places
from .base import add_resource

bp = Blueprint('places', __name__, url_prefix='/api/places')
CORS(bp)
api = Api(bp)


class PlacesListEndpoint(Resource):
    uri = ''

    def get(self):
        places = _places.get_root_places_query()
        res = [
            {"name": p.name, "description": p.description}
            for p in places]

        if not res:
            abort(404, description="There don't seem to be any place categories, hmmm")

        return res


class PlaceEndpoint(Resource):
    uri = '/<place_name>'

    def get(self, place_name):
        if "_" in place_name:
            place_name = " ".join(place_name.split("_"))
        place = _places.first_or_404(name=place_name)
        payload = place.as_dict()
        payload["plants"] = [{"name": plant.primary_name} for plant in place.plants]
        payload["subplaces"] = [{"name": p.name} for p in place.subplaces]
        return payload


add_resource(api, PlacesListEndpoint)
add_resource(api, PlaceEndpoint)
