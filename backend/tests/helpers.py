# -*- coding: utf-8 -*-
"""
    tests.helpers
    ~~~~~~~~~~~~~~~~~~~~~
    test utility functions
"""
from locali.helpers import LocaliJSONEncoder
import json


class TestFixtureException(Exception):
    pass


def assert_equal_keys(d1, d2, *keys):
    for k in keys:
        assert d1[k] == d2[k]
    return True


def assert_inequal_keys(d1, d2, *keys):
    for k in keys:
        assert d1[k] != d2[k]
    return True


def jsonify_req(data):
    return dict(data=json.dumps(data, cls=LocaliJSONEncoder),
                content_type='application/json')
