# -*- coding: utf-8 -*-
"""
    tests.locali.test_core
    ~~~~~~~~~~~~~~~~
    Tests MatcheME Api core
"""

import pytest


@pytest.mark.functional
def test_ping(client, session):
    resp = client.get("/_ping")
    assert resp.status_code == 200
