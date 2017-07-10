# -*- coding: utf-8 -*-
"""
    tests.locali.api.test_seasons
    ~~~~~~~~~~~~~~~~
    test REST seasons api
"""

import pytest
import json
from locali.services import plants


@pytest.mark.functional
def test_season_get(client, sample_data):
    resp = json.loads(client.get("/season/4").get_data())
    assert len(resp) == 3
    assert "pitahaya" in {x["name"] for x in resp}

    resp = client.get("/season")
    data = json.loads(resp.get_data())
    plants_in_season = plants.get_plants_in_season_query().all()
    assert {x["name"] for x in data} == {x.primary_name for x in plants_in_season}
    assert resp.status_code == 200
