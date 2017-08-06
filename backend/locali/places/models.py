
# -*- coding: utf-8 -*-
"""
locali.places.models
~~~~~~~~
Locali Place models
"""
from uuid import uuid4
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from ..core import db
from ..helpers import Dictable
from sqlalchemy import ForeignKey


class Place(db.Model, Dictable):
    __tablename__ = 'places'
    id = db.Column(UUID, primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String, nullable=False, unique=True, index=True)
    image_urls = db.Column(ARRAY(db.String))
    description = db.Column(db.String)
    superplace_id = db.Column(UUID, ForeignKey("places.id"))
    subplaces = db.relationship("Place")
