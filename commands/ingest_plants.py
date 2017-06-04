# -*- coding: utf-8 -*-
from locali.core import db
from locali.models import Plant
from flask_script import Command, Option
import csv
from unidecode import unidecode


class IngestPlants(Command):
    """From a CSV ingest some plants"""

    option_list = (
        Option('--filename', '-f', dest='filename', help='an csv file path'),
        Option('--cols', '-c', nargs='+', dest='columns',
               default=['name', 'image_url']))

    def _isunique(self, row):
        return Plant.query.filter_by(primary_name=row["name"]).first() is None

    def _shape(self, row):
        return {"primary_name": unidecode(row["name"]), "image_urls": [row["image_url"]]}

    def run(self, filename, columns):
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile, columns)
            plants = map(self._shape, filter(self._isunique, list(reader)))

        db.session.bulk_insert_mappings(Plant, plants)
        db.session.commit()
        print("created {} items".format(len(list(plants))))
