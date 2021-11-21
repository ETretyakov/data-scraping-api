from fastapi.testclient import TestClient

from app.core.config import API_V1_PREFIX


def test_limit(client: TestClient):
    url = f"{API_V1_PREFIX}/quotes/search/"
    payload = {"tag": None,
               "offset": 0,
               "limit": 10}

    response = client.post(url, json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["status"]

    quotes = response_data["data"]
    assert len(quotes) == 10


def test_pagination(client: TestClient):
    url = f"{API_V1_PREFIX}/quotes/search/"
    payload = {"tag": None,
               "offset": 0,
               "limit": 30}

    response = client.post(url, json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["status"]

    quotes = response_data["data"]
    assert len(quotes) == 30


def test_offset(client: TestClient):
    url = f"{API_V1_PREFIX}/quotes/search/"
    payload = {"tag": None,
               "offset": 7,
               "limit": 15}

    response = client.post(url, json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["status"]

    quotes = response_data["data"]
    assert len(quotes) == 15


def test_tags(client: TestClient):
    url = f"{API_V1_PREFIX}/quotes/search/"
    payload = {"tag": "thinking",
               "offset": 0,
               "limit": 1}

    response = client.post(url, json=payload)
    assert response.status_code == 200

    response_data = response.json()
    assert response_data["status"]

    quotes = response_data["data"]
    assert len(quotes) == 1
