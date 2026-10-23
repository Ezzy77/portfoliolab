
from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_portfolio_valuation():
    response = client.post(
        "/api/v1/portfolio/valuation",
        json={
            "positions": [
                {
                    "symbol": "aapl",
                    "quantity": "10",
                    "current_price": "200",
                },
                {
                    "symbol": "MSFT",
                    "quantity": "5",
                    "current_price": "400",
                },
            ]
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert float(data["total_value"]) == 4000.0
    assert len(data["positions"]) == 2

    apple = data["positions"][0]

    assert apple["symbol"] == "AAPL"
    assert float(apple["market_value"]) == 2000.0
    assert float(apple["weight"]) == 0.5


def test_negative_quantity_is_rejected():
    response = client.post(
        "/api/v1/portfolio/valuation",
        json={
            "positions": [
                {
                    "symbol": "AAPL",
                    "quantity": "-10",
                    "current_price": "200",
                }
            ]
        },
    )

    assert response.status_code == 422


def test_duplicate_symbols_are_rejected():
    response = client.post(
        "/api/v1/portfolio/valuation",
        json={
            "positions": [
                {
                    "symbol": "AAPL",
                    "quantity": "10",
                    "current_price": "200",
                },
                {
                    "symbol": "aapl",
                    "quantity": "5",
                    "current_price": "210",
                },
            ]
        },
    )

    assert response.status_code == 422
