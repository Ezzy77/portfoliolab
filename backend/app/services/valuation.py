from decimal import Decimal
from turtle import position

def calculate_position_value(quantity: Decimal, current_price: Decimal) -> Decimal:
    """
    Calculate the value of a position based on its quantity and price.

    Args:
        quantity (Decimal): The quantity of the position.
        current_price (Decimal): The current price of the position.

    Returns:
        Decimal: The total value of the position.
    """
    return quantity * current_price

def calculate_portfolio_value(positions: list[dict]) -> Decimal:
    """
    Calculate the total value of a portfolio based on its positions.

    Args:
        positions (list): A list of position dictionaries.

    Returns:
        Decimal: The total value of the portfolio.
    """
    total= Decimal(0)
    for position in positions:
        total += calculate_position_value(position['quantity'], position['current_price'])
    return total


def calculate_portfolio_concentration(positions: list[dict]) -> Decimal:
    """
    Calculate the concentration of a portfolio based on its positions.

    Args:
        positions (list): A list of position dictionaries.

    Returns:
        Decimal: The Herfindahl-Hirschman Index (HHI) representing the concentration of the portfolio.
    """
    if not positions:
        return Decimal(0)
    total_value = calculate_portfolio_value(positions)
    if total_value == 0:
        return Decimal(0)
    hhi = Decimal(0)

    for position in positions:
        market_value = calculate_position_value(position['quantity'], position['current_price'])
        weight = market_value / total_value
        hhi += weight ** 2
    return hhi   