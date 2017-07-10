# -*- coding: utf-8 -*-
"""
    tests.locali.api.test_quizzes
    ~~~~~~~~~~~~~~~~
    test REST Quiz api
"""

import pytest
import json


@pytest.mark.functional
def test_quiz_items_get(client, sample_data):
    resp = json.loads(client.get("/quizzes/plants").get_data())
    assert resp
    assert len(resp) == 5
    assert set(resp[0].keys()) == {"name", "image_url"}
