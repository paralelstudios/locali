# -*- coding: utf-8 -*-
"""
    locali test configuration
    ~~~~~~
"""
import os
import pytest
import csv
from alembic.command import upgrade
from alembic.config import Config
from sqlalchemy.exc import ProgrammingError
from locali.models import Plant, Place, PlaceCategory
from locali.core import db as _db
from locali.api import create_app
from ..helpers import TestFixtureException
from .. import settings


@pytest.yield_fixture(scope="session")
def app():
    app = create_app(settings)
    app_ctx = app.app_context()
    app_ctx.push()

    def teardown():
        app_ctx.pop()

    yield app

    teardown()


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.yield_fixture(scope="session")
def db(app):
    def teardown():
        print("reflecting")
        _db.reflect()
        print("dropping all")
        _db.drop_all()

    def buildup_alembic():
        os.environ["SQLALCHEMY_DATABASE_URI"] = app.config["SQLALCHEMY_DATABASE_URI"]
        config = Config(app.config["ALEMBIC_CONFIG"])
        config.set_main_option("script_location", app.config["ALEMBIC_MIGRATIONS"])
        upgrade(config, 'head')
        try:
            Plant.query.first()
        except ProgrammingError:
            raise TestFixtureException(
                "DB fixture not ready: Users table not built")

    def buildup():
        _db.create_all()

    buildup_alembic()

    yield _db
    print("tearing down db")
    teardown()
    print("done")


@pytest.yield_fixture(scope="function")
def session(db):
    def teardown():
        session.close()
        transaction.rollback()
        connection.close()

    try:
        teardown()
    except:
        pass

    print("starting session")

    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session(options=dict(bind=connection, binds={}))
    db.session = session

    yield session
    print("tearing down session")
    teardown()
    print("done")


@pytest.fixture
def plant_data(quiz):
    return dict(primary_name="test-plant",
                image_urls=["test-url"])


@pytest.fixture
def plant(plant_data):
    return Plant(**plant_data)


@pytest.fixture
def committed_plant(plant, session):
    session.add(plant)
    session.commit()
    return Plant.query.get(plant.id)


def sample_file(app, session, file_name, columns, key, model, create_func):
    path = os.path.join(app.config["BASE_DIR"], "tests/data/{}".format(file_name))
    with open(path) as csvfile:
        reader = csv.DictReader(csvfile, columns)
        items = [
            create_func(model, row)
            for row in reader
            if not model.query.filter_by(**{key: row[key]}).first()]
    for item in items:
        session.add(item)
        session.commit()
    print("ingested {} items for sample set".format(len(items)))


@pytest.fixture()
def sample_place_categories(session, app):
    sample_file(app, session,
                "sample_place_categories.csv",
                ["name", "description"],
                "name", PlaceCategory,
                lambda model, row: model(**row))


@pytest.fixture()
def sample_places(session, app, sample_place_categories):
    def make_place(model, row):
        category = PlaceCategory.query.filter_by(name=row["category"]).first()
        m = model(name=row['name'], description=row['description'],
                  primary_image=row["primary_image"],
                  category_id=category.id)
        category.places.append(m)
        return m

    sample_file(app, session,
                "sample_places.csv",
                ["name", "description", "category", "primary_image"],
                "name", Place,
                make_place)


@pytest.fixture()
def sample_plants(session, app, sample_places):
    def make_plant(model, row):
        place_names = row["places"].split(',')
        months = [int(x) for x in row["months_available"].split(',')]
        places = Place.query.filter(Place.name.in_(place_names)).all()
        return model(primary_name=row["primary_name"],
                     image_urls=[row["image_url"]],
                     months_available=months,
                     places=places)

    sample_file(app, session,
                "sample_plants.csv",
                ["primary_name", "image_url", "places", "months_available"],
                "primary_name", Plant,
                make_plant)


@pytest.fixture()
def sample_data(sample_plants):
    pass
