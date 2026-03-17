import os
import requests

def simulate_real_investment(time_series, monthly_investment, years_requested):
    # Sort dates from oldest to newest (YYYY-MM-DD strings sort correctly)
    dates = sorted(time_series.keys())

    # Ensure we don't try to simulate more data than we actually have
    months_available = len(dates)
    months_to_simulate = min(years_requested * 12, months_available)
    
    dates = dates[-months_to_simulate:]

    total_shares = 0
    total_invested = 0
    yearly_data = []

    for i, date in enumerate(dates, start=1):
        # Using .get() prevents a KeyError if the API field name is slightly different
        price_data = time_series[date]
        price = float(price_data.get("5. adjusted close") or price_data.get("4. close"))

        shares_bought = monthly_investment / price
        total_shares += shares_bought
        total_invested += monthly_investment

        if i % 12 == 0:
            yearly_data.append({
                "year": i // 12,
                "portfolio_value": total_shares * price,
                "total_invested": total_invested
            })

    final_price = float(time_series[dates[-1]].get("5. adjusted close") or time_series[dates[-1]].get("4. close"))
    final_value = total_shares * final_price

    return {
        "total_invested": total_invested,
        "final_value": final_value,
        "total_shares": total_shares,
        "years_simulated": months_to_simulate / 12,
        "yearly_data": yearly_data
    }

# Quick test block (only runs if you execute this file directly)
if __name__ == "__main__":

    API_KEY = os.getenv("API_KEY")

    symbol = input("Enter stock symbol: ")
    monthly_investment = float(input("Enter monthly investment amount: "))
    years = int(input("Enter number of years: "))

    base_url = "https://www.alphavantage.co/query"

    # Get historical data
    history_params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": symbol,
        "apikey": API_KEY
    }

    response = requests.get(base_url, params=history_params)
    data = response.json()

    time_series = data.get("Monthly Adjusted Time Series")

    if not time_series:
        print("Failed to retrieve data.")
        exit()

    # Run real investment simulation
    results = simulate_real_investment(
        time_series,
        monthly_investment,
        years
    )

    # Calculate total growth (add this since function doesn’t return it)
    total_growth = results["final_value"] - results["total_invested"]

    # Display results
    print("\n--- Simulation Results ---")
    print(f"Total Invested: ${results['total_invested']:.2f}")
    print(f"Final Portfolio Value: ${results['final_value']:.2f}")
    print(f"Total Growth: ${total_growth:.2f}")
    print(f"Total Shares Owned: {results['total_shares']:.4f}")