import pytest
from fastapi.testclient import TestClient


def test_get_faculties(test_client: TestClient):
    # Test the GET /faculties endpoint
    response = test_client.get("/api/v1/faculties")

    # Check if the response is successful
    assert response.status_code == 200

    # Check if the response contains the expected data structure
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data

    # Check if there are faculties in the response
    assert len(data["items"]) > 0

    # Check if each faculty has the expected fields
    for faculty in data["items"]:
        assert "id" in faculty
        assert "long_name" in faculty
        assert "short_name" in faculty
        assert "active" in faculty

        # Check if all faculties are active (as per the router implementation)
        assert faculty["active"] is True


def test_get_faculties_with_pagination(test_client: TestClient):
    # Test the GET /faculties endpoint with pagination parameters
    limit = 2
    offset = 1
    response = test_client.get(f"/api/v1/faculties?limit={limit}&offset={offset}")

    # Check if the response is successful
    assert response.status_code == 200

    # Check if pagination parameters are respected
    data = response.json()
    assert data["limit"] == limit
    assert data["offset"] == offset

    # Check if the number of items is less than or equal to the limit
    assert len(data["items"]) <= limit