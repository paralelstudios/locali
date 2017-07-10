# -*- coding: utf-8 -*-
"""

matcheme.plants.models
~~~~~~~~

"""
from sqlalchemy import ForeignKey
from ..core import db
from ..helpers import Dictable
from sqlalchemy.dialects.postgresql import ARRAY

plant_place_table = db.Table('plant_place',
                             db.Column('plant_id', db.Integer,
                                       ForeignKey('plants.id')),
                             db.Column('place_id', db.Integer,
                                       ForeignKey('places.id')))


class Plant(db.Model, Dictable):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    primary_name = db.Column(db.String, unique=True, index=True, nullable=False)
    scientific_name = db.Column(db.String)
    image_urls = db.Column(ARRAY(db.String), nullable=False)
    location_description = db.Column(db.String)
    places = db.relationship(
        "Place", secondary=plant_place_table,
        backref="plants")
    season_description = db.Column(db.String)
    months_available = db.Column(ARRAY(db.Integer))
    harvest_description = db.Column(db.String)
    taste_description = db.Column(db.String)
    smell_description = db.Column(db.String)
    uses_description = db.Column(db.String)
    prep_description = db.Column(db.String)
    storage_description = db.Column(db.String)
