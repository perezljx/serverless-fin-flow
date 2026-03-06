import os
from fetch_price import get_historical_annual_return
from growth_engine import simulate_growth


def run_simulation(symbol, monthly_investment, years, history_years=10):
    """
    Main financial simulation pipeline.

    1. Pull historical return for stock
    2. Run compound growth simulation
    3. Return structured result (API-ready)
    """

    api_key = os.getenv("API_KEY")

    if not api_key:
        return {"error": "API key not found"}

    # Step 1: Get historical annual return
    annual_return = get_historical_annual_return(
        symbol,
        api_key,
        years=history_years
    )

    if annual_return is None:
        return {"error": "Could not retrieve historical return"}

    # Step 2: Run growth simulation
    simulation = simulate_growth(
        monthly_investment,
        annual_return,
        years
    )

    # Step 3: Combine results
    return {
        "symbol": symbol.upper(),
        "historical_annual_return_percent": annual_return,
        "investment_years": years,
        "monthly_investment": monthly_investment,
        "results": simulation
    }


# Temporary test runner (will remove when we go web/cloud)
if __name__ == "__main__":
    result = run_simulation("AAPL", 500, 20)
    print(result)