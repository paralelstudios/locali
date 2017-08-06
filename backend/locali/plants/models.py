# -*- coding: utf-8 -*-
"""

matcheme.plants.models
~~~~~~~~

"""
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy import ForeignKey
from ..core import db
from ..helpers import Dictable


plant_place_table = db.Table('plant_place',
                             db.Column('plant_id', UUID,
                                       ForeignKey('plants.id')),
                             db.Column('place_id', UUID,
                                       ForeignKey('places.id')))


class Plant(db.Model, Dictable):
    __tablename__ = 'plants'
    id = db.Column(UUID, primary_key=True, default=lambda: str(uuid4()))
    primary_name = db.Column(db.String, unique=True, index=True, nullable=False)
    description = db.Column(db.String, nullable=False)
    common_names = db.Column(ARRAY(db.String))
    scientific_names = db.Column(ARRAY(db.String))
    substrates = db.Column(ARRAY(db.String))
    plant_type = db.Column(db.String)
    seed_image_urls = db.Column(ARRAY(db.String))
    flower_image_urls = db.Column(ARRAY(db.String))
    leaf_image_urls = db.Column(ARRAY(db.String))
    other_image_urls = db.Column(ARRAY(db.String))
    uses = db.Column(ARRAY(db.String))
    places = db.relationship(
        "Place", secondary=plant_place_table,
        backref="plants")
    months_available = db.Column(ARRAY(db.Integer))
