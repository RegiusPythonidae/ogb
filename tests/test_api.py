import pytest

from app import create_app

URL = "/word_tags"


@pytest.fixture
def client():
    app = create_app()
    with app.test_client() as client:
        yield client


@pytest.mark.parametrize("palindrome", [
    (0, True),
    (1, True),
    (202020202, False)
])
def test_word_get(client, word_id, result):
    response = client.get(f"{URL}/{word_id}")
    data = response.json
    assert data == result