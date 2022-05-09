from pytest import fixture
from fastapi.testclient import TestClient

from powerplant.app import app


@fixture
def test_client():
    return TestClient(app)


def test_incomplete_submission_should_return_422(test_client):
    response = test_client.post("/solve", json={
        "load": 480,
        "fuels": {
            "gas(euro/MWh)": 13.4,
        }
    })
    assert response.status_code == 422


def test_impossible_problem_should_return_400(test_client):
    response = test_client.post("/solve", json={
        "load": 480,
        "fuels": {
            "gas(euro/MWh)": 13.4,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 460
            }
        ]
    })
    assert response.status_code == 400


def test_return_solution(test_client):
    response = test_client.post("/solve", json={
        "load": 300,
        "fuels": {
            "gas(euro/MWh)": 13.4,
        },
        "powerplants": [
            {
                "name": "gasfiredbig1",
                "type": "gasfired",
                "efficiency": 0.53,
                "pmin": 100,
                "pmax": 400
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == [
        {
            "name": "gasfiredbig1",
            "p": 300
        }
    ]
