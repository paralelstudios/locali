# -*- coding: utf-8 -*-
"""
    locali.api.places
    ~~~~~~~~~~~~~~~~
    Plant Quizes API resources
"""
from flask_restful import abort, Resource, Api
from flask import Blueprint, request, current_app
from flask_cors import CORS
from flask_jwt import jwt_required
from ..services import places as _places
from .base import add_resource, SchemaEndpoint
from ..helpers import is_allowed_file, ALLOWED_EXTENSIONS
from ..core import s3


bp = Blueprint('places', __name__, url_prefix='/api/places')
CORS(bp)
api = Api(bp)


class PlacesEndpoint(SchemaEndpoint):
    uri = ''
    schema = {
        "type": "object",
        "title": "place",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "superplace": {"type": "string"}
        },
        "required": ["name", "description"]
    }

    def get(self):
        places = _places.get_root_places_query()
        res = [
            {"name": p.name, "description": p.description}
            for p in places]

        if not res:
            abort(404, description="There don't seem to be any place categories, hmmm")

        return res

    def _process_file(self, f, place):
        name, content = f
        if not is_allowed_file(content.filename):
            abort(400,
                  description='Please only submit {} files'.format(
                      ALLOWED_EXTENSIONS))
        key = 'places/{place_id}/{file_name}'.format(
            place_id=place.id, file_name=content.filename.replace(' ', '-'))
        file_name = 'https://s3.amazonaws.com/{bucket}/{key}'.format(
            bucket=current_app.config['LOCALI_PHOTO_UPLOAD_BUCKET'],
            key=key)
        if not place.image_urls or (place.image_urls and file_name not in place.image_urls):
            s3.Object(
                current_app.config['LOCALI_PHOTO_UPLOAD_BUCKET'],
                key).put(Body=content.stream, ACL='public-read')
        return file_name

    def _enrich_superplace(self, superplace_name, place):
        superplace = _places.first(name=superplace_name, with_for_update=True)
        if not superplace:
            abort(400,
                  description="The place, {},  must exist before the another place, {}, can be inside of it!".format(superplace_name, place.name))
        if superplace.subplaces:
            superplace.subplaces.append(place)
        else:
            superplace.subplaces = [place]

    @jwt_required()
    def post(self):
        self.validate_form(request.form)

        if _places.first(name=request.form['name']):
            abort(400, description="{} already exists!".format(request.form['name']))

        place = _places.new(
            name=request.form['name'],
            description=request.form['description'])

        superplace_name = request.form.get('superplace')
        if superplace_name:
            self._enrich_superplace(superplace_name, place)

        # gonna want to put this into a celery task
        for f in request.files.items():
            file_name = self._process_file(f, place)
            if place.image_urls:
                place.image_urls.append(file_name)
            else:
                place.image_urls = [file_name]

        _places.save(place)

        return 201


class PlaceNamesEndpoint(Resource):
    uri = '/names'

    def get(self):
        places = _places.get_query_with_cols("name").order_by("name")
        res = [dict(name=p.name) for p in places]

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


add_resource(api, PlacesEndpoint)
add_resource(api, PlaceEndpoint)
add_resource(api, PlaceNamesEndpoint)
