import json

from fastapi.testclient import TestClient

from app.main import app

client_test = TestClient(app)

test_data = {
    "2020-10-10": [
        {"cargo_type": "Glass", "rate": 0.01},
        {"cargo_type": "Other", "rate": 0.02},
    ],
    "2020-10-12": [
        {"cargo_type": "Glass", "rate": 0.01},
        {"cargo_type": "Other", "rate": 0.02},
    ],
}


def test_add_prices():
    response = client_test.post("/prices", json=test_data)
    assert response.status_code == 200, response.text
    assert response.json() == test_data


def test_add_prices_that_alredy_exist():
    response = client_test.post("/prices", json=test_data)
    assert response.status_code == 422, response.text


def test_get_prices():
    response = client_test.get("/prices")
    assert response.status_code == 200
    assert len(response.json()) == 4


def test_price_by_correct_date():
    response = client_test.get("/prices/2020-10-10")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_price_by_incorrect_date():
    response = client_test.get("/prices/9999-99-99")
    assert response.status_code == 422


def test_price_by_date_and_type():
    response = client_test.get("/prices/2020-10-10?cargo_type=Glass")
    assert response.status_code == 200
    assert type(response.json()) == dict
    assert response.json()["rate"] == 0.01


def test_insurance_calculation_incorrect_date():
    response = client_test.get(
        "/insurance?declared_value=100000&cargo_type=Glass&date=2021-10-10"
    )
    assert response.status_code == 200
    assert response.json() == "For date 2021-10-10 there is no tariff for type Glass"


def test_insurance_calculation_incorrect_values():
    response = client_test.get(
        "/insurance?declared_value=sss&cargo_type=132&date=11111-10-10"
    )
    assert response.status_code == 422


def test_insurance_calculation_correct_date():
    declared_value = 100000
    cargo_type = "Glass"
    date = "2020-10-10"
    rate_response = client_test.get("/prices/2020-10-10?cargo_type=Glass")
    rate = rate_response.json()["rate"]
    response = client_test.get(
        f"/insurance?declared_value={declared_value}&cargo_type={cargo_type}&date={date}"
    )
    insurance_cost = rate * declared_value
    assert response.status_code == 200
    assert response.json()["insurance_cost"] == insurance_cost
