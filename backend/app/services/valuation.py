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