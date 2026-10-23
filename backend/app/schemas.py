from decimal import Decimal
from pydantic import BaseModel, Field, model_validator


class PositionInput(BaseModel):
    """
    Schema for input data representing a financial position.
    """
    symbol: str = Field(min_length=1, max_length=10, description="The symbol of the financial instrument.")
    quantity: Decimal = Field(gt=0, description="The quantity of the position.")
    current_price: Decimal = Field(gt=0, description="The current price of the position.")

    @model_validator(mode='after')
    def normalize_symbol(self):
        """
        Normalize the symbol to uppercase.
        """
        self.symbol = self.symbol.strip().upper()

        if not self.symbol:
            raise ValueError("Symbol cannot be empty")
        return self

    @model_validator(mode='before')
    def validate_fields(cls, values):
        """
        Validate that quantity and price are non-negative.

        Args:
            values (dict): The input values to validate.

        Returns:
            dict: The validated values.
        """
        quantity = values.get('quantity')
        price = values.get('price')

        if quantity is not None and quantity < 0:
            raise ValueError("Quantity must be a non-negative number.")

        if price is not None and price < 0:
            raise ValueError("Price must be a non-negative number.")

        return values

class PortfolioValuationRequest(BaseModel):
    """
    Schema for input data representing a portfolio valuation request.
    """
    positions: list[PositionInput] = Field(min_length=1, description="A list of financial positions to be valued.")

    @model_validator(mode='after')
    def validate_unique_symbols(self):
        """
        Validate that all symbols in the positions are unique.

        Raises:
            ValueError: If duplicate symbols are found.
        """
        symbols = [position.symbol for position in self.positions]
        if len(symbols) != len(set(symbols)):
            raise ValueError("Duplicate symbols found in positions.")
        return self

class PositionValuation(BaseModel):
    """
    Schema for output data representing a position valuation.
    """
    symbol: str = Field(min_length=1, max_length=10, description="The symbol of the financial instrument.")
    quantity: Decimal = Field(gt=0, description="The quantity of the position.")
    current_price: Decimal = Field(gt=0, description="The current price of the position.")
    value: Decimal = Field(gt=0, description="The total value of the position.")

class PortfolioValuationResponse(BaseModel):
    """
    Schema for output data representing a portfolio valuation response.
    """
    positions: list[PositionValuation] = Field(min_length=1, description="A list of financial positions in the portfolio.")
    total_value: Decimal = Field(gt=0, description="The total value of the portfolio.")
