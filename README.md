# Stablecoin Treasury Toolkit

A modular Python toolkit exploring how a treasury team could monitor
stablecoins, compare cash deployment yields, review protocol treasuries,
and estimate swap costs in liquidity pools.

## Status

Work in progress. Currently set up: project structure and environment.

## Planned modules

| Module | Purpose | Status |
|---|---|---|
| Stablecoin monitor | Peg deviation and supply trends | In progress |
| Yield optimizer | Compare stablecoin yields with a risk free benchmark | Planned |
| Pool swap simulator | Slippage in constant product and stable pools | Planned |
| Protocol treasury analyzer | Treasury composition and runway | Planned |

## Setup

Python 3.10 or later. Create a virtual environment, activate it, then
run: pip install -r requirements.txt

## Data sources

Public APIs such as DefiLlama and CoinGecko. No keys are stored in this
repository.