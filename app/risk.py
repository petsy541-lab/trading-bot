from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class SurvivalWallet:
    balance: float
    max_risk_fraction: float = 0.02
    max_position_fraction: float = 0.10
    max_drawdown_fraction: float = 0.25
    dead: bool = False
    total_realized_pnl: float = 0.0
    total_trades: int = 0

    def max_risk_amount(self) -> float:
        return max(self.balance * self.max_risk_fraction, 0.0)

    def max_trade_amount(self) -> float:
        return max(self.balance * self.max_position_fraction, 0.0)

    def can_trade(self) -> bool:
        if self.dead:
            return False
        if self.balance <= 0:
            self.dead = True
            return False
        return True

    def apply_trade(self, pnl: float, trade_value: float) -> None:
        if self.dead:
            return
        self.balance += pnl
        self.total_realized_pnl += pnl
        self.total_trades += 1
        if self.balance <= 0:
            self.dead = True

    def risk_is_allowed(self, notional: float) -> bool:
        if not self.can_trade():
            return False
        risk_amount = min(notional, self.max_risk_amount())
        return risk_amount <= self.max_risk_amount() and notional <= self.max_trade_amount()

    def state_summary(self) -> dict:
        return {
            "balance": round(self.balance, 2),
            "dead": self.dead,
            "total_trades": self.total_trades,
            "risk_budget": round(self.max_risk_amount(), 2),
            "max_trade_amount": round(self.max_trade_amount(), 2),
        }


class RiskGuard:
    def __init__(self, wallet: SurvivalWallet):
        self.wallet = wallet

    def validate_trade(self, symbol: str, side: str, notional: float) -> bool:
        if not self.wallet.can_trade():
            return False
        if notional <= 0:
            return False
        if notional > self.wallet.max_trade_amount():
            return False
        if notional > self.wallet.max_risk_amount():
            return False
        return True

    def market_shutdown(self) -> bool:
        return self.wallet.dead or self.wallet.balance <= 0
