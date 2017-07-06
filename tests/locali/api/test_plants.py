# -*- coding: utf-8 -*-
"""
    tests.locali.api.test_plants
    ~~~~~~~~~~~~~~~~
    test REST Plants api
"""

import pytest
import json


@pytest.mark.functional
def test_plants_list_get(client, sample_data):
    resp = json.loads(client.get("/plants/").get_data())
    assert resp
    assert len(resp) == 5
    assert set(resp[0].keys()) == {"name"}


@pytest.mark.functional
def test_plant_get(client, sample_data):
    resp = json.loads(client.get("/plants/acacia").get_data())
    assert resp
    assert resp["primary_name"] == "acacia"
