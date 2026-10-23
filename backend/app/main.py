from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import model_validator

from backend.app.schemas import PortfolioValuationRequest, PortfolioValuationResponse
from backend.app.services.valuation import (
    calculate_portfolio_value,
    calculate_position_value
)

app = FastAPI(
    title="Portfolio Valuation API", 
    description="An API for calculating the value of financial portfolios based on positions and current market prices.",
    version="1.0.0"
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/v1/portfolio/valuation", response_model=PortfolioValuationResponse, tags=["Portfolio Valuation"])
def portfolio_valuation(request: PortfolioValuationRequest) -> PortfolioValuationResponse:
    """
    Calculate the valuation of a financial portfolio.

    Args:
        request (PortfolioValuationRequest): The request containing the portfolio information.

    Returns:
        PortfolioValuationResponse: The valuation response for the portfolio.
    """
    positions = [
        position.model_dump() for position in request.positions
    ]

    total_value = calculate_portfolio_value(positions)

    valued_positions = []
    for position in positions:
        market_value = calculate_position_value(position['quantity'], position['current_price'])

        weight = market_value / total_value
        valued_positions.append({
            "symbol": position["symbol"],
            "quantity": position["quantity"],
            "current_price": position["current_price"],
            "market_value": market_value,
            "weight": weight
            })
    return PortfolioValuationResponse(total_value=total_value, positions=valued_positions)
