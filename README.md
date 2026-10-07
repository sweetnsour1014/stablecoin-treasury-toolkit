# Stablecoin Treasury Toolkit

A beginner-friendly Python project for collecting stablecoin market data and building treasury analysis tools in stages. The first release focuses on a repeatable snapshot of USD-pegged stablecoins, their reported prices, and their deviations from a $1 peg.

## Release roadmap

| Release | Planned capability | Status |
|---|---|---|
| V1: Stablecoin snapshot monitor | Fetch stablecoin data, retain USD-pegged assets with valid prices, calculate and rank deviations from $1, and save a CSV snapshot. | First release candidate is being published as `v1.0.0`. |
| V2: Yield optimizer | Compare stablecoin deployment opportunities using documented yield sources and comparable yield measures, with risk context made explicit. | Planned. Selection of data sources, benchmarks, and risk conventions remains future work. |
| V3: Pool swap simulator | Estimate swap outcomes and costs for stablecoin liquidity pools, including price impact or slippage where the selected data supports it. | Planned. Pool data and pricing assumptions remain future work. |
| V4: Protocol treasury analyzer | Review protocol treasury composition and provide a transparent framework for estimating runway and exposure. | Planned. Portfolio inputs and runway methodology remain future work. |

The later releases are roadmap goals, not existing features. V1 does not provide yield recommendations, swap quotes, protocol runway estimates, alerts, or a dashboard.

## V1 features

The V1 script, `snapshot.py`, requests the public DefiLlama stablecoin endpoint, validates the response shape, and creates a pandas DataFrame from the returned assets. It converts price and USD circulation values to numeric columns, filters to USD-pegged assets with valid prices, calculates peg deviation in basis points, prints the ten largest absolute deviations, and saves the filtered rows as a CSV.

The deviation calculation is:

```text
peg_deviation_bps = (price - 1) * 10,000
```

A positive result means the reported price is above $1; a negative result means it is below $1. The absolute deviation is used to rank the largest movements regardless of direction.

## Requirements

Use Python 3.12, which is the version used during development. The script depends on `requests` for the HTTP request and `pandas` for tabular processing.

From the repository root, create and activate a virtual environment, then install the listed dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

## Run the V1 snapshot

Run the script from the repository root so its relative `data/` output path points to the repository's data directory:

```bash
python snapshot.py
```

The terminal prints a UTC timestamp, a table of the ten USD-pegged assets with the largest absolute deviations, and the saved CSV path. The timestamp currently represents when the script starts, and the filename uses day-month-year plus hour and minute. Two runs in the same minute can therefore produce the same filename. Generated CSV snapshots are local outputs and are excluded from Git; running the script does not publish market data to the repository.

## CSV fields

| Column | Meaning |
|---|---|
| `name` | Asset name returned by the data source. |
| `symbol` | Asset symbol returned by the data source. |
| `peg_type` | Peg category returned by the data source. V1 retains `peggedUSD`. |
| `peg_mechanism` | Peg mechanism returned by the data source, when provided. |
| `price` | Reported asset price, converted to a numeric value. |
| `circulating_usd` | Reported USD-pegged circulation value, converted to a numeric value. |
| `retrieved_at` | UTC timestamp recorded by the script for this snapshot run. |
| `peg_deviation_bps` | Signed price difference from $1, expressed in basis points. |
| `abs_deviation_bps` | Absolute signed deviation, used to rank the largest deviations. |

## Data source and limitations

V1 uses the public [DefiLlama stablecoins API](https://stablecoins.llama.fi/stablecoins) with price inclusion enabled. Availability, field definitions, coverage, and update timing depend on that service. The script handles request failures and validates the broad response structure, but the result is still a point-in-time third-party data snapshot.

Price deviation alone does not establish reserve quality, redemption access, liquidity, counterparty safety, or whether an asset is appropriate for a treasury. Circulating supply is included as context and is not proof of backing. This toolkit is educational and informational; it is not investment, legal, or treasury advice.

## Development status

`first call.py` and `explore coin.py` are exploratory learning scripts. The V1 supported workflow is `snapshot.py`, run from the repository root. The yield optimizer, pool swap simulator, and protocol treasury analyzer have not been implemented.
