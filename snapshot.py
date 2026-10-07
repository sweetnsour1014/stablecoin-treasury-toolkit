from dbm import error
from datetime import datetime, timezone
from pathlib import Path

import requests
import pandas as pd
#imports pandas library for data manipulation and analysis

url = "https://stablecoins.llama.fi/stablecoins"
retrieved_at = datetime.now(timezone.utc)
retrieved_at_text = retrieved_at.isoformat(timespec="seconds")

try:
    response = requests.get(url, params={"includePrices": "true"}, timeout=30)
    #makes a GET request to the specified URL with query parameters and a timeout of 30 seconds
    response.raise_for_status()
    #raises an HTTPError if the response status code indicates an error
    data = response.json()
    #parses the JSON response into a Python dictionary
    print("Retrieved at (UTC):", retrieved_at_text)
    #prints the timestamp of when the data was retrieved in UTC format to provide context for the snapshot of stablecoin data

    if not isinstance(data,dict):
        raise ValueError("Expected the response to be a JSON object")
        #raises a ValueError if the parsed data is not a dictionary, indicating that the response format is unexpected

    if not isinstance(data.get("peggedAssets"), list):
        raise ValueError("Expected 'peggedAssets' to be a list")
        #raises a ValueError if the "peggedAssets" key in the parsed data is not a list, indicating that the expected structure of the response is not met

except (requests.RequestException, ValueError) as error:
    raise SystemExit(f"Unable to retrieve stablecoin data: {error}")
    #exits the program with an error message if there is an issue with the request or parsing the JSON response

rows = []
for coin in data["peggedAssets"]:
    circulating = coin.get("circulating") or {}
    rows.append({
        "name": coin.get("name"),
        "symbol": coin.get("symbol"),
        "peg_type": coin.get("pegType"),
        "peg_mechanism": coin.get("pegMechanism"),
        "price": coin.get("price"),
        "circulating_usd": circulating.get("peggedUSD"),
        "retrieved_at": retrieved_at_text,
    })
#creates a list of dictionaries (rows) containing relevant information about each stablecoin, including name, symbol, peg type, peg mechanism, price, and circulating USD value

df = pd.DataFrame(rows)

df["price"] = pd.to_numeric(df["price"], errors="coerce")
#converts the "price" column to numeric values, coercing any errors to NaN
df["circulating_usd"] = pd.to_numeric(df["circulating_usd"], errors="coerce")
#converts the "circulating_usd" column to numeric values, coercing any errors to NaN

'''
print(df.shape)
#prints the shape of the DataFrame (number of rows and columns) to check how many stablecoins were processed and how many attributes were included
print(df.head(10))
#prints the first 10 rows of the DataFrame to display a sample of the data collected
print(df.dtypes)
#prints the data types of each column in the DataFrame to verify that the data has been converted to the correct types
'''

'''
print(df.sort_values(by="circulating_usd", ascending=False).head(10))
'''

usd_df = df[df["peg_type"] == "peggedUSD"].copy()
#Keep only dollar pegged coins so non-dollar coins do not create false-alarms
usd_df = usd_df.dropna(subset=["price"])
#Dropping rows with NaN prices to ensure accurate calculations of peg deviation
if usd_df.empty:
    raise SystemExit("No USD-pegged assets with valid prices were returned.")
#If the filtered DataFrame is empty after dropping NaN prices, exit the program with an error message indicating that no valid USD-pegged assets were found

'''
print(usd_df.shape)
#Prints the shape of the filtered DataFrame (number of rows and columns) to check how many dollar-pegged stablecoins were retained after filtering and dropping NaN prices
'''

'''
print(df["peg_mechanism"].value_counts())
'''

usd_df["peg_deviation_bps"] = (usd_df["price"] - 1) * 10000
#calculates the peg deviation in basis points (bps) for each stablecoin by subtracting 1 from the price and multiplying by 10,000, which helps assess how closely each stablecoin maintains its peg to the target value (e.g., USD)
usd_df["abs_deviation_bps"] = usd_df["peg_deviation_bps"].abs()
#calculates the absolute value of the peg deviation in basis points (bps) for each stablecoin to analyze
print(usd_df.sort_values("abs_deviation_bps", ascending=False).head(10))
#Prints the top 10 dollar-pegged stablecoins with the highest absolute peg deviation in basis points (bps) to identify which stablecoins are deviating the most from their intended peg

'''
#save
df.to_csv("data/stablecoins data.csv", index=False)
#saves the DataFrame to a CSV file named "stablecoins data.csv" in the "data" directory without including the index column
'''

output_dir = Path("data")
#output_dir is a Path object representing the directory where the CSV file will be saved, in this case, the "data" directory
output_dir.mkdir(parents=True, exist_ok=True)
#creates the "data" directory if it does not already exist, allowing for the saving of the CSV file without errors

timestamp_for_filename = retrieved_at.strftime("%d%m%Y_%H%M")
#formats the timestamp of when the data was retrieved into a string suitable for use in a filename, using the format "YYYYMMDD_HHMMSS" to ensure uniqueness and chronological order
output_path = f"data/stablecoins_usd_{timestamp_for_filename}.csv"
#defines the full path for the output CSV file, incorporating the formatted timestamp into the filename to create a unique and descriptive name for the saved snapshot of USD-pegged stablecoin data

usd_df.to_csv(output_path, index=False)
#saves the filtered DataFrame containing only USD-pegged stablecoins to a CSV file at the specified output path without including the index column

print("Saved USD snapshot to:", output_path)
#prints a message indicating that the USD-pegged stablecoin snapshot has been successfully saved to the specified output path, providing confirmation of the operation's success