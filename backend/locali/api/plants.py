# -*- coding: utf-8 -*-
"""
    locali.api.plants
    ~~~~~~~~~~~~~~~~
    Plants API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint, current_app, request
from flask_cors import CORS
from flask_jwt import jwt_required
from dateparser import parse as dateparse
from ..services import plants as _plants, places as _places
from .base import add_resource, SchemaEndpoint, JWTEndpoint
from ..helpers import is_allowed_file, ALLOWED_EXTENSIONS
from ..core import s3


bp = Blueprint('plants', __name__, url_prefix="/api/plants")
CORS(bp)
api = Api(bp)


class PlantsListEndpoint(SchemaEndpoint):
    uri = ""
    schema = {
        "type": "object",
        "title": "plant",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "plantType": {"type": "string"},
            "substrates": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "scientificNames": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "commonNames": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "places": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "monthsAvailable": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            },
            "uses": {
                "type": "array",
                "items": {
                    "type": "string"
                }
            }
        },
        "required": ["name", "description"]
    }

    def _enrich_with_place(self, place_name, plant):
        place = _places.first(name=place_name, with_for_update=True)
        if not place:
            abort(400,
                  description="The place, {},  must exist before the a plant, {}, can be inside of it!".format(place_name, plant.name))
        if plant.places:
            plant.places.append(place)
        else:
            plant.places = [place]

    @jwt_required()
    def post(self):
        self.validate_form(request.json)
        if _plants.first(primary_name=request.json['name']):
            print("found")
            abort(400, description="Place, {}, already exists!".format(request.json['name']))

        plant = _plants.new(
            primary_name=request.json['name'].lower(),
            description=request.json['description']
        )

        for place_name in request.json.get('places', []):
            self._enrich_with_place(place_name, plant)

        plant.uses = request.json.get('uses')
        plant.substrates = request.json.get('substrates', [])
        plant.months_available = [
            dateparse(d).month for d in request.json.get('monthsAvailable', [])]
        plant.plant_type = request.json.get('plantType', [])
        plant.common_names = request.json.get('commonNames', [])
        plant.scientific_names = request.json.get('scientificNames', [])

        _plants.save(plant)

        return 201

    def get(self):
        plants = _plants.get_query_with_cols("primary_name").order_by("primary_name")
        resp = [
            {"name": plant.primary_name}
            for plant in plants
        ]

        if not resp:
            abort(404,
                  description="For some reason, there are no plants. Hmmm...")

        return resp, 200


class PlantPhotoEndpoint(JWTEndpoint):
    uri = "/<plant_name>/photos"

    def post(self, plant_name):
        plant = _plants.first_or_404(
            primary_name=plant_name.replace('_', ' '))
        for part in ["flower", "seed", "leaf", "other"]:
            photos = request.files.getlist(part + "Photos[]")
            setattr(plant, part + "_image_urls",
                    [
                        self._process_file(f, plant, part)
                        for f in photos
                    ])

        _plants.save(plant)

        return 201

    def _process_file(self, f, plant, part):
        if not is_allowed_file(f.filename):
            abort(400,
                  description='Please only submit {} files'.format(
                      ALLOWED_EXTENSIONS))
        key = 'plants/{plant_id}/{part}/{file_name}'.format(
            plant_id=plant.id, part=part, file_name=f.filename.replace(' ', '-'))
        file_name = 'https://s3.amazonaws.com/{bucket}/{key}'.format(
            bucket=current_app.config['LOCALI_PHOTO_UPLOAD_BUCKET'],
            key=key)
        images = getattr(plant, part + "_image_urls")
        if not images or file_name not in images:
            s3.Object(
                current_app.config['LOCALI_PHOTO_UPLOAD_BUCKET'],
                key).put(Body=f.stream, ACL='public-read')
        return file_name


class PlantEndpoint(Resource):
    uri = "/<plant_name>"

    def get(self, plant_name):
        plant = _plants.first_or_404(
            primary_name=plant_name.replace('_', ' '))

        return plant.as_dict()


add_resource(api, PlantsListEndpoint)
add_resource(api, PlantEndpoint)
add_resource(api, PlantPhotoEndpoint)
