from dataclasses import dataclass, field
from typing import Literal, Optional

SignalAction = Literal["BUY", "SELL", "HOLD"]

@dataclass
class MarketSnapshot:
    symbol: str
    price: float
    trend: float
    volatility: float
    sentiment: float
    event_bias: float
    timestamp: str

@dataclass
class Trade:
    symbol: str
    side: SignalAction
    price: float
    quantity: float
    notional: float
    pnl: float = 0.0
    status: str = "OPEN"
    reason: str = ""

@dataclass
class TradeLogEntry:
    symbol: str
    side: str
    price: float
    quantity: float
    pnl: float
    wallet_balance: float
    reason: str
    timestamp: str

@dataclass
class StrategyDecision:
    action: SignalAction
    confidence: float
    signal_score: float
    reason: str
