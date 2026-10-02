from __future__ import annotations

import math
from random import Random

from app.config import BotConfig
from app.models import MarketSnapshot


class DemoMarketData:
    def __init__(self, config: BotConfig):
        self.config = config
        self.rng = Random(42)
        self.iteration = 0

    def _base_price(self, symbol: str) -> float:
        prices = {
            "EURUSD": 1.085,
            "GBPUSD": 1.275,
            "USDJPY": 156.2,
            "XAUUSD": 2345.12,
            "USOIL": 82.14,
            "NGAS": 2.69,
        }
        return prices.get(symbol, 100.0)

    def _event_bias(self, symbol: str) -> float:
        biases = {
            "EURUSD": 0.10,
            "GBPUSD": 0.12,
            "USDJPY": -0.08,
            "XAUUSD": 0.18,
            "USOIL": 0.15,
            "NGAS": 0.16,
        }
        return biases.get(symbol, 0.0)

    def next_snapshot(self):
        self.iteration += 1
        snapshots = {}
        for symbol in self.config.symbols:
            base = self._base_price(symbol)
            wave = math.sin((self.iteration + self.rng.randint(1, 20)) / 4)
            noise = (self.rng.random() - 0.5) * 0.02
            price = base * (1 + (wave * 0.006) + noise)
            trend = math.sin(self.iteration / 4 + self.rng.random())
            volatility = 0.008 + (self.rng.random() * 0.022)
            sentiment = (self.rng.random() - 0.5) * 2.0 + self._event_bias(symbol)
            event_bias = self._event_bias(symbol) * (0.6 + (self.rng.random() * 0.4))
            snapshots[symbol] = MarketSnapshot(
                symbol=symbol,
                price=float(round(price, 5)),
                trend=float(round(trend, 5)),
                volatility=float(round(volatility, 5)),
                sentiment=float(round(sentiment, 5)),
                event_bias=float(round(event_bias, 5)),
                timestamp=f"demo-step-{self.iteration}",
            )
        return snapshots
