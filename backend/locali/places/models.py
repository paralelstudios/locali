# -*- coding: utf-8 -*-
"""
locali.places.models
~~~~~~~~
Locali Place models
"""
from ..core import db
from ..helpers import Dictable
from sqlalchemy import ForeignKey


class Place(db.Model, Dictable):
    __tablename__ = 'places'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    primary_image = db.Column(db.String)
    description = db.Column(db.String)
    superplace_id = db.Column(db.Integer, ForeignKey("places.id"))
    subplaces = db.relationship("Place")
