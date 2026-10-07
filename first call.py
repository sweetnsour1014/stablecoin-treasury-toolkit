import requests
#imports the requests library for making HTTP requests

url = "https://stablecoins.llama.fi/stablecoins"
response = requests.get(url, params = {"includePrices": "true"}, timeout = 30)
#makes a GET request to the specified URL with query parameters and a timeout of 30 seconds
print("Status code:", response.status_code)
#prints the HTTP status code of the response to check if the request was successful (200 OK)

data = response.json()
print("Top-level keys:", list(data.keys()))
print("Number of stablecoins:", len(data["peggedAssets"]))
#prints the top-level keys of the JSON response and the number of stablecoins in the "peggedAssets" list