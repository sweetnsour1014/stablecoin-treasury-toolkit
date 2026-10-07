import json
#imports the json library for working with JSON data
import requests

url = "https://stablecoins.llama.fi/stablecoins"
response = requests.get(url, params={"includePrices": "true"}, timeout=30)
#makes a GET request to the specified URL with query parameters and a timeout of 30 seconds
data = response.json()
#parses the JSON response into a Python dictionary

first_coin = data["peggedAssets"][0]
#retrieves the first stablecoin from the "peggedAssets" list in the JSON response
print(json.dumps(first_coin, indent=2)[:3000])
#prints the first 3000 characters of the first stablecoin's data in a pretty JSON format

print(list(first_coin.keys()))
#prints the keys of the first stablecoin's data to understand the structure and available attributes
print(first_coin["price"])
#prints the price of the first stablecoin to check its current value