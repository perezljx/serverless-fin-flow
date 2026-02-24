import os
import requests

# Retrieve API Key from your environment
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    print("API Key not found")
    exit()

# Ask user which stock symbol to check
symbol = input("Enter a symbol: ") #e.g. APPL for Apple

# Define the base API URL
base_url = "https://www.alphavantage.co/query"

params = {"function":"GLOBAL_QUOTE", # Tells API we want the latest price
          "symbol":symbol, # The stock symbol user typed
          "apikey":API_KEY # Your API Key from environment
          }

# Send the request to the API
r = requests.get(base_url, params=params)

# Convert the response to JSON
data = r.json()

# Print the full data returned from the API
print(data)