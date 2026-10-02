from __future__ import annotations

from app.config import BotConfig
from app.demo_market import DemoMarketData
from app.execution import PaperBroker
from app.risk import SurvivalWallet
from app.strategy_engine import MultiStrategySelector


class TradingBot:
    def __init__(self, config: BotConfig | None = None):
        self.config = config or BotConfig()
        self.wallet = SurvivalWallet(
            balance=self.config.starting_balance,
            max_risk_fraction=self.config.max_risk_fraction,
            max_position_fraction=self.config.max_position_fraction,
            max_drawdown_fraction=self.config.max_drawdown_fraction,
        )
        self.market = DemoMarketData(self.config)
        self.strategy = MultiStrategySelector()
        self.broker = PaperBroker(self.wallet, self.config)

    def step(self):
        snapshots = self.market.next_snapshot()
        results = []
        for symbol, snapshot in snapshots.items():
            decision = self.strategy.choose(snapshot)
            if decision.action == "HOLD":
                results.append({"symbol": symbol, "action": "HOLD", "reason": decision.reason})
                continue

            if not self.wallet.can_trade():
                results.append({"symbol": symbol, "action": "HOLD", "reason": "Account is dead; no trades allowed."})
                continue

            exposure = self.wallet.max_risk_amount()
            notional = min(max(exposure, self.config.min_trade_value), self.wallet.max_trade_amount())
            action = self.broker.execute(symbol, decision.action, snapshot.price, notional, decision.reason)
            action["confidence"] = decision.confidence
            action["signal_score"] = decision.signal_score
            results.append(action)
        return results

    def run(self, steps: int = 20):
        print("Starting paper-trading bot...")
        for idx in range(steps):
            print(f"\nStep {idx + 1}")
            trade_results = self.step()
            for result in trade_results:
                print(result)
            if self.wallet.dead:
                print("Survival mode triggered: account is depleted.")
                break
            print("Wallet:", self.wallet.state_summary())
        print("\nFinal wallet:", self.wallet.state_summary())
        return self.wallet.state_summary()
