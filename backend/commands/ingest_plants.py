# -*- coding: utf-8 -*-
from locali.core import db
from locali.models import Plant, Place, PlaceCategory
from flask_script import Command, Option
import csv


def make_plant(row):
    place_names = row["places"].split(',')
    months = [int(x) for x in row["months_available"].split(',')]
    places = Place.query.filter(Place.name.in_(place_names)).all()
    return dict(primary_name=row["primary_name"],
                image_urls=[row["image_url"]],
                months_available=months,
                places=places)


def post_plant(plant):
    p = Plant.query.filter_by(primary_name=plant["primary_name"]).first()
    p.places = plant["places"]


def make_place(row):
    category = PlaceCategory.query.filter_by(name=row["category"]).first()
    m = dict(name=row['name'], description=row['description'],
             category_id=category.id)
    return m


class Ingest(Command):
    """From a CSV ingest some plants"""
    MODELS = {
        'plants': {
            "cols": ["primary_name", "image_url", "places", "months_available"],
            "key": "primary_name",
            "class": Plant,
            "make": make_plant,
            "post": post_plant
        },
        'places': {
            "cols": ["name", "description", "category"],
            "key": "name",
            "class": Place,
            "make": make_place
        },
        'categories': {
            "cols": ["name", "description"],
            "key": "name",
            "class": PlaceCategory,
            "make": lambda x: x
        }
    }

    option_list = (
        Option('--filename', '-f', dest='filename', help='an csv file path'),
        Option('--model', '-m', dest='model_name'))

    def _isunique(self, row):
        return self.model["class"].query.filter_by(
            **{self.model["key"]: row[self.model["key"]]}).first() is None

    def run(self, filename, model_name):
        self.model = self.MODELS[model_name]
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, self.model["cols"])
            models = list(map(self.model["make"], filter(self._isunique, list(reader))))

        db.session.bulk_insert_mappings(self.model["class"], models)
        db.session.commit()

        if self.model.get("post"):
            [self.model["post"](model) for model in models]
            db.session.commit()
        print("created {} items".format(len(models)))
