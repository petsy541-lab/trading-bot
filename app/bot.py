from __future__ import annotations

from datetime import datetime

from app.config import BotConfig
from app.models import Trade, TradeLogEntry
from app.risk import RiskGuard, SurvivalWallet


class PaperBroker:
    def __init__(self, wallet: SurvivalWallet, config: BotConfig):
        self.wallet = wallet
        self.config = config
        self.risk_guard = RiskGuard(wallet)
        self.trade_log: list[TradeLogEntry] = []

    def execute(self, symbol: str, side: str, price: float, notional: float, reason: str) -> dict:
        if not self.risk_guard.validate_trade(symbol, side, notional):
            return {
                "accepted": False,
                "symbol": symbol,
                "reason": "Trade rejected by risk guard or wallet constraint.",
                "balance": self.wallet.balance,
                "dead": self.wallet.dead,
            }

        quantity = notional / max(price, 1e-8)
        pnl = 0.0
        if side == "BUY":
            pnl = 0.0
        elif side == "SELL":
            pnl = 0.0

        self.wallet.apply_trade(pnl, notional)
        entry = TradeLogEntry(
            symbol=symbol,
            side=side,
            price=price,
            quantity=quantity,
            pnl=pnl,
            wallet_balance=self.wallet.balance,
            reason=reason,
            timestamp=datetime.utcnow().isoformat(),
        )
        self.trade_log.append(entry)

        return {
            "accepted": True,
            "symbol": symbol,
            "side": side,
            "notional": notional,
            "balance": self.wallet.balance,
            "dead": self.wallet.dead,
            "reason": reason,
        }
