# -*- coding: utf-8 -*-
"""
    tests.locali.api.test_places
    ~~~~~~~~~~~~~~~~
    test REST Places api
"""

import pytest
import json


@pytest.mark.functional
def test_place_categories_list_get(client, sample_data):
    resp = json.loads(client.get("/api/places").get_data())
    assert resp
    assert len(resp) == 2
    assert set(resp[0].keys()) == {"name", "description"}


@pytest.mark.functional
def test_places_super_get(client, sample_data):
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
