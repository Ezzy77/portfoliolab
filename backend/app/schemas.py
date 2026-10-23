
from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class PositionInput(BaseModel):
    symbol: str = Field(min_length=1, max_length=10)
    quantity: Decimal = Field(gt=0)
    current_price: Decimal = Field(gt=0)

    @model_validator(mode="after")
    def normalize_symbol(self):
        self.symbol = self.symbol.strip().upper()

        if not self.symbol:
            raise ValueError("Symbol cannot be empty")

        return self


class PortfolioValuationRequest(BaseModel):
    positions: list[PositionInput] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_unique_symbols(self):
        symbols = [position.symbol for position in self.positions]

        if len(symbols) != len(set(symbols)):
            raise ValueError("Duplicate symbols are not allowed")

        return self


class PositionValuation(BaseModel):
    symbol: str
    quantity: Decimal
    current_price: Decimal
    market_value: Decimal
    weight: Decimal


class PortfolioValuationResponse(BaseModel):
    positions: list[PositionValuation]
    total_value: Decimal

class PortfolioValuationResponse(BaseModel):
    positions: list[PositionValuation]
    total_value: Decimal
    concentration: Decimal