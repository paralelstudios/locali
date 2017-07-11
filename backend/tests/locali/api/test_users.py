# -*- coding: utf-8 -*-
"""
    tests.api.resources.test_users
    ~~~~~~~~~~~~~~~~
    Tests Users API resources
"""
from toolz import dissoc
import pytest
from locali.models import User
from tests.helpers import jsonify_req, assert_equal_keys
import json


@pytest.mark.functional
def test_user_post(client, session):
    user_data = {
        "password": "password",
        "email": "email"}
    data = jsonify_req(user_data)
    resp = client.post('/users', **data)
    r_data = json.loads(resp.get_data())
    assert resp.status_code == 201
    assert "user_id" in r_data
    user_id = r_data["user_id"]
    user = User.query.get(user_id)
    assert user
    assert assert_equal_keys(user_data, user.as_dict(),
                             *dissoc(user_data, "password").keys())

    # test duplicate post
    resp = client.post('/users', **data)
    assert resp.status_code == 409

    # test post without reqs
    resp = client.post('/users', **jsonify_req(dict(email="foff@foff.gmail.com")))
    assert resp.json == {'message': ": 'password' is a required property"}
