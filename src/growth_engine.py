def simulate_growth(monthly_investment, annual_return_percent, years):
    """
    Simulates investment growth using monthly contributions
    and compound interest.

    Returns a dictionary containing:
    - total_invested
    - final_value
    - total_growth
    - yearly_data (for charts later)
    """

    # Convert annual return percent to decimal
    # Example: 8% -> 0.08
    annual_return = annual_return_percent / 100

    # Convert annual return to monthly return
    monthly_return = annual_return / 12

    # Total number of months we will simulate
    total_months = years * 12

    # Track how much money has been invested
    total_invested = 0

    # Track the portfolio value over time
    portfolio_value = 0

    # Store year-by-year results for future charts
    yearly_data = []

    # Loop through each month
    for month in range(1, total_months + 1):

        # Step 1: Add this month's investment
        portfolio_value += monthly_investment
        total_invested += monthly_investment

        # Step 2: Grow the entire portfolio by monthly return
        portfolio_value *= (1 + monthly_return)

        # If we've reached the end of a year, store snapshot
        if month % 12 == 0:
            yearly_data.append({
                "year": month // 12,
                "portfolio_value": round(portfolio_value, 2),
                "total_invested": total_invested
            })

    # Calculate total growth (profit)
    total_growth = portfolio_value - total_invested

    # Return everything in a structured format
    return {
        "total_invested": round(total_invested, 2),
        "final_value": round(portfolio_value, 2),
        "total_growth": round(total_growth, 2),
        "yearly_data": yearly_data
    }


# Quick test block (only runs if you execute this file directly)
if __name__ == "__main__":
    
    # Ask user for inputs
    monthly_investment = float(input("Enter monthly investment amount: "))
    annual_return_percent = float(input("Enter expected annual return (%): "))
    years = int(input("Enter number of years: "))

    # Run simulation
    results = simulate_growth(
        monthly_investment,
        annual_return_percent,
        years
    )

    # Display results cleanly
    print("\n--- Simulation Results ---")
    print(f"Total Invested: ${results['total_invested']}")
    print(f"Final Portfolio Value: ${results['final_value']}")
    print(f"Total Growth: ${results['total_growth']}")