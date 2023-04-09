import logging

import pytest

from app import create_app

URL = "/api/word_tags"


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("word_id, result", [
    (0, 404),
    (1, 200),
    (202020202, 404)
])
def test_word_get(client, word_id, result):
    path = f"{URL}/{word_id}"
    response = client.get(path)

    assert response.status_code == result