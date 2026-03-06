import os
import requests
import time

# Retrieve API Key from your environment
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("API Key not found")
    exit()

# Ask user which stock symbol to check
symbol = input("Enter a symbol: ") #e.g. APPL for Apple

# Define the base API URL
base_url = "https://www.alphavantage.co/query"

# Retrieve current stock price
params = {"function":"GLOBAL_QUOTE", # Tells API we want the latest price
          "symbol":symbol, # The stock symbol user typed
          "apikey":API_KEY # Your API Key from environment
          }

# Send request to API
price_response = requests.get(base_url, params=params)

# Convert API response into JSON format (dictionary)
price_data = price_response.json()

# Extract quote section
quote = price_data.get("Global Quote")

if not quote:
    print("Could not retrieve current price.")
    exit()

# Convert price string into float
current_price = float(quote["05. price"])

print(f"\nCurrent Price of {symbol}: ${round(current_price, 2)}")
time.sleep(1)

def get_historical_annual_return(symbol, api_key, years=10):

    # Retrieve long-term monthly adjusted data
    # Adjusted data accounts for stock splits and dividends
    history_params = {
        "function": "TIME_SERIES_MONTHLY_ADJUSTED",
        "symbol": symbol,
        "apikey": api_key
    }

    history_response = requests.get(base_url, params=history_params)
    history_data = history_response.json()

    # Extract the time series section
    time_series = history_data.get("Monthly Adjusted Time Series")

    if not time_series:
        print("Could not retrieve historical data.")
        return None

    # Sort dates from oldest to newest
    dates = sorted(time_series.keys())

    # Ensure we have sufficient data
    if len(dates) < years * 12:
        print("Not enough historical data available.")
        return None

    # Find price from 10 years ago and most recent price
    start_date = dates[-(years * 12)]
    end_date = dates[-1]

    start_price = float(time_series[start_date]["5. adjusted close"])
    end_price = float(time_series[end_date]["5. adjusted close"])

    # CAGR formula
    # CAGR (Compound Annual Growth Rate)
    cagr = (end_price / start_price) ** (1 / years) - 1

    # Convert to percentage
    annual_return_percent = round(cagr * 100, 2)

    return annual_return_percent, time_series, dates

# Call the function so script still behaves exactly the same
years = 10  # Calculate 10-year historical return
annual_return_percent, time_series, dates = get_historical_annual_return(symbol, API_KEY, years)

if annual_return_percent is not None:
    print(f"{symbol} {years}-Year Historical Annual Return: {annual_return_percent}%")

# Ask user how much they invest each month
monthly_investment = float(input("\nEnter monthly investment amount: "))

# Track total shares accumulated over time
total_shares = 0

# Loop through each month in the selected 10-year window
for date in dates[-(years * 12):]:

    # Retrieve the adjusted closing price for that month
    monthly_price = float(time_series[date]["5. adjusted close"])

    # Calculate how many shares could be purchased that month
    shares_bought = monthly_investment / monthly_price

    # Add those shares to the running total
    total_shares += shares_bought

# Calculate final portfolio value using today's price
portfolio_value = total_shares * current_price

# Calculate total amount invested over the time period
total_invested = monthly_investment * years * 12

print("\n--- Investment Simulation ---")
print(f"Total Invested: ${round(total_invested,2)}")
print(f"Portfolio Value: ${round(portfolio_value,2)}")
print(f"Total Shares Owned: {round(total_shares,4)}")