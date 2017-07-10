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
    resp = json.loads(client.get("/places/categories").get_data())
    assert resp
    assert len(resp) == 2
    assert set(resp[0].keys()) == {"name", "description", "id"}


@pytest.mark.functional
def test_places_list_get(client, sample_data):
    resp = json.loads(client.get("/places/category/urban").get_data())
    assert resp
    assert len(resp) == 1
    assert resp[0]["name"] == "city"
    assert resp[0]["description"] == "dirty cesspool where only the hardiest survive"


@pytest.mark.functional
def test_place_get(client, sample_data):
    resp = json.loads(client.get("/places/rain_forest").get_data())
    assert resp
    assert resp["name"] == "rain forest"
    assert resp["description"] == "magical place of dark green"
    assert resp["plants"]
