# -*- coding: utf-8 -*-
"""
locali.places.models
~~~~~~~~
Locali Place models
"""
from ..core import db
from ..helpers import Dictable
from sqlalchemy import ForeignKey


class PlaceCategory(db.Model, Dictable):
    __tablename__ = 'place_categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    description = db.Column(db.String, nullable=False)
    places = db.relationship('Place', backref='place_category')
    banner_url = db.Column(db.String)
    icon_url = db.Column(db.String)


class Place(db.Model, Dictable):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    category_id = db.Column(db.Integer, ForeignKey("place_categories.id"))
    primary_image = db.Column(db.String)
    image_urls = db.Column(db.String)
    description = db.Column(db.String)
    seasons_description = db.Column(db.String)
