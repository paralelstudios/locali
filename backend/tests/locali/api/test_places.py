# -*- coding: utf-8 -*-
"""
    tests.locali.api.test_places
    ~~~~~~~~~~~~~~~~
    test REST Places api
"""
import boto3
from moto import mock_s3
from locali.services import places
import pytest
import json
from io import BytesIO


@pytest.mark.functional
def test_place_categories_list_get(client, sample_data):
    resp = json.loads(client.get("/api/places").get_data())
    assert resp
    assert len(resp) == 2
    assert set(resp[0].keys()) == {"name", "description"}


@pytest.mark.functional
@mock_s3
def test_place_post(client, auth_key, app, sample_data):
    conn = boto3.resource('s3', region_name='us-east-1')
    conn.create_bucket(Bucket=app.config['LOCALI_PHOTO_UPLOAD_BUCKET'])

    req = dict(
        name="testPlace",
        photo1=((BytesIO(b'some foto')), 'photo.png'),
        description="test description"
    )

    resp = client.post("/api/places", headers=auth_key,
                       content_type='multipart/form-data', data=req)
    place = places.first(name="testPlace")
    assert place
    assert not place.superplace_id
    body = conn.Object(app.config['LOCALI_PHOTO_UPLOAD_BUCKET'],
                       'places/{}/photo.png'.format(place.id)).get()['Body'].read().decode('utf-8')
    assert body == 'some foto'
    assert resp.status_code == 200

    # test auth
    req = dict(
        name="testPlace2",
        photo1=((BytesIO(b'some foto')), 'photo.png'),
        description="test description"
    )

    resp = client.post("/api/places",
                       content_type='multipart/form-data', data=req)
    assert resp.status_code == 401

    # test dup foto
    req = dict(
        name="testPlace2",
        photo1=((BytesIO(b'some foto')), 'photo.png'),
        photo2=((BytesIO(b'some foto')), 'photo.png'),
        description="test description"
    )

    resp = client.post("/api/places", headers=auth_key,
                       content_type='multipart/form-data', data=req)
    place = places.first(name="testPlace")
    assert place
    assert not place.superplace_id
    body = conn.Object(app.config['LOCALI_PHOTO_UPLOAD_BUCKET'],
                       'places/{}/photo.png'.format(place.id)).get()['Body'].read().decode('utf-8')
    assert body == 'some foto'
    assert len(place.image_urls) == 1
    assert resp.status_code == 200

    # test bad file
    req = dict(
        name="testPlace3",
        photo1=((BytesIO(b'some foto')), 'photo.whatever'),
        description="test description"
    )

    resp = client.post("/api/places", headers=auth_key,
                       content_type='multipart/form-data', data=req)
    assert resp.status_code == 400


@pytest.mark.functional
def test_places_super_get(client, sample_data, app):
    resp = json.loads(client.get("/api/places/urban").get_data())
    assert resp
    assert resp["name"] == "urban"
    assert resp["description"] == "great metropolis of consumption"
    assert resp["subplaces"]


@pytest.mark.functional
def test_place_get(client, sample_data):
    resp = json.loads(client.get("/api/places/rain_forest").get_data())
    assert resp
    assert resp["name"] == "rain forest"
    assert resp["description"] == "magical place of dark green"
    assert resp["plants"]
