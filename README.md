# Open-Source Event-Aware Trading Bot

A safe, paper-trading-first trading bot for currencies and commodities. It is designed to:

- monitor market conditions and geopolitical/news-driven macro events
- evaluate multiple strategy signals
- use conservative risk sizing tied to wallet balance
- shut down automatically if the portfolio is depleted (survival mode)
- operate in demo mode by default

This project is for research, education, and simulation. It does not enable live-money execution by default.

## Important safety rules

- No live trading is enabled by default.
- The bot will not risk more than a configured fraction of the available wallet balance.
- If the account balance reaches zero or below, the bot enters a dead state and stops opening new trades.
- This is not financial advice and is not a guarantee of profit.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
python -m app.main
```

## What it includes

- demo market generator for major FX and commodity pairs
- event sentiment scoring
- multiple strategy templates (trend, mean reversion, macro event)
- risk guard and survival logic
- paper trading execution simulation
- tests for safety behavior

## Supported demo instruments

- EURUSD
- GBPUSD
- USDJPY
- XAUUSD
- USOIL
- NGAS

## Environment / configuration

Edit `app/config.py` to change:

- starting balance
- risk fraction
- max drawdown
- symbol list
- demo mode / live mode flags

## Survival logic

The bot uses a strict survivability model:

- max risk per trade = wallet_balance * `max_risk_fraction`
- total exposure is capped
- if equity drops to zero, `can_trade` becomes false
- new trades are rejected when the account is dead or over risk limits

## License

MIT
