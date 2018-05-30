import os
import tempfile
import json
import pytest

from app import app


@pytest.fixture
def client():
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    # with app.app_context():
    #     app.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])

# Test Getting /


def test_home(client):
    """Should be an html document"""
    rv = client.get('/')
    assert 200 == rv.status_code


# def test_restart_api(client):
#     res = client.put('/restart')
#     assert 200 == res.status_code
#     print(res.data)


# def test_pig_in_data_api(client):
#     res = client.put('/restart')
#     assert b'Pig' in res.data


# def test_location_in_data_api(client):
#     res = client.put('/restart')
#     json_data = json.loads(res.data)
#     assert 'location' in json_data


# def test_text_in_data_api(client):
#     res = client.put('/restart')
#     json_data = json.loads(res.data)
#     assert 'text' in json_data
