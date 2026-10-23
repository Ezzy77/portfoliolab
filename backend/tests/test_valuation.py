
from decimal import Decimal

from backend.app.services.valuation import (
    calculate_position_value,
    calculate_portfolio_value,
)


def test_calculate_position_value():
    result = calculate_position_value(
        Decimal("10"),
        Decimal("200"),
    )

    assert result == Decimal("2000")


def test_calculate_portfolio_value():
    positions = [
        {
            "symbol": "AAPL",
            "quantity": Decimal("10"),
            "current_price": Decimal("200"),
        },
        {
            "symbol": "MSFT",
            "quantity": Decimal("5"),
            "current_price": Decimal("400"),
        },
    ]

    result = calculate_portfolio_value(positions)

    assert result == Decimal("4000")


def test_empty_portfolio_has_zero_value():
    assert calculate_portfolio_value([]) == Decimal("0")


def test_decimal_arithmetic():
    result = calculate_position_value(
        Decimal("3"),
        Decimal("0.10"),
    )

    assert result == Decimal("0.30")


from decimal import Decimal

from backend.app.services.valuation import (
    calculate_portfolio_concentration,
)


def test_equal_positions_have_expected_concentration():
    positions = [
        {
            "quantity": Decimal("1"),
            "current_price": Decimal("100"),
        },
        {
            "quantity": Decimal("1"),
            "current_price": Decimal("100"),
        },
    ]

    result = calculate_portfolio_concentration(positions)

    assert result == Decimal("0.5")


def test_concentrated_portfolio_has_expected_concentration():
    positions = [
        {
            "quantity": Decimal("7"),
            "current_price": Decimal("1000"),
        },
        {
            "quantity": Decimal("2"),
            "current_price": Decimal("1000"),
        },
        {
            "quantity": Decimal("1"),
            "current_price": Decimal("1000"),
        },
    ]

    result = calculate_portfolio_concentration(positions)

    assert result == Decimal("0.54")


def test_empty_portfolio_has_zero_concentration():
    result = calculate_portfolio_concentration([])

    assert result == Decimal("0")

